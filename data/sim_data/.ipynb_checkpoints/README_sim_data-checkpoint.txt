==================================
    SIMULATION DATA AND INPUTS
==================================

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
