# Importar las bibliotecas necesarias
import simpy  # SimPy para simulación de eventos discretos
import numpy as np  # NumPy para generación de números aleatorios

# Definir una función para simular la llegada de clientes a la notaría
def llegada_clientes(env, notaria, tiempo_entre_llegadas):
    llegada = 0  # Inicializar el tiempo de llegada del primer cliente
    while True:
        # Esperar hasta que llegue el próximo cliente
        yield env.timeout(llegada)
        # Iniciar el proceso de atención para el nuevo cliente
        env.process(cliente(env, notaria))
        # Generar el tiempo hasta la próxima llegada de cliente
        llegada = np.random.exponential(tiempo_entre_llegadas)

# Definir una función para simular el proceso de atención de un cliente en la notaría
def cliente(env, notaria):
    # Solicitar un turno en la notaría
    with notaria.request() as turno:
        # Esperar hasta que sea el turno del cliente
        yield turno
        # Simular el tiempo que el cliente pasa en la actividad de atención
        tiempo_atencion = np.random.normal(2, 0.5)  # Media de 2 minutos y desviación estándar de 0.5 minutos
        yield env.timeout(tiempo_atencion)
        # Imprimir el momento en que el cliente es atendido y sale de la notaría
        print(f"Cliente atendido en tiempo {env.now}")

# Configurar los parámetros de la simulación
tiempo_simulacion = 9 * 60  # Duración total de la simulación en minutos (8am a 5pm)
tiempo_entre_llegadas = 4  # Media del tiempo entre llegadas de clientes en minutos

# Inicializar el entorno de simulación de SimPy
env = simpy.Environment()

# Crear el recurso que representa la notaría (una cola de clientes)
notaria = simpy.Resource(env, capacity=1)

# Iniciar el proceso de llegada de clientes a la notaría
env.process(llegada_clientes(env, notaria, tiempo_entre_llegadas))

# Ejecutar la simulación hasta alcanzar el tiempo de simulación especificado
env.run(until=tiempo_simulacion)

