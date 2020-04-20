import pandas as pd
import requests
from datetime import datetime
from urllib.parse import quote

MONTH_LAST_DAY = [
#    ("01","31"),
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

DICT_COLUMN_MAP = {
    'timestamp':'timestamp',
    'tempC':'Temperatur °C',
    'humidity':'Feuchte %rF',
    'pressure':'Druck hPa',
    'windspeedKmph':'Windgeschwindigkeit km/h'
}

API_INFO_URL = 'https://www.worldweatheronline.com/'

def query_location(api_key:str, search_location:str='Munich'):
    url = f'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={quote(search_location)}&format=json&num_of_days=0&includelocation=yes'
    maps_url = None
    response = requests.get(url)
    if response.ok:
        try:
            location_obj = response.json()['data']['nearest_area'][0]
            location = f"{location_obj['country'][0]['value']} > {location_obj['region'][0]['value']} > {location_obj['areaName'][0]['value']}"
            maps_url = f"https://maps.google.com/maps?q={location_obj['latitude']}, {location_obj['longitude']}&z=15&output=embed"
            if len(location) <= 3:
                location = None
        except:
            location = None
    else:
        location = None
    return (location, maps_url)

def response_to_df_old(response):
    required_columns = DICT_COLUMN_MAP.keys()
    if response.ok:
        df_weather = pd.DataFrame(response.json()['data']['weather'], dtype=float).set_index('date')
        df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
        df_reformed = pd.DataFrame(columns=DICT_COLUMN_MAP.values(), dtype=float)
        for date, v in df_weather['hourly'].items():
            df_temp = pd.DataFrame(v)
            df_temp['timestamp'] = df_temp['time'].apply(lambda x: date.replace(hour=int(int(x)/100)))
            df_temp = df_temp[required_columns].rename(columns=DICT_COLUMN_MAP)
            df_reformed = df_reformed.append(df_temp)
        df_weather = df_reformed.set_index('timestamp')      
    return df_weather

def response_to_df(response):
    df_weather = pd.DataFrame()
    if response.ok:        
        for day in response.json()['data']['weather']:
            date = datetime.strptime(day['date'],'%Y-%m-%d')
            hourly = [
                {
                    'time':hour['time'], 
                    'Temperatur °C':float(hour['tempC']),
                    'Feuchte %rF':float(hour['humidity']),
                    'Druck hPa':float(hour['pressure']),
                    'Windgeschwindigkeit km/h':float(hour['windspeedKmph']),
                } 
                for hour in day['hourly']
            ]
            df_hourly = pd.DataFrame(hourly)
            df_hourly['timestamp'] = df_hourly['time'].apply(lambda x: date.replace(hour=int(int(x)/100)))
            df_hourly = df_hourly.drop(['time'], axis=1).set_index('timestamp')
            df_weather = df_weather.append(df_hourly)
    return df_weather

def fetch_data(api_key:str, search_location:str='Munich', year:int=None, tp:int=1):
    """Submit either start_date and end_date or year
    returns a tuple (df_response:df, query_city:str)"""
    if year is None:
        year = datetime.now().year - 1
    start_date = f'{year}-01-01'
    end_date = f'{year}-01-31'
    url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
    response = requests.get(url)
    df_weather = response_to_df(response)
    for month, last_day in MONTH_LAST_DAY:
        start_date = f'{year}-{month}-01'
        end_date = f'{year}-{month}-{last_day}'
        url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
        response = requests.get(url)
        df_update = response_to_df(response)
        if not df_update.empty:
            df_weather = df_weather.append(df_update)
    if not df_weather.empty:
        df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
        return df_weather
    else:
        return pd.DataFrame()


# #TESTING:
# search_location='Kirchanschöring'
# api_key='ff5b9e1041ca4317add75758200904'
# tp= 1
# df, response_city = fetch_data(api_key=api_key,search_location=search_location,year=2018,tp=tp)
# print(response_city, df)
