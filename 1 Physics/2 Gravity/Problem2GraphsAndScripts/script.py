import numpy as np
import matplotlib.pyplot as plt

# Constants (mass in kg, radius in meters)
planets = {"Earth": (5.97e24, 6.371e6),
           "Mars": (6.42e23, 3.389e6),
           "Jupiter": (1.898e27, 6.9911e7)}
G = 6.67430e-11  # Gravitational constant

# Compute escape velocities
velocities = {planet: np.sqrt(2 * G * mass / radius) / 1000 for planet, (mass, radius) in planets.items()}

# Plot results
plt.bar(velocities.keys(), velocities.values(), color=['blue', 'red', 'orange'])
plt.ylabel("Escape Velocity (km/s)")
plt.title("Escape Velocities of Planets")
plt.show()