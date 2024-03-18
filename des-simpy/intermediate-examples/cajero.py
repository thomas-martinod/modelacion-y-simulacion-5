import simpy
import numpy as np

RANDOM_SEED = 42
NUM_ATMS = 1
SIM_TIME = 60

class ATM:
    def __init__(self, env, num_atms, extraction_time) -> None:
        self.env = env
        self.atm = simpy.Resource(env, num_atms)
        self.extraction_time = extraction_time

    def extract(self, person):
        yield self.env.timeout(self.extraction_time)
        print(f'Person {}')
