import datetime
import logging
import pytz
import requests
import json
import azure.functions as func
import os  # Import the os module

def get_current_and_next_half_hour():
    now = datetime.datetime.now(pytz.timezone('Europe/London'))
    if now.minute < 30:
        now = now.replace(minute=0, second=0, microsecond=0)
    else:
        now = now.replace(minute=30, second=0, microsecond=0)
    next_time = now + datetime.timedelta(minutes=30)
    return [now.strftime('%Y-%m-%dT%H:%M:%S'), next_time.strftime('%Y-%m-%dT%H:%M:%S')]

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    time_params = get_current_and_next_half_hour()
    url = f'https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-H/standard-unit-rates/?period_from={time_params[0]}&period_to={time_params[1]}'

    response = requests.get(url, headers={'Content-Type': 'application/json'})
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        value_inc_vat = data['results'][0]['value_inc_vat']
        value_inc_vat_in_pounds = value_inc_vat / 100
        rounded_value_inc_vat = round(value_inc_vat_in_pounds, 2)
        logging.info(f'Rounded Value: {rounded_value_inc_vat}')
    else:
        logging.error("No data received from the API")

    # Get values from environment variables
    easee_user = os.environ['EASEE_USER']
    easee_password = os.environ['EASEE_PASSWORD']
    easee_site_id = os.environ['EASEE_SITE_ID']

    login_options = {
        'headers': {
            'accept': 'application/json',
            'content-type': 'application/json'
        },
        'data': json.dumps({
            'username': easee_user,
            'password': easee_password
        })
    }

    response = requests.post('https://api.easee.com/api/accounts/login', **login_options)
    data = response.json()
    access_token = data['accessToken']

    price_options = {
        'headers': {
            'content-type': 'application/*+json',
            'Authorization': f'Bearer {access_token}'
        },
        'data': json.dumps({
            'currencyId': 'GBP',
            'costPerKWh': rounded_value_inc_vat
        })
    }

    response = requests.post(f'https://api.easee.com/api/sites/{easee_site_id}/price', **price_options)
    data = response.text
    if data:
        data = json.loads(data)
    logging.info(data)
