from fipy import CellVariable, FaceVariable, Grid2D, DiffusionTerm, Viewer
from fipy.tools import numerix
from fipy.variables.faceGradVariable import _FaceGradVariable
import numpy as np
import time

# Define grid parameters
latitudes = np.linspace(0, 1, 10)  # Example latitudes
longitudes = np.linspace(0, 1, 10)  # Example longitudes
nlong = 0.1  # Example grid spacing in the x-direction
nlat = 0.1   # Example grid spacing in the y-direction

# Create mesh
mesh = Grid2D(nx=len(latitudes), ny=len(longitudes), dx=nlong, dy=nlat)

# Define variables
pressure = CellVariable(mesh=mesh, name='pressure')
pressureCorrection = CellVariable(mesh=mesh)
uVelocity = CellVariable(mesh=mesh, name='u velocity')
vVelocity = CellVariable(mesh=mesh, name='v velocity')
velocity = FaceVariable(mesh=mesh, rank=1)

# Constants
viscosity = 14.88e-6  # Adjusted the scientific notation
u_ = 1.0
pressureRelaxation = 0.8
velocityRelaxation = 0.5

# Number of sweeps based on the script context
sweeps = 300 if __name__ == '__main__' else 5

# Stokes equations
uVelocityEq = DiffusionTerm(coeff=viscosity) - pressure.grad.dot([1.0, 0.0])
vVelocityEq = DiffusionTerm(coeff=viscosity) - pressure.grad.dot([0.0, 1.0])

# Coefficient for pressure correction
ap = CellVariable(mesh=mesh, value=1.0)
coeff = 1. / ap.arithmeticFaceValue * mesh._faceAreas * mesh._cellDistances
pressureCorrectionEq = DiffusionTerm(coeff=coeff) - velocity.divergence

# Volume and face volumes
volume = CellVariable(mesh=mesh, value=mesh.cellVolumes, name="Volume")
contrvolume = volume.arithmeticFaceValue

# Boundary conditions
uVelocity.constrain(0.0, mesh.facesRight | mesh.facesLeft | mesh.facesBottom)
uVelocity.constrain(u_, mesh.facesTop)
vVelocity.constrain(0.0, mesh.exteriorFaces)
pressureCorrection.constrain(0.0, mesh.facesLeft & (mesh.faceCenters[1] < nlat))

# Viewer setup
viewer = Viewer(vars=(pressure, uVelocity, vVelocity, velocity),
                xmin=min(longitudes), xmax=max(longitudes),
                ymin=min(latitudes), ymax=max(latitudes),
                colorbar='vertical', scale=5)

# Main simulation loop
for sweep in range(sweeps):
    # Solve the Stokes equations to get starred values
    uVelocityEq.cacheMatrix()
    ures = uVelocityEq.sweep(var=uVelocity, underRelaxation=velocityRelaxation)
    umat = uVelocityEq.matrix
    vres = vVelocityEq.sweep(var=vVelocity, underRelaxation=velocityRelaxation)

    # Update ap coefficient from the matrix diagonal
    ap[:] = -numerix.asarray(umat.takeDiagonal())

    # Update face velocities using Rhie-Chow correction
    presgrad = pressure.grad
    facepresgrad = _FaceGradVariable(pressure)
    velocity[0] = uVelocity.arithmeticFaceValue + contrvolume / ap.arithmeticFaceValue * (presgrad[0].arithmeticFaceValue - facepresgrad[0])
    velocity[1] = vVelocity.arithmeticFaceValue + contrvolume / ap.arithmeticFaceValue * (presgrad[1].arithmeticFaceValue - facepresgrad[1])
    
    # Enforce boundary conditions
    velocity[..., mesh.exteriorFaces.value] = 0.0
    velocity[0, mesh.facesTop.value] = u_

    # Solve the pressure correction equation
    pressureCorrectionEq.cacheRHSvector()
    pres = pressureCorrectionEq.sweep(var=pressureCorrection)
    rhs = pressureCorrectionEq.RHSvector

    # Update the pressure
    pressure.setValue(pressure + pressureRelaxation * pressureCorrection)

    # Update the velocity
    uVelocity.setValue(uVelocity - pressureCorrection.grad[0] / ap * mesh.cellVolumes)
    vVelocity.setValue(vVelocity - pressureCorrection.grad[1] / ap * mesh.cellVolumes)

    # Output for monitoring
    if __name__ == '__main__':
        if sweep % 10 == 0:
            print(f'sweep: {sweep}, u residual: {ures}, v residual: {vres}, p residual: {pres}, continuity: {max(abs(rhs))}')
            viewer.plot()
            time.sleep(3)
