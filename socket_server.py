"""
Módulo del servidor socket para aceptar y procesar conexiones de clientes.
Maneja E/S de red y delega el procesamiento de mensajes a MessageProcessor.

Principio: Responsabilidad Única - solo gestiona la comunicación por socket.
"""

import socket
import time
from message_handler import DefaultMessageProcessor
from models import Message
import config


class SocketServer:
    """
    Servidor socket TCP que acepta conexiones y procesa mensajes.
    Responsabilidad única: gestión de conexiones y E/S de red.
    """
    
    def __init__(self):
        """Inicializa el servidor."""
        self.processor = DefaultMessageProcessor()
        self.server_socket = None
    
    def start(self) -> None:
        """Inicia la escucha de conexiones de clientes."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((config.SERVER_HOST, config.SERVER_PORT))
        self.server_socket.listen(config.SERVER_BACKLOG)
        
        print(f"Servidor socket ejecutándose en {config.SERVER_HOST}:{config.SERVER_PORT}")
        print(f"Esperando conexiones... (Presiona Ctrl+C para detener)")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self._handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """
        Maneja una única conexión de cliente.
        
        Argumentos:
            client_socket: La conexión socket del cliente.
            client_address: Tupla de (IP, puerto) del cliente.
        """
        print(f"\nConexión de {client_address[0]}:{client_address[1]}")
        
        with client_socket:
            # Configura el socket para comunicación de baja latencia
            if config.TCP_NODELAY_ENABLED:
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            while True:
                try:
                    received_bytes = client_socket.recv(config.BUFFER_SIZE)
                    
                    if not received_bytes:
                        break
                    
                    # Parsea el mensaje entrante
                    received_text = received_bytes.decode(config.MESSAGE_ENCODING).strip()
                    
                    if not received_text:
                        continue
                    
                    print(f"  Recibido: {received_text}")
                    
                    # Crea objeto de mensaje y lo procesa
                    request_time = time.perf_counter()
                    message = Message(content=received_text, timestamp=request_time)
                    response = self.processor.process(message)
                    
                    # Envía la respuesta
                    response_bytes = response.to_bytes(config.MESSAGE_ENCODING)
                    client_socket.sendall(response_bytes)
                    
                    print(f"  Enviado: {response.content}")
                    
                except Exception as e:
                    print(f"  Error: {e}")
                    break
        
        print(f"Desconexión de {client_address[0]}:{client_address[1]}\n")
    
    def stop(self) -> None:
        """Detiene el servidor y cierra el socket."""
        if self.server_socket:
            self.server_socket.close()


def run_socket_server() -> None:
    """Punto de entrada para ejecutar el servidor."""
    server = SocketServer()
    server.start()


if __name__ == "__main__":
    run_socket_server()