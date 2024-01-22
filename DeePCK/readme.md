

# DeePCK : Deep Chemical Kinetics

DeePCK is a task of the DeepCombustion project, which aims at developing DNN-based surrogate model to accelerate the simulation of chemical kinetics.

This open project will release various models based on our algorithms.

## How to use DNN model
### Python Env
- create python environment including `torch`, `cantera`, `matplotlib` and `easydict`.

- cofigure `modelname`, `mech_path` in the file `useModel.py`

- Then execute the following command: 

    ```python
    python useModel.py
    ```

### C++ Env
- set  `modelname` and `epoch`, run the following code for instance.

    ```python
    from ModelUse import ModelUse
    model = ModelUse()
    modelname = "HE03_Hydrogen_ESH2_GMS_20221019"
    epoch = 5000
    model.convert2TorchScript(modelname, epoch)
    ```
 - Then the corresponding torch script `.pt` file will be saved in the sub-fold `Model/$(modelname)/checkpoint/`.

## Navigation of models

See the file [`contents.md`](contents.md).

## Citation
Please cite: 
```
@article{Zhang_Xu,
title = {A multi-scale sampling method for accurate and robust deep neural network to predict combustion chemical kinetics},
journal = {Combustion and Flame},
volume = {245},
pages = {112319},
year = {2022},
issn = {0010-2180},
doi = {https://doi.org/10.1016/j.combustflame.2022.112319},
url = {https://www.sciencedirect.com/science/article/pii/S0010218022003340},
author = {Tianhan Zhang and Yuxiao Yi and Yifan Xu and Zhi X. Chen and Yaoyu Zhang and Weinan E and Zhi-Qin John Xu},
keywords = {Stiff ODE, Machine learning, Deep neural network, Chemical kinetics, Direct numerical simulation},
abstract = {Machine learning has long been considered a black box for predicting combustion chemical kinetics due to the extremely large number of parameters and the lack of evaluation standards and reproducibility. The current work aims to understand two basic questions regarding the deep neural network (DNN) method: what data the DNN needs and how general the DNN method can be. Sampling and preprocessing determine the DNN training dataset, and further affect DNN prediction ability. The current work proposes using Box-Cox transformation (BCT) to preprocess the combustion data. In addition, this work compares different sampling methods with or without preprocessing, including the Monte Carlo method, manifold sampling, generative neural network method (cycle-GAN), and newly-proposed multi-scale sampling. Our results reveal that the DNN trained by the manifold data can capture the chemical kinetics in limited configurations but cannot remain robust toward perturbation, which is inevitable for the DNN coupled with the flow field. The Monte Carlo and cycle-GAN samplings can cover a wider phase space but fail to capture small-scale intermediate species, producing poor prediction results. A three-hidden-layer DNN, based on the multi-scale method without specific flame simulation data, allows predicting chemical kinetics in various scenarios and being stable during the temporal evolutions. This single DNN is readily implemented with several CFD codes and validated in various combustors, including (1). zero-dimensional autoignition, (2). one-dimensional freely propagating flame, (3). two-dimensional jet flame with triple-flame structure, and (4). three-dimensional turbulent lifted flames. The ignition delay time, laminar flame speed, lifted flame height, and contours of physical quantities demonstrate the satisfying accuracy and generalization ability of the pre-trained DNN. The Fortran and Python versions of DNN and example codes are attached in the supplementary for reproducibility, which can also be found on the https://github.com/tianhanz/DNN-Models-for-Chemical-Kinetics.}
}

@misc{xu2024solving,
      title={Solving multiscale dynamical systems by deep learning}, 
      author={Zhi-Qin John Xu and Junjie Yao and Yuxiao Yi and Liangkai Hang and Weinan E and Yaoyu Zhang and Tianhan Zhang},
      year={2024},
      eprint={2401.01220},
      doi = {https://arxiv.org/pdf/2401.01220.pdf},
      archivePrefix={arXiv},
      primaryClass={math.NA}
}

```
