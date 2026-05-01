import os
import pandas as pd
from db.conexion import obtener_motor

RUTA_CSV = os.path.join(os.path.dirname(__file__), "..", "..", "data", "02_Base_Customer-Churn.csv")

def transformar_booleano(valor):
    if valor == "Yes":
        return True
    elif valor == "No":
        return False
    return valor

def ejecutar_ingesta():
    motor = obtener_motor()
    try:
        print("Leyendo archivo CSV...")
        df = pd.read_csv(RUTA_CSV, sep=";")

        print("Renombrando columnas...")
        df = df.rename(columns={
            "customerID"        : "id_cliente",
            "gender"            : "genero",
            "SeniorCitizen"     : "es_adulto_mayor",
            "Partner"           : "tiene_pareja",
            "Dependents"        : "tiene_dependientes",
            "tenure"            : "meses_permanencia",
            "PhoneService"      : "tiene_telefono",
            "MultipleLines"     : "tiene_multiples_lineas",
            "InternetService"   : "tipo_internet",
            "OnlineSecurity"    : "tiene_seguridad_online",
            "OnlineBackup"      : "tiene_backup_online",
            "DeviceProtection"  : "tiene_proteccion_dispositivo",
            "TechSupport"       : "tiene_soporte_tecnico",
            "StreamingTV"       : "tiene_streaming_tv",
            "StreamingMovies"   : "tiene_streaming_peliculas",
            "Contract"          : "tipo_contrato",
            "PaperlessBilling"  : "facturacion_sin_papel",
            "PaymentMethod"     : "metodo_pago",
            "MonthlyCharges"    : "cargo_mensual",
            "TotalCharges"      : "cargo_total",
            "Churn"             : "abandono_servicio",
        })

        print("Transformando columnas booleanas...")
        columnas_booleanas = [
            "tiene_pareja", "tiene_dependientes", "tiene_telefono",
            "facturacion_sin_papel", "abandono_servicio"
        ]
        for columna in columnas_booleanas:
            df[columna] = df[columna].apply(transformar_booleano)

        print("Cargando datos crudos a la base de datos...")
        df.to_sql(
            name      = "datos",
            con       = motor,
            if_exists = "append",
            index     = False,
        )

        print(f"Ingesta completada: {len(df)} registros cargados.")

    except ValueError as e:
        raise RuntimeError(f"La tabla ya existe en la base de datos: {e}")
    except Exception as e:
        raise RuntimeError(f"Error durante la ingesta de datos: {e}")
    finally:
        motor.dispose()