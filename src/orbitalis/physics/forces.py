from orbitalis.physics.body import CelestialBody


def gravitational_accelerations(
    bodies: list[CelestialBody],
    gravitational_constant: float,
) -> list[tuple[float, float]]:
    """
    Calculate gravitational accelerations for all bodies.

    Returns:
        A list of (ax, ay) acceleration tuples.
    """

    accelerations = []

    for i, body in enumerate(bodies):

        ax = 0.0
        ay = 0.0

        for j, other in enumerate(bodies):

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
                gravitational_constant
                * other.mass
                / distance_cubed
            )

            ax += factor * dx
            ay += factor * dy

        accelerations.append((ax, ay))

    return accelerations