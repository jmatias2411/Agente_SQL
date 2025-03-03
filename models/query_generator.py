import requests
import json

def generate_sql(prompt, df, endpoint, model="mathstral-7b-v0.1", max_tokens=256, temperature=0.3):
    """
    Genera una consulta SQL basada en lenguaje natural, asegurando que use los nombres reales de la tabla y columnas.
    """
    # Detectar el nombre de la tabla en función del nombre del archivo CSV si está disponible
    table_name = df.attrs.get("table_name", "data")  # Si no tiene nombre, usa "data"
    
    # Extraer nombres de columnas reales del DataFrame
    column_names = list(df.columns)  # Lista con nombres de columnas reales
    column_info = ", ".join([f"{col} ({str(df[col].dtype)})" for col in column_names])

    # Asegurar que la tabla tenga siempre el mismo nombre en SQLite
    df.attrs["table_name"] = table_name

    # Instrucción más clara para el modelo
    system_prompt = (
        f"Eres un experto en SQL. Tu tarea es generar una consulta SQL válida para una tabla llamada '{table_name}'.\n"
        f"La tabla tiene las siguientes columnas y tipos de datos:\n"
        f"{column_info}\n"
        "Debes generar exclusivamente consultas válidas que usen **únicamente** las columnas mencionadas.\n"
        "Si la consulta no puede formarse correctamente, devuelve solo la palabra 'ERROR'.\n"
        "Devuelve solo la consulta SQL, sin explicaciones ni comentarios adicionales."
    )

    user_prompt = f"Genera una consulta SQL para la siguiente solicitud: {prompt}."

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        
        data = response.json()
        sql_query = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Limpiar formato si el modelo devuelve código envuelto en ```sql ... ```
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        # Validar que la consulta solo use columnas existentes
        words = sql_query.replace(",", " ").split()  # Separar palabras clave de la consulta
        invalid_columns = [word for word in words if word not in column_names and word.upper() not in ["SELECT", "FROM", "WHERE", "ORDER", "BY", "LIMIT", "DESC", "ASC"]]

        if sql_query == "ERROR" or any(invalid_columns):
            return "No se pudo generar una consulta SQL válida."

        return sql_query

    except requests.exceptions.RequestException as e:
        return f"Error en la comunicación con el modelo: {e}"

    except json.JSONDecodeError:
        return "Error al procesar la respuesta del modelo."
