import os
import numpy as np
import pyemma

ffw = 'CHARMM36m_TIP3P'
traj_dir = f'/project/dinner/ianjefab/research/ELP/paper/IVAC_prod/{ffw}'
gro_file = os.path.join(traj_dir, 'VPG_solv_ions.gro')

# Initialize Featurizer
feat = pyemma.coordinates.featurizer(gro_file)

# Get all atoms named 'C' and their corresponding residue indices
atom_indices = [i for i, atom in enumerate(feat.topology.atoms) if atom.name == 'C']
res_indices = np.array([feat.topology.atom(i).residue.index for i in atom_indices])

# Generate distance pairs only if residues are at least 2 apart
dist_pairs = [(atom_indices[i], atom_indices[j]) 
              for i in range(len(atom_indices)) 
              for j in range(i + 1, len(atom_indices)) 
              if abs(res_indices[i] - res_indices[j]) >= 2]

# Ensure there are distance pairs before proceeding
if not dist_pairs:
    raise ValueError("No valid atom pairs found for distance computation.")

# Add distance features using PyEMMA's featurizer
feat.add_distances(dist_pairs, periodic=True)

# Process multiple trajectory files
for num in range(1, 11):
    traj_in = os.path.join(traj_dir, f'spec_prod_{ffw}_{num}.xtc')
    npy_out = f'C_feat_{ffw}_{num}.npy'

    if not os.path.exists(traj_in):
        print(f"Warning: Missing trajectory file {traj_in}, skipping.")
        continue

    # Load trajectory and compute distances
    data = pyemma.coordinates.load(traj_in, features=feat)  # every ps

    # Save feature data
    np.save(npy_out, data)
    print(f"Saved {npy_out}")
