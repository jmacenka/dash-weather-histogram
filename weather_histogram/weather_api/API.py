import pandas as pd
import requests
from datetime import datetime
from urllib.parse import quote
from calendar import monthrange

def fetch_data(api_key, search_location='Munich', year=None, tp=1):
    """Submit either start_date and end_date or year
    returns a tuple (df_response:df, query_city:str)"""
    if year is None:
        year = datetime.now().year - 1
    start_date = f'{year}-01-01'
    end_date = f'{year}-01-31'
    url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
    response = requests.get(url)
    if response.ok:
        df_weather = pd.DataFrame(response.json()['data']['weather'])
        df_weather = df_weather.drop(['astronomy','hourly'], axis=1).set_index('date')
        response_city = response.json()['data']['request'][0]['query']
    else:
        df_weather = pd.DataFrame()
        response_city = f'No Data for "{search_location}"'

    for month in range(2,13):
        month_start, month_end = monthrange(year, month)

        start_date = f'{year}-{month}-{month_start}'
        end_date = f'{year}-{month}-{month_end}'
        url = f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={quote(search_location)}&format=json&date={start_date}&enddate={end_date}&tp={tp}'
        response = requests.get(url)
        if response.ok:
            df = pd.DataFrame(response.json()['data']['weather'])
            df_c = df.drop(['astronomy','hourly'], axis=1).set_index('date')
            df_weather = df_weather.append(df_c)

    if not df_weather.empty:
        df_weather.index = pd.to_datetime(df_weather.index, infer_datetime_format=True)
        return df_weather, response_city
    else:
        return None, response_city

"""     
#TESTING:
search_location='Kirchanschöring'
api_key='ff5b9e1041ca4317add75758200904'
tp= 24

res = fetch_data_request(api_key=api_key,search_location=search_location,year=2018,tp=365)

print(res)
"""