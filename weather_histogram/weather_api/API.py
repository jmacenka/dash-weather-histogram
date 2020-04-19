import pandas as pd
import requests
from datetime import datetime
from urllib.parse import quote
from calendar import monthrange

MONTH_LAST_DAY = [
    ("01","31"),
    ("02","28"),
    ("03","31"),
    ("04","30"),
    ("05","31"),
    ("06","30"),
    ("07","31"),
    ("08","31"),
    ("09","30"),
    ("10","31"),
    ("11","30"),
    ("12","31"),
]

API_INFO_URL = 'https://www.worldweatheronline.com/'

def response_to_df(response):
    dict_column_map = {
        'timestamp':'timestamp',
        'tempC':'temperature_°C',
        'humidity':'humidity_%',
        'pressure':'pressure_hpa',
        'windspeedKmph':'windspeed_kmh'
    }
    required_columns = dict_column_map.keys()
    response_city = None
    df_weather = pd.DataFrame(columns=dict_column_map.values()).set_index('timestamp')
    df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
    if response.ok:
        df_weather = pd.DataFrame(response.json()['data']['weather']).set_index('date')
        df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
        df_reformed = pd.DataFrame(columns=dict_column_map.values())
        for date, v in df_weather['hourly'].items():
            df_temp = pd.DataFrame(v)
            df_temp['timestamp'] = df_temp['time'].apply(lambda x: date.replace(hour=int(int(x)/100)))
            df_temp = df_temp[required_columns].rename(columns=dict_column_map)
            df_reformed = df_reformed.append(df_temp)
        df_weather = df_reformed.set_index('timestamp')
        response_city = response.json()['data']['request'][0]['query']        
    return response_city, df_weather

def query_location(api_key:str, search_location:str='Munich'):
    url = f'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={quote(search_location)}&format=json&num_of_days=0&includelocation=yes'
    response = requests.get(url)
    if response.ok:
        try:
            location_obj = response.json()['data']['nearest_area'][0]
            location = f"{location_obj['country'][0]['value']} > {location_obj['region'][0]['value']} > {location_obj['areaName'][0]['value']} // lat: {location_obj['latitude']}, long: {location_obj['longitude']}"
            if len(location) <= 3:
                location = None
        except:
            location = None
    else:
        location = None
    return (location,)

def fetch_data(api_key:str, search_location:str='Munich', year:int=None, tp:int=1):
    """Submit either start_date and end_date or year
    returns a tuple (df_response:df, query_city:str)"""
    if year is None:
        year = datetime.now().year - 1
    start_date = f'{year}-01-01'
    end_date = f'{year}-01-31'
    url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
    response = requests.get(url)
    response_city, df_weather = response_to_df(response)
    if response_city is None:
        return None, response_city
    for month, last_day in MONTH_LAST_DAY:
        start_date = f'{year}-{month}-01'
        end_date = f'{year}-{month}-{last_day}'
        url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
        response = requests.get(url)
        _, df_update = response_to_df(response)
        if not df_update.empty:
            df_weather = df_weather.append(df_update)
    if not df_weather.empty:
        df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
        return df_weather, response_city
    else:
        return pd.DataFrame(), response_city


# #TESTING:
# search_location='Kirchanschöring'
# api_key='ff5b9e1041ca4317add75758200904'
# tp= 1
# df, response_city = fetch_data(api_key=api_key,search_location=search_location,year=2018,tp=tp)
# print(response_city, df)