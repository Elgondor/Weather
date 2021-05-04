import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'
    api_id = '125f6598d052f50269c4f003b0a7bb96'
    units = 'metric'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name = new_city).count()

            if existing_city_count == 0:
                request_data_weather = requests.get(url.format(new_city, units, api_id)).json()
                print(request_data_weather)

                if request_data_weather['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exists in the world!'

                
            else:
                err_msg = 'City already exists in database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'
        

    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        request_data_weather = requests.get(url.format(city.name, units, api_id)).json()

        city_weather = {
            'city': city.name,
            'temperature': request_data_weather['main']['temp'],
            'description': request_data_weather['weather'][0]['description'],
            'icon': request_data_weather['weather'][0]['icon'],
        }

        weather_data.append(city_weather)


    context = {
        'weather_data': weather_data, 
        'form': form,
        'message': message,
        'message_class': message_class,
    }
    
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('home')