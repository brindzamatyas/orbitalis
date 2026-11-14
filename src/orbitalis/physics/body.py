from dataclasses import dataclass


@dataclass
class CelestialBody:
    """Represents a physical celestial body."""

    name: str
    mass: float

    x: float
    y: float

    vx: float
    vy: float