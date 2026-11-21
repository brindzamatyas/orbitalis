import pytest

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation

from orbitalis.diagnostics import (
    kinetic_energy,
    gravitational_potential_energy,
    total_energy,
    total_momentum,
)


def test_physical_diagnostics():

    body_a = CelestialBody(
        name="A",
        mass=5.0,
        x=0.0,
        y=0.0,
        vx=2.0,
        vy=3.0,
    )

    body_b = CelestialBody(
        name="B",
        mass=10.0,
        x=3.0,
        y=4.0,
        vx=-1.0,
        vy=4.0,
    )

    simulation = Simulation(
        bodies=[body_a, body_b],
        gravitational_constant=2.0,
        time_step=0.5,
    )

    assert kinetic_energy(simulation) == pytest.approx(117.5)

    assert gravitational_potential_energy(
        simulation
    ) == pytest.approx(-20.0)

    assert total_energy(simulation) == pytest.approx(97.5)

    px, py = total_momentum(simulation)

    assert px == pytest.approx(0.0)
    assert py == pytest.approx(55.0)