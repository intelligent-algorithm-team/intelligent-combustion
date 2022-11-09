from ModelUse import ModelUse
import numpy as np
import os

def oneStepPred(modelname,epoch,mech_path,input,label,data_name,plot_dims):
    r"""plot DNN prediction and label w.r.t a test dataset
        Arguments:
            modelname (str): the model's name
            epoch (int): epoch for model checkpoint
            input (str or np.ndarray): input dataset, could be np.ndarray format data or data path 
            label (str or np.ndarray): label dataset, could be np.ndarray format data or data path
            data_name (str): data name suffix to save figure
            plot_dims (str,list or range): list of dimension expected to be plotted, e.g. [1,4,5,7] or Range(20)
                                            or list of ['T','P',species names], e.g. ['T','O','CH4','N2']
                                            default str 'all' means plotting all dims.
            dpi (int): figure dpi, default 200
        Return 
            prediction (np.ndarray): DNN model onr-step prediction on the input dataset
    """
    model=ModelUse()
    model.initGas(mech_path)
    model.loadModel(modelname,epoch)
    model.oneStepPredict(modelname,epoch,input,label,data_name,plot_dims,dpi=200)


def temporalEvolution(modelname,epoch,mech_path,gas_condition,n_step,builtin_t):
    r"""temporal evolution simulated by DNN model and Cantera"""
    model = ModelUse()
    model.initGas(mech_path)
    model.loadModel(modelname,epoch)
    model.evolutionPredict(modelname,
                         epoch,
                         gas_condition,
                         n_step,
                         builtin_t,
                         plotAll=1,
                         dpi=200)

def main():
    ## model name
    modelname = 'MG01_Methane_GRI3_Man_20220731'
    epoch = 5000

    ## mechanism path
    mech_path = os.path.join('Model', modelname, 'mechanism', 'gri.yaml')

    
    n_step=2000 # dnn interation steps
    builtin_t=1e-8 # cantera max time step
    for phi in [1]:
        gas_condition=[phi,1500,1,'CH4','constP'] # Phi,T,P(atm),fuel,reactor
        temporalEvolution(modelname,epoch,mech_path,gas_condition,n_step,builtin_t)



if __name__ == '__main__':
    main()