import simpy
import numpy as np

# Llegada al cajero con tiempo entre llegadas con distribución exponencial de media 10
# Tiempo de retiro de cash, normal con media 5 y sd 1.2

SIMULATION_TIME = 60
wait_times = []
system_times = []
customers_served = 0
idle_times = []

class ATM:
    def __init__(self, env):
        self.env = env
        self.queue = simpy.Resource(env, capacity=1)
        self.last_departure_time = 0  # Inicializar el tiempo de salida del último cliente

    def withdraw_cash(self, customer):
        global wait_times
        global customers_served
        global system_times
        global idle_times
        arrival_time = self.env.now
        with self.queue.request() as request:
            yield request
            wait_time = self.env.now - arrival_time
            wait_times.append(wait_time)
            print(f"{self.env.now:.2f}: {customer} begins transaction")
            processing_time = np.random.normal(loc = 5, scale = 1.2)
            if processing_time < 0:
                processing_time = 0
            yield self.env.timeout(processing_time)
            departure_time = self.env.now
            system_time = departure_time - arrival_time
            system_times.append(system_time)
            print(f"{self.env.now:.2f}: {customer} withdrew cash")
            customers_served += 1

            # Calcular el tiempo de ocio del cajero
            idle_time = max(0, arrival_time - self.last_departure_time)
            idle_times.append(idle_time)

            # Actualizar el tiempo de salida del último cliente
            self.last_departure_time = departure_time

def customer(env, name, atm):
    print(f"{env.now:.2f}: {name} arrives at the ATM")
    yield env.process(atm.withdraw_cash(name))

def simulate_atm(env, num_customers):
    global wait_times
    atm = ATM(env)
    for i in range(num_customers):
        env.process(customer(env, f"Customer-{i+1}", atm))
        inter_arrival_time = np.random.exponential(10)  # Tiempo entre llegadas con media 4
        yield env.timeout(inter_arrival_time)

    # Ejecutar el cajero automático durante 4 horas
    yield env.timeout(4 * 60)  # 4 horas * 60 minutos por hora

# Configuración y inicio de la simulación
np.random.seed(42)
env = simpy.Environment()
env.process(simulate_atm(env, num_customers=10**6))
env.run(until=SIMULATION_TIME)  # Ejecutar hasta 4 horas

print("-----------------------------------------------------------------\n")
print("Estadísticos:")
# Imprimir el número de clientes atendidos
print(f"Número de personas atendidas: {customers_served}")

# Estadísticas después de la simulación
average_wait_time = np.mean(wait_times)
average_system_time = np.mean(system_times)
print(f"Tiempo promedio de espera en cola: {average_wait_time:.2f} minutos")
print(f"Tiempo promedio en el sistema: {average_system_time:.2f} minutos")
print(f"Máximo tiempo en el sistema: {max(system_times):.2f} minutos")

# Calcular el tiempo total de ocio del cajero
total_idle_time = sum(idle_times)
idle_percentaje = total_idle_time/SIMULATION_TIME
occupation_percentage = 1-idle_percentaje
print(f"El porcentaje de ocio es: {idle_percentaje*100:.2f}%")
print(f"El porcentaje de ocupación es: {occupation_percentage*100:.2f}%")