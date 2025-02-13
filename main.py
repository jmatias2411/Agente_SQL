import streamlit as st
import pandas as pd
from models.query_generator import generate_sql
from database.db_loader import load_database
from utils.query_validator import validate_sql
from utils.db_connector import execute_query
from config import LM_STUDIO_ENDPOINT

st.set_page_config(page_title="AI SQL Agent", layout="wide")

st.title("🧠 SQL AI Agent - Generador de Consultas SQL")

# Subir archivo CSV o JSON
uploaded_file = st.file_uploader("Sube tu base de datos en CSV o JSON", type=["csv", "json"])

df = None
sql_query = ""  # Inicializar sql_query

if uploaded_file is not None:
    df = load_database(uploaded_file)
    st.write("### Vista previa de la base de datos:")
    st.dataframe(df.head())

# Entrada del usuario en lenguaje natural
user_input = st.text_area("Escribe tu consulta en lenguaje natural:")

if st.button("Generar SQL") and user_input and df is not None:
    sql_query = generate_sql(user_input, df, LM_STUDIO_ENDPOINT)

    if not sql_query or sql_query.lower().startswith("error") or "No se pudo generar" in sql_query:
        st.error("El modelo no generó una consulta SQL válida. Intenta reformular la petición.")
    else:
        st.code(sql_query, language='sql')
        st.success("Consulta generada correctamente")

        # Validar SQL antes de ejecutarla
        if validate_sql(sql_query):
            result = execute_query(df, sql_query)

            if isinstance(result, str):  # Si execute_query devuelve un mensaje de error
                st.error(result)
            else:
                st.write("### Resultado de la consulta:")
                st.dataframe(result)
        else:
            st.error("La consulta SQL generada contiene operaciones no permitidas.")
