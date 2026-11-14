from orbitalis.physics.body import CelestialBody


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
        accelerations = []

        # Calculate gravitational acceleration
        for i, body in enumerate(self.bodies):

            ax = 0.0
            ay = 0.0

            for j, other in enumerate(self.bodies):

                if i == j:
                    continue

                dx = other.x - body.x
                dy = other.y - body.y

                distance_squared = dx**2 + dy**2

                if distance_squared == 0:
                    raise ValueError(
                        "Two bodies occupy the same position."
                    )

                distance_cubed = distance_squared ** 1.5

                factor = (
                    self.G * other.mass / distance_cubed
                )

                ax += factor * dx
                ay += factor * dy

            accelerations.append((ax, ay))

        # Update velocities and positions
        for body, (ax, ay) in zip(
            self.bodies, accelerations
        ):

            body.vx += ax * dt
            body.vy += ay * dt

            body.x += body.vx * dt
            body.y += body.vy * dt

        self.simulation_time += dt