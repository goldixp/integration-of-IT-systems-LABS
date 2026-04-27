import os
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.shortcuts import render

def get_weather_data(lat=54.04, lon=22.50):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current=temperature_2m&timezone=auto&forecast_days=2"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()
    
def cut_data(data):
    current_temp = data['current']['temperature_2m']
    current_time_str = data['current']['time'] 
    current_hour_prefix = current_time_str[:13] 
  
    start_idx = 0
    for i, time_str in enumerate(data['hourly']['time']):
        if time_str.startswith(current_hour_prefix):
            start_idx = i
            break
            
    times = data['hourly']['time'][start_idx : start_idx + 24]
    temps = data['hourly']['temperature_2m'][start_idx : start_idx + 24]
    
    return times, temps, current_temp
       
def gen_chart(times, temps):
    plt.clf()
    formatted_times = [t.split('T')[1] for t in times]
    
    plt.plot(formatted_times, temps, marker='o', color='b')
    plt.title("Prognoza temperatury (najblizsze 24h)")
    plt.xlabel("Godzina")
    plt.ylabel("Temperatura (C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Tworzymy folder static, jeśli nie istnieje
    filepath = 'external_data/static/weather_chart.png'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath)
    
def weather_view(req):
    data = get_weather_data()
    times, temps, current_temp = cut_data(data)
    gen_chart(times, temps)
    
    context = {
        'current_temp': current_temp
    }
    
    return render(req, 'weather.html', context)