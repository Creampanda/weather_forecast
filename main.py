import requests

api_key = "6908e3d91226bdbad035dbd393005beb"

owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    "lat": "56.331718",
    "lon": "36.729210",
    "appid": api_key
}

response = requests.get(owm_endpoint,params=weather_params)
print(response)