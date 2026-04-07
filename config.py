"""
Módulo de configuración para el sistema de comunicación por socket.
Centraliza todas las constantes y configuraciones.
"""

# Configuración del servidor
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000
BUFFER_SIZE = 256
MESSAGE_ENCODING = "utf-8"
SERVER_BACKLOG = 5

# Configuración de comunicación
SOCKET_TIMEOUT = 5.0
TCP_NODELAY_ENABLED = True

# Configuración de respuesta
DEFAULT_RESPONSE = "Hola mundo"

# Configuración de benchmark
BENCHMARK_REQUESTS = 10
BENCHMARK_MESSAGE = "test_message"
