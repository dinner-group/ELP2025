from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
from mdtraj.reporters import XTCReporter
import os

# System preparation

ffw = 'CHARMM36m_TIP3P'
num = 2

gro = GromacsGroFile('VPG_solv_ions.gro')
top = GromacsTopFile('topol.top', periodicBoxVectors=gro.getPeriodicBoxVectors(),
        includeDir=os.getcwd())
system = top.createSystem(nonbondedMethod=PME, nonbondedCutoff=1.2*nanometer,
        constraints=HBonds)
T = 283.15
integrator = LangevinMiddleIntegrator(T*kelvin, 1/picosecond, 0.002*picoseconds)
platform = Platform.getPlatformByName("CUDA")

simulation = Simulation(top.topology, system, integrator, platform=platform)
# save coordinates every 5000 x 2 fs = 10 ps for IVAC
simulation.reporters.append(XTCReporter(f'spec_prod_{ffw}_{num}.xtc', 5000))
simulation.reporters.append(StateDataReporter(f'spec_prod_{num}.log', 5000, step=True,
        potentialEnergy=True,
        kineticEnergy=True,
        totalEnergy=True,
        temperature=True,
        volume=True,
        density=True,
        #remainingTime=True,
        speed=True,
        elapsedTime=True,
        separator="\t"))
simulation.reporters.append(CheckpointReporter(f'spec_prod_{num}.chk', 25000))

if num == 1:
        restart_file = 'equil.chk'
else:
        restart_file = f'spec_prod_{num - 1}.chk'

with open(restart_file, "rb") as f:
    simulation.context.loadCheckpoint(f.read())

simulation.step(250000000) # 500 ns at a time
