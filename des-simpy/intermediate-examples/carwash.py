import simpy
import random
import numpy as np

class ATM:
    def __init__(self, env):
        self.env = env
        self.queue = simpy.Resource(env, capacity=1)
        self.wait_times = []
        self.customers_served = 0

    def withdraw_cash(self, customer):
        arrival_time = self.env.now
        with self.queue.request() as request:
            yield request
            wait_time = self.env.now - arrival_time
            self.wait_times.append(wait_time)
            print(f"{self.env.now:.2f}: {customer} begins transaction")  # Print the start time
            processing_time = random.normalvariate(5, 1.2)
            if processing_time < 0:
                processing_time = 0
            yield self.env.timeout(processing_time)
            print(f"{self.env.now:.2f}: {customer} withdrew cash")
            self.customers_served += 1

def customer_generator(env, atm):
    i = 1
    while True:
        yield env.timeout(random.expovariate(1/4))  # Tiempo entre llegadas con media 4
        env.process(atm.withdraw_cash(f"Customer-{i}"))
        i += 1

def simulate_atm(env):
    atm = ATM(env)
    env.process(customer_generator(env, atm))
    yield env.timeout(4 * 60)  # Ejecutar durante 4 horas
    
    # Calculate average wait time
    average_wait_time = np.mean(atm.wait_times)
    print(f"Tiempo promedio de espera en cola: {average_wait_time:.2f} unidades de tiempo")
    
    # Print number of customers served
    print(f"Número de personas atendidas: {atm.customers_served}")

# Setup and start the simulation
random.seed(42)
env = simpy.Environment()
env.process(simulate_atm(env))
env.run(until=4 * 60)  # Ejecutar la simulación durante 4 horas
