# main.py

from data_extraction import extract_data_from_api, preprocess_wind_data, data_opener
from data_visualisation import wind_visualisation
from data_interp_Spline import interpSplineLibrary

def main():
	#Initialisation des variables
	lat_min = 41.5
	lat_max = 42.21 #43.01
	lon_min = 8.5
	lon_max = 9.51
	pas = 0.06
	start_d = "2024-09-09"
	end_d = "2024-09-09"
	
	#Si on veut créer un nouveau dataset :
	#wind_data = extract_data_from_api(lat_min, lat_max, lon_min, lon_max, pas, start_d, end_d)
	
	name_file = "df_117.csv"
	wind_data = data_opener(name_file)
	preprocess_wind_data(wind_data)
	
	altitude = 10 #ou 100
	
	#Si on veut afficher le champ de vents
	#wind_visualisation(wind_data, altitude)
	
	pas_interpolation = 10e-2
	interpSplineLibrary(wind_data, altitude, pas_interpolation)
	
if __name__ == "__main__":
	main()
	
	
