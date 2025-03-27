import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Gravitational parameters (normalized units)
G, M = 1.0, 1.0

# Orbital radii
r_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
T_values = []  # To store orbital periods

# Differential equations for orbital motion
def orbital_motion(t, state, G, M):
    x, y, vx, vy = state
    r = np.sqrt(x ** 2 + y ** 2)
    ax = - (G * M / r ** 3) * x
    ay = - (G * M / r ** 3) * y
    return [vx, vy, ax, ay]

# Event to detect a full orbit (y = 0 crossing upward with positive vy)
def event_full_orbit(t, state, *args):
    return state[1]  # y = 0 condition

event_full_orbit.direction = 1  # Detect crossing from negative to positive
event_full_orbit.terminal = False  # Continue detecting multiple events

# Plot orbits
plt.figure(figsize=(10, 8))

for r in r_values:
    v = np.sqrt(G * M / r)  # Initial velocity for circular orbit
    state0 = [r, 0.0, 0.0, v]  # Initial conditions: (x, y, vx, vy)
    t_span = [0, 100]  # Time span for simulation

    sol = solve_ivp(orbital_motion, t_span, state0, args=(G, M),
                    t_eval=np.linspace(0, 100, 10000), events=event_full_orbit)

    # Plot the orbit
    plt.plot(sol.y[0], sol.y[1], label=f'r = {r}')

    # Check if at least two crossings were detected (one full orbit)
    if len(sol.t_events[0]) > 1:
        T = sol.t_events[0][1] - sol.t_events[0][0]  # Full orbit time
        T_values.append(T)
    else:
        print(f"Warning: No complete orbit detected for r = {r}")
        T_values.append(np.nan)

# Orbit plot settings
plt.xlabel('x')
plt.ylabel('y')
plt.title('Simulated Circular Orbits')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

# Convert to numpy arrays
T_values = np.array(T_values)
T_squared = T_values ** 2
r_cubed = r_values ** 3

# Remove NaN values if any
valid_indices = ~np.isnan(T_squared)
T_squared = T_squared[valid_indices]
r_cubed = r_cubed[valid_indices]

# Plot Kepler’s Third Law (T^2 vs r^3)
plt.figure(figsize=(8, 6))
plt.plot(r_cubed, T_squared, 'o-', label='Simulated Data')

# Linear fit for T^2 vs r^3
slope, intercept = np.polyfit(r_cubed, T_squared, 1)
plt.plot(r_cubed, slope * r_cubed + intercept, 'r--', label=f'Fit: slope={slope:.3f}')

# Theoretical Kepler’s Third Law slope (T² = (4π²/GM) * r³)
theoretical_slope = 4 * np.pi ** 2
plt.plot(r_cubed, theoretical_slope * r_cubed, 'g--', label=f'Theoretical: {theoretical_slope:.3f}')
plt.legend()
plt.grid(True)
plt.xlabel('$r^3$')
plt.ylabel('$T^2$')
plt.title('Verification of $T^2 \\propto r^3$')
plt.show()

# Print slopes for comparison
print(f"Simulated slope: {slope:.3f}")
print(f"Theoretical slope (4π²): {theoretical_slope:.3f}")
