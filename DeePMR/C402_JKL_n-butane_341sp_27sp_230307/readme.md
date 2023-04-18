## Reduced model for the n-butane kinetic model (JKL, 2021) 

Date: Mar 07, 2023; Maintainer: Zhiwei Wang.

### Detailed kinetic model 

- Mechanism: JKL_n-butane_341sp_detailed.yaml
- See [Si J, Wang G, Li P, et al (2021) A new skeletal mechanism for simulating MILD combustion optimized using Artificial Neural Network. Energy 237:121,603](https://www.sciencedirect.com/science/article/pii/S036054422101851X)
- Species num: *<font color=red>341</font>*
- Reactions num: *<font color=red>1977</font>*

### Model reduced by DeePMR

- Mechanism: JKL_n-butane_27sp_skeletal.yaml
- Species num: *<font color=red>27</font>*
- Reactions num: *<font color=red>149</font>*
- Overall average relative error: *<font color=red>14.8%</font>*

### Working condition

**Zero-dimensional homogeneous ignition under constant pressure**

- initial condition
    - Temperature: *<font color=red>1000 ~ 1400 K</font>*
    - Pressure: *<font color=red>1 ~ 40 atm</font>*
    - Equivalence ratio: *<font color=red>0.5 ~ 2</font>*
- validation
    
    ![IDT](validation/IDT.png)