from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint

from weatherapp.models import City


def home(request):
    API_KEY=config("API_KEY")
    city = request.GET.get('city')
    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            r_city = data['name']
            id = data["id"]


            if City.objects.filter(name=r_city).exists():
                messages.info(request, f"{r_city} is already in the database.")
            else:
                City.objects.create(name=r_city , id=id)
                messages.success(request, f"{r_city} has been added to the database.")
        else:
            data = None
            messages.error(request, "City not found")
        return redirect('home')
    
    cities = City.objects.all().order_by('-id')
    weather_data = []
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={API_KEY}&units=metric&lang=tr"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            detail={
        "city":city,
        "temp":data["main"]["temp"],
        "description":data["weather"][0]["description"],
        "icon":data["weather"][0]["icon"],
        "main":data["weather"][0]["main"],
        "id":data["id"]
        }
            pprint(detail)
            weather_data.append(detail)
        else:
            data = None
            messages.error(request, "City not found")

    context = {
        "weather_data": weather_data,
    }
    pprint(weather_data)
    return render(request, "weatherapp/home.html", context)

def delete_city(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, "City has been deleted.")
    return redirect('home')