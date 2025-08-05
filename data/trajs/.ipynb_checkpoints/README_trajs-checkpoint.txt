====================
    TRAJECTORIES
====================

Two subdirectories, one for each FF, with GROMACS FF inputs
    - CHARMM27_TIP3P/ 
    - CHARMM36m_TIP3P/
Note: 
    - CHARMM27_TIP3P is divided into 5 x 100 ns segments
    - CHARMM36m_TIP3P is all in 1 x 500 ns segment 

0_setup/
    - Setup files for system, prepared with GROMACS

1_equil/
    - Equilibration files for system, with OpenMM 8.0
    - equil.py
        - 100 ps NVT with position restraints, 1 ps NPT with position restraints, 1 ns NPT, 5 ns NVT
        - NOTE: second step was supposed to be 10 ns NPT with position restraints, 
        but copy/paste error truncated nsteps. However, system is sufficiently equilibrated 
        (1 ps NPT more than sufficient to converge box size for small peptide).

2_prod/
    - Production files, with OpenMM 8.0
    - prod.py (or prod_{N}.py)
        - Outputs trajectory
    - feature_inv_HON.py (or feature_inv_HON_{N}.py)
        - Featurization for distance analysis
        - Note: .py script uses inverse distances, but they are reinverted back for analysis
        - Output: spec_traj_inv_HON.npy (or spec_traj_inv_HON_{N}.npy
            - Shape: (n_frames, n_feat) = (5000000, 74) x 5 for C27, (25000000, 74) for C36m
            - Located in /data/prop_array/{FF}
