# scripts/extract.py
import requests
import pandas as pd
import json
from datetime import datetime
import os

def fetch_weather_data(cities=['Paris', 'Lille', 'Lyon', 'Marseille']):
    API_KEY = "9890ab562c1f62d7e6965cd6b77e3a7a" 
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    weather_data = []
    
    for city in cities:
        try:
            params = {
                'q': city + ',FR',
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'fr'
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                # Extraction des données pertinentes
                city_weather = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                weather_data.append(city_weather)
                print(f" Données récupérées pour {city}")
            else:
                print(f" Erreur pour {city}: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f" Exception pour {city}: {str(e)}")
    
    # Sauvegarde en JSON brut
    os.makedirs('data/raw', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'data/raw/weather_raw_{timestamp}.json', 'w') as f:
        json.dump(weather_data, f, indent=2)
    
    return weather_data

if __name__ == "__main__":
    data = fetch_weather_data()
    print(f" {len(data)} villes traitées")