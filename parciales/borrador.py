import simpy
import numpy as np

# Tiempo de inicio y fin de la jornada laboral
SIMULATION_TIME = 60 * 1
tiempos_de_espera_asignacion = []
tiempos_de_espera_autenticacion = []
tiempos_de_espera_emision = []
tiempos_en_el_sistema_autenticacion = []
tiempos_en_el_sistema_emision = []
tiempos_en_el_sistema_hasta_autenticación = []
personas_autenticacion = 0
personas_emision = 0
personas_con_turno_asignado = 0
tiempos_ocio_asignacion = []
tiempos_ocio_autenticacion = []
tiempos_ocio_emision = []



class Notaria:
    def __init__(self, env):
        self.env = env
        self.fila_asignacion = simpy.Resource(env, capacity=1)
        self.last_departure_time = 0  # Inicializar el tiempo de salida del último cliente

    def asignacion_de_turno(self, customer):
        global tiempos_de_espera_autenticacion
        global tiempos_en_el_sistema_hasta_autenticación
        global personas_con_turno_asignado
        global tiempos_ocio_asignacion

        tiempo_de_llegada = self.env.now
        with self.fila_asignacion.request() as request:
            yield request
            wait_time = self.env.now - tiempo_de_llegada
            tiempos_de_espera_autenticacion.append(wait_time)

            print(f"{self.env.now:.2f}: {customer} llega a la asignacion")
            tiempo_en_asignacion = np.random.normal(loc = 2, scale = 0.5)
            if tiempo_en_asignacion < 0:
                tiempo_en_asignacion = 0

            yield self.env.timeout(tiempo_en_asignacion)
            salida_de_asignacion = self.env.now

            tiempo_total_hasta_asignacion = salida_de_asignacion - tiempo_de_llegada
            tiempos_en_el_sistema_hasta_autenticación.append(tiempo_total_hasta_asignacion)
            print(f"{self.env.now:.2f}: {customer} obtuvo su turno")
            personas_con_turno_asignado += 1

            # Calcular el tiempo de ocio del cajero
            idle_time = max(0, tiempo_de_llegada - self.last_departure_time)
            tiempos_ocio_asignacion.append(idle_time)

            # Actualizar el tiempo de salida del último cliente
            self.last_departure_time = salida_de_asignacion


def persona(env, name, notaria):
    print(f"{env.now:.2f}: {name} llega a la fila")
    yield env.process(notaria.asignacion_de_turno(name))



def simular_notaria(env, numero_de_personas_a_generar):
    global wait_times
    atm = Notaria(env)
    for i in range(numero_de_personas_a_generar):
        env.process(persona(env, f"Customer-{i+1}", atm))
        inter_arrival_time = np.random.exponential(10)  # Tiempo entre llegadas con media 4
        yield env.timeout(inter_arrival_time)

    # Ejecutar el cajero automático durante 4 horas
    yield env.timeout(4 * 60)  # 4 horas * 60 minutos por hora

# Configuración y inicio de la simulación
np.random.seed(42)
env = simpy.Environment()
env.process(simular_notaria(env, numero_de_personas_a_generar=10**6))
env.run(until=SIMULATION_TIME)  # Ejecutar hasta 4 horas

