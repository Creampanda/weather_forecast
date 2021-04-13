import requests
import telebot
import datetime
import config


owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

bot = telebot.TeleBot(config.token)

weather_params = {
    "lat": "56.331718",
    "lon": "36.729210",
    "appid": config.api_key,
    "exclude": "current,minutely"
}

# send_time = datetime.time(7,0,0,000000)


will_rain = False
counter = 0

response = requests.get(owm_endpoint,params=weather_params)
response.raise_for_status()
weather_data = response.json()

for hour in weather_data["hourly"][:24]:
    counter += 1
    if hour["weather"][0]["id"] < 700:
        will_rain = True
        rain_hour = (7 + counter) % 24
        if rain_hour < 10:
            rain_hour = f"0{rain_hour}.00"
        else:
            rain_hour = f"{rain_hour}.00"

day_temp = round(weather_data["daily"][0]["temp"]["day"] - 273)
night_temp = round(weather_data["daily"][0]["temp"]["night"] - 273)
if will_rain:
    weather_message = f"""
        Зеленоград
        Температура днем: {day_temp}°C
        Температура ночью: {night_temp}°C
        Ожидается дождь c {rain_hour}
        """
else:
    weather_message = f"""
        Зеленоград
        Температура днем: {day_temp}°C
        Температура ночью: {night_temp}°C
        Дождь не ожидается
        """
bot.send_message(config.chat_id, weather_message)