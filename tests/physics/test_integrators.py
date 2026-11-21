import pytest

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.integrators import (
    SemiImplicitEuler,
    VelocityVerlet,
)


def test_semi_implicit_euler_step():

    body = CelestialBody(
        name="Test",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=2.0,
        vy=3.0,
    )

    integrator = SemiImplicitEuler()

    def constant_acceleration(bodies):
        return [(4.0, -2.0)]

    integrator.step(
        bodies=[body],
        time_step=0.5,
        acceleration_function=constant_acceleration,
    )

    assert body.vx == pytest.approx(4.0)
    assert body.vy == pytest.approx(2.0)

    assert body.x == pytest.approx(2.0)
    assert body.y == pytest.approx(1.0)


def test_velocity_verlet_step():

    body = CelestialBody(
        name="Test",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=2.0,
        vy=3.0,
    )

    integrator = VelocityVerlet()

    def constant_acceleration(bodies):
        return [(4.0, -2.0)]

    integrator.step(
        bodies=[body],
        time_step=0.5,
        acceleration_function=constant_acceleration,
    )

    assert body.vx == pytest.approx(4.0)
    assert body.vy == pytest.approx(2.0)

    assert body.x == pytest.approx(1.5)
    assert body.y == pytest.approx(1.25)
