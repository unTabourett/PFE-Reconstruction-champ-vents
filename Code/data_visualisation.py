import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

from mayavi import mlab

def wind_visualisation2D(data, lat_min, lat_max, lon_min, lon_max, altitude):
    # Création de la carte
    plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.Mercator())

    # Tracer les contours de la Corse
    ax.coastlines()
    ax.set_extent([-15.0, 15.0, 30.0, 60.5], crs=ccrs.PlateCarree())
    ax.set_title("Direction et vitesse du vent à "+str(altitude)+"m au temps " + data['date'][0])
    print(data.head(3))
    ax.quiver(data['lon'], data['lat'], data['u'+str(altitude)], data['v'+str(altitude)], scale=300, transform=ccrs.PlateCarree(), color='r')
    
    plt.show()

def wind_visualisation3D(data, lat_min, lat_max, lon_min, lon_max):
    # Créer une figure Mayavi
    mlab.figure(size=(800, 600), bgcolor=(1, 1, 1))

    # Tracer les vecteurs de vent à 10 m
    mlab.quiver3d(data['lon'], data['lat'], np.zeros_like(data['lon']),
                data['u10'], data['v10'], np.zeros_like(data['u10']),
                scale_factor=0.5, color=(0, 0, 1), line_width=1, mode='arrow')

    # Tracer les vecteurs de vent à 100 m
    mlab.quiver3d(data['lon'], data['lat'], np.ones_like(data['lon']),
                data['u100'], data['v100'], np.ones_like(data['u100']),
                scale_factor=0.5, color=(1, 0, 0), line_width=1, mode='arrow')

    # Configurer les axes
    mlab.axes(xlabel='Longitude', ylabel='Latitude', zlabel='Altitude (m)', color=(0, 0, 0))
    mlab.title("Champ de vents le " + data['date'][0])

    # Afficher la visualisation
    mlab.show()

    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Tracer les vecteurs de vent à 10 m
    ax.quiver(data['lon'], data['lat'], np.zeros_like(data['lon']), data['u10'], data['v10'], np.zeros_like(data['u10']), color='blue', length=0.1, label='Vent à 10 m')

    # Tracer les vecteurs de vent à 100 m
    ax.quiver(data['lon'], data['lat'], np.ones_like(data['lon']),  data['u100'], data['v100'], np.ones_like(data['u100']), color='red', length=0.1, label='Vent à 100 m')

    # Configurer les axes
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude (m)')
    ax.set_title("Champ de vents le " + data['date'][0])
    
    ax.legend()

    # Afficher la visualisation
    plt.show()"""
