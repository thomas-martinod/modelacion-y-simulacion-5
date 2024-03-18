import simpy
import random
import numpy as np

wait_times = []
customers_served = 0

class ATM:
    def __init__(self, env):
        self.env = env
        self.queue = simpy.Resource(env, capacity=1)

    def withdraw_cash(self, customer):
        global wait_times
        global customers_served
        arrival_time = self.env.now
        with self.queue.request() as request:
            yield request
            wait_time = self.env.now - arrival_time
            wait_times.append(wait_time)
            print(f"{self.env.now:.2f}: {customer} begins transaction")  # Print the start time
            processing_time = random.normalvariate(5, 1.2)
            if processing_time < 0:
                processing_time = 0
            yield self.env.timeout(processing_time)
            print(f"{self.env.now:.2f}: {customer} withdrew cash")
            customers_served += 1

def customer(env, name, atm):
    print(f"{env.now:.2f}: {name} arrives at the ATM")
    yield env.process(atm.withdraw_cash(name))

def simulate_atm(env, num_customers):
    global wait_times
    atm = ATM(env)
    for i in range(num_customers):
        env.process(customer(env, f"Customer-{i+1}", atm))
        inter_arrival_time = random.expovariate(1/4)  # Tiempo entre llegadas con media 4
        yield env.timeout(inter_arrival_time)

    # Run the ATM for 4 hours
    yield env.timeout(4 * 60)  # 4 hours * 60 minutes per hou

# Setup and start the simulation
random.seed(42)
env = simpy.Environment()
env.process(simulate_atm(env, num_customers=10**6))
env.run(until=4 * 60)  # Run until 4 hours

# Code executed after simulation ends
# You can place any additional code here
# For example, you can calculate and print more statistics
# Calculate average wait time
average_wait_time = np.mean(wait_times)
print(f"Tiempo promedio de espera en cola: {average_wait_time:.2f} unidades de tiempo")

# Print number of customers served
print(f"Numero de personas atendidas: {customers_served}")