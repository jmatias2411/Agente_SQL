# Configuración del endpoint de LM Studio
LM_STUDIO_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

# Opciones adicionales de configuración
DEFAULT_MODEL = "mathstral-7b-v0.1"  # Puedes cambiarlo por el modelo que estés usando en LM Studio
MAX_TOKENS = 256  # Límite de tokens para la respuesta del modelo
TEMPERATURE = 0.5  # Controla la creatividad de la IA (0 = determinista, 1 = más creativo)

# Mensaje de bienvenida en la aplicación (opcional)
WELCOME_MESSAGE = "Bienvenido al AI SQL Agent. Escribe tu consulta en lenguaje natural y obtén una consulta SQL optimizada."
