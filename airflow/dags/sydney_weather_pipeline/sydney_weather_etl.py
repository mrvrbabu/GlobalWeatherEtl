from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from airflow.decorators import task
import requests
import json

# Extract the weather data of specific location (Sydney in this case)
LATITUDE = '33.8688'
LONGITUDE = '151.2093'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_id'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# Create dag object 
with DAG(dag_id='sydney_weather_pipeline',
         default_args=default_args,
         schedule_interval='@hourly',
         catchup=False) as dag:
    
    @task()
    def extract_weather_data():
        """Extract weather using open meteo api. """
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        
        # Endpoint to extract weather data
        # https://open-meteo.com
        endpoint=f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
        
        response = http_hook.run(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception (f'Failed to fecth weather data: { response.status_code}')
        
    
    @task()
    def transform_weather_data(weather_data):
        """Transform weather data. """
        current_weather = weather_data['current_weather']
        
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data
    
    @task()
    def load_weather_data(transformed_data):
        """Load the weather data in the database. """
        pg_hook = PostgresHook(POSTGRES_CONN_ID)
        
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        # Create table if not exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sydney_weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Insert data into table
        cursor.execute("""
        INSERT INTO sydney_weather_data ( latitude, longitude, temperature, windspeed, winddirection, weathercode )
        VALUES ( %s, %s, %s, %s, %s, %s )
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))
        conn.commit()
        cursor.close()
        
    # Create task dependencies 
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)