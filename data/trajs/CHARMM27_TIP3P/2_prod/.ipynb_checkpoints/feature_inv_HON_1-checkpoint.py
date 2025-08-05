import sys
import numpy as np
import pyemma
from pyemma.util.contexts import settings

ffw = 'CHARMM27_TIP3P'
feature_name = 'inv_HON'
num = 1

traj_in = f'spec_prod_{ffw}_{num}.xtc'
gro = 'VPG_solv_ions.gro'

npy_out = f'spec_traj_{feature_name}_{num}.npy'

# Initialize the featurizer
feat = pyemma.coordinates.featurizer(gro)

# Select nitrogen, oxygen, and hydrogen atoms in the protein
nitrogen_atoms = feat.select('protein and name N')
oxygen_atoms = feat.select('protein and name O')
hydrogen_atoms = feat.select('protein and name H')

# Get the residue indices for each atom
topology = feat.topology
residue_indices_nitrogen = [topology.atom(atom_idx).residue.index for atom_idx in nitrogen_atoms]
residue_indices_oxygen = [topology.atom(atom_idx).residue.index for atom_idx in oxygen_atoms]
residue_indices_hydrogen = [topology.atom(atom_idx).residue.index for atom_idx in hydrogen_atoms]

# Create pairs of N/H and O/H but exclude those belonging to adjacent residues
pairs = []

# Add N-H pairs 
for i in range(len(nitrogen_atoms)):
    for j in range(len(hydrogen_atoms)):
        # Ensure the nitrogen and hydrogen are from residues that are at least one residue apart
        if abs(residue_indices_nitrogen[i] - residue_indices_hydrogen[j]) > 1:
            pairs.append([nitrogen_atoms[i], hydrogen_atoms[j]])

# Add O-H pairs 
for i in range(len(oxygen_atoms)):
    for j in range(len(hydrogen_atoms)):
        # At least one residue apart
        if abs(residue_indices_oxygen[i] - residue_indices_hydrogen[j]) > 1:
            pairs.append([oxygen_atoms[i], hydrogen_atoms[j]])

# Add the inverse distances of the selected pairs
feat.add_inverse_distances(pairs)

data = pyemma.coordinates.load(traj_in, features=feat, stride=1, chunksize=1000, parallel=True, processes=48)
np.save(npy_out, data)
