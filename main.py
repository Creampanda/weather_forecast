import requests

api_key = "6908e3d91226bdbad035dbd393005beb"

owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    "lat": "56.331718",
    "lon": "36.729210",
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint,params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour in weather_data["hourly"][:12]:
    if hour["weather"][0]["id"] < 700:
        will_rain