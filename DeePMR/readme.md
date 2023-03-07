# DeePMR

DeePMR is one taks of the DeepCombustion project.  
DeePMR: DeeP Model Reduction, develop DNN-based algorithms for reducing chemical reaction mechanisms.

## Content of Models

This is a brief description of our reduced kinetic model, check the file readme.md in each sub-folder for detailed infomation.


| Model | Detailed Mechanism | Reduced<br>Species/Reactions | Detailed<br>Species/Reactions |
| :---: | :----: | :----: | :----: |
| [C701][4]  |  [Dryer_116sp_PRF][1]  |35/192 | 116/830 |
| [C702][5]  |  [LLNL_648sp_gasoline_surrogate][2]   |54/419 | 648/4846 |
| [C801][6]  |  [GMIT_857sp_iso-octane][3]   |46/301 | 857/6480 |


## Citation

We now have a [paper](https://arxiv.org/abs/2201.02025) you can cite for the reduced model library:

```
@article{wang2022deep,
  title={A deep learning-based model reduction (DeePMR) method for simplifying chemical kinetics},
  author={Wang, Zhiwei and Zhang, Yaoyu and Ju, Yiguang and Xu, Zhi-Qin John and Zhang, Tianhan},
  journal={arXiv preprint arXiv:2201.02025},
  year={2022}
}
```


[1]:https://onlinelibrary.wiley.com/doi/abs/10.1002/kin.20253?casa_token=c6moaDb5X8cAAAAA:YuDVLaHFZ9_mSmRCt2ghEiAsH12Lbp1IIcXWmx8llSjXFCq0e9fkgvb3e2hwe6wKvPI52dnbqeUTUV0
[2]:https://www.sciencedirect.com/science/article/pii/S1540748910000787?casa_token=OIW80_QsZB0AAAAA:I0alvoVky-3dZOqIFU-JCajEKagglHgnYbzjuKiXiD3ixFN7VeriIBfb_scKyTQzN2N_26UyQIk
[3]:https://www.sciencedirect.com/science/article/pii/S001021800100373X?casa_token=KrGC-ED1BQAAAAAA:-yNgs5Ka1W8uqOxt2Eqc4d7yVS6Tz5G4wwvxYRGLZuVNLSzYX9U2YSu4IO8OjveAL-KsovkqV4E
[4]:C701_Dryer_n-heptane_116sp_35sp_221017
[5]:C702_LLNL_n-heptane_648sp_54sp_221014
[6]:C801_GMIT_iso-octane_857sp_46sp_221015