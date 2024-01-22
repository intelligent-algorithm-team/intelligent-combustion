# Methane (CH4)

Date: Nov 13, 2022; Maintainer: Junjie Yao.

A deep-learning based surrogate model for GRI3.0 mechanism (Available for zero-dimensional auto-ignition and flame propagation).

## Table of contents
- [Basic Info](#basic-info)
- [DNN Details](#dnn-details)
- [Files Description](#files-description)
- [DNN Validation](#dnn-validation)


### Basic Info

**Mechanism** : GRI3.0 Mech at http://www.gri.org, or see ```mechanism/gri.yaml```[<sup>1</sup>](#GRI)

**Species_num** : *53*

**Reactions_num** : *325*

**DNN_time_step** : *1e-6*s

**Working_condition** : Zero-dimensional homogeneous ignition under constant pressure with the following initial condition $(T,P,\Phi)$ in [1500K,1900K],[0.5atm,2atm],[0.5,3], respectively.


### DNN Details

**data_format** : `TPY`, *55*-dimensional state vector consists of temperature (K), pressure (atm) and mass fraction (Y, the order of species should conform with the provided mechanism)

**pre-conditions** : 

- Apply BCT operator 

    $$\mathcal{F}(x)=\frac{x^\lambda-1}{\lambda},\quad \lambda=0.1$$

    on the dimensions denoting the mass fraction.
               
- Normalization 

    $$\mathcal{N}(X)=\frac{X-input\_{mean}}{input\_{std}}$$ 
    
    `input_mean` and `input_std` is the `mean` and `std` of input data $X$. See `checkpoint/norm.json` .

**DNN input** : the *55*-dimensional state vector after the pre-conditions.

**DNN structure** : feed-forward full-connected 

$$u_{\theta}(x)=W^{[L-1]}\sigma\circ(W^{[L-2]}\sigma\circ(\dots(W^{[1]}\sigma\circ(W^{[0]}x+b^{[0]})+b^{[1]})\dots)+b^{[L-2]})+b^{[L-1]}$$ 

where $W^{[l]}\in\mathbb{R}^{m_{l+1}\times m_l},b^{[l]}\in \mathbb{R}^{m_{l+1}},m_0=m_L=55$,  $\sigma$ denotes the activation fucntion. See ```checkpoint/settings.json``` 

**Activation function** : 

$$GELU(x)=\frac{x}{2}(1+\tanh(x+0.044715x^3)\sqrt{\frac{2}{\pi}})$$

**How to get state vector after delta_t** `1e-6s`:

```python
## python pseudo-code

input state 

state_bct = (state[:, 2:]**lam - 1) / lam          # BCT
state_norm = (state_bct - input_mean) / input_std  # normalization
output_norm = DNN(state_norm)                      # DNN prediction
output = output_norm * label_std + label_mean      # inverse-normalization
output_bct = output * delta_t + state_bct          
output_bct[:, 2:] = (lam * output_bct[:, 2:] + 1)**(1 / lam) # inverse-BCT

return output_bct
```


### Files Description

- `mechanism/gri.yaml` : chemical mechanism files. CHEMKIN format is also provided.

- `checkpoint/norm.json` : `mean` and `std` of input and label data for normalization and inverse-normalization.
 
- `checkpoint/settings.json` : basic hyper-parameters for setting and training DNNs.

- `checkpoint/model3005.pt` : DNN parameters in pytorch format. The suffix number denotes the training epoch.

### DNN Validation
 

Ignition delay time comparison between Cantera (CVODE) and DNN.
 
![test](./pic/GRI_IDT.png)

One-dimensional laminar flame trajectory and flame speed simulated by EBI[<sup>2</sup>](#EBI).
 
![test](./pic/1d/GRI_1d.png)

![test](./pic/1d/GRI_flamespeed.png)

Two-dimensional spherical flame simulated by EBI.

![test](./pic/SphericalFlame/GRI_SphericalFlame.png)

Two-dimensional counter flow simulated by EBI.

![test](./pic/counterflow/GRI_counterflow.png)

### Citation

If you use our DNN model in your work, please cite it as follows:

```
@article{ZHANG2022112319,
    title = {A multi-scale sampling method for accurate and robust deep neural network to predict combustion chemical kinetics}, 
    journal = {Combustion and Flame},
    volume = {245},
    pages = {112319},
    year = {2022},
    issn = {0010-2180},
    doi = {https://doi.org/10.1016/j.combustflame.2022.112319},
    url = {https://www.sciencedirect.com/science/article/pii/S0010218022003340},
    author = {Tianhan Zhang and Yuxiao Yi and Yifan Xu and Zhi X. Chen and Yaoyu Zhang and Weinan E and Zhi-Qin John Xu}
}
```

<div id="GRI"></div>

[1] [Smith, Gregory P. "GRI-Mech 3.0."(1999).](http://www.me.berkley.edu/gri_mech/)

<div id="EBI"></div>

[2] [Thorsten Zirwes, Feichi Zhang, Peter Habisreuther, Maximilian Hansinger, Henning Bockhorn, Michael Pfitzner, Dimosthenis Trimis (2020) Quasi-DNS Dataset of a Piloted Flame with Inhomogeneous Inlet Conditions; Flow, Turbulence and Combustion. vol. 104, pp. 997–1027. doi: 10.1007/s10494-019-00081-5](https://link.springer.com/article/10.1007/s10494-019-00081-5)