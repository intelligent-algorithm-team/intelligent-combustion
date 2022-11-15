

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
 - Then the corresponding torch script `.pt` file will be saved in the sub-fold `Model/$(modelname)/checkpoint`.

## Navigation of models

See the file [`contents.md`](contents.md).
