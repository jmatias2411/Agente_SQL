import requests
import json

# Configuración del endpoint
LM_STUDIO_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "mathstral-7b-v0.1"

# Payload de prueba
payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "system", "content": "Eres un modelo de IA que responde preguntas en SQL."},
        {"role": "user", "content": "Escribe una consulta SQL para obtener todos los clientes de una tabla llamada clientes."}
    ],
    "max_tokens": 50,
    "temperature": 0.5
}

try:
    response = requests.post(LM_STUDIO_ENDPOINT, json=payload)
    response.raise_for_status()
    
    # Intentar procesar la respuesta JSON
    data = response.json()
    sql_query = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    print("Respuesta del modelo:")
    print(sql_query if sql_query else "No se recibió una consulta SQL válida.")

except requests.exceptions.RequestException as e:
    print(f"Error en la conexión con LM Studio: {e}")
except json.JSONDecodeError:
    print("Error al procesar la respuesta del modelo.")

