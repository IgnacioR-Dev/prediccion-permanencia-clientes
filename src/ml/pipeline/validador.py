# import os
import pandas as pd
import numpy as np


# ── Metadata - Estructura del dataset
tipos = {

    "customerID": "id",

    # Numérica binaria (0/1)
    "SeniorCitizen": "binaria",

    # Categórica
    "gender": "categorica",
    "Partner": "categorica",
    "Dependents": "categorica",
    "PhoneService": "categorica",
    "PaperlessBilling": "categorica",
    "Churn": "categorica",

    "MultipleLines": "categorica",
    "InternetService": "categorica",
    "OnlineSecurity": "categorica",
    "OnlineBackup": "categorica",
    "DeviceProtection": "categorica",
    "TechSupport": "categorica",
    "StreamingTV": "categorica",
    "StreamingMovies": "categorica",
    "Contract": "categorica",
    "PaymentMethod": "categorica",

    # Numérica
    "tenure": "numerico",
    "MonthlyCharges": "numerico",
    "TotalCharges": "numerico",
}

# ── Contrato de datos - valores válidos
dominios = {
    "gender": ["Male", "Female"],
    "Partner": ["Yes", "No"],
    "Dependents": ["Yes", "No"],
    "PhoneService": ["Yes", "No"],
    "PaperlessBilling": ["Yes", "No"],
    "Churn": ["Yes", "No"],
    "SeniorCitizen": [0, 1],

    "MultipleLines": ["Yes", "No", "No phone service"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "OnlineSecurity": ["Yes", "No", "No internet service"],
    "OnlineBackup": ["Yes", "No", "No internet service"],
    "DeviceProtection": ["Yes", "No", "No internet service"],
    "TechSupport": ["Yes", "No", "No internet service"],
    "StreamingTV": ["Yes", "No", "No internet service"],
    "StreamingMovies": ["Yes", "No", "No internet service"],

    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaymentMethod": [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ],
}

# ── Peso de cada chequeo en el score final
pesos = {
    "nulos": 0.35,
    "duplicados": 0.20,
    "consistencia": 0.30,
    "outliers": 0.15,
}


class Validador:

    # Constructor que recibe el dataset a validar
    def __init__(self, df):
        self.df = df

    # ── Chequeo de nulos en una columna específica
    def nulos(self, columna):
        cantidad_nulos = self.df[columna].isna().sum()
        return cantidad_nulos == 0   # True = sin nulos

    # ── Chequeo de duplicados (solo aplica a CustomerID)
    def duplicados(self, columna):
        return self.df[columna].is_unique   # True = todos distintos

    # ── Chequeo de consistencia con el contrato de datos
    def consistencia(self, columna):

        serie = self.df[columna].dropna() # ignoramos nulos para este chequeo

        tipo = tipos.get(columna) # obtenemos el tipo de variable según la metadata

        # variables categóricas
        if tipo == "categorica":

            if columna not in dominios:
                return True

            valores_validos = set(map(str, dominios[columna]))

            return serie.astype(str).str.strip().isin(valores_validos).all()

        # variables numéricas o binarias numéricas
        if tipo in ["numerico", "binaria"]:

            numero = pd.to_numeric(serie, errors="coerce") 

            # si hay valores que no se pudieron convertir a número, consideramos que no es consistente
            if numero.isna().any():
                return False

            return (numero >= 0).all() # revisamos que no haya números negativos 

        return True

    # ── Chequeo de outliers usando el método del IQR (solo para variables numéricas)
    def outliers(self, columna):

        numero = pd.to_numeric(self.df[columna], errors="coerce").dropna()

        if len(numero) == 0:
            return True   # si no hay datos, no evaluamos

        Q1 = numero.quantile(0.25)
        Q3 = numero.quantile(0.75)
        IQR = Q3 - Q1

        if IQR == 0:
            return True   # si no hay variabilidad, no consideramos outliers

        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        return ((numero >= limite_inferior) & (numero <= limite_superior)).all() 

    # ── Score ponderado por columna
    # ── Cada chequeo aporta su peso si pasó, cero si falló
    # ── Se divide por la suma de pesos usados porque no todas las
    # ── columnas tienen los mismos chequeos
    def calcular_score(self, checks):

        suma_puntos = 0.0
        suma_pesos = 0.0

        for check, resultado in checks.items():

            if check not in pesos:
                continue                            

            peso = pesos[check] 

            if resultado:
                suma_puntos += peso                 #si el chequeo pasó, sumamos el peso correspondiente al puntaje total
            else:
                suma_puntos += 0                    #si el chequeo falló, no sumamos puntos

            suma_pesos += peso                      #sumamos el peso del chequeo al total de pesos para luego calcular el promedio ponderado

        if suma_pesos == 0:
            return 1.0                              # si no se realizaron chequeos con peso, consideramos que la columna está 100% limpia

        return suma_puntos / suma_pesos             

    # ── Se encarga de ejecutar todos los chequeos para cada columna del dataset y generar un reporte con los resultados
    def evaluar(self):

        reporte = {}

        for columna, tipo in tipos.items():

            checks = {}

            checks["nulos"] = self.nulos(columna)

            if tipo == "id":
                checks["duplicados"] = self.duplicados(columna)
            else:
                checks["consistencia"] = self.consistencia(columna)

            if tipo == "numerico":
                checks["outliers"] = self.outliers(columna)

            reporte[columna] = checks

        return reporte

    # ── Imprime el reporte final en consola
    def imprimir(self, reporte):

        print("-"*50)
        print("Reporte de validación de datos:\n")
        print(f"Total de columnas evaluadas: {len(reporte)}")
        print(f"Total de filas evaluadas: {len(self.df)}")
        print(f"Fecha de evaluación: {pd.Timestamp.now().strftime('%d-%m-%Y')}")
        print("-"*50 , "\n")

        lista_scores = [] 

        for columna, checks in reporte.items():

            score = self.calcular_score(checks)
            lista_scores.append(score)

            detalle_checks = []

            for nombre_check, resultado in checks.items():
                if resultado:
                    detalle_checks.append(f"{nombre_check}: Pasó")
                else:
                    detalle_checks.append(f"{nombre_check}: Falló")

            detalle = " | ".join(detalle_checks)

            estado = "Limpio" if all(checks.values()) else "Revisar"

            porcentaje = f"{round(score * 100, 1)}%"

            print(f"{columna.ljust(16)} | {detalle} | Score: {porcentaje} | Estado: {estado}")

        score_general = round(np.mean(lista_scores) * 100, 2) 

        print("\n----------------------------------")
        print(f"Score general del dataset: {score_general}%")
        print("----------------------------------\n")


