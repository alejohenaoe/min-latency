# Sistema de Comunicación por Socket - Arquitectura e Implementación

## Objetivo del Proyecto

Desarrollar un sistema de comunicación de **baja latencia** que logre **tiempos de respuesta menores a 1ms**.

---


## Descripción General de la Arquitectura

```
┌─────────────────────────────────┐
│   CAPA CLIENTE                  │
│  (socket_client.py)             │
│  • Interacción con usuario      │
│  • Medición de tiempos          │
└────────────┬────────────────────┘
             │ Socket TCP
             ▼
┌─────────────────────────────────┐
│   CAPA SERVIDOR                 │
│  (socket_server.py)             │
│  • Gestión de conexiones        │
│  • Recepción de mensajes        │
│  • Envío de respuestas          │
└────────────┬────────────────────┘
             │ Delega
             ▼
┌─────────────────────────────────┐
│   CAPA DE PROCESAMIENTO         │
│  (message_handler.py)           │
│  • Lógica de negocio            │
│  • Validación de mensajes       │
│  • Generación de respuestas     │
└─────────────────────────────────┘
```

---

## Implementacion

Arquitectura **minimalista** enfocada únicamente en **baja latencia**:

- **`config.py`**: Configuración (puertos, buffers, respuestas)
- **`models.py`**: Estructuras de datos (Message, Response)
- **`message_handler.py`**: Procesador de mensajes
- **`socket_server.py`**: Servidor TCP
- **`socket_client.py`**: Cliente interactivo
- **`benchmark.py`**: Medición de rendimiento


## Decisiones de Rendimiento Clave

### 1. **TCP_NODELAY = 1**

Desactiva el algoritmo de Nagle para eliminar retrasos de buffering:

- **Sin TCP_NODELAY**: ~40-100ms de latencia (mensaje espera a llenar el buffer)
- **Con TCP_NODELAY**: <1ms de latencia (envío inmediato)

**Código:**
```python
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

### 2. **perf_counter() para Medición de Tiempo**

Usa `time.perf_counter()` en lugar de `time.time()`:

- **time.time()**: Sujeto a ajustes del reloj del sistema
- **time.perf_counter()**: Monótono, alta resolución, no afectado por cambios de reloj

### 3. **Tamaño de Buffer Pequeño**

BUFFER_SIZE reducido a 256 bytes (en lugar de 1024):

- Minimiza la sobrecarga de asignación de memoria
- Suficiente para mensajes de prueba
- Mejor para paquetes pequeños

### 4. **Conexión Persistente**

El cliente mantiene una conexión para múltiples mensajes:

- Elimina la sobrecarga de configuración de conexión
- Reutiliza recursos del socket
- Más representativo del uso en producción

---

## Estructura de Archivos

```
Modulo-1/
├── config.py              # Configuración
├── models.py              # Estructuras de datos
├── message_handler.py     # Procesador de mensajes
├── socket_server.py       # Servidor TCP
├── socket_client.py       # Cliente interactivo
├── benchmark.py           # Benchmarking automatizado
└── README.md             # Este archivo
```

---

## Cómo Usar

### Requisitos:

- Python instalado de manera local 

### 1. **Iniciar el Servidor**

```bash
python3 socket_server.py
```

Salida:
```
Servidor socket ejecutándose en 127.0.0.1:9000
Esperando conexiones... (Presiona Ctrl+C para detener)
```

### 2. **Ejecutar Cliente Interactivo**

En otra terminal:

```bash
python3 socket_client.py
```

Salida:
```
✓ Conectado a 127.0.0.1:9000

============================================================
Cliente Socket Interactivo
============================================================
Ingresa mensajes a enviar (escribe 'quit' para salir):

Mensaje a enviar: Hola
  Respuesta: Hola mundo
  Tiempo de respuesta: 0.5234 ms

Mensaje a enviar: Mensaje de prueba
  Respuesta: Hola mundo
  Tiempo de respuesta: 0.4891 ms

Mensaje a enviar: quit
✓ Desconectado
```

### 3. **Ejecutar Benchmark Automatizado**

En una tercera terminal (con el servidor ejecutándose):

```bash
python3 benchmark.py
```

Salida:
```
======================================================================
Benchmark: 10 peticiones
======================================================================
Petición #   Mensaje              Respuesta            Tiempo (ms)    
----------------------------------------------------------------------
1            test_message         Hola mundo           0.5123       
2            test_message         Hola mundo           0.4987       
3            test_message         Hola mundo           0.5345       
4            test_message         Hola mundo           0.5102       
5            test_message         Hola mundo           0.5234       
...
----------------------------------------------------------------------

Resumen:
  Total de peticiones: 10
  Exitosas: 10
  Fallidas: 0

Estadísticas de tiempo:
  Mínimo: 0.4567 ms
  Máximo: 0.6234 ms
  Promedio: 0.5123 ms
======================================================================
```

Los resultados también se exportan a `benchmark_results.csv` para análisis.

---

## Modelos de Datos

### Message
```python
@dataclass
class Message:
    content: str           # Texto del mensaje
    timestamp: float       # Cuándo se creó el mensaje
    
    def is_valid() -> bool # Valida el mensaje
```

### Response
```python
@dataclass
class Response:
    content: str              # Texto de la respuesta
    processing_time_ms: float # Duración del procesamiento
    
    def to_bytes() -> bytes   # Convierte a bytes
```

---

## Extender el Sistema

### Agregar Procesador de Mensajes Personalizado

```python
# processor.py
from interfaces import MessageProcessor
from models import Message, Response

class EchoProcessor(MessageProcessor):
    def process(self, message: Message) -> Response:
        # Repite el mensaje devuelto
        return Response(
            content=message.content,
            processing_time_ms=0.1
        )

# Ejecutar servidor con procesador personalizado
from socket_server import SocketServer
from processor import EchoProcessor

server = SocketServer(processor=EchoProcessor())
server.start()
```

### Modificar Configuración

Edita `config.py`:

```python
SERVER_PORT = 9001              # Cambiar puerto
BUFFER_SIZE = 512               # Aumentar buffer
BENCHMARK_REQUESTS = 100        # Ejecutar 100 en lugar de 10
DEFAULT_RESPONSE = "Personalizado"     # Cambiar respuesta
```

---

## Objetivos de Rendimiento

| Métrica | Objetivo | Estado |
|---------|----------|--------|
| Tiempo de Respuesta | < 1 ms | ✓ Logrado |
| Sobrecarga de Memoria | Mínima | ✓ Optimizado |
| Escalabilidad | Múltiples clientes | ✓ Soportado |
| Extensibilidad | Arquitectura de plugins | ✓ Basado en SOLID |

---

## Especificaciones Técnicas

- **Lenguaje**: Python 3.7+
- **Protocolo**: TCP/IP (socket de bajo nivel)
- **Codificación**: UTF-8
- **Medición de Tiempo**: `time.perf_counter()` (precisión nanosegundos)
- **Patrón de Arquitectura**: En capas + Inyección de Dependencias

---

## Notas del Autor

Esta implementación prioriza:

1. **Claridad** - El código es legible y bien documentado
2. **Mantenibilidad** - Los principios SOLID permiten modificaciones fáciles
3. **Rendimiento** - Optimizado para latenza sub-1ms
4. **Extensibilidad** - Arquitectura de plugins para procesadores personalizados
5. **Simplicidad** - Sin complejidad innecesaria

---
