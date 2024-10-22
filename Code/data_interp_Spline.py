# data_interp_Spline.py

from scipy.interpolate import RectBivariateSpline
from error_interpolation import create_test_dataset, error_interp_df
import numpy as np
import matplotlib.pyplot as plt

def plot_interp(u_interpolated,v_interpolated, lat_interp, lon_interp, altitude):
    # Création d'une figure avec deux sous-graphes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
    
    # Carte de u_interpolated
    contour_u = ax1.contourf(lon_interp, lat_interp, u_interpolated, cmap='coolwarm')
    ax1.set_title('Interpolation des valeurs de vent (u) à '+str(altitude)+'m')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    fig.colorbar(contour_u, ax=ax1, label='Valeur du vent (u) interpolé')
    
    # Carte de v_interpolated
    contour_v = ax2.contourf(lon_interp, lat_interp, v_interpolated, cmap='coolwarm')
    ax2.set_title('Interpolation des valeurs de vent (v) à '+str(altitude)+'m')
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    fig.colorbar(contour_v, ax=ax2, label='Valeur du vent (v) interpolé')
    
    # Affiche les deux cartes côte à côte
    plt.tight_layout()
    plt.show()

def interpSplineLibrary(data, altitude, pas_interp, UnSeulDataset) :
	min_lat, max_lat, min_lon, max_lon = min(data['lat']), max(data['lat']), min(data['lon']), max(data['lon'])
	latitudes = np.unique(data['lat'])
	longitudes = np.unique(data['lon'])

	latitudes_interp = np.arange(min_lat, max_lat, pas_interp)
	longitudes_interp = np.arange(min_lon, max_lon, pas_interp)

	wind_data_u_grid = np.empty([len(latitudes), len(longitudes)], dtype = float)
	wind_data_u_grid[:] = data['u'+str(altitude)].values[:data.size].reshape((len(latitudes),len(longitudes)))

	wind_data_v_grid = np.empty([len(latitudes), len(longitudes)], dtype = float)
	wind_data_v_grid[:] = data['v'+str(altitude)].values[:data.size].reshape((len(latitudes),len(longitudes)))

	test_u_interp = RectBivariateSpline(latitudes,longitudes,wind_data_u_grid, bbox=[min_lat, max_lat, min_lon, max_lon])
	test_v_interp = RectBivariateSpline(latitudes,longitudes,wind_data_v_grid, bbox=[min_lat, max_lat, min_lon, max_lon])

	u_interpolated = test_u_interp(latitudes_interp, longitudes_interp)
	v_interpolated = test_v_interp(latitudes_interp, longitudes_interp)
	if (UnSeulDataset):
		plot_interp(u_interpolated, v_interpolated, latitudes_interp, longitudes_interp, altitude)
	return test_u_interp, test_v_interp
	
