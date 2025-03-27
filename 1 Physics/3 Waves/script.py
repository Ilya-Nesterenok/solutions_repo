import numpy as np
import matplotlib.pyplot as plt

# Define wave parameters
A = 1         # Amplitude
lambda_ = 5   # Wavelength
k = 2 * np.pi / lambda_  # Wave number
f = 1         # Frequency
omega = 2 * np.pi * f    # Angular frequency
phi = 0       # Initial phase

# Grid size
x_range = np.linspace(-10, 10, 300)
y_range = np.linspace(-10, 10, 300)
X, Y = np.meshgrid(x_range, y_range)

# Time variable (static snapshot)
t = 0

def polygon_vertices(n, radius=5):
    """Returns coordinates of n vertices of a regular polygon."""
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    return np.array([(radius * np.cos(a), radius * np.sin(a)) for a in angles])

# Choose number of sources (triangle, square, pentagon)
N_sources = 80  # Change to 3 for triangle, 5 for pentagon, etc.
sources = polygon_vertices(N_sources)

def wave_from_source(x0, y0, X, Y, t):
    """Computes the wave displacement from a single point source."""
    r = np.sqrt((X - x0)**2 + (Y - y0)**2) + 1e-6  # Avoid division by zero
    return (A / np.sqrt(r)) * np.cos(k * r - omega * t + phi)

# Superposition of waves from all sources
total_wave = np.zeros_like(X)

for x0, y0 in sources:
    total_wave += wave_from_source(x0, y0, X, Y, t)

plt.figure(figsize=(8, 6))
plt.contourf(X, Y, total_wave, levels=50, cmap="coolwarm")
plt.colorbar(label="Wave Displacement")
plt.scatter(sources[:, 0], sources[:, 1], color='black', marker='o', label="Sources")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title(f"Interference Pattern for {N_sources}-sided Polygon")
plt.legend()
plt.show()