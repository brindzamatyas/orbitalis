import math

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation
from orbitalis.diagnostics import total_energy


# Physical parameters
G = 1.0
mass = 1.0
separation = 10.0
dt = 0.01

# Initial circular orbital velocity
omega = math.sqrt(
    G * (2 * mass) / separation**3
)

orbital_radius = separation / 2
velocity = omega * orbital_radius


# Create two bodies
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


# Initial energy
initial_energy = total_energy(simulation)

max_relative_deviation = 0.0

steps = 100_000


# Run simulation
for _ in range(steps):

    simulation.step()

    current_energy = total_energy(simulation)

    relative_deviation = abs(
        (current_energy - initial_energy)
        / initial_energy
    )

    max_relative_deviation = max(
        max_relative_deviation,
        relative_deviation,
    )


# Final results
final_energy = total_energy(simulation)

print(f"Simulation time: {simulation.simulation_time}")
print(f"Initial energy: {initial_energy:.12f}")
print(f"Final energy: {final_energy:.12f}")

print(
    "Maximum relative energy deviation: "
    f"{max_relative_deviation:.12e}"
)