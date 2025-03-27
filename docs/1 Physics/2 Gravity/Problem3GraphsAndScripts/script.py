import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M = 5.972e24  # Mass of Earth (kg)
R = 6371e3  # Radius of Earth (m)


# Equations of motion
def equations(t, state):
    x, y, vx, vy = state
    r = np.sqrt(x ** 2 + y ** 2)
    ax = -G * M * x / r ** 3
    ay = -G * M * y / r ** 3
    return [vx, vy, ax, ay]


# Initial conditions for different scenarios
initial_conditions = [
    (R + 500e3, 0, 0, 7500),  # Low Earth orbit
    (R + 500e3, 0, 0, 9000),  # Higher orbit
    (R + 500e3, 0, 0, 11200),  # Escape trajectory
    (R + 500e3, 0, 0, 3000)  # Suborbital flight
]

labels = ['Low Earth Orbit', 'Higher Orbit', 'Escape Trajectory', 'Suborbital Flight']

plt.figure(figsize=(8, 8))
for (x0, y0, vx0, vy0), label in zip(initial_conditions, labels):
    # Solve the equations of motion
    t_span = (0, 15000)  # Time range
    state0 = [x0, y0, vx0, vy0]
    sol = solve_ivp(equations, t_span, state0, t_eval=np.linspace(0, 15000, 1000))

    x, y = sol.y[0], sol.y[1]
    plt.plot(x / 1e3, y / 1e3, label=label)

# Plot Earth
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(R * np.cos(theta) / 1e3, R * np.sin(theta) / 1e3, 'k', label='Earth')
plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.legend()
plt.title('Payload Trajectories Near Earth')
plt.axis('equal')
plt.grid(True)
plt.show()