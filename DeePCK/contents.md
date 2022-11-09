# Contents of Models

## Naming rules

Model Name: 
```
abbreviation_material_mechanism_sampling-method_[model-partition]_date
```

- `abbreviation` : initial of the material + initial of the mechanism + serial number.

- `material` : the fuel.

- `mechanism` : chemical mechanism.

- `sampling-method` : the sampling method we use.

- `model-partition` : (optional) sub-model 

- `date` : the date when model created.


For instance
```
MG01_Methane_GRI3_Man_20220731
```



## Model List

This is a brief description of our DNN models, check the file `Model/modelname/readme.md` in each sub-folder for detailed infomation.

<!-- | C701 |  |  |  |  |  |  | -->

| Model |Fuel| Mechanism | Species/Reactions| Auto-ignition | Flame Propagation | DNN Hidden Size| Publication|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [HE03](Model/HE03_Hydrogen_ESH2_GMS_20221019) |hydrogen(氢气)| [Evans-Schexnayder H2](https://arc.aiaa.org/doi/10.2514/3.50747) |8/16| Available | Available | -1600-800-400-| [Zhang et al., 2022](https://doi.org/10.1016/j.combustflame.2022.112319)
