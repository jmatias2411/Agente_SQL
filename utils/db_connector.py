import sqlite3
import pandas as pd
import streamlit as st

import pandas as pd
import sqlite3

def execute_query(df, sql_query):
    try:
        # Crear una base de datos en memoria
        conn = sqlite3.connect(":memory:")
        df.to_sql("data", conn, index=False, if_exists="replace")  # Guardar DataFrame en SQLite con nombre "data"

        # Reemplazar nombre de la tabla en la consulta
        sql_query = sql_query.replace("Anime", "data")  

        # Ejecutar la consulta SQL
        result = pd.read_sql_query(sql_query, conn)

        # Cerrar conexión
        conn.close()

        return result

    except Exception as e:
        return f"Error al ejecutar la consulta: {e}"
