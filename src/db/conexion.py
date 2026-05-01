import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USUARIO  = os.getenv("DB_USER")
DB_CLAVE    = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST", "db")
DB_PUERTO   = os.getenv("DB_PORT", "5432")
DB_NOMBRE   = os.getenv("DB_NAME")

motor = None

def obtener_motor():
    global motor
    if motor is None:
        try:
            url = f"postgresql+psycopg2://{DB_USUARIO}:{DB_CLAVE}@{DB_HOST}:{DB_PUERTO}/{DB_NOMBRE}"
            motor = create_engine(url)
        except Exception as e:
            raise RuntimeError(f"Error al crear la conexión con la base de datos: {e}")
    return motor