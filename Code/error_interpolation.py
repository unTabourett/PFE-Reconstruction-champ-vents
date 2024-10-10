import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import random 
from data_extraction import extract_data_from_resp, preprocess_wind_data
import numpy as np

def create_test_dataset(nb_points, min_lat, max_lat, min_lon, max_lon, start_d, end_d, u_interp, v_interp):
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
    wind_data_test = pd.DataFrame({'lat': latitudes_test, 'lon': longitudes_test, 'date' : 0 ,'spd10': 0.0, 'spd100': 0.0,'dir10':0.0, 'dir100':0.0})

    extract_data_from_resp(responses_test, wind_data_test, nb_points)
    return wind_data_test

def error_interp(nb_points, altitude, test_dataset, u_interp, v_interp):
    error_L1 = 0
    error_L2 = 0
    preprocess_wind_data(test_dataset) #rajoute u et v à partir de speed direction
    for i in range(nb_points):
        u_interpolated_test = u_interp(test_dataset.loc[i, 'lat'], test_dataset.loc[i, 'lon'])
        v_interpolated_test = v_interp(test_dataset.loc[i, 'lat'], test_dataset.loc[i, 'lon'])
        test_dataset.loc[i, 'u_interp'] = u_interpolated_test
        test_dataset.loc[i, 'v_interp'] = v_interpolated_test
        error_L1 += np.abs(u_interpolated_test - test_dataset.loc[i, 'u'+str(altitude)]) + np.abs(v_interpolated_test - test_dataset.loc[i, 'v'+str(altitude)])
        error_L2 += (u_interpolated_test - test_dataset['u'+str(altitude)][i])**2 + (v_interpolated_test - test_dataset['v'+str(altitude)][i])**2
    return error_L1, error_L2
