# main.py

from data_extraction import preprocess_wind_data, data_opener, extract_data_from_api
from data_visualisation import wind_visualisation2D, wind_visualisation3D
from database_choice import choix_db
from error_interpolation import error_interp_global
from data_interp_Spline import interpSplineLibrary
import pandas as pd
def main():
	#Initialisation des variables
	"""lat_min = 41.5
	lat_max = 42.21 #43.01
	lon_min = 8.5
	lon_max = 9.51
	pas = 0.06
	start_d = "2024-09-09"
	end_d = "2024-09-09"""
	lat_min = 42.0
	lat_max = 51.5 #43.01
	lon_min = -5.0
	lon_max = 10.0
	pas_lat = 1.0
	pas_lon = 5.0
	start_d = "2024-09-09"
	end_d = "2024-09-09"
	createDataset = False #Mettre à True pour créer un nouveau dataset
	interp3D = True

	
	if (createDataset):
		#Si on veut créer un nouveau dataset :
		extract_data_from_api(lat_min, lat_max, lon_min, lon_max, pas_lat, pas_lon, start_d, end_d)
	
	chemin_dossier = '../data/API/'
	file_name = choix_db(chemin_dossier)
	
	if interp3D:
		wind_data3D = data_opener(file_name)
		preprocess_wind_data(wind_data3D)
		wind_visualisation3D(wind_data3D, lon_min, lon_max, lat_min, lat_max)
	else:
		altitude = 10 #ou 100
		pas_interpolation = 10e-3
		print("Interpolation 2D : Altitude "+str(altitude)+"m - pas d'interp : "+ str(pas_interpolation))
		
		#Si on veut afficher le champ de vents
		#wind_visualisation(wind_data, 8.25, 9.6, 41.2, 43.1, altitude) Corsica

		
		
		if (file_name == "Erreur-Interpolation"): #Erreur globale par nb de points
			nb_points = 100
			error_interp_global(nb_points, chemin_dossier, altitude, pas_interpolation, lat_min, lat_max, lon_min, lon_max)
			#error_interp_global(nb_points, chemin_dossier, altitude, pas_interpolation)
		else: #Visualisation d'un dataset
			
			wind_data = data_opener(file_name)
			preprocess_wind_data(wind_data)
			wind_visualisation2D(wind_data, lon_min, lon_max, lat_min, lat_max, altitude) 

		#u_interp, v_interp = interpSplineLibrary(wind_data, altitude, pas_interpolation, True)
	
	
	
if __name__ == "__main__":
	main()
	
	
