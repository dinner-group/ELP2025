#!/bin/bash

# SBATCH DIRECTIVES HERE

module load g_amide
module load g_spec
module load libmatheval

FF='CHARMM27_TIP3P'
DATADIR=/data/
TPR=$DATADIR/trajs/${FF}/0_setup/em.tpr
TRAJ=$DATADIR/trajs/${FF}/2_prod/spec_prod_${FF}_5.xtc

MAPDIR=$DATADIR/sim_data/mapfiles/
MAPFILE=$MAPDIR/DC1Fnew.txt
CHARGEFILE=$MAPDIR/ch27g.txt

g_amide -s $TPR -f $TRAJ -mapfile $MAPFILE -chargefile $CHARGEFILE
