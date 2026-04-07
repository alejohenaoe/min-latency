"""
Benchmark de rendimiento.
Envía múltiples solicitudes y muestra tiempos de respuesta en consola.
"""

import time
from socket_client import SocketClient
import config


class BenchmarkRunner:
    """Ejecuta benchmarks y muestra resultados."""
    
    def __init__(self, num_requests: int = config.BENCHMARK_REQUESTS):
        """Inicializa el ejecutor de benchmark."""
        self.num_requests = num_requests
        self.client = SocketClient()
    
    def run(self, test_message: str = config.BENCHMARK_MESSAGE) -> None:
        """Ejecuta la suite de benchmark y muestra resultados."""
        if not self.client.connect():
            print("✗ No se puede ejecutar el benchmark: conexión fallida")
            return
        
        print(f"\n{'='*70}")
        print(f"Benchmark: {self.num_requests} peticiones")
        print(f"{'='*70}")
        print(f"{'Petición #':<12} {'Mensaje':<20} {'Respuesta':<20} {'Tiempo (ms)':<12}")
        print(f"{'-'*70}")
        
        total_time = 0.0
        successful_requests = 0
        times = []
        
        for request_num in range(1, self.num_requests + 1):
            response, response_time_ms = self.client.send_and_measure(test_message)
            
            if response:
                print(f"{request_num:<12} {test_message:<20} {response:<20} "
                      f"{response_time_ms:<12.4f}")
                total_time += response_time_ms
                successful_requests += 1
                times.append(response_time_ms)
            else:
                print(f"{request_num:<12} {test_message:<20} {'FALLIDO':<20} "
                      f"{'N/A':<12}")
        
        # Resumen
        print(f"{'-'*70}")
        print(f"\nResumen:")
        print(f"  Total de peticiones: {self.num_requests}")
        print(f"  Exitosas: {successful_requests}")
        print(f"  Fallidas: {self.num_requests - successful_requests}")
        
        if successful_requests > 0:
            avg_time = total_time / successful_requests
            min_time = min(times)
            max_time = max(times)
            
            print(f"\nEstadísticas de tiempo:")
            print(f"  Mínimo: {min_time:.4f} ms")
            print(f"  Máximo: {max_time:.4f} ms")
            print(f"  Promedio: {avg_time:.4f} ms")
        
        print(f"{'='*70}\n")
        
        self.client.disconnect()


def run_benchmark() -> None:
    """Punto de entrada para ejecutar benchmarks."""
    runner = BenchmarkRunner(num_requests=config.BENCHMARK_REQUESTS)
    runner.run(test_message=config.BENCHMARK_MESSAGE)


if __name__ == "__main__":
    run_benchmark()
