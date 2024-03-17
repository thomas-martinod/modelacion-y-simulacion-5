# Our first example will be a car process.
# The car will alternately drive and park for a while. When it starts driving (or parking),
# it will print the current simulation time.

import simpy


# env is an instance
def car(env):
    # Infinite loop representing continuous operation of the car
    while True:
        # Print a message indicating the car is starting to park at the current simulation time
        print('Start parking at %d' % env.now)

        # Set the duration for which the car will remain parked
        parking_duration = 5

        # Create a SimPy event to wait for parking_duration time units to elapse
        # The yield statement pauses the function until this event completes
        yield env.timeout(parking_duration)

        # Print a message indicating the car has started driving again
        print('Start driving at %d' % env.now)

        # Set the duration of the trip
        trip_duration = 2

        # Create a SimPy event to wait for trip_duration time units to elapse
        # The yield statement pauses the function until this event completes
        yield env.timeout(trip_duration)

# Create a SimPy environment
env = simpy.Environment()

# Add the car process to the environment
env.process(car(env))

# Run the simulation until the specified time (15 in this case)
env.run(until=15)