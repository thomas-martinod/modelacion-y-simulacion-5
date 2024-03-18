import simpy
import numpy as np

# Lista para almacenar los tiempos en cola
tiempos_en_cola = []

# Definir una función para la llegada de los clientes
def llegada_clientes(env, notaria, tiempo_entre_llegadas):
    # Inicializar el tiempo de llegada del primer cliente
    llegada = 0
    while True:  # Continuar simulando la llegada de clientes indefinidamente
        yield env.timeout(llegada)  # Esperar hasta que llegue el próximo cliente
        tiempo_llegada = env.now  # Guardar el tiempo de llegada del cliente
        env.process(cliente(env, notaria, tiempo_llegada))  # Iniciar el proceso del nuevo cliente
        llegada = np.random.exponential(tiempo_entre_llegadas)  # Calcular el tiempo hasta la próxima llegada

# Definir una función para el proceso del cliente
def cliente(env, notaria, tiempo_llegada):
    with notaria.request() as turno_notaria:  # Solicitar un turno en la notaría
        tiempo_en_cola = env.now - tiempo_llegada  # Calcular el tiempo en cola
        tiempos_en_cola.append(tiempo_en_cola)  # Agregar el tiempo en cola a la lista
        yield turno_notaria  # Esperar hasta que se obtenga un turno disponible
        # Determinar si el cliente va a autenticación o emisión
        if np.random.random() < 0.6:  # 60% de probabilidad de ir a autenticación
            yield env.process(autenticacion(env))  # Ir a la actividad de autenticación
        else:
            yield env.process(emision(env))  # Ir a la actividad de emisión

# Definir la actividad de autenticación de documentos
def autenticacion(env):
    tiempo_autenticacion = np.random.normal(8, 1.5)  # Generar tiempo de autenticación
    yield env.timeout(tiempo_autenticacion)  # Esperar durante el tiempo de autenticación
    print(f"Cliente autenticó documentos en tiempo {env.now}")  # Imprimir el tiempo en que autenticó documentos

# Definir la actividad de emisión de documentos
def emision(env):
    tiempo_emision = np.random.uniform(7, 10)  # Generar tiempo de emisión
    yield env.timeout(tiempo_emision)  # Esperar durante el tiempo de emisión
    print(f"Cliente emitió documentos en tiempo {env.now}")  # Imprimir el tiempo en que emitió documentos

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

# Imprimir los tiempos en cola
print("Tiempos en cola:", tiempos_en_cola)
