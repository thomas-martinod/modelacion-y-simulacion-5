import simpy
import numpy as np

SIMULATION_TIME = 60 * 9 # 9 horas
tiempos_de_espera_asignacion = []
tiempos_en_el_sistema_asignacion = []
personas_con_turno_asignado = 0
tiempos_de_ocio_asignacion = []
tiempos_de_espera_autenticacion = []
tiempos_en_el_sistema_autenticacion = []
tiempos_de_ocio_autenticacion = []
tiempos_de_espera_emision = []
tiempos_en_el_sistema_emision = []
tiempos_de_ocio_emision = []

class Notaria:
    def __init__(self, env):
        self.env = env
        self.fila_asignacion = simpy.Resource(env, capacity=1)
        self.fila_autenticacion = simpy.Resource(env, capacity=1)
        self.fila_emision = simpy.Resource(env, capacity=1)
        self.salida_ultimo_cliente = 0

    def asignacion_de_turno(self, customer):
        global tiempos_de_espera_asignacion
        global personas_con_turno_asignado
        global tiempos_en_el_sistema_asignacion
        global tiempos_de_ocio_asignacion
        hora_de_llegada = self.env.now

        with self.fila_asignacion.request() as request:
            yield request
            tiempo_de_espera = self.env.now - hora_de_llegada
            tiempos_de_espera_asignacion.append(tiempo_de_espera)

            print(f"{self.env.now:.2f}: {customer} llega a que le asignen el turno")
            tiempo_de_asignacion = np.random.normal(loc=2, scale=0.5)
            if tiempo_de_asignacion < 0:
                tiempo_de_asignacion = 0
            yield self.env.timeout(tiempo_de_asignacion)
            tiempo_salida_asignacion = self.env.now
            tiempo_en_asignacion = tiempo_salida_asignacion - hora_de_llegada
            tiempos_en_el_sistema_asignacion.append(tiempo_en_asignacion)

            print(f"{self.env.now:.2f}: {customer} le fue asignado el turno")
            personas_con_turno_asignado += 1

            tiempo_de_ocio = max(0, hora_de_llegada - self.salida_ultimo_cliente)
            tiempos_de_ocio_asignacion.append(tiempo_de_ocio)
            self.salida_ultimo_cliente = tiempo_salida_asignacion

            # Decide si el cliente va a autenticación o emisión de documentos
            if np.random.rand() < 0.6:
                self.env.process(self.autenticacion_de_documentos(customer))
                print(f"{self.env.now:.2f}: {customer} comienza a hacer fila en autenticación")
            else:
                self.env.process(self.emision_de_documentos(customer))
                print(f"{self.env.now:.2f}: {customer} comienza a hacer fila en emisión")

    def autenticacion_de_documentos(self, customer):
        global tiempos_de_espera_autenticacion
        global tiempos_en_el_sistema_autenticacion
        global tiempos_de_ocio_autenticacion
        hora_de_llegada = self.env.now

        with self.fila_autenticacion.request() as request:
            yield request
            tiempo_de_espera = self.env.now - hora_de_llegada
            print(f"{self.env.now:.2f}: {customer} comienza la autenticación de documentos")
            tiempo_autenticacion = np.random.uniform(8, 1.5)
            yield self.env.timeout(tiempo_autenticacion)
            tiempo_salida_autenticacion = self.env.now
            tiempo_en_autenticacion = tiempo_salida_autenticacion - hora_de_llegada
            print(f"{self.env.now:.2f}: {customer} completó la autenticación de documentos")
            tiempos_de_espera_autenticacion.append(tiempo_de_espera)
            tiempos_en_el_sistema_autenticacion.append(tiempo_en_autenticacion)
            tiempo_de_ocio = max(0, hora_de_llegada - self.salida_ultimo_cliente)
            tiempos_de_ocio_autenticacion.append(tiempo_de_ocio)
            self.salida_ultimo_cliente = tiempo_salida_autenticacion

    def emision_de_documentos(self, customer):
        global tiempos_de_espera_emision
        global tiempos_en_el_sistema_emision
        global tiempos_de_ocio_emision
        hora_de_llegada = self.env.now

        with self.fila_emision.request() as request:
            yield request
            tiempo_de_espera = self.env.now - hora_de_llegada
            print(f"{self.env.now:.2f}: {customer} comienza la emisión de documentos")
            tiempo_emision = np.random.uniform(low=7, high=10)
            if tiempo_emision < 0:
                tiempo_emision = 0
            yield self.env.timeout(tiempo_emision)
            tiempo_salida_emision = self.env.now
            tiempo_en_emision = tiempo_salida_emision - hora_de_llegada
            print(f"{self.env.now:.2f}: {customer} completó la emisión de documentos")
            tiempos_de_espera_emision.append(tiempo_de_espera)
            tiempos_en_el_sistema_emision.append(tiempo_en_emision)
            tiempo_de_ocio = max(0, hora_de_llegada - self.salida_ultimo_cliente)
            tiempos_de_ocio_emision.append(tiempo_de_ocio)
            self.salida_ultimo_cliente = tiempo_salida_emision


