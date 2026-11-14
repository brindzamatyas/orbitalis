import tkinter as tk

from orbitalis.physics.body import CelestialBody


class Renderer:
    """Handles the graphical representation of physical objects."""

    def __init__(
        self,
        canvas: tk.Canvas,
        reference_distance: float = 7_000_000.0,
    ):
        self.canvas = canvas
        self.reference_distance = reference_distance

        # Visual-only orbital trails (stored in world coordinates).
        self.trails = {}

    def draw(
        self,
        bodies: list[CelestialBody],
        central_body_name: str = "Earth",
    ):
        """Render physical bodies on the canvas."""

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            return

        center_x = width / 2
        center_y = height / 2

        # Find the central body.
        central_body = next(
            (
                body for body in bodies
                if body.name == central_body_name
            ),
            None,
        )

        if central_body is None:
            return

        # World-to-screen scaling.
        scale = min(width, height) * 0.30 / self.reference_distance

        def to_screen(x, y):
            return (
                center_x + (x - central_body.x) * scale,
                center_y - (y - central_body.y) * scale,
            )

        # Coordinate axes.
        self.canvas.create_line(
            0, center_y, width, center_y,
            fill="#35424D",
            dash=(4, 6),
        )

        self.canvas.create_line(
            center_x, 0, center_x, height,
            fill="#35424D",
            dash=(4, 6),
        )

        # Render orbital trails.
        for body in bodies:

            if body.name == central_body_name:
                continue

            trail = self.trails.setdefault(body.name, [])

            relative_position = (
                body.x - central_body.x,
                body.y - central_body.y,
            )

            trail.append(relative_position)

            # Limit memory usage.
            if len(trail) > 2000:
                trail.pop(0)

            if len(trail) >= 2:
                points = []

                for x, y in trail:
                    sx = center_x + x * scale
                    sy = center_y - y * scale

                    points.extend((sx, sy))

                self.canvas.create_line(
                    *points,
                    fill="#55758A",
                    width=1,
                )

        # Render celestial bodies.
        for body in bodies:

            sx, sy = to_screen(body.x, body.y)

            if body.name == central_body_name:
                radius = 24
                color = "#2676B8"
                outline = "#78C8F0"
            else:
                radius = 6
                color = "#F5C542"
                outline = "#FFF0A5"

            self.canvas.create_oval(
                sx - radius,
                sy - radius,
                sx + radius,
                sy + radius,
                fill=color,
                outline=outline,
                width=2,
            )

            self.canvas.create_text(
                sx + radius + 12,
                sy - radius - 8,
                text=body.name.upper(),
                fill=color,
                font=("DejaVu Sans", 9),
            )