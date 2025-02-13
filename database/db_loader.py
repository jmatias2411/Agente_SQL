import pandas as pd
import streamlit as st

def load_database(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            raise ValueError("Formato no soportado. Solo CSV y JSON.")
        return df
    except Exception as e:
        return st.error(f"Error al cargar la base de datos: {e}")
