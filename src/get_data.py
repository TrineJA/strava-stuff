import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd

import sys
sys.path.append('.')
from api_key import api_key


def get_activity_data():
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # setup payload
    payload = {
        'client_id': api_key['client_id'],
        'client_secret': api_key['client_secret'],
        'refresh_token': api_key['refresh_token'],
        'grant_type': "refresh_token",
        'f': 'json'
    }

    # Request access token
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    # Get data
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    df = pd.json_normalize(my_dataset)

    # handle datetime
    df['start_date_local'] =  pd.to_datetime(df['start_date_local'])


    return df


if __name__ == "__main__":
    df = get_activity_data()
    print(df.head())