##  Reduced model for the high-temperature n-heptane kinetic model (Dryer, 2007) 

Date: Oct 20, 2022; Maintainer: Zhiwei Wang.

### Detailed kinetic model 

- Mechanism: Dryer_n-heptane_116sp_detailed.yaml
- See: [Chaos M, Kazakov A, Zhao Z, et al. A high‐temperature chemical kinetic model for primary reference fuels[J]. International Journal of Chemical Kinetics, 2007, 39(7): 399-414.](https://onlinelibrary.wiley.com/doi/abs/10.1002/kin.20253?casa_token=c6moaDb5X8cAAAAA:YuDVLaHFZ9_mSmRCt2ghEiAsH12Lbp1IIcXWmx8llSjXFCq0e9fkgvb3e2hwe6wKvPI52dnbqeUTUV0)
- Species num: *<font color=red>116</font>*
- Reactions num: *<font color=red>830</font>*


### Model reduced by DeePMR

- Mechanism: Dryer_n-heptane_35sp_skeletal.yaml
- Species num: *<font color=red>35</font>*
- Reactions num: *<font color=red>192</font>*
- Overall average relative error: *<font color=red>less than 3%</font>*

### Working condition


**Zero-dimensional homogeneous ignition under constant pressure**

- initial condition
    - Temperature: *<font color=red>1200 ~ 1800 K</font>*
    - Pressure: *<font color=red>1 ~ 20 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 2</font>*
- validation
    ![IDT](validation/IDT.png)


**perfectly stirred reactors**
- initial condition
    - Temperature: *<font color=red>around 500 K</font>*
    - Pressure: *<font color=red>1 ~ 20 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 2</font>*
- validation
    ![PSR](validation/PSR_T=500K.png)


**One-dimensional premixed laminar flame** 
- initial condition
    - Temperature: *<font color=red>300 ~ 900 K</font>*
    - Pressure: *<font color=red>1 ~ 20 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 1.5</font>*
- validation
    ![Flame speed](validation/Flame_phi_500K_log.png)

    ![Flame speed](validation/Flame_1phi.png)

### DNN loss
This picture shows the DNN loss history during iterative sampling. The Adam optimizer and mean square loss function are used for training such DNN model.
![DNN loss](validation/loss_his.png)

