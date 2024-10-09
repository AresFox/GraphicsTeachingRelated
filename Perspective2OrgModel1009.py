from manimlib import *

class PerspectiveToOrthographic(Scene):
    def construct(self):
        # Creating a 3D frame
        # frame = self.camera.frame
        # frame.set_euler_angles(theta=30 * DEGREES, phi=60 * DEGREES)
        # frame.set_field_of_view(PI / 10)
        # frame.shift(2 * OUT + RIGHT)
        frame = self.camera.frame
        frame.set_euler_angles(theta=30 * DEGREES, phi=60 * DEGREES)
        frame.set_field_of_view(PI / 20)
        frame.shift(2.5 * OUT )  # 这里将相机向后移动得更远


        axisMax = 6.5
        axisStep = 1
        axisX = 0
        WIDTH = 4
        # Adding 3D axes
        axes = ThreeDAxes(
            x_range=(axisX, axisMax, axisStep),
            y_range=(axisX, axisMax, axisStep),
            z_range=(axisX, axisMax, axisStep),
            height=WIDTH, width=WIDTH, depth=WIDTH,
            axis_config={"color": BLUE}
        )
        self.add(axes)

        # Labels for axes
        labels = {
            "X": [axisMax, 0, 0],
            "-Z": [0, axisMax, 0],
            "Y": [0, 0, axisMax]
        }
        for label, position in labels.items():
            dot = Dot(axes.c2p(*position), fill_color=PINK)
            text = Text(label, font_size=40, color=BLUE_E)
            text.rotate(PI / 2, axis=RIGHT)
            text.next_to(dot, RIGHT if label == "X" else LEFT)
            self.add(text)

        # Frustum base points (near plane)
        base_points = [
            [-2, 5, -2], [-2, 5, 2], [2, 5, 2], [2, 5, -2]
        ]

        # Frustum far plane points
        far_plane_points = [
            [-4, 10, -4], [-4, 10, 4], [4, 10, 4], [4, 10, -4]
        ]

        # Draw the frustum's base and far planes
        base_polygon = Polygon(
            *[axes.c2p(*point) for point in base_points],
            fill_color=YELLOW, fill_opacity=0.2
        )
        far_plane_polygon = Polygon(
            *[axes.c2p(*point) for point in far_plane_points],
            fill_color=GREEN, fill_opacity=0.2
        )

        self.add(base_polygon, far_plane_polygon)

        # Draw the sides of the frustum
        sides = []
        for i in range(len(base_points)):
            side_polygon = Polygon(
                axes.c2p(*base_points[i]), axes.c2p(*base_points[(i + 1) % len(base_points)]),
                axes.c2p(*far_plane_points[(i + 1) % len(far_plane_points)]), axes.c2p(*far_plane_points[i]),
                fill_color=BLUE, fill_opacity=0.1
            )
            sides.append(side_polygon)
            self.add(side_polygon)

        # Define the new far plane points (compression)
        new_far_plane_points = [
            [-2, 10, -2], [-2, 10, 2], [2, 10, 2], [2, 10, -2]
        ]

        # Create a new far plane after compression
        new_far_plane_polygon = Polygon(
            *[axes.c2p(*point) for point in new_far_plane_points],
            fill_color=GREEN, fill_opacity=0.2
        )

        # Transform the far plane
        animationlist = []
        animationlist.append(Transform(far_plane_polygon, new_far_plane_polygon))


        # Now, transform each side of the frustum to align with the new far plane
        for i in range(len(base_points)):
            new_side_polygon = Polygon(
                axes.c2p(*base_points[i]), axes.c2p(*base_points[(i + 1) % len(base_points)]),
                axes.c2p(*new_far_plane_points[(i + 1) % len(new_far_plane_points)]), axes.c2p(*new_far_plane_points[i]),
                fill_color=BLUE, fill_opacity=0.1
            )
            # Transform each side polygon
            animationlist.append(Transform(sides[i], new_side_polygon))

        # Play the animations
        self.play(*animationlist, run_time=3)
        # Hold the final view for 2 seconds
        self.wait(2)