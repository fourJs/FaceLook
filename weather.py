import pyowm

owm = pyowm.OWM("1304584f22b294d48aae0bfff0fe655f")  # You MUST provide a valid API key

# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Needham,MA")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

# Search for current weather in London (UK)
observation = owm.weather_at_place('London,uk')
w = observation.get_weather()
# print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
summary = w.get_detailed_status()
wind = w.get_wind()                  # {'speed': 4.6, 'deg': 330}
humidity = w.get_humidity()              # 87
temperature = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
pressure = w.get_pressure()
text = "say hello my majesty, today the weather is " + str(summary) + ", the wind speed is " + str(wind["speed"]) + ", the humidity is " + str(humidity) + ", the temperature is around " + str(temperature["temp"]) + " and the pressure is " + str(pressure["press"])
print text



# from os import system
# system(text)



