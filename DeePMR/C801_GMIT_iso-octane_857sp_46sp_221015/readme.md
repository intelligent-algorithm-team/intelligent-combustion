## Reduced model for the iso-octane kinetic model (GMIT, 2002) 

Date: Oct 20, 2022; Maintainer: Zhiwei Wang.

### Detailed kinetic model 

- Mechanism: GMIT_iso-octane_857sp_detailed.yaml
- See [Curran H J, Gaffuri P, Pitz W J, et al. A comprehensive modeling study of iso-octane oxidation[J]. Combustion and flame, 2002, 129(3): 253-280.](https://www.sciencedirect.com/science/article/pii/S001021800100373X?casa_token=KrGC-ED1BQAAAAAA:-yNgs5Ka1W8uqOxt2Eqc4d7yVS6Tz5G4wwvxYRGLZuVNLSzYX9U2YSu4IO8OjveAL-KsovkqV4E)
- Species num: *<font color=red>857</font>*
- Reactions num: *<font color=red>6480</font>*

### Model reduced by DeePMR

- Mechanism: GMIT_iso-octane_46sp_skeletal.yaml
- Species num: *<font color=red>46</font>*
- Reactions num: *<font color=red>301</font>*
- Overall average relative error: *<font color=red>less than 15%</font>*

### Working condition

**Zero-dimensional homogeneous ignition under constant pressure**

- initial condition
    - Temperature: *<font color=red>600 ~ 1700 K</font>*
    - Pressure: *<font color=red>1 ~ 40 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 1.5</font>*
- validation
    ![IDT](validation/IDT.png)


**perfectly stirred reactors**
- initial condition
    - Temperature: *<font color=red>around 500 K</font>*
    - Pressure: *<font color=red>1 ~ 40 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 1.5</font>*
- validation
    ![PSR](validation/PSR_T=500K.png)


**One-dimensional premixed laminar flame** 
- initial condition
    - Temperature: *<font color=red>298 ~ 500 K</font>*
    - Pressure: *<font color=red>1 ~ 40 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 1.5</font>*
- validation
    ![Flame speed](validation/Flame_phi_298K_log.png)

    ![Flame speed](validation/Flame_phi_500K_log.png)

### Reaction graph
This picture is the species-reaction graph for reduced iso-octane mechanism. Circles represent species, and black dots represent reactions. Species are colored according to class and sized according to vortex degree.
![reaction graph](validation/graph.png)


### DNN loss
This picture shows the DNN loss history during iterative sampling. The SGD optimizer and mean square loss function are used for training such DNN model.
![DNN loss](validation/loss_his.png)