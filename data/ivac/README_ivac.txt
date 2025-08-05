===========================================
    IVAC TRAJECTORIES AND FEATURIZATION
===========================================

IVAC trajectories to determine slow modes

(N = 1 .. 10)

trajs/
    - prod_{N}.py (N = 1 .. 10)
        - Production 
        - 10 x 500 ns trajectories = 5 us

feat/
    - C_feat_CHARMM36m_TIP3P.py
        - Featurizes trajectories from trajs/ by amide C distances at least two residues apart
    - C_feat_CHARMM36m_TIP3P_{N}.npy
        - Featurized trajectories
        - Shape: (n_frames, n_feat) = (50000, 21)
