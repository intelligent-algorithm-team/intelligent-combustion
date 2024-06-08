import cantera as ct 
import os  

import warnings
warnings.filterwarnings('ignore')

for subdir, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            mech_path = os.path.join(subdir, file)
            gas = ct.Solution(mech_path)
            print("Mechanism: ", mech_path)
            print("Number of species and reactions: ", gas.n_species, gas.n_reactions)
            
