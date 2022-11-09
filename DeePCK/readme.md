

# DeePCK : Deep Chemical Kinetics

DeePCK is a task of the DeepCombustion project, which aims at developing DNN-based surrogate model to accelerate the simulation of chemical kinetics.

This open project will release various models based on our algorithms.

## How to use DNN model

- create python environment including `torch`, `cantera`, `matplotlib` and `easydict`.

- cofigure `modelname`, `mech_path` in the file `useModel.py`

- Then execute the following command: 

    ```python
    python useModel.py
    ```

## Navigation of models

See the file [`contents.md`](contents.md).