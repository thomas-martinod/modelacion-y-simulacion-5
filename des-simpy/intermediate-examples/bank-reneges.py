"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""

import random
import simpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience

def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        # Generate a new customer
        c = customer(env, f'Customer{i:02d}', counter, time_in_bank=12.0)
        # Process the customer
        env.process(c)
        # Generate a random time interval for the next customer
        t = random.expovariate(1.0 / interval)
        # Wait for the next customer arrival
        yield env.timeout(t)

def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    # Record the arrival time of the customer
    arrive = env.now
    print(f'{arrive:7.4f} {name}: Here I am')

    # Request a counter to be served
    with counter.request() as req:
        # Determine the patience of the customer
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or timeout if patience runs out
        results = yield req |  env.timeout(patience)

        # Calculate the wait time
        wait = env.now - arrive

        if req in results:
            # The customer reached the counter
            print(f'{env.now:7.4f} {name}: Waited {wait:6.3f}')

            # Generate service time for the customer
            tib = random.expovariate(1.0 / time_in_bank)
            # Serve the customer for the generated service time
            yield env.timeout(tib)
            print(f'{env.now:7.4f} {name}: Finished')

        else:
            # The customer left without being served (reneged)
            print(f'{env.now:7.4f} {name}: RENEGED after {wait:6.3f}')

# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Create a counter resource with capacity 1 (only 1 customer can be served at a time)
counter = simpy.Resource(env, capacity=1)

# Start generating customers and running the simulation
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()