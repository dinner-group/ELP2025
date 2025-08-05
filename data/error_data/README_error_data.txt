===================================
    ERROR TERMS FOR REWEIGHTING
===================================

RUN THE .ipynb FILES BEFORE MAKING FIGURES

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
