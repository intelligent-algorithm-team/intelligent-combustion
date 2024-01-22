

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
    author = {Tianhan Zhang and Yuxiao Yi and Yifan Xu and Zhi X. Chen and Yaoyu Zhang and Weinan E and Zhi-Qin John Xu},
    journal = {Combustion and Flame},
    volume = {245},
    pages = {112319},
    year = {2022},
    issn = {0010-2180},
    doi = {https://doi.org/10.1016/j.combustflame.2022.112319},
    url = {https://www.sciencedirect.com/science/article/pii/S0010218022003340},
}

@misc{xu2024solving,
    title={Solving multiscale dynamical systems by deep learning}, 
    author={Zhi-Qin John Xu and Junjie Yao and Yuxiao Yi and Liangkai Hang and Weinan E and Yaoyu Zhang and Tianhan Zhang},
    year={2024},
    eprint={2401.01220},
    url = {https://arxiv.org/pdf/2401.01220.pdf},
    archivePrefix={arXiv},
    primaryClass={math.NA}
}

```
