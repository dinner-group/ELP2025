from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
from mdtraj.reporters import XTCReporter
import os

# System preparation

gro = GromacsGroFile('VPG_solv_ions.gro')
top = GromacsTopFile('topol.top', periodicBoxVectors=gro.getPeriodicBoxVectors(),
        includeDir=os.getcwd())
system = top.createSystem(nonbondedMethod=PME, nonbondedCutoff=1.2*nanometer,
        constraints=HBonds)
T = 283.15
integrator = LangevinMiddleIntegrator(T*kelvin, 1/picosecond, 0.002*picoseconds)
platform = Platform.getPlatformByName("CUDA")

# Position restraints for equilibration

restraint = CustomExternalForce('k*periodicdistance(x, y, z, x0, y0, z0)^2')
system.addForce(restraint)
restraint.addGlobalParameter('k', 100.0*kilojoules_per_mole/nanometer)
restraint.addPerParticleParameter('x0')
restraint.addPerParticleParameter('y0')
restraint.addPerParticleParameter('z0')

for atom in top.topology.atoms():
    if atom.name in ['CA', 'C', 'N']:
        restraint.addParticle(atom.index, gro.positions[atom.index])

# Simulation setup

simulation = Simulation(top.topology, system, integrator)
simulation.reporters.append(XTCReporter('equil.xtc', 1000))
simulation.reporters.append(StateDataReporter('equil.log', 100, step=True,
        potentialEnergy=True,
        kineticEnergy=True,
        totalEnergy=True,
        temperature=True,
        volume=True,
        density=True,
        speed=True,
        elapsedTime=True,
        separator="\t"))
simulation.reporters.append(CheckpointReporter('equil.chk', 100))
simulation.context.setPositions(gro.positions)

# EQUILIBRATION PROCESS

# Energy minimization

simulation.minimizeEnergy()

# NVT with position restraints, 100 ps

print('NVT with position restraints, 100 ps')
mdsteps = 50000
simulation.step(mdsteps)

# NPT with position restraints, 10 ns
# Was supposed to be 10 ns (5000000 steps) was but was accidentally truncated to 1 ps (500 steps) for production,
# but box size equilibrates very quickly/sufficiently in the 1 ns NPT equilibration used later

# mdsteps = 5000000
barostat = system.addForce(MonteCarloBarostat(1 * atmosphere, T * kelvin, 25))
simulation.context.setVelocitiesToTemperature(T * kelvin)

mdsteps = 500
simulation.step(mdsteps)

# Remove position restraints

restraint_index = next((i for i, f in enumerate(system.getForces()) if isinstance(f, openmm.CustomExternalForce)), -1)
system.removeForce(restraint_index) if restraint_index != -1 else print("The restraint force was not found in the system.")

# NPT without position restraints, 1 ns

mdsteps = 500000
simulation.context.reinitialize(True)
simulation.step(mdsteps)

# NVT without position restraints, 5 ns

barostat_index = next((i for i, f in enumerate(system.getForces()) if isinstance(f, openmm.MonteCarloBarostat)), -1)
system.removeForce(barostat_index) if barostat_index != -1 else print("Error")

mdsteps = 2500000
simulation.context.reinitialize(True)
print('NVT without position restraints, 5 ns')
simulation.step(mdsteps)

simulation.saveState('equil.xml')
