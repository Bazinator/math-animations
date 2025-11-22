from manim import *
import numpy as np

class MosquitoProblem(ThreeDScene):
    def construct(self):
        # --- CONFIGURATION ---
        # Point P(2, -1, 0)
        p_val = np.array([2, -1, 0])
        
        # 1. SETUP SCENE
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4])
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.add(axes)
        
        # 2. CREATE THE SURFACE f(x,y,z) = 2x^2 + 3y^2
        # The point is (2, -1, 0), so the level curve is 2(4) + 3(1) = 11.
        # Equation: 2x^2 + 3y^2 = 11 (Elliptic Cylinder)
        # Parametrization: x = sqrt(11/2)cos(u), y = sqrt(11/3)sin(u), z = v
        cylinder = Surface(
            lambda u, v: np.array([
                np.sqrt(11/2) * np.cos(u),
                np.sqrt(11/3) * np.sin(u),
                v
            ]),
            u_range=[0, 2 * PI],
            v_range=[-2, 2],
            resolution=(24, 12), # Low res for fast rendering
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.5
        )

        # 3. MATH CALCULATIONS
        # Gradient of Surface f (Direction of flight)
        # grad_f = <4x, 6y, 0> at (2, -1, 0) => <8, -6, 0>
        grad_f_vec = np.array([8, -6, 0])
        # Normalize it to get direction u
        norm_f = np.linalg.norm(grad_f_vec) # Length is 10
        direction_u = grad_f_vec / norm_f   # <0.8, -0.6, 0>
        
        # Velocity v = speed * direction = 5 * u
        velocity_vec = 5 * direction_u # <4, -3, 0>

        # Gradient of Temperature T (The Heat Field)
        # T = x^3y + y^3z + xz^3
        # grad_T at (2, -1, 0)
        # dx = 3x^2y + z^3 => 3(4)(-1) + 0 = -12
        # dy = x^3 + 3y^2z => 8 + 0 = 8
        # dz = y^3 + 3xz^2 => -1 + 0 = -1
        grad_T_vec = np.array([-12, 8, -1])

        # 4. VISUAL ELEMENTS
        
        # The Mosquito
        mosquito = Dot3D(point=p_val, color=YELLOW, radius=0.15)
        label_p = MathTex("P(2, -1, 0)").next_to(mosquito, UP + RIGHT)
        
        # Vector 1: The Normal to the Surface (Direction of flight)
        # We scale it down visually so it fits on screen, but math is real
        arrow_flight = Arrow3D(
            start=p_val, 
            end=p_val + (grad_f_vec * 0.3), 
            color=GREEN
        )
        
        # Vector 2: The Temperature Gradient (Direction of Heat Increase)
        arrow_temp = Arrow3D(
            start=p_val, 
            end=p_val + (grad_T_vec * 0.3), 
            color=RED
        )

        # 5. HUD TEXT (Fixed on screen)
        # We use add_fixed_in_frame_mobjects for explanatory text
        title = Tex("Midterm 2 Problem 2B Visualization").to_corner(UL)
        
        step1 = MathTex(r"\vec{v} \parallel \nabla f = \langle 8, -6, 0 \rangle").scale(0.7).to_corner(UR)
        step2 = MathTex(r"\text{Speed} = 5 \implies \vec{v} = \langle 4, -3, 0 \rangle").scale(0.7).next_to(step1, DOWN)
        step3 = MathTex(r"\nabla T = \langle -12, 8, -1 \rangle").scale(0.7).next_to(step2, DOWN)
        step4 = MathTex(r"\frac{dT}{dt} = \nabla T \cdot \vec{v}").scale(0.7).next_to(step3, DOWN)
        step5 = MathTex(r"= (-12)(4) + (8)(-3) + (-1)(0)").scale(0.7).next_to(step4, DOWN)
        step6 = MathTex(r"= -72").scale(0.7).next_to(step5, DOWN).set_color(YELLOW)

        # --- ANIMATION SEQUENCE ---
        
        # Phase 1: Show Geometry
        self.add_fixed_in_frame_mobjects(title)
        self.play(Create(cylinder), run_time=2)
        self.play(FadeIn(mosquito))
        self.begin_ambient_camera_rotation(rate=0.1) # Slow rotation starts
        
        # Phase 2: Show Direction of Flight (Normal to Surface)
        self.add_fixed_in_frame_mobjects(step1)
        self.play(Create(arrow_flight))
        self.wait(1)
        self.add_fixed_in_frame_mobjects(step2)
        
        # Phase 3: Show Temperature Gradient
        self.add_fixed_in_frame_mobjects(step3)
        self.play(Create(arrow_temp))
        self.wait(1)
        
        # Phase 4: Solve
        self.add_fixed_in_frame_mobjects(step4)
        self.wait(1)
        self.add_fixed_in_frame_mobjects(step5)
        self.wait(1)
        self.add_fixed_in_frame_mobjects(step6)
        
        self.wait(4)