def cliente(env, nombre, nota):
    print(f"{env.now:.2f}: {nombre} llega a la notaria")
    yield env.process(nota.asignacion_de_turno(nombre))


def simular_notaria(env, numero_clientes):
    nota = Notaria(env)
    for i in range(numero_clientes):
        env.process(cliente(env, f"Customer-{i+1}", nota))
        tiempo_de_llegada_entre_clientes = np.random.exponential(4)
        yield env.timeout(tiempo_de_llegada_entre_clientes)

    yield env.timeout(SIMULATION_TIME)

np.random.seed(42)
env = simpy.Environment()
env.process(simular_notaria(env, numero_clientes=10**6))
env.run(until=SIMULATION_TIME)



print("-----------------------------------------------------------------\n")
print("Estadísticos para la etapa de asignación de turno:")
print(f"Número de personas atendidas: {personas_con_turno_asignado}")

average_wait_time = np.mean(tiempos_de_espera_asignacion)
average_system_time = np.mean(tiempos_en_el_sistema_asignacion)
print(f"Tiempo promedio de espera en cola: {average_wait_time:.2f} minutos")
print(f"Tiempo promedio en el sistema: {average_system_time:.2f} minutos")
print(f"Máximo tiempo en el sistema: {max(tiempos_en_el_sistema_asignacion):.2f} minutos")

total_idle_time = sum(tiempos_de_ocio_asignacion)
idle_percentage = total_idle_time / SIMULATION_TIME
occupation_percentage = 1 - idle_percentage
print(f"El porcentaje de ocio es: {idle_percentage*100:.2f}%")
print(f"El porcentaje de ocupación es: {occupation_percentage*100:.2f}%")

print("-----------------------------------------------------------------\n")
print("Estadísticos para la etapa de autenticación de documentos:")
print(f"Número de personas que completaron la autenticación de documentos: {len(tiempos_de_espera_autenticacion)}")

if len(tiempos_de_espera_autenticacion) > 0:
    average_wait_time_autenticacion = np.mean(tiempos_de_espera_autenticacion)
    average_system_time_autenticacion = np.mean(tiempos_en_el_sistema_autenticacion)
    print(f"Tiempo promedio de espera en cola de autenticación: {average_wait_time_autenticacion:.2f} minutos")
    print(f"Tiempo promedio en el sistema de autenticación: {average_system_time_autenticacion:.2f} minutos")
    print(f"Máximo tiempo en el sistema de autenticación: {max(tiempos_en_el_sistema_autenticacion):.2f} minutos")

    total_idle_time_autenticacion = sum(tiempos_de_ocio_autenticacion)
    idle_percentage_autenticacion = total_idle_time_autenticacion / SIMULATION_TIME
    occupation_percentage_autenticacion = 1 - idle_percentage_autenticacion

    print(f"El porcentaje de ocio durante la autenticación de documentos es: {idle_percentage_autenticacion*100:.2f}%")
    print(f"El porcentaje de ocupación durante la autenticación de documentos es: {occupation_percentage_autenticacion*100:.2f}%")

else:
    print("No hay personas que hayan completado la autenticación de documentos en esta simulación.")

print("-----------------------------------------------------------------\n")
print("Estadísticos para la etapa de emisión de documentos:")
print(f"Número de personas que completaron la emisión de documentos: {len(tiempos_de_espera_emision)}")

if len(tiempos_de_espera_emision) > 0:
    average_wait_time_emision = np.mean(tiempos_de_espera_emision)
    average_system_time_emision = np.mean(tiempos_en_el_sistema_emision)
    print(f"Tiempo promedio de espera en cola de emisión: {average_wait_time_emision:.2f} minutos")
    print(f"Tiempo promedio en el sistema de emisión: {average_system_time_emision:.2f} minutos")

    total_idle_time_emision = sum(tiempos_de_ocio_emision)
    idle_percentage_emision = total_idle_time_emision / SIMULATION_TIME
    occupation_percentage_emision = 1 - idle_percentage_emision

    print(f"El porcentaje de ocio durante la emisión de documentos es: {idle_percentage_emision*100:.2f}%")
    print(f"El porcentaje de ocupación durante la emisión de documentos es: {occupation_percentage_emision*100:.2f}%")

else:
    print("No hay personas que hayan completado la emisión de documentos en esta simulación.")
