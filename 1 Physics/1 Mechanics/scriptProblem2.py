import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters
g = 9.8  # m/s^2
l = 1.0  # m
m = 1.0  # kg
omega_0 = np.sqrt(g / l)
zeta = 0.1
b = 2 * m * zeta * omega_0
omega_d = omega_0  # Resonance
T = 2 * np.pi / omega_d


# ODE system
def pendulum_deriv(state, t, b, m, g, l, F0, omega_d):
    theta, theta_dot = state
    dtheta_dt = theta_dot
    dtheta_dot_dt = -b / m * theta_dot - g / l * np.sin(theta) + F0 / (m * l) * np.cos(omega_d * t)
    return [dtheta_dt, dtheta_dot_dt]


# Simulation
def simulate(F0, t_max, points_per_period=100):
    dt = T / points_per_period
    t = np.arange(0, t_max * T, dt)
    state0 = [0, 0]
    sol = odeint(pendulum_deriv, state0, t, args=(b, m, g, l, F0, omega_d))
    theta = sol[:, 0]
    theta_dot = sol[:, 1]
    theta_mod = np.mod(theta + np.pi, 2 * np.pi) - np.pi
    return t, theta, theta_dot, theta_mod


# Plotting
def plot_results(F0, label):
    t, theta, theta_dot, theta_mod = simulate(F0, 100)
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(t[:1000], theta[:1000])
    plt.title(f'Time Series (F0={F0} N)')
    plt.xlabel('Time (s)')
    plt.ylabel('θ (rad)')

    plt.subplot(2, 2, 2)
    plt.plot(theta_mod, theta_dot, '.', ms=1)
    plt.title('Phase Diagram')
    plt.xlabel('θ mod 2π (rad)')
    plt.ylabel('dθ/dt (rad/s)')

    poincare_idx = np.arange(100, len(t), 100)
    plt.subplot(2, 2, 3)
    plt.plot(theta_mod[poincare_idx], theta_dot[poincare_idx], '.', ms=2)
    plt.title('Poincaré Section')
    plt.xlabel('θ mod 2π (rad)')
    plt.ylabel('dθ/dt (rad/s)')

    plt.tight_layout()
    plt.savefig(f'pendulum_F0_{label}.png')
    plt.close()


# Bifurcation diagram
def bifurcation_diagram(F0_range=np.arange(0, 20.1, 0.2)):
    theta_poincare = []
    F0_vals = []
    for F0 in F0_range:
        t, _, theta_dot, theta_mod = simulate(F0, 200)
        poincare_idx = np.arange(100 * 100, 200 * 100, 100)
        theta_poincare.extend(theta_mod[poincare_idx])
        F0_vals.extend([F0] * len(poincare_idx))
    plt.figure(figsize=(10, 6))
    plt.plot(F0_vals, theta_poincare, '.', ms=1)
    plt.title('Bifurcation Diagram')
    plt.xlabel('Driving Amplitude F0 (N)')
    plt.ylabel('θ mod 2π (rad)')
    plt.savefig('bifurcation.png')
    plt.close()


# Run
plot_results(1, 'small')
plot_results(15, 'chaotic')
bifurcation_diagram()