# -*- coding: utf-8 -*-
"""
Utilize the trained neural network to finish downstream tasks.

Created on Wed Jul 27 22:30:20 2022
@author: Yuxiao Yi
"""

import os,re
import json
import math
import logging
import cantera as ct
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from ModelDefine import *
from easydict import EasyDict as edict
from distutils.spawn import find_executable
matplotlib.use('AGG')


class ModelUse():

    def __init__(self) -> None:
        pass

    def initGas(self, mech_path):
        r"""Instantiate cantera.Solution object. 

        Parameters
        ----------
        mech_path : str
            Mechanism input file, could be .yaml, .xml or .cti format.

        Returns
        -------
                
        """
        self.gas = ct.Solution(mech_path)

    def buildModel(self, args):
        """Create a neural network."""
        act_funs = {
            'relu': nn.ReLU(),
            'gelu': nn.GELU(),
            'CustomGELU': CustomGELU(),
            'tanh': nn.Tanh(),
            'sin': Sin(),
            'sigmoid': nn.Sigmoid(),
            'CEL': nn.CrossEntropyLoss(),
        }
        dnn_types = {
            'fc': FeedForwardNet,
            'resnet': ResNet,
            'mscale': MultiscaleNet
        }
        self.net = dnn_types[args.net_type](args, act_funs)
        print(
            f"The neural network is created. Network type: {args.net_type}")

    def loadModel(self, modelname, epoch):
        """Load a checkpoint, args and norm on cpu."""
        model_path = os.path.join('Model', f'{modelname}')
        ckpoint_path = os.path.join(model_path, 'checkpoint',
                                    f'model{epoch}.pt')
        setting_path = os.path.join(model_path, 'checkpoint', f'settings.json')
        norm_path = os.path.join(model_path, 'checkpoint', f'norm.json')
        self.args = self.json2Parser(setting_path)
        self.buildModel(self.args)
        self.norm = self.json2Parser(norm_path)
        self.net.load_state_dict(torch.load(ckpoint_path, map_location='cpu'))
        print(f"the {ckpoint_path} has been loaded")

    @staticmethod
    def json2Parser(json_path):
        """Load json and return a parser-like object

        Parameters
        ----------
        json_path : str
            The json file path.
        
        Returns
        -------
        args : easydict.EasyDict
            A parser-like object.


        """
        with open(json_path, 'r') as f:
            args = json.load(f)
        return edict(args)

    def ctOneStep(self, state, delta_t, reactor, builtin_t):
        r"""Use Cantera to advance the state of the reactor network from the current time :math:`t` towards :math:`t+\Delta t`. 
        
        Parameters
        ----------
        state : numpy.ndarray
            State vector organized as T,P(atm),Y.
        delta_t : float
            Evolution time step (sec).
        reactor : str
            The type of reactor, could be 'constP' or 'constV'.
        builtin_t : float
            Max time step for CVODE in Cantera.
        
        Returns
        ------- 
        state_out : numpy.ndarray
            The output state vector after :math:`\Delta t` which is organized as T,P(atm),Y.
        """

        state = state.reshape(1, -1)
        reactor_types = {
            'constV': ct.IdealGasReactor,
            'constP': ct.IdealGasConstPressureReactor
        }
        self.gas.TPY = state[0, 0], state[0, 1] * ct.one_atm, state[0, 2:]
        r = reactor_types[reactor](self.gas)
        sim = ct.ReactorNet([r])
        sim.max_time_step = builtin_t
        sim.max_steps = 2e5  # max iteration steps for CVODES,default 2e4
        # sim.atol = 1e-24  # default 1e-15
        sim.rtol = 1e-15  # default 1e-9
        sim.advance(delta_t)

        state_out = np.hstack(self.gas.TPY)
        state_out[1] = self.gas.P / ct.one_atm
        return state_out.reshape(1, -1)
    

    def netOneStep(self, state):
        r"""Use DNN to advance the state of the reactor network from the current time :math:`t` towards :math:`t+\Delta t`.

        Parameters
        ----------
        state : numpy.ndarray
            State vector organized as T,P(atm),Y.

        Returns
        -------
            output_bct : numpy.ndarray
                The output state vector after :math:`\Delta t` which is organized as T,P(atm),Y.

        """
        args = self.args
        norm = self.norm
        lamda = args.power_transform
        delta_t = args.delta_t
        state_bct = state.reshape(-1, args.dim)  #TPY
        state_bct[:, 2:] = (state_bct[:, 2:]**(lamda) - 1) / lamda  #BCT
        state_normalized = (state_bct - norm.input_mean) / norm.input_std
        for inert_gas in ['Ar']:
            try:
                index_Ar = self.gas.species_index(inert_gas) + 2
                state_normalized[:, index_Ar] = 0  # set mass fraction of Ar zero
            except:
                pass
        state_normalized = torch.from_numpy(state_normalized).float()
        output_normalized = self.net(state_normalized)
        output_normalized = output_normalized.detach().cpu().numpy()
        output = output_normalized * norm.label_std + norm.label_mean
        output_bct = output * delta_t + state_bct
        
        output_bct[:, 2:] = (lamda * output_bct[:, 2:] + 1)**(1 / lamda)
        # output_bct[:,2:] = self.inverBCT(output_bct[:,2:], lamda)
        # index_N2 = self.gas.species_index('N2')+2
        # idx = np.arange(2+self.gas.n_species)
        # idx = np.delete(idx, [0, 1, index_N2], axis=0)
        # output_bct[:, index_N2] = 1 - np.sum(output_bct[:, idx])
        # print('sum',np.sum(output_bct[:,2:]))
        return output_bct
    
    @staticmethod
    def inverBCT(x, lamda):
        func = np.select([x < -10, x <= 0, x > 0],
                      [0, (x * lamda + 1)**(1 / lamda), 1])
        return func

    def evolutionPredict(self,
                         modelname,
                         epoch,
                         gas_condition,
                         n_step,
                         builtin_t,
                         plotAll=False,
                         dpi=200):
        r"""Temporal evolution simulation computed by DNN and Cantera, respectively. The simualtion will be saved as .png.

        Parameters
        ----------
        modelname : str
            The folder name of DNN model.
        epoch : int
            Epoch for loading checkpoint.  
        gas_condition : list or tuple
            Initial conditions for zero dimensional ignition. Organized as [Phi,T,P(atm),fuel,reactor]. 
            **Phi**: equivalence ratio. **T**: temperature (K). **P**: pressure (atm). **fuel**: fuel species name. **reactor**: reactor type.
        n_step : int
            Simulation steps, time step = args.delta_t.
        builtin_t : float
            Max time step for CVODES in Cantera.
        plotAll : bool,optional
            Whether plot all the features (T,P,Yi), if True plot all else plot temperature. Default False.
        dpi : int,optional
            The dpi used to save figure. Default 200. 

        """
        Phi, T, P, fuel, reactor = gas_condition
        self.gas.set_equivalence_ratio(Phi, fuel, 'O2:1.0,N2:3.76')
        delta_t = self.args.delta_t

        initial_state = np.c_[T, P, self.gas.Y.reshape(1, -1)]
        state_net = initial_state.copy()
        state_cantera = initial_state.copy()
        for i in range(n_step):
            ## todo: calculate cantera output
            current_cantera = state_cantera[i, :].copy()
            next_cantera = self.ctOneStep(current_cantera, delta_t, reactor,
                                          builtin_t)
            state_cantera = np.r_[state_cantera, next_cantera] 

            ## todo: calculate net output
            current_net = state_net[i, :].copy()
            next_net = self.netOneStep(current_net)
            # if i<200:
            #     next_net=next_cantera
            state_net = np.r_[state_net, next_net]
        ###
        # col = 10
        # state_net[:,col]=state_cantera[:,col]
        ## todo: display simulation results
        handle = self.plotAll if plotAll else self.plotTemperature
        handle(modelname, epoch, gas_condition, state_net, state_cantera, dpi)

    def plotTemperature(self, modelname, epoch, gas_condition, state_net,
                        state_cantera, dpi):
        r"""Draw and save the ignition curves simulated by Cantera and DNN.

        Parameters
        ----------
        modelname : str
            The folder name of DNN model.
        epoch : int
            Epoch for loading checkpoint.  
        gas_condition : list or tuple
            Initial conditions for zero dimensional ignition. Organized as [Phi,T,P(atm),fuel,reactor]. 
            **Phi**: equivalence ratio. **T**: temperature (K). **P**: pressure (atm). **fuel**: fuel species name. **reactor**: reactor type.
        state_net : numpy.ndarray
            The n-step continuous evolution simulated by DNN.
        state_cantera : numpy.ndarray
            The n-step continuous evolution simulated by Cantera.
        dpi : int
            The dpi used to save figure.
        
        """
        Phi, T, P, fuel, reactor = gas_condition
        num_steps = range(len(state_net))
        time_seq = np.array(num_steps) * self.args.delta_t * 1e3  # ms


        title_size=25
        label_size=16
        legend_size=13
        tick_size=11.5

        p1, = plt.plot(time_seq,
                       state_cantera[:, 0],
                       color="chocolate",
                       linewidth=1.5,
                       alpha=1)
        p2, = plt.plot(time_seq,
                       state_net[:, 0],
                       color="green",
                       linewidth=1.5,
                       linestyle='-.',
                       alpha=1)
        plt.xticks(fontsize=tick_size)
        plt.yticks(fontsize=tick_size)
        plt.title(self._latexStyleName(0),fontsize=title_size)
        plt.xlabel("time (ms)",fontsize=label_size)
        plt.ylabel('Temperature (K)',fontsize=label_size)
        
        plt.ylim(
            np.min(state_cantera[:, 0]) - 100,
            np.max(state_cantera[:, 0]) + 100)
        plt.legend([p1, p2], ["CVODE", 'DNN'], loc="lower right",fontsize=legend_size)
        

        pic_name = f'{modelname}_Phi={Phi}_T={T}_P={P}_epoch={epoch}.png'
        pic_folder = os.path.join(self.args.model_path, 'pic', f'pics{epoch}')
        os.makedirs(pic_folder, exist_ok=True)
        pic_path = os.path.join(pic_folder, pic_name)
        print(f'simulation picture saved in {pic_path}')
        plt.savefig(pic_path, dpi=dpi)
        plt.close()

    def plotAll(self, modelname, epoch, gas_condition, state_net,
                state_cantera, dpi):
        r"""Draw and save the evolution of temperature, pressure and species mass fraction simulated by Cantera and DNN.

        Parameters
        ----------
        modelname : str
            The folder name of DNN model.
        epoch : int
            Epoch for loading checkpoint.  
        gas_condition : list or tuple
            Initial conditions for zero dimensional ignition. Organized as [Phi,T,P(atm),fuel,reactor]. 
            **Phi**: equivalence ratio. **T**: temperature (K). **P**: pressure (atm). **fuel**: fuel species name. **reactor**: reactor type.
        state_net : numpy.ndarray
            The n-step continuous evolution simulated by DNN.
        state_cantera : numpy.ndarray
            The n-step continuous evolution simulated by Cantera.
        dpi : int
            The dpi used to save figure.
        """

        Phi, T, P,_,_ = gas_condition
        num_steps = range(len(state_net))
        time_seq = np.array(num_steps) * self.args.delta_t * 1e3  # ms

        title_size=20
        label_size=16
        legend_size=13
        tick_size=14

        fig = plt.figure(figsize=(12.8, 9.6))
        plot_methods = {'semilogy': plt.semilogy, 'plot': plt.plot}
        for i in range(2 + self.gas.n_species):
            order_subplot = i % 9 + 1
            ax = fig.add_subplot(3, 3, order_subplot)
            method = 'plot' if i in [0, 1] else 'semilogy'
            plot_handle = plot_methods[method]
            p1, = plot_handle(time_seq,
                              state_cantera[:, i],
                              color="chocolate",
                              linewidth=2,
                              alpha=1)
            p2, = plot_handle(time_seq,
                              state_net[:, i],
                              color="green",
                              linewidth=2,
                              linestyle='-.',
                              alpha=1)

            ## todo: set label/ticks/legend
            if i == 1:
                plt.ylabel('Pressure (atm)',fontsize=label_size)
            elif i == 0:
                plt.ylim(
                    np.min(state_cantera[:, 0]) - 100,
                    np.max(state_cantera[:, 0]) + 100)
                plt.ylabel('Temperature (K)',fontsize=label_size)
            else:
                ## todo: adjust the display range of mass fraction
                degree_mid = math.floor(np.log10(state_cantera[-1, i] + 1e-30))
                degree_lower = degree_mid - 3
                degree_upper = min(0, degree_mid + 3)
                plt.ylim(10**degree_lower, 10**degree_upper)
                ticks = [10**(i) for i in range(degree_lower, degree_upper + 1)]
                plt.yticks(ticks,fontsize=tick_size)
                # ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2))
                plt.ylabel('mass fraction',fontsize=label_size)

            ##
            plt.legend([p1, p2], [
                "CVODE",
                'DNN',
            ],
                       fontsize=legend_size,
                       loc='lower right')
            plt.title(self._latexStyleName(i),fontsize=title_size,fontweight='bold')
            plt.xlabel("time (ms)",fontsize=label_size)
            plt.yticks(fontsize=tick_size)
            plt.xticks(fontsize=tick_size)

            ## condition for saving pictures
            pic_folder = os.path.join(self.args.model_path, 'pic',
                                      f'pics{epoch}')
            os.makedirs(pic_folder, exist_ok=True)
            if order_subplot == 9:
                plt.tight_layout()
                # fig.suptitle('epoch={}'.format(epoch))
                pic_name = f'{ modelname}_Phi={Phi}_T={T}_P={P}_epoch={epoch}_all{math.ceil(i / 9)}.png'
                pic_path = os.path.join(pic_folder, pic_name)
                plt.savefig(pic_path, dpi=dpi)
                print(f'simulation picture saved in {pic_path}')
                plt.close()
                fig = plt.figure(figsize=(12.8, 9.6))
            elif i == 1 + self.gas.n_species:
                plt.tight_layout()
                pic_name = f'{ modelname}_Phi={Phi}_T={T}_P={P}_epoch={epoch}_all{math.ceil((i+1) / 9)}.png'

                pic_path = os.path.join(pic_folder, pic_name)
                plt.savefig(pic_path, dpi=dpi)
                print(f'simulation picture saved in {pic_path}')
                plt.close()


    def oneStepPredict(self,modelname,epoch,input,label,data_name,plot_dims='all',dpi=200):
        r"""Draw and save single-step prediction of DNN w.r.t an chemical test dataset. The ordinate axis is DNN prediction  while abscissa axis is 
        the corresponding label. The scatter plot will be saved in .png format.

        Parameters
        ----------
        modelname : str
            The folder name of DNN model.
        epoch : int
            Epoch for loading checkpoint. 
        input : str or numpy.ndarray
            Input dataset, could be file path or numpy.ndarray.
        label : str or numpy.ndarray
            Label dataset, could be file path or numpy.ndarray.
        data_name : str
            The data name suffix to save figure.
        plot_dims : str,list or tuple,optional
            List of dimensions expected to be plotted e.g. [1,4,5,7] or Range(20) or ['T','O','CH4','N2'].
            Default string 'all' means plotting all the dimensions.
        dpi : int 
            The dpi used to save figure. Default 200.

        Returns
        -------
        prediction : numpy.ndarray
            DNN model one-step prediction on the input dataset.

        """
        ## check input class type
        if isinstance(input,np.ndarray):
            pass
        elif isinstance(input,str):
            input=np.load(input)
            label=np.load(label)
        else:
            raise TypeError(f"expected input be <class 'str'> or <class 'np.ndarray'> but got {input.__class__}")
        
        prediction=self.netOneStep(input) # dnn prediction

        ## check dims expected to display
        names=['T','P']+self.gas.species_names # ['T','P',species_names]
        n_dims=self.gas.n_species+2
        if plot_dims=='all':
            plot_dims=range(n_dims)
        for dim in plot_dims:
            if isinstance(dim,str):
                if dim in ['T','P']:
                    dim = names.index(dim)
                else:
                    dim = self.gas.species_index(dim) + 2
            self._oneStepPredPlot(modelname,epoch,label,prediction,dim,data_name,dpi)

    def _oneStepPredPlot(self,modelname,epoch,label,prediction,dim,data_name,dpi):
        r"""The built-in function to plot and save one-step prediction."""
        label_size=14
        title_size=14 # cbar_title_size
        ticks_size=14
        cbar_size=12 # cbar_tick_size
        species = self.gas.species_names
        axis_labels=['Temperature (K)','Pressure (atm)']+[sp for sp in species ]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        plt.plot(label[:, dim], label[:, dim], 'k-', linewidth=0.8, alpha=0.6) #indentity line
        points = plt.scatter(
            label[:, dim],
            prediction[:, dim],
            c=label[:, 0],  # colored by temperature
            vmin=1000, 
            vmax=3000,
            cmap='rainbow',
            s=1,
            marker='.',
            alpha=1)
        if dim>1:
            ax.set_xscale('log')
            ax.set_yscale('log')

        plt.xticks(fontsize=ticks_size)
        plt.yticks(fontsize=ticks_size)
        
        plt.xlabel(f'Label {axis_labels[dim]}',fontsize=label_size)
        plt.ylabel(f'Predicted {axis_labels[dim]}',fontsize=label_size)
        plt.axis('square')
        # ax.yaxis.set_major_locator(ax.xaxis.get_major_locator())
        # ax.yaxis.set_major_formatter(ax.xaxis.get_major_formatter())
        # cbar_ax = fig.add_axes([0.8, 0.1, 0.02, 0.8]) #left,down, width ,height
        # cbar = plt.colorbar(points,orientation="vertical",cax=cbar_ax)
        cbar = plt.colorbar(points)
        cbar.set_label("Temperature (K)",
                        fontsize=title_size,
                        fontweight='bold')
        cbar.ax.tick_params(labelsize=cbar_size)

        pic_folder=os.path.join('Picture','OneStepPred',f'{modelname}')
        os.makedirs(pic_folder,exist_ok=True)
        pic_path=os.path.join(pic_folder,f'{modelname}_epoch{epoch}_OneStepPred_on_{data_name}_dim={dim}.png')
        plt.savefig(pic_path,dpi=dpi)
        plt.close()
        print(f'one-step prediction picture saved in {pic_path}')
    
    @staticmethod
    def _latexStyle(text):
        r"""Convert the given text to :math:`\LaTeX` bold style e.g. T-->$\\bf{T}$, CH4-->$\\bf{CH_{4}}$, C10H18O8-->$\\bf{C_{10}H_{18}O_{8}}$ """
        content = re.findall('\w\d+', text) # find letter+number e.g. C10 H2 N8 O12...
        content = list(set(content))  #unique
        for letter_number in content:
            letter = letter_number[0]
            number = letter_number[1:]
            text = re.sub(letter_number, f'{letter}_'+ '{'+number+'}', text)
        return '$\\bf{' + text + '}$'

    def _latexStyleName(self, index):
        r"""For a chemical dataset (TPY), the state names could be denoted as ['T','P',...species names]. Convert state_names[index] to 
        :math:`\LaTeX` bold style if there exists :math:`\LaTeX` enviroment.
        """
        state_names = ['T', 'P']+self.gas.species_names
        name=self._latexStyle(state_names[index]) if find_executable('latex') else state_names[index]
        return name







        



        