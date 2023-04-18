# DeePMR

DeePMR is one task of the DeepCombustion project.  
DeePMR: DeeP Model Reduction, develop DNN-based algorithms for reducing chemical reaction mechanisms.

## Content of Models

This is a brief description of our reduced kinetic model, check the file readme.md in each sub-folder for detailed infomation.


| Model | Detailed Mechanism | Reduced<br>Species/Reactions | Detailed<br>Species/Reactions |
| :---: | :----: | :----: | :----: |
| [C101][C101]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |20/146 | 648/4846 |
| [C201][C201]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |19/120 | 648/4846 |
| [C301][C301]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |20/132 | 648/4846 |
| [C401][C401]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |21/138 | 648/4846 |
| [C402][C402]  |  [JKL_341sp_C0-C4_skeletal][JKL]  |27/149 | 341/1977 |
| [C501][C501]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |24/165 | 648/4846 |
| [C601][C601]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |24/162 | 648/4846 |
| [C701][C701]  |  [Dryer_116sp_PRF][Dryer]               |35/192 | 116/830  |
| [C702][C702]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |54/419 | 648/4846 |
| [C703][C703]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |49/354 | 648/4846 |
| [C704][C704]  |  [LLNL_648sp_gasoline_surrogate][LLNL]  |41/292 | 648/4846 |
| [C801][C801]  |  [GMIT_857sp_iso-octane][GMIT]          |46/301 | 857/6480 |


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


[Dryer]:https://onlinelibrary.wiley.com/doi/abs/10.1002/kin.20253?casa_token=c6moaDb5X8cAAAAA:YuDVLaHFZ9_mSmRCt2ghEiAsH12Lbp1IIcXWmx8llSjXFCq0e9fkgvb3e2hwe6wKvPI52dnbqeUTUV0
[LLNL]:https://www.sciencedirect.com/science/article/pii/S1540748910000787?casa_token=OIW80_QsZB0AAAAA:I0alvoVky-3dZOqIFU-JCajEKagglHgnYbzjuKiXiD3ixFN7VeriIBfb_scKyTQzN2N_26UyQIk
[GMIT]:https://www.sciencedirect.com/science/article/pii/S001021800100373X?casa_token=KrGC-ED1BQAAAAAA:-yNgs5Ka1W8uqOxt2Eqc4d7yVS6Tz5G4wwvxYRGLZuVNLSzYX9U2YSu4IO8OjveAL-KsovkqV4E
[JKL]:https://pubs.acs.org/doi/10.1021/acs.energyfuels.1c00158
[C101]:C101_LLNL_methane_648sp_20sp_230307
[C201]:C201_LLNL_ethane_648sp_19sp_230307
[C301]:C301_LLNL_propane_648sp_20sp_230307
[C401]:C401_LLNL_n-butane_648sp_21sp_230307
[C402]:C402_JKL_n-butane_341sp_27sp_230307
[C501]:C501_LLNL_n-pentane_648sp_24sp_230307
[C601]:C601_LLNL_n-hexane_648sp_24sp_230307
[C701]:C701_Dryer_n-heptane_116sp_35sp_221017
[C702]:C702_LLNL_n-heptane_648sp_54sp_221014
[C703]:C703_LLNL_n-heptane_648sp_49sp_221027
[C704]:C704_LLNL_n-heptane_648sp_41sp_230307
[C801]:C801_GMIT_iso-octane_857sp_46sp_221015