import math
import matplotlib.pyplot as plt

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation
from orbitalis.diagnostics import total_energy


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

    initial_energy = total_energy(simulation)

    max_deviation = 0.0

    time_history = [simulation.simulation_time]
    energy_error_history = [0.0]

    steps = round(total_time / dt)

    for _ in range(steps):

        simulation.step()

        current_energy = total_energy(simulation)

        relative_error = (
            (current_energy - initial_energy)
            / abs(initial_energy)
        )

        max_deviation = max(
            max_deviation,
            abs(relative_error),
        )

        time_history.append(simulation.simulation_time)
        energy_error_history.append(relative_error)

    return (
        simulation.simulation_time,
        max_deviation,
        time_history,
        energy_error_history,
    )


time_steps = [0.04, 0.02, 0.01, 0.005]

results = {}

print(
    f"{'Time step':>12} | "
    f"{'Simulation time':>16} | "
    f"{'Max energy deviation':>22}"
)

print("-" * 58)

for dt in time_steps:

    simulated_time, deviation, times, errors = run_experiment(dt)

    results[dt] = (times, errors)

    print(
        f"{dt:12.5f} | "
        f"{simulated_time:16.6f} | "
        f"{deviation:22.12e}"
    )


# Plot energy error over simulation time

plt.figure(figsize=(12, 6))

for dt, (times, errors) in results.items():

    plt.plot(
        times,
        errors,
        label=f"dt = {dt}",
    )

plt.axhline(0.0, linewidth=0.8)

plt.title("Relative Energy Error Over Simulation Time")
plt.xlabel("Simulation Time")
plt.ylabel("Relative Energy Error")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()