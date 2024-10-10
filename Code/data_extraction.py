# data_extraction.py

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import openmeteo_requests
import requests_cache
from retry_requests import retry
from openmeteo_sdk.Variable import Variable

def extract_data_from_resp(response, wind_data, nb_coord): #Sort un dataframe avec les valeurs pour les 4 fuseaux horaires des nb_coord coordonnées
    for i in range(nb_coord): #On prend les données coordonnée par coordonnée
        resp = response[i] #i-ème coordonnée 
        hourl = resp.Hourly()
        
        hourl_wind_speed_10m = hourl.Variables(0).ValuesAsNumpy()
        hourl_wind_speed_100m = hourl.Variables(1).ValuesAsNumpy()
        hourl_wind_direction_10m = hourl.Variables(2).ValuesAsNumpy()
        hourl_wind_direction_100m = hourl.Variables(3).ValuesAsNumpy()
        hourl_data = {"date": pd.date_range(
            start = pd.to_datetime(hourl.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourl.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourl.Interval()),
            inclusive = "left"
        )}
        
        hourl_data["spd10"] = hourl_wind_speed_10m
        hourl_data["dir10"] = hourl_wind_direction_10m
        hourl_data["spd100"] = hourl_wind_speed_100m
        hourl_data["dir100"] = hourl_wind_direction_100m
    
        hourl_df = pd.DataFrame(data = hourl_data)
        #print(hourl_df)
        wind_data.at[i, "date"] = hourl_data["date"][0]
        wind_data.at[i, "spd10"] = hourl_data["spd10"][0]
        wind_data.at[i, "dir10"] = hourl_data["dir10"][0]
        wind_data.at[i, "spd100"] = hourl_data["spd100"][0]
        wind_data.at[i, "dir100"] = hourl_data["dir100"][0]
        #print(wind_data)
    return wind_data

def extract_data_from_api(lat_min, lat_max, lon_min, lon_max, pas, start_d, end_d):
    #dates au format "AAAA-MM-JJ"
                          
    latitudes = np.arange(lat_min, lat_max, pas)
    longitudes = np.arange(lon_min, lon_max, pas)
    
    latitudes_list = latitudes.round(3).tolist()
    longitudes_list = longitudes.round(3).tolist()
    
    l_latitudes = np.repeat(latitudes_list, len(longitudes)).tolist()
    l_longitudes = np.tile(longitudes_list, len(latitudes)).tolist()
    #print(l_latitudes, l_longitudes)
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
    	"latitude": l_latitudes,
    	"longitude": l_longitudes,
    	"start_date": start_d,
    	"end_date": end_d,
    	"hourly": ["wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m"],
        "temporal_resolution": "hourly_6"
    } #On demande les infos toutes les 6h. Cela renvoie donc 16x4 = 64 valeurs par jour
    responses = openmeteo.weather_api(url, params=params)
    
    wind_data = pd.DataFrame({'lat': l_latitudes, 'lon': l_longitudes, 'date' : '2024-09-09 00:00:00+00:00' ,'spd10': 0.0, 'spd100': 0.0,'dir10':0.0, 'dir100':0.0})

    extract_data_from_resp(responses, wind_data, len(l_latitudes))
    
    return wind_data

def preprocess_wind_data(data):
    data['u10'] = -data['spd10'] * np.sin(np.radians(data['dir10']))
    data['v10'] = -data['spd10'] * np.cos(np.radians(data['dir10']))
    data['u100'] = -data['spd100'] * np.sin(np.radians(data['dir100']))
    data['v100'] = -data['spd100'] * np.cos(np.radians(data['dir100']))

def data_opener(name):
	#os.chdir("./Documents/INSA/PFE-Reconstruction-champ-vents/")
	wind_data = pd.read_csv("../data/API/"+name)
	return wind_data
