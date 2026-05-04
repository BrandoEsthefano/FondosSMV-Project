import requests
import pandas as pd
import json, os
from datetime import datetime
from urllib.parse import quote

url = 'https://mvnet.smv.gob.pe/SMV.OData.Api/api/registro'

def extraccion_fondos(razon_social: str) -> dict:
    razon_codificada = quote(razon_social)
    endpoint = f'{url}/ListadoFondoNombre?sRazsoc={razon_codificada}'
    response = requests.get(endpoint, timeout=20)
    response.raise_for_status()
    return response.json()

def convertir_dataframe(data: dict) -> pd.DataFrame:
    registro = data.get('Resultado', [])
    df = pd.DataFrame(registro)
    df['FechaInscripcion'] = pd.to_datetime(df['FechaInscripcion'], format='%d/%m/%Y' , errors='coerce')
    df['FechaInformacion'] = pd.to_datetime(df['FechaInformacion'], format='%d/%m/%Y' , errors='coerce')
    columnas_numericas = ['PatrimonioInscrito', 'ValorCuota', 'NumeroParticipes', 'NumeroCuotas']
    for i in columnas_numericas:
        df[i] = pd.to_numeric(df[i].replace('', None), errors='coerce')
    return df

def limpieza(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['RazonSocial'] = df['RazonSocial'].str.strip()
    df['TipoFondo'] = df['TipoFondo'].str.strip().str.upper()
    
    df['AnioInscripcion'] = df['FechaInscripcion'].dt.year
    df['TieneDatos'] = df['PatrimonioInscrito'].notna()
    df['FechaCarga'] = datetime.now()
    return df

if __name__ == '__main__':
    
    razon = 'CREDICORP CAPITAL S.A. SOCIEDAD ADMINISTRADORA DE FONDOS'
    raw = extraccion_fondos(razon)
    df = convertir_dataframe(raw)
    df_normalizado = limpieza(df)




    

