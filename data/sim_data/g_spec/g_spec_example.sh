#!/bin/bash

# Assume N segments
# Split up the Hamiltonian files into N directories with unique NUM containing:
# ham.txt dipx.txt dipy.txt dipz.txt
# For the frames corresponding to that segment

module load g_amide
module load g_spec
module load libmatheval

NUM='0001'
SHIFT='WT'
SPLIT_AMIDE_DIR='HERE' # Directory with split g_amide inputs, as mentioned above

DATADIR=/data/
SHIFT_DIR=$DATADIR/sim_data/shiftfiles/

g_spec -deffnm ${SPLIT_AMIDE_DIR}/g_amide_${NUM}/ -shift $SHIFT_DIR/shift_WT.txt -outname DC1Fnew_WT_${NUM} -tstep 20 -tscan 10000 -nise

# Assumes 20 fs sample rate in .xtc
