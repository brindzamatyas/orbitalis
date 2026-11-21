from orbitalis.physics.body import CelestialBody
from orbitalis.physics.forces import gravitational_accelerations
from orbitalis.physics.integrators import Integrator, SemiImplicitEuler


class Simulation:
    """Manages the physical simulation of celestial bodies."""

    def __init__(
        self,
        bodies: list[CelestialBody] | None = None,
        gravitational_constant: float = 6.67430e-11,
        time_step: float = 1.0,
        integrator: Integrator | None = None,
    ):
        if gravitational_constant <= 0:
            raise ValueError("Gravitational constant must be positive.")

        if time_step <= 0:
            raise ValueError("Time step must be positive.")

        self.bodies = list(bodies) if bodies is not None else []
        self.G = gravitational_constant
        self.time_step = time_step
        self.simulation_time = 0.0

        self.integrator = (
            integrator if integrator is not None else SemiImplicitEuler()
        )

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

        def acceleration_function(
            bodies: list[CelestialBody],
        ) -> list[tuple[float, float]]:
            return gravitational_accelerations(
                bodies=bodies,
                gravitational_constant=self.G,
            )

        self.integrator.step(
            bodies=self.bodies,
            time_step=self.time_step,
            acceleration_function=acceleration_function,
        )

        self.simulation_time += self.time_step
