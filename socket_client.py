"""
Módulo cliente socket para enviar mensajes y medir tiempo de respuesta.
Permite entrada interactiva del usuario o pruebas automatizadas.
"""

import socket
import time
import sys
from typing import Tuple
import config


class SocketClient:
    """
    Cliente socket TCP que envía mensajes y mide el tiempo de respuesta.
    
    Mide:
    - Tiempo de solicitud a respuesta
    - Latencia de red
    - Rendimiento general de comunicación
    """
    
    def __init__(self, host: str = config.SERVER_HOST, port: int = config.SERVER_PORT):
        """
        Inicializa el cliente con la dirección del servidor.
        
        Argumentos:
            host: Nombre de host o dirección IP del servidor.
            port: Número de puerto del servidor.
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self) -> bool:
        """
        Conecta al servidor.
        
        Retorna:
            True si la conexión es exitosa, False en otro caso.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            if config.TCP_NODELAY_ENABLED:
                self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            print(f"✓ Conectado a {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Conexión fallida: {e}")
            return False
    
    def send_and_measure(self, message: str) -> Tuple[str, float]:
        """
        Envía un mensaje y mide el tiempo de respuesta.
        
        Argumentos:
            message: El mensaje a enviar.
            
        Retorna:
            Tupla de (contenido_respuesta, tiempo_respuesta_ms)
        """
        if not self.socket:
            return None, 0.0
        
        try:
            # Codifica y envía mensaje
            message_bytes = message.encode(config.MESSAGE_ENCODING)
            
            # Mide el tiempo
            start_time = time.perf_counter()
            self.socket.sendall(message_bytes)
            
            # Espera la respuesta
            response_bytes = self.socket.recv(config.BUFFER_SIZE)
            end_time = time.perf_counter()
            
            # Calcula el tiempo de respuesta en milisegundos
            response_time_ms = (end_time - start_time) * 1000
            response_content = response_bytes.decode(config.MESSAGE_ENCODING)
            
            return response_content, response_time_ms
        
        except Exception as e:
            print(f"✗ Error: {e}")
            return None, 0.0
    
    def disconnect(self) -> None:
        """Cierra la conexión."""
        if self.socket:
            self.socket.close()
            print("✓ Desconectado")


def run_interactive_client() -> None:
    """
    Ejecuta un cliente interactivo que acepta entrada del usuario.
    El usuario puede ingresar mensajes uno por uno y ver los tiempos de respuesta.
    """
    client = SocketClient()
    
    if not client.connect():
        return
    
    print("\n" + "="*60)
    print("Cliente Socket Interactivo")
    print("="*60)
    print("Ingresa mensajes a enviar (escribe 'quit' para salir):\n")
    
    try:
        while True:
            user_input = input("Mensaje a enviar: ").strip()
            
            if user_input.lower() == "quit":
                break
            
            if not user_input:
                print("  (mensaje vacío ignorado)\n")
                continue
            
            # Envía y mide
            response, response_time_ms = client.send_and_measure(user_input)
            
            if response:
                print(f"  Respuesta: {response}")
                print(f"  Tiempo de respuesta: {response_time_ms:.4f} ms\n")
            else:
                print("  No se recibió respuesta\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    run_interactive_client()