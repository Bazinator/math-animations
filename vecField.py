from manim import *
import numpy as np

class TemperatureField(ThreeDScene):
    def construct(self):
        # 1. Setup the Camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 2. Define the Vector Field Function (The Gradient)
        # T = x^3y + y^3z + xz^3
        def func(pos):
            x, y, z = pos
            # Calculate the partial derivatives
            dx = 3 * x**2 * y + z**3
            dy = x**3 + 3 * y**2 * z
            dz = y**3 + 3 * x * z**2
            
            # Combine into a vector
            vector = np.array([dx, dy, dz])
            
            # SCALING: These cubic values get HUGE very fast. 
            # We normalize the vector so arrows are uniform size, 
            # showing direction rather than magnitude for clarity.
            norm = np.linalg.norm(vector)
            if norm == 0:
                return vector
            return (vector / norm) * 0.5 # Scale down to length 0.5

        # 3. Create the 3D Vector Field
        # We manually create a grid of arrows because ArrowVectorField is planar by default
        arrows = VGroup()
        range_vals = range(-2, 3) # Grid from -2 to 2
        
        for x in range_vals:
            for y in range_vals:
                for z in range_vals:
                    point = np.array([x, y, z])
                    # Get the gradient direction at this point
                    direction = func(point)
                    # Create an arrow
                    arrow = Arrow3D(
                        start=point,
                        end=point + direction,
                        resolution=8,
                        color=BLUE
                    )
                    arrows.add(arrow)

        # 4. Create the Mosquito (The Dot)
        mosquito = Dot3D(point=np.array([-2, -2, -2]), color=RED, radius=0.1)
        
        # 5. Define the Path (A simple curve through the space)
        # A parametric curve: t goes from 0 to 1
        path = ParametricFunction(
            lambda t: np.array([
                2 * np.sin(t),      # x
                2 * np.cos(t),      # y
                t                   # z
            ]),
            t_range=[-2, 2],
            color=YELLOW
        )

        # 6. Animation Sequence
        self.add(ThreeDAxes(x_range=[-3,3], y_range=[-3,3], z_range=[-3,3]))
        
        # Show the field
        self.play(Create(arrows), run_time=2)
        self.wait(1)
        
        # Fly the mosquito
        self.add(mosquito)
        self.play(MoveAlongPath(mosquito, path), run_time=4)
        
        # Rotate camera to see the 3D depth
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)