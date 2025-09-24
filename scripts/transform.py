# scripts/transform.py
import pandas as pd
from datetime import datetime
import json
import os

def transform_weather_data(raw_data):
    """
    Nettoie et enrichit les données météo
    """
    # Conversion en DataFrame
    df = pd.DataFrame(raw_data)
    
    # Nettoyage
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    
    # Ajout de colonnes calculées
    df['temperature_category'] = df['temperature'].apply(
        lambda x: 'Froid' if x < 10 else 'Doux' if x < 20 else 'Chaud'
    )
    
    df['humidity_category'] = df['humidity'].apply(
        lambda x: 'Sec' if x < 40 else 'Normal' if x < 70 else 'Humide'
    )
    
    # Réorganisation des colonnes
    df = df[['timestamp', 'date', 'hour', 'city', 'temperature', 'temperature_category', 
             'humidity', 'humidity_category', 'pressure', 'wind_speed', 'description']]
    
    # Sauvegarde intermédiaire
    os.makedirs('data/processed', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f'data/processed/weather_processed_{timestamp}.csv', index=False)
    
    return df

if __name__ == "__main__":
    # Test avec des données d'exemple
    sample_data = [
        {
            'city': 'Paris',
            'temperature': 15.5,
            'humidity': 65,
            'pressure': 1015,
            'description': 'light rain',
            'wind_speed': 3.5,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    transformed_data = transform_weather_data(sample_data)
    print("✅ Données transformées")
    print(transformed_data.head())