import tkinter as tk

from orbitalis.physics.body import CelestialBody
from orbitalis.physics.simulation import Simulation
from orbitalis.visualization.renderer import Renderer


class OrbitalisApp:
    """Main application window for ORBITALIS."""

    def __init__(self, root: tk.Tk):

        self.root = root

        self.root.title(
            "ORBITALIS | Orbital Mechanics Sandbox"
        )

        self.root.geometry("1000x700")
        self.root.minsize(600, 450)

        self.background = "#101820"
        self.foreground = "#E6EDF3"
        self.accent = "#55B8E8"

        self.root.configure(bg=self.background)

        self._initialize_physics()
        self._build_interface()

        self.renderer = Renderer(self.canvas)

        self.steps_per_frame = 10

        self._update_simulation()

    def _initialize_physics(self):
        """Initialize the physical simulation."""

        earth = CelestialBody(
            name="Earth",
            mass=5.972e24,
            x=0.0,
            y=0.0,
            vx=0.0,
            vy=0.0,
        )

        satellite = CelestialBody(
            name="SAT-01",
            mass=1000.0,
            x=7_000_000.0,
            y=0.0,
            vx=0.0,
            vy=7546.0,
        )

        self.simulation = Simulation(
            bodies=[earth, satellite],
            time_step=1.0,
        )

    def _build_interface(self):
        """Create the graphical interface."""

        header = tk.Frame(
            self.root,
            bg=self.background,
            padx=20,
            pady=15,
        )

        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="ORBITALIS",
            font=("DejaVu Sans", 20, "bold"),
            fg=self.accent,
            bg=self.background,
        )

        title.pack(side=tk.LEFT)

        subtitle = tk.Label(
            header,
            text="Orbital Mechanics Sandbox | v0.3",
            font=("DejaVu Sans", 10),
            fg=self.foreground,
            bg=self.background,
        )

        subtitle.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(
            self.root,
            bg=self.background,
            highlightthickness=0,
        )

        self.canvas.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=5,
        )

        self.status = tk.Label(
            self.root,
            text="SYSTEM READY",
            font=("DejaVu Sans", 9),
            fg="#8B949E",
            bg=self.background,
            anchor=tk.W,
            padx=20,
            pady=10,
        )

        self.status.pack(fill=tk.X)

    def _update_simulation(self):
        """Advance physics and update visualization."""

        for _ in range(self.steps_per_frame):
            self.simulation.step()

        self.renderer.draw(self.simulation.bodies)

        self.status.configure(
            text=(
                f"SYSTEM RUNNING | "
                f"Simulation time: "
                f"{self.simulation.simulation_time:.0f} s"
            )
        )

        # Schedule the next update.
        self.root.after(16, self._update_simulation)


def main():

    root = tk.Tk()

    OrbitalisApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()