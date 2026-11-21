import math

from orbitalis.physics.simulation import Simulation


def kinetic_energy(simulation: Simulation) -> float:
    """Calculate the total kinetic energy of the system."""

    energy = 0.0

    for body in simulation.bodies:
        speed_squared = body.vx**2 + body.vy**2
        energy += 0.5 * body.mass * speed_squared

    return energy


def gravitational_potential_energy(
    simulation: Simulation,
) -> float:
    """Calculate the total gravitational potential energy."""

    energy = 0.0
    bodies = simulation.bodies

    for i, body in enumerate(bodies):
        for other in bodies[i + 1:]:

            dx = other.x - body.x
            dy = other.y - body.y

            distance = math.hypot(dx, dy)

            if distance == 0:
                raise ValueError(
                    "Two bodies occupy the same position."
                )

            energy -= (
                simulation.G * body.mass * other.mass
            ) / distance

    return energy


def total_energy(simulation: Simulation) -> float:
    """Calculate the total mechanical energy."""

    return (
        kinetic_energy(simulation)
        + gravitational_potential_energy(simulation)
    )


def total_momentum(
    simulation: Simulation,
) -> tuple[float, float]:
    """Calculate the total linear momentum (px, py)."""

    px = 0.0
    py = 0.0

    for body in simulation.bodies:
        px += body.mass * body.vx
        py += body.mass * body.vy

    return px, py