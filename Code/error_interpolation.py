# error_interpolation.py


"""
import numpy as np

from data_extraction import  preprocess_wind_data, data_opener
from data_interp_Spline import interpSplineLibrary
from database_choice import extract_file_names
"""

def create_test_dataset(nb_points, min_lat, max_lat, min_lon, max_lon, start_d, end_d):
	from data_extraction import extract_data_from_resp
	import requests_cache
	import pandas as pd
	from retry_requests import retry
	import random 
	import openmeteo_requests

	latitudes_test = [random.uniform(min_lat, max_lat) for _ in range(nb_points)]
	longitudes_test = [random.uniform(min_lon, max_lon) for _ in range(nb_points)]

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://archive-api.open-meteo.com/v1/archive"
	params_test = {
		"latitude": latitudes_test,
		"longitude": longitudes_test,
		"start_date": start_d,
		"end_date": end_d,
		"hourly": ["wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m"],
		"temporal_resolution": "hourly_6"
	}
	responses_test = openmeteo.weather_api(url, params=params_test)
	wind_data_test = pd.DataFrame({'lat': latitudes_test, 'lon': longitudes_test, 'date': pd.to_datetime(["2024-09-09 00:00:00+00:00"] * len(latitudes_test)),'spd10': 0.0, 'spd100': 0.0,'dir10':0.0, 'dir100':0.0})

	extract_data_from_resp(responses_test, wind_data_test, nb_points)
	return wind_data_test

def error_interp_df(nb_points, altitude, test_dataset, u_interp, v_interp):
	from data_extraction import  preprocess_wind_data
	from data_interp_Spline import interpSplineLibrary
	import numpy as np

	error_L1 = 0
	error_L2 = 0
	preprocess_wind_data(test_dataset) #rajoute u et v à partir de speed direction 
	u_name = 'u'+str(altitude)
	v_name = 'v'+str(altitude)
	for i in range(nb_points):
		u_interpolated_test = u_interp(test_dataset.loc[i, 'lat'], test_dataset.loc[i, 'lon'])
		v_interpolated_test = v_interp(test_dataset.loc[i, 'lat'], test_dataset.loc[i, 'lon'])
		test_dataset.loc[i, 'u_interp'] = u_interpolated_test
		test_dataset.loc[i, 'v_interp'] = v_interpolated_test
		error_L1 += np.abs(u_interpolated_test - test_dataset.loc[i, u_name]) + np.abs(v_interpolated_test - test_dataset.loc[i, v_name])
		error_L2 += (u_interpolated_test - test_dataset[u_name][i])**2 + (v_interpolated_test - test_dataset[v_name][i])**2
	return error_L1, error_L2

def error_interp_global(nb_points, dossier, altitude, pas_interp, min_lat, max_lat, min_lon, max_lon):
	from database_choice import extract_file_names
	import pandas as pd
	from data_extraction import data_opener, preprocess_wind_data
	from data_interp_Spline import interpSplineLibrary

	names_db = extract_file_names(dossier)
	list_errors = []
	
	df_test = create_test_dataset(nb_points, min_lat, max_lat, min_lon, max_lon, "2024-09-09", "2024-09-09")

	for name_db in names_db:
		data_tmp = data_opener(name_db)
		preprocess_wind_data(data_tmp)
		#print(data_tmp.columns)
		u_interp_tmp, v_interp_tmp = interpSplineLibrary(data_tmp, altitude, pas_interp, False)
		errorL1_tmp, errorL2_tmp = error_interp_df(nb_points, altitude, df_test, u_interp_tmp, v_interp_tmp)
		list_errors.append({'filename':name_db, 'erreurL1':errorL1_tmp, 'erreurL2':errorL2_tmp})
	errors = pd.DataFrame(list_errors)
	print(errors)
	errors_sorted = errors.sort_values(by='filename')
	errors_sorted.to_csv('../data/evol-errors-splines.csv', index = False)
	plot_errors(errors_sorted)
    
def plot_errors(errors):
	import matplotlib.pyplot as plt
	 # Plotting
	plt.figure(figsize=(10, 6))

	# Plot tmp1 and tmp2
	plt.plot(errors['filename'], errors['erreurL1'], marker='o', label='erreurL1', color='blue')
	plt.plot(errors['filename'], errors['erreurL2'], marker='o', label='erreurL2', color='orange')

	#plt.yscale('log') Pour l'echelle logarithmique au besoin
	# Adding labels and title
	plt.xlabel('Données')
	plt.ylabel('Errors in norm ')
	plt.title("Evolution de l'erreur selon le nombre de points interp")
	plt.xticks(rotation=45)  # Rotate filenames for better visibility
	plt.legend()
	plt.grid()

	# Show the plot
	plt.tight_layout()  # Adjust layout for better spacing
	plt.show()
