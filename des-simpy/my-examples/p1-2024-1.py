import simpy
import numpy as np

# Definir una función para la llegada de los clientes
def llegada_clientes(env, notaria, tiempo_entre_llegadas):
    llegada = 0  # Inicializar el tiempo de llegada del primer cliente
    while True:  # Continuar simulando la llegada de clientes indefinidamente
        yield env.timeout(llegada)  # Esperar hasta que llegue el próximo cliente
        env.process(cliente(env, notaria))  # Iniciar el proceso del nuevo cliente
        llegada = np.random.exponential(tiempo_entre_llegadas)  # Calcular el tiempo hasta la próxima llegada

# Definir una función para el proceso del cliente
def cliente(env, notaria):
    with notaria.request() as turno:  # Solicitar un turno en la notaría
        yield turno  # Esperar hasta que se obtenga un turno disponible
        print(f"Cliente obtuvo un turno en tiempo {env.now}")  # Imprimir el tiempo en que el cliente obtuvo el turno
        # Determinar aleatoriamente la siguiente actividad del cliente
        if np.random.uniform() < 0.6:  # 60% de probabilidad de ir a autenticación de documentos
            env.process(autenticacion_documentos(env))
        else:  # 40% de probabilidad de ir a emisión de documentos
            env.process(emision_documentos(env))

# Definir una función para la actividad de autenticación de documentos
def autenticacion_documentos(env):
    duracion = np.random.normal(8, 1.5)  # Duración de la autenticación de documentos
    yield env.timeout(duracion)  # Esperar durante el tiempo de autenticación
    print(f"Cliente autenticó documentos en tiempo {env.now}")  # Imprimir el tiempo en que el cliente autenticó documentos

# Definir una función para la actividad de emisión de documentos
def emision_documentos(env):
    duracion = np.random.uniform(7, 10)  # Duración de la emisión de documentos
    yield env.timeout(duracion)  # Esperar durante el tiempo de emisión
    print(f"Cliente emitió documentos en tiempo {env.now}")  # Imprimir el tiempo en que el cliente emitió documentos

# Configuración de la simulación
tiempo_simulacion = 9 * 60  # Duración total de la simulación en minutos (8am a 5pm)
tiempo_entre_llegadas = 4  # Media del tiempo entre llegadas de clientes en minutos

# Inicializar el entorno de simulación
env = simpy.Environment()

# Crear el recurso para representar la notaría (una cola de clientes)
notaria = simpy.Resource(env, capacity=1)  # Capacidad de atender a un cliente a la vez

# Iniciar el proceso de llegada de clientes
env.process(llegada_clientes(env, notaria, tiempo_entre_llegadas))

# Ejecutar la simulación hasta alcanzar el tiempo de simulación especificado
env.run(until=tiempo_simulacion)
