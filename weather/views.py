from django.shortcuts import render
import urllib.request
import json, os

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # newsapi.org

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        print(city)
        source = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid='+ WEATHER_API_KEY +''
        data = urllib.request.urlopen(url).read()
        parsed = json.loads(data)
        weather = {
            "country_code": str(parsed['sys']['country']),
            "city": str(parsed['name']),
            "temp": str(parsed['main']['temp']) + '°C',
            "description": str(parsed['weather'][0]['description']),
            "icon": parsed['weather'][0]['icon'],
            "wind": str(parsed['wind']['speed']) + ' m/s',
            "humidity": str(parsed['main']['humidity']) + '%',
            "pressure": str(parsed['main']['pressure']) + ' hPa',
            "clouds": str(parsed['clouds']['all']) + '%',

        }
        print(weather)
        context = {'weather' : weather}
        return render(request, 'home/left-side.html', context)
    else:
        text = {
            "name": "name"
        }
        return render(request, 'home/left-side.html', text)