# scripts/load.py
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, MetaData
import os

def setup_database():
    
    engine = create_engine('sqlite:///database/weather.db')
    metadata = MetaData()
    
    # Définition de la table
    weather_table = Table('weather_metrics', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('timestamp', DateTime),
        Column('date', String),
        Column('hour', Integer),
        Column('city', String),
        Column('temperature', Float),
        Column('temperature_category', String),
        Column('humidity', Float),
        Column('humidity_category', String),
        Column('pressure', Float),
        Column('wind_speed', Float),
        Column('description', String)
    )
    
    # Création de la table
    os.makedirs('database', exist_ok=True)
    metadata.create_all(engine)
    return engine

def load_to_database(df, engine):
    """Charge les données transformées dans la base"""
    try:
        df.to_sql('weather_metrics', engine, if_exists='append', index=False)
        print(f"✅ {len(df)} lignes chargées en base")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {str(e)}")
        return False

if __name__ == "__main__":
    # Test
    engine = setup_database()
    print("Base de données initialisée")