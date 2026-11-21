import pytest

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.forces import gravitational_accelerations


def test_two_body_gravitational_acceleration():

    body_a = CelestialBody(
        name="A",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=0.0,
        vy=0.0,
    )

    body_b = CelestialBody(
        name="B",
        mass=10.0,
        x=10.0,
        y=0.0,
        vx=0.0,
        vy=0.0,
    )

    accelerations = gravitational_accelerations(
        bodies=[body_a, body_b],
        gravitational_constant=2.0,
    )

    assert accelerations[0][0] == pytest.approx(0.2)
    assert accelerations[0][1] == pytest.approx(0.0)

    assert accelerations[1][0] == pytest.approx(-0.1)
    assert accelerations[1][1] == pytest.approx(0.0)


def test_coincident_bodies_raise_error():

    body_a = CelestialBody(
        name="A",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=0.0,
        vy=0.0,
    )

    body_b = CelestialBody(
        name="B",
        mass=10.0,
        x=0.0,
        y=0.0,
        vx=0.0,
        vy=0.0,
    )

    with pytest.raises(ValueError):
        gravitational_accelerations(
            bodies=[body_a, body_b],
            gravitational_constant=2.0,
        )