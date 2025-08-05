===============================================================================
    CV EXTRACTION, STATE ASSIGNMENTS, AND STATE PROPORTIONS WITHIN SEGMENTS 
===============================================================================

Two subdirectories, one for each FF
    - CHARMM27_TIP3P/ 
    - CHARMM36m_TIP3P/

- CV_array_generator.ipynb 
    - Extracts the CVs (r_24, r_26, r_47, r_57) from the trajectories
    - OUTPUT: CV_array_{FF}.npy
        - Shape: (n_frames, n_CVs) = (25000000, 4)

- state_array_generator.ipynb 
    - Assigns each frame to a state based on the 4-state [ 1 2 3 4 ] model or 16-state [ 1 2 ... 15 16] model
    - OUTPUT: 04_states_array_{FF}.npy
        - Shape: (n_frames,) = (25000000,)
    - OUTPUT: 16_states_array_{FF}.npy
        - Shape: (n_frames,) = (25000000,)

- prop_array_generator.ipynb 
    - Calculates the proportions of each state (4-state model) within each 100-ps segment
    - OUTPUT: proportions_array_0100ps_CHARMM27_TIP3P_PAPER.npy
