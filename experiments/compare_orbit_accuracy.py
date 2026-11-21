import math
import matplotlib.pyplot as plt

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation


def run_experiment(dt: float, total_time: float = 1000.0):

    G = 1.0
    mass = 1.0
    separation = 10.0

    omega = math.sqrt(
        G * (2 * mass) / separation**3
    )

    orbital_radius = separation / 2
    velocity = omega * orbital_radius

    body_a = CelestialBody(
        name="A",
        mass=mass,
        x=-orbital_radius,
        y=0.0,
        vx=0.0,
        vy=-velocity,
    )

    body_b = CelestialBody(
        name="B",
        mass=mass,
        x=orbital_radius,
        y=0.0,
        vx=0.0,
        vy=velocity,
    )

    simulation = Simulation(
        bodies=[body_a, body_b],
        gravitational_constant=G,
        time_step=dt,
    )

    time_history = []
    position_error_history = []

    max_error = 0.0
    steps = round(total_time / dt)

    for _ in range(steps):

        simulation.step()

        t = simulation.simulation_time

        # Analytical position of body A
        analytical_x = -orbital_radius * math.cos(omega * t)
        analytical_y = -orbital_radius * math.sin(omega * t)

        # Numerical position of body A
        numerical_x = body_a.x
        numerical_y = body_a.y

        # Euclidean position error
        dx = numerical_x - analytical_x
        dy = numerical_y - analytical_y

        position_error = math.sqrt(dx**2 + dy**2)

        relative_error = position_error / orbital_radius

        max_error = max(max_error, position_error)

        time_history.append(t)
        position_error_history.append(relative_error)

    return (
        simulation.simulation_time,
        max_error,
        time_history,
        position_error_history,
    )


time_steps = [0.04, 0.02, 0.01, 0.005]

results = {}

print(
    f"{'Time step':>12} | "
    f"{'Simulation time':>16} | "
    f"{'Max position error':>20}"
)

print("-" * 56)

for dt in time_steps:

    simulated_time, max_error, times, errors = run_experiment(dt)

    results[dt] = (times, errors)

    print(
        f"{dt:12.5f} | "
        f"{simulated_time:16.6f} | "
        f"{max_error:20.12e}"
    )


# Plot relative position error

plt.figure(figsize=(12, 6))

for dt, (times, errors) in results.items():

    plt.plot(
        times,
        errors,
        label=f"dt = {dt}",
    )

plt.title("Relative Position Error Over Simulation Time")
plt.xlabel("Simulation Time")
plt.ylabel("Relative Position Error")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()