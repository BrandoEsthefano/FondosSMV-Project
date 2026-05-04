import pyodbc
import pandas as pd
from extraccion import extraccion_fondos, convertir_dataframe, limpieza

# Cadena de conexión a SQL Server
CONN_STR = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ESTHEFANO\\PRUEBAS;'
    'DATABASE=SMV_FONDOS;'
    'Trusted_Connection=yes;'
)

RAZON = 'CREDICORP CAPITAL S.A. SOCIEDAD ADMINISTRADORA DE FONDOS'

def insertar_administradora(cursor, razon_social):
    '''Inserta la administradora si no existe y retorna su id.'''
    cursor.execute('''
        IF NOT EXISTS (
            SELECT 1 FROM dim_administradoras WHERE RazonSocial = ?
        )
        INSERT INTO dim_administradoras (RazonSocial) VALUES (?)
    ''', razon_social, razon_social)

    cursor.execute(
        'SELECT idAdministradora FROM dim_administradoras WHERE RazonSocial = ?',
        razon_social
    )
    return cursor.fetchone()[0]


def insertar_fondos(cursor, df, id_administradora):
    '''Inserta cada fondo del DataFrame en fact_fondos.'''
    insertados = 0

    for _, fila in df.iterrows():

        # Convertir NaN a None para que SQL Server los reciba como NULL
        patrimonio  = None if pd.isna(fila.PatrimonioInscrito) else fila.PatrimonioInscrito
        valor_cuota = None if pd.isna(fila.ValorCuota)         else fila.ValorCuota
        participes  = None if pd.isna(fila.NumeroParticipes)   else int(fila.NumeroParticipes)
        cuotas      = None if pd.isna(fila.NumeroCuotas)       else fila.NumeroCuotas

        cursor.execute('''
            INSERT INTO fact_fondos (
                idAdministradora, DenominacionFondo, TipoFondo,
                FechaInscripcion, ResolucionInscripcion, Moneda,
                FechaInformacion, PatrimonioInscrito, ValorCuota,
                NumeroParticipes, NumeroCuotas,
                AnioInscripcion, TieneDatos,
                FechaCarga
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',
            id_administradora,
            fila.DenominacionFondo,
            fila.TipoFondo,
            fila.FechaInscripcion,
            fila.ResolucionInscripcion,
            fila.Moneda,
            fila.FechaInformacion,
            patrimonio,
            valor_cuota,
            participes,
            cuotas,
            fila.AnioInscripcion,
            int(fila.TieneDatos),
            fila.FechaCarga
        )
        insertados += 1

    return insertados


def cargar_datos():
    '''Función principal: extrae, limpia y carga en SQL Server.'''

    # Obtener el DataFrame limpio desde extraccion.py
    raw = extraccion_fondos(RAZON)
    df  = convertir_dataframe(raw)
    df  = limpieza(df)

    # Conectarse a SQL Server
    conn   = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    id_adm = insertar_administradora(cursor, RAZON)
    print(f'[OK] Administradora con id: {id_adm}')

    total = insertar_fondos(cursor, df, id_adm)
    conn.commit()
    conn.close()
    print(f'[OK] {total} fondos insertados correctamente')

if __name__ == '__main__':
    cargar_datos()
