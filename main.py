#!/usr/bin/python3
import requests
import telebot
import datetime
import config


def _main(city):
    owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

    bot = telebot.TeleBot(config.token)

    if city == "Klin":
        city = config.Klin
    elif city == "Zelenograd":
        city = config.Zelenograd

    weather_params = {
        "lat": city["lat"],
        "lon": city["long"],
        "appid": config.api_key,
        "exclude": "current,minutely"
    }

    will_rain = False
    counter = 0
    rain_hours = []

    response = requests.get(owm_endpoint,params=weather_params)
    response.raise_for_status()
    weather_data = response.json()
    
    for hour in weather_data["hourly"][:23]:
        if hour["weather"][0]["id"] < 700:
            will_rain = True
            rain_hour = (7 + counter) % 24
            if rain_hour < 10:
                rain_hour = f"0{rain_hour}.00"
            else:
                rain_hour = f"{rain_hour}.00"
            rain_hours.append(rain_hour)
        counter += 1

    day_temp = round(weather_data["daily"][0]["temp"]["day"] - 273)
    night_temp = round(weather_data["daily"][0]["temp"]["night"] - 273)
    if will_rain:
        weather_message = f"""
            {city}
            Температура днем: {day_temp}°C
            Температура ночью: {night_temp}°C
            Ожидается дождь в {rain_hours} часов
            """
    else:
        weather_message = f"""
            {city}
            Температура днем: {day_temp}°C
            Температура ночью: {night_temp}°C
            Дождь не ожидается
            """
    bot.send_message(config.chat_id, weather_message)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("city",
        help="City",
        type=str)
    args = parser.parse_args()
    _main(**vars(args))