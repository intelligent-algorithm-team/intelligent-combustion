# DeePMR
Fuel chemistry represents a typical complex system involving thousands of intermediate species and elementary reactions. Traditional mechanism reduction methods, such as sensitivity analysis and graph-based approaches, fail to explore global correlations of the sub-systems, thereby compromising their efficiency and accuracy. A novel machine learning-based approach called deep mechanism reduction (DeePMR) has been developed to address this issue. The current method transforms mechanism reduction into an optimization problem in the combinatorial space of chemical species while mitigating the curse of dimensionality inherent in the high-dimensional space. We propose an iterative sampling–training–predicting strategy combining deep neural networks with genetic algorithms to learn the landscape of the combinatorial space and locate the targeted subspace. Applying DeePMR to fuel chemistry mechanisms has led to much more compact mechanisms than traditional methods, including directed relation graph (DRG) or path flux analysis (PFA) methods, with three to four orders of magnitude acceleration in numerical simulation. In addition, reduced mechanisms by DeePMR indicate a principal-satellite formulation for constructing chemical reaction mechanisms, providing a straightforward yet effective alternative to hierarchy-based construction methods. The DeePMR method provides a general framework for model reduction across various fields.

We shared all reduced models in the current repo. 

## Content of Models

This is a brief description of our reduced kinetic models; check the file `readme.md` in each sub-folder for detailed information.


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


## DeePMR-reduced mechanisms for supersonic combustion

The detailed ethylene oxidation mechanism with 57 species and 269 reactions was reduced via DeePMR method with different indicators, and further validated in the practical supersonic combustion. See [HiSCFOAM] for more information.

## Citation
Please cite: 
```
@article{wang2024deep,
  title={Deep mechanism reduction (DeePMR) method for fuel chemical kinetics},
  author={Wang, Zhiwei and Zhang, Yaoyu and Lin, Pengxiao and Zhao, Enhan and Weinan, E and Zhang, Tianhan and Xu, Zhi-Qin John},
  journal={Combustion and Flame},
  volume={261},
  pages={113286},
  year={2024},
  publisher={Elsevier}
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
