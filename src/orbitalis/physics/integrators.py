from typing import Callable, Protocol

from orbitalis.physics.body import CelestialBody


AccelerationFunction = Callable[
    [list[CelestialBody]],
    list[tuple[float, float]],
]


class Integrator(Protocol):
    """Interface for numerical integration methods."""

    def step(
        self,
        bodies: list[CelestialBody],
        time_step: float,
        acceleration_function: AccelerationFunction,
    ) -> None:
        ...


class SemiImplicitEuler:
    """Semi-implicit Euler integration method."""

    def step(
        self,
        bodies: list[CelestialBody],
        time_step: float,
        acceleration_function: AccelerationFunction,
    ) -> None:
        """Advance all bodies by one integration step."""

        accelerations = acceleration_function(bodies)

        for body, (ax, ay) in zip(bodies, accelerations):
            body.vx += ax * time_step
            body.vy += ay * time_step

            body.x += body.vx * time_step
            body.y += body.vy * time_step


class VelocityVerlet:
    """Velocity Verlet integration method."""

    def step(
        self,
        bodies: list[CelestialBody],
        time_step: float,
        acceleration_function: AccelerationFunction,
    ) -> None:
        """Advance all bodies by one Velocity Verlet step."""

        dt = time_step

        # 1. Calculate accelerations at the current positions.
        accelerations_initial = acceleration_function(bodies)

        # 2. Update positions using initial velocities
        #    and initial accelerations.
        for body, (ax, ay) in zip(bodies, accelerations_initial):
            body.x += body.vx * dt + 0.5 * ax * dt**2
            body.y += body.vy * dt + 0.5 * ay * dt**2

        # 3. Recalculate accelerations at the new positions.
        accelerations_final = acceleration_function(bodies)

        # 4. Update velocities using the average acceleration.
        for body, (a0x, a0y), (a1x, a1y) in zip(
            bodies,
            accelerations_initial,
            accelerations_final,
        ):
            body.vx += 0.5 * (a0x + a1x) * dt
            body.vy += 0.5 * (a0y + a1y) * dt
