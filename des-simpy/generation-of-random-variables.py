import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, logistic, uniform

# Set the seed for reproducibility
np.random.seed(42)

# Generate 100 observations from the exponential distribution with mean 10
exponential_observations = np.random.exponential(scale=10, size=10000)


# Generate 100 observations from the logistic distribution with mean 10
logistic_observations = np.random.logistic(loc=10, scale=10/1.8138, size=10000)


# Generate 100 observations from the uniform distribution with range [8, 25]
uniform_observations = np.random.uniform(low=8, high=25, size=10000)




# Plot histograms for each distribution with theoretical probability density function (PDF)
plt.figure(figsize=(15, 5))



# Exponential distribution
plt.subplot(1, 3, 1)
plt.hist(exponential_observations, bins=20, density=True, color='blue', alpha=0.7, label='Histogram')
x = np.linspace(0, np.max(exponential_observations), 1000)
plt.plot(x, expon.pdf(x, scale=10), color='red', label='Theoretical PDF')
plt.title('Exponential Distribution')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()



# Logistic distribution
plt.subplot(1, 3, 2)
plt.hist(logistic_observations, bins=20, density=True, color='green', alpha=0.7, label='Histogram')
x = np.linspace(logistic.ppf(0.01, loc=10, scale=10/1.8138), logistic.ppf(0.99, loc=10, scale=10/1.8138), 1000)
plt.plot(x, logistic.pdf(x, loc=10, scale=10/1.8138), color='red', label='Theoretical PDF')
plt.title('Logistic Distribution')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()




# Uniform distribution
plt.subplot(1, 3, 3)
plt.hist(uniform_observations, bins=20, density=True, color='orange', alpha=0.7, label='Histogram')
x = np.linspace(8, 25, 1000)
plt.plot(x, uniform.pdf(x, loc=8, scale=17), color='red', label='Theoretical PDF')
plt.title('Uniform Distribution')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()

plt.tight_layout()
plt.show()
