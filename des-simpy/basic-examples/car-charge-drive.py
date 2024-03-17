import simpy

# Define a process representing the behavior of a driver
def driver(env, car):
    # Wait for 3 time units and then interrupt the car's action process
    yield env.timeout(3)
    car.action.interrupt()

# Define a class representing a car object in the simulation
class Car(object):
    def __init__(self, env):
        self.env = env
        # Start the car's run method as a SimPy process
        self.action = env.process(self.run())

    # Method representing the car's behavior
    def run(self):
        while True:
            # Start parking and charging
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We may get interrupted while charging the battery
            try:
                # Start the charging process for a specified duration
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                # When interrupted during charging, handle it gracefully
                print('Was interrupted. Hope, the battery is full enough ...')

            # Start driving after charging
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            # Drive for a specified duration
            yield self.env.timeout(trip_duration)

    # Method representing the charging process
    def charge(self, duration):
        # Simulate the charging process for a specified duration
        yield self.env.timeout(duration)

# Create a SimPy environment
env = simpy.Environment()

# Create a car instance within the environment
car = Car(env)

# Start the driver process within the simulation environment
env.process(driver(env, car))

# Run the simulation until the specified time (15 in this case)
env.run(until=15)
