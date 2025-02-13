import requests
import json

def generate_sql(prompt, df, endpoint, model="mathstral-7b-v0.1", max_tokens=256, temperature=0.3):
    """
    Genera una consulta SQL a partir de una instrucción en lenguaje natural.
    """
    # Detectar el nombre de la tabla cargada o asignar "data" si no existe
    table_name = df.attrs.get("table_name", "data")

    # Asegurar que la tabla tenga siempre el mismo nombre en SQLite
    df.attrs["table_name"] = table_name

    # Extraer nombres de columnas reales del DataFrame
    column_names = ", ".join(df.columns)

    system_prompt = (
        f"Eres un experto en SQL. Tu tarea es generar consultas SQL válidas y bien formateadas "
        f"para extraer datos de una tabla llamada '{table_name}' con las siguientes columnas: \n"
        f"{column_names}\n"
        "Responde solo con la consulta SQL, sin explicaciones ni comentarios adicionales."
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

        # Asegurar que la consulta use el nombre correcto de la tabla
        sql_query = sql_query.replace("Anime", table_name)

        if not sql_query or "SELECT" not in sql_query.upper():
            return "No se pudo generar una consulta SQL válida."

        return sql_query

    except requests.exceptions.RequestException as e:
        return f"Error en la comunicación con el modelo: {e}"

    except json.JSONDecodeError:
        return "Error al procesar la respuesta del modelo."
