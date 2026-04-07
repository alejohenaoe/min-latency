"""
Modelos de datos para intercambio de mensajes.
"""

from dataclasses import dataclass


@dataclass
class Message:
    """Representa un mensaje del cliente."""
    content: str
    timestamp: float = 0.0


@dataclass
class Response:
    """Representa una respuesta del servidor."""
    content: str
    
    def to_bytes(self, encoding: str = "utf-8") -> bytes:
        """Convierte la respuesta a bytes."""
        return self.content.encode(encoding)
