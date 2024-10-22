import numpy
import mayavi
from tvtk.api import tvtk

sphere = tvtk.SphereSource(radius=1.0)
sphere.update()

print("NumPy version:", numpy.__version__)
print("Mayavi version:", mayavi.__version__)

