import os
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import JsonResponse

def weather_summary_api(request):
    """Własny endpoint API zwracający zagregowane dane w JSON."""
    try:
        data = get_weather_data()
        times, temps, current_temp = cut_data(data)
        
        avg_temp = sum(temps) / len(temps)
        
        response_data = {
            'status': 'success',
            'location': 'Olecko, PL',
            'current_temperature': current_temp,
            'forecast_24h_average': round(avg_temp, 2),
            'data_points_analyzed': len(temps)
        }
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
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
    plt.ylabel("Temperatura (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    filepath = 'external_data/static/weather_chart.png'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath)
    
def weather_view(req):
    """Podstrona z pogodą i wykresem."""
    data = get_weather_data()
    times, temps, current_temp = cut_data(data)
    gen_chart(times, temps)
    
    context = {'current_temp': current_temp}
    return render(req, 'weather.html', context)

def get_user_posts_stats(user_id=1):
    """Pobiera posty, filtruje i wylicza statystyki z obsługą błędów."""
    url = "https://jsonplaceholder.typicode.com/posts"
    
   
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status() 
        posts = res.json()
        
        user_posts = [p for p in posts if p['userId'] == user_id]
        post_count = len(user_posts)
        
        if post_count > 0:
            avg_title_len = sum(len(p['title']) for p in user_posts) / post_count
        else:
            avg_title_len = 0
            
        return {
            'success': True,
            'user_id': user_id,
            'post_count': post_count,
            'avg_title_len': round(avg_title_len, 2),
            'sample_posts': user_posts[:3] 
        }
        
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}  
        
 
def posts_view(req,user_id):
    """Podstrona ze statystykami postów."""
    posts_data = get_user_posts_stats(user_id)
    
    context = {'posts_data': posts_data}
    return render(req, 'posts.html', context)
    