================================================================================
                                 ALL DATA FOR:                                  
                Using Multiple Isotope-Labeled Infrared Spectra                 
                      for the Structural Characterization                       
                     of an Intrinsically Disordered Peptide                     
================================================================================

Individual README files available within each subdirectory, reproduced here for convenience:


=================================================
    error_data/ : ERROR TERMS FOR REWEIGHTING
=================================================

Output of all .ipynb files is of shape (n_segments, n_thetas) = (5000, 1000)

error_overlap_full.ipynb
    - Calculates error terms used for 
    - Outputs to ./overlap_full/

error_overlap_nomainband.ipynb
    - Same function as error_overlap_full.ipynb, but restricts fit to below main band (<1625 cm^-1)
    - Outputs to ./overlap_nomainband/

The following use the informative regions and labels identified in Figure S15

error_overlap_N_regions.ipynb
    - Same function as error_overlap_full.ipynb, but restricts fit to informative regions for N-bend
    - Outputs to ./overlap_informative/

error_overlap_C_regions.ipynb
    - Same function as error_overlap_full.ipynb, but restricts fit to informative regions for C-turn
    - Outputs to ./overlap_informative/


=====================================
    exp_data/ : EXPERIMENTAL DATA
=====================================

Note: in original Lessing naming scheme

raw_FTIRs/
    - Contains all raw experimental data
    - GVGn1_{ORIGINAL}_50mgmL_phos_150mM_pH1_basecorr.CSV
        - Note: '+' is 'dag'

process_FTIR_data.ipynb
    - Processes FTIR data (Figure S1)

processed_FTIRs/ 
    - Contains all processed FTIR data
    - GVGn1_{ORIGINAL}_50mgmL_phos_150mM_pH1_basecorr_processed.npy

+----------+-------------+
| Original | Publication |
+----------+-------------+
| G3dag    | G1          |
| G5dag    | G3          |
| V1       | V4          |
| G3       | G6          |
| V4       | V7          |
+----------+-------------+


===================================================
    ivac/ : IVAC TRAJECTORIES AND FEATURIZATION
===================================================

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



=============================================================================================
    prop_array/ : CV EXTRACTION, STATE ASSIGNMENTS, AND STATE PROPORTIONS WITHIN SEGMENTS 
=============================================================================================

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



==============================================
    sim_data/ : SIMULATION DATA AND INPUTS
==============================================

g_amide/, g_spec/, and sim_data/ each have two subdirectories, one for each FF
    - CHARMM27_TIP3P/ 
    - CHARMM36m_TIP3P/

Note: 
- CHARMM27_TIP3P is divided into 5 x 100 ns segments
- CHARMM36m_TIP3P is all in 1 x 500 ns segment 

g_amide/ 
- Files necessary to calculate the amide I Hamiltonian from MD trajectories
- Outputs for 500 ns trajectory used for paper 

g_spec/ 
- Example of sbatch script to calculate spectrum for a given segment and label

mapfiles/ contains Reppert 1-site field map used in g_amide inputs
shiftfiles/ contains frequency shifts for isotope labels for g_spec inputs

sim_data/ 
- Contains all simulated spectra for the 5000 segments
- np arrays of shape (n_segments, n_wavenumbers) = (5000, 225)
- Note: naming scheme is original naming scheme from Lessing thesis

+----------+-------------+
| Original | Publication |
+----------+-------------+
| G3+      | G1          |
| G5+      | G3          |
| V1       | V4          |
| G3       | G6          |
| V4       | V7          |
+----------+-------------+



=============================
    trajs/ : TRAJECTORIES
=============================

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
