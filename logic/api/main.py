from fastapi import FastAPI, HTTPException, Request
import httpx
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
db_config = {
    'host': 'mysql_container',
    'user': 'root',
    'password': '1234',
    'database': 'apod',
}

# Endpoint que consume el servicio de la NASA y almacena en la base de datos MySQL
@app.get('/nasa_apod')
async def nasa_apod(request: Request):
    nasa_api_url = "https://api.nasa.gov/planetary/apod"
    api_key = "DEMO_KEY"  # Reemplaza esto con tu clave de API de la NASA

    params = {'api_key': api_key}

    # Realizar la solicitud HTTP a la API de la NASA
    async with httpx.AsyncClient() as client:
        response = await client.get(nasa_api_url, params=params)

    if response.status_code == 200:
        apod_data = response.json()

        # Almacenar en la base de datos MySQL
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Asumiendo que tienes una tabla nasa_data con las columnas adecuadas
            query = "INSERT INTO nasa_data (date, title, explanation, hdurl) VALUES (%s, %s, %s, %s)"
            values = (apod_data['date'], apod_data['title'], apod_data['explanation'], apod_data['hdurl'])

            cursor.execute(query, values)
            connection.commit()

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f'Error al almacenar en la base de datos: {err}')

        finally:
            cursor.close()
            connection.close()

        return apod_data

    else:
        raise HTTPException(status_code=response.status_code, detail='Error al obtener datos de la NASA')
