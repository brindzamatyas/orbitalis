from orbitalis.physics.body import CelestialBody
from orbitalis.physics.forces import gravitational_accelerations


class Simulation:
    """Manages the physical simulation of celestial bodies."""

    def __init__(
        self,
        bodies: list[CelestialBody] | None = None,
        gravitational_constant: float = 6.67430e-11,
        time_step: float = 1.0,
    ):
        if gravitational_constant <= 0:
            raise ValueError("Gravitational constant must be positive.")

        if time_step <= 0:
            raise ValueError("Time step must be positive.")

        self.bodies = list(bodies) if bodies is not None else []
        self.G = gravitational_constant
        self.time_step = time_step
        self.simulation_time = 0.0

        for body in self.bodies:
            if body.mass <= 0:
                raise ValueError("Body mass must be positive.")

    def add_body(self, body: CelestialBody):
        """Add a celestial body to the simulation."""

        if body.mass <= 0:
            raise ValueError("Body mass must be positive.")

        self.bodies.append(body)

    def step(self):
        """Advance the simulation by one time step."""

        dt = self.time_step

        # Delegate force calculation to the physics force module.
        accelerations = gravitational_accelerations(
            bodies=self.bodies,
            gravitational_constant=self.G,
        )

        # Update velocities and positions.
        for body, (ax, ay) in zip(self.bodies, accelerations):
            body.vx += ax * dt
            body.vy += ay * dt

            body.x += body.vx * dt
            body.y += body.vy * dt

        self.simulation_time += dt
