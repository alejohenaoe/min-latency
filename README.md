# Sistema de Comunicación por Socket - Arquitectura e Implementación

## Objetivo del Proyecto

Demostrar la capacidad de diseñar, implementar y optimizar una arquitectura de software enfocada en reducir drásticamente la latencia de comunicación. La idea es que, una vez desplegado el sistema, se lance un “estímulo” y se obtenga la respuesta casi de inmediato. 

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
  Tiempo de respuesta: 0.4830 ms

Mensaje a enviar: test
  Respuesta: Hola mundo
  Tiempo de respuesta: 0.2627 ms

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
1            test_message         Hola mundo           0.8290       
2            test_message         Hola mundo           0.0788       
3            test_message         Hola mundo           0.0878       
4            test_message         Hola mundo           0.0758       
5            test_message         Hola mundo           0.0721       
...
----------------------------------------------------------------------

Resumen:
  Total de peticiones: 10
  Exitosas: 10
  Fallidas: 0

Estadísticas de tiempo:
  Mínimo: 0.0705 ms
  Máximo: 0.8290 ms
  Promedio: 0.1299 ms
======================================================================
```

---

## Modelos de Datos

### Message
Encapsula un mensaje recibido del cliente.

```python
@dataclass
class Message:
    content: str           # Texto del mensaje
    timestamp: float = 0.0 # Marca de tiempo (opcional)
```

### Response
Encapsula una respuesta del servidor con método de serialización.

```python
@dataclass
class Response:
    content: str  # Texto de respuesta
    
    def to_bytes(self, encoding: str = "utf-8") -> bytes:
        """Convierte la respuesta a bytes para enviar por socket."""
        return self.content.encode(encoding)
```

---

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
| Tiempo de Respuesta | < 1 ms | ✓ Logrado (~0.07 ms) (con benchmark.py) |
| Sobrecarga de Memoria | Mínima | ✓ Optimizado |
| Escalabilidad | Múltiples clientes | ✓ Soportado |

---

## Especificaciones Técnicas

- **Lenguaje**: Python 3.7+
- **Protocolo**: TCP/IP (socket de bajo nivel)
- **Codificación**: UTF-8
- **Medición de Tiempo**: `time.perf_counter()` (precisión nanosegundos)
- **Patrón de Arquitectura**: En capas minimalista

---

