"""
Procesador de mensajes para respuestas de baja latencia.
"""

from models import Message, Response
import config


class DefaultMessageProcessor:
    """Responde con "Hola Mundo"."""
    
    def process(self, message: Message) -> Response:
        """Procesa un mensaje y devuelve una respuesta."""
        return Response(content=config.DEFAULT_RESPONSE)
