import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def wind_visualisation(data, lat_min, lat_max, lon_min, lon_max, altitude):
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
