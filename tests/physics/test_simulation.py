
import pytest

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation
from orbitalis.physics.integrators import (
    SemiImplicitEuler,
    VelocityVerlet,
)

def test_two_body_gravity_and_semi_implicit_euler():

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

    simulation = Simulation(
        bodies=[body_a, body_b],
        gravitational_constant=2.0,
        time_step=0.5,
    )

    simulation.step()

    # Velocity assertions
    assert body_a.vx == pytest.approx(0.1)
    assert body_b.vx == pytest.approx(-0.05)

    # Position assertions
    assert body_a.x == pytest.approx(0.05)
    assert body_b.x == pytest.approx(9.975)

    # Simulation time assertion
    assert simulation.simulation_time == pytest.approx(0.5)

def test_total_momentum_is_conserved():

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

    simulation = Simulation(
        bodies=[body_a, body_b],
        gravitational_constant=2.0,
        time_step=0.5,
    )

    initial_momentum_x = (
        body_a.mass * body_a.vx
        + body_b.mass * body_b.vx
    )

    initial_momentum_y = (
        body_a.mass * body_a.vy
        + body_b.mass * body_b.vy
    )

    for _ in range(100):
        simulation.step()

    final_momentum_x = (
        body_a.mass * body_a.vx
        + body_b.mass * body_b.vx
    )

    final_momentum_y = (
        body_a.mass * body_a.vy
        + body_b.mass * body_b.vy
    )

    assert final_momentum_x == pytest.approx(
        initial_momentum_x,
        abs=1e-10,
    )

    assert final_momentum_y == pytest.approx(
        initial_momentum_y,
        abs=1e-10,
    )

def test_single_body_moves_with_constant_velocity():

    body = CelestialBody(
        name="Test body",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=2.0,
        vy=3.0,
    )

    simulation = Simulation(
        bodies=[body],
        gravitational_constant=2.0,
        time_step=0.5,
    )

    for _ in range(10):
        simulation.step()

    assert body.x == pytest.approx(10.0)
    assert body.y == pytest.approx(15.0)

    assert body.vx == pytest.approx(2.0)
    assert body.vy == pytest.approx(3.0)

    assert simulation.simulation_time == pytest.approx(5.0)


def test_simulation_uses_semi_implicit_euler_by_default():

    simulation = Simulation()

    assert isinstance(simulation.integrator, SemiImplicitEuler)


def test_simulation_can_use_velocity_verlet():

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

    simulation = Simulation(
        bodies=[body_a, body_b],
        gravitational_constant=2.0,
        time_step=0.5,
        integrator=VelocityVerlet(),
    )

    simulation.step()

    final_distance = 9.9625

    expected_ax = 20.0 / final_distance**2
    expected_bx = -10.0 / final_distance**2

    assert body_a.x == pytest.approx(0.025)
    assert body_b.x == pytest.approx(9.9875)

    assert body_a.vx == pytest.approx(0.25 * (0.2 + expected_ax))
    assert body_b.vx == pytest.approx(0.25 * (-0.1 + expected_bx))

    assert isinstance(simulation.integrator, VelocityVerlet)
    assert simulation.simulation_time == pytest.approx(0.5)
