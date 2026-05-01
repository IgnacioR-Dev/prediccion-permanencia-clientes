from pipeline.ingesta_datos import ejecutar_ingesta
from pipeline.validador import Validador
import pandas as pd
import os 

# ── Carga de datos para validación
ruta = os.path.join(os.path.dirname(__file__), "..", "data", "02_Base_Customer-Churn.csv")
df = pd.read_csv(ruta, sep=";")

validador = Validador(df) # Instancia del validador con el dataset cargado

def main():
    try:
        print("-"*50)
        print("Iniciando pipeline de datos...\n")
        ejecutar_ingesta()

        print("\nVerificando calidad de datos con el validador...")
        validador.imprimir(validador.evaluar())
        print("Pipeline de datos finalizado.")
        
    except RuntimeError as e:
        print(f"Error en el pipeline: {e}")


if __name__ == "__main__":
    main()