import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def wind_visualisation(data, altitude):
    # Création de la carte
    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.Mercator())

    # Tracer les contours de la Corse
    ax.coastlines()
    ax.set_extent([8.25, 9.6, 41.2, 43.1], crs=ccrs.PlateCarree())
    ax.set_title("Direction et vitesse du vent à "+str(altitude)+"m au temps " + wind_data['date'][0])
    
    
    ax.quiver(wind_data['lon'], wind_data['lat'], wind_data['u'+str(altitude)], wind_data['v'+str(altitude)], scale=300, transform=ccrs.PlateCarree(), color='r')
    
    plt.show()
