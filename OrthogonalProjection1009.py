from manimlib import *

#目前是正交投影转NDC
class PerspectiveToOrthographic(Scene):
    def construct(self):
        # 创建3D框架
        frame = self.camera.frame
        frame.set_euler_angles(theta=30 * DEGREES, phi=70 * DEGREES)
        frame.set_field_of_view(PI / 20)
        frame.shift(1 * OUT)  # 将相机向后移动得更远

        axisMax = 6.5
        axisStep = 1
        axisX = 0
        WIDTH = 4
        # 添加3D坐标轴
        axes = ThreeDAxes(
            x_range=(axisX, axisMax, axisStep),
            y_range=(axisX, axisMax, axisStep),
            z_range=(axisX, axisMax, axisStep),
            height=WIDTH, width=WIDTH, depth=WIDTH,
            axis_config={"color": BLUE}
        )
        self.add(axes)

        # 坐标轴标签
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

        # 正交投影观察体的基础点（近面）
        base_points = [
            [-2, 5, -2], [-2, 5, 2], [2, 5, 2], [2, 5, -2]
        ]

        # 正交投影观察体的远平面点
        far_plane_points = [
            # [-4, 10, -4], [-4, 10, 4], [4, 10, 4], [4, 10, -4]
            [-2, 10, -2], [-2, 10, 2], [2, 10, 2], [2, 10, -2]
        ]

        # 绘制观察体的基础和远平面
        base_polygon = Polygon(
            *[axes.c2p(*point) for point in base_points],
            fill_color=YELLOW, fill_opacity=0.2
        )
        far_plane_polygon = Polygon(
            *[axes.c2p(*point) for point in far_plane_points],
            fill_color=GREEN, fill_opacity=0.2
        )

        self.add(base_polygon, far_plane_polygon)

        # 绘制观察体的侧面
        sides = []
        for i in range(len(base_points)):
            side_polygon = Polygon(
                axes.c2p(*base_points[i]), axes.c2p(*base_points[(i + 1) % len(base_points)]),
                axes.c2p(*far_plane_points[(i + 1) % len(far_plane_points)]), axes.c2p(*far_plane_points[i]),
                fill_color=BLUE, fill_opacity=0.1
            )
            sides.append(side_polygon)
            self.add(side_polygon)

        # 定义新的远平面点（压缩后）
        new_far_plane_points = [
            [-2, 10, -2], [-2, 10, 2], [2, 10, 2], [2, 10, -2]
        ]

        # 创建新的远平面
        new_far_plane_polygon = Polygon(
            *[axes.c2p(*point) for point in new_far_plane_points],
            fill_color=GREEN, fill_opacity=0.2
        )

        # 转换远平面
        animationlist = []
        animationlist.append(Transform(far_plane_polygon, new_far_plane_polygon))


        # 现在，转换每个侧面以与新的远平面对齐
        for i in range(len(base_points)):
            new_side_polygon = Polygon(
                axes.c2p(*base_points[i]), axes.c2p(*base_points[(i + 1) % len(base_points)]),
                axes.c2p(*new_far_plane_points[(i + 1) % len(new_far_plane_points)]), axes.c2p(*new_far_plane_points[i]),
                fill_color=BLUE, fill_opacity=0.1
            )
            # 转换每个侧面多边形
            animationlist.append(Transform(sides[i], new_side_polygon))

        # 播放动画
        self.play(*animationlist, run_time=0.5)



        # 我们还需要将正交投影观察体规范化，让x,y,z 的范围规范到-1到1.
        #
        # 如下图所示，正交投影观察体中的点（xmin，ymin，-znear）/（left，bottom，-near）规范化后成为点（-1，-1，-1），点（xmax，ymax，-zfar）规范化后成为点（1，1，1）
        #
        # ，也就是下图呈现的，将正交投影矩阵规范化，即将矩阵移动到中心
        animationlist2 = []
        # 将观察体的基础平面/近平面 移动到-2.5
        new_Near_ndc = -1
        NEW_base_points = [
            [-1, new_Near_ndc , -1], [-1, new_Near_ndc , 1], [1, new_Near_ndc , 1], [1, new_Near_ndc , -1]
        ]
        new_base_polygon = Polygon(
            *[axes.c2p(*point) for point in NEW_base_points],
            fill_color=YELLOW, fill_opacity=0.2
        )
        animationlist2.append(Transform(base_polygon, new_base_polygon))

        New_far_ndc = 1
        NEW_far_plane_points = [
            [-1, New_far_ndc, -1], [-1, New_far_ndc, 1], [1, New_far_ndc, 1], [1, New_far_ndc, -1]
        ]
        new_far_plane_polygon = Polygon(
            *[axes.c2p(*point) for point in NEW_far_plane_points],
            fill_color=GREEN, fill_opacity=0.2
        )
        animationlist2.append(Transform(far_plane_polygon, new_far_plane_polygon))

        # 侧面也移动
        for i in range(len(NEW_base_points)):
            new_side_polygon = Polygon(
                axes.c2p(*NEW_base_points[i]), axes.c2p(*NEW_base_points[(i + 1) % len(NEW_base_points)]),
                axes.c2p(*NEW_far_plane_points[(i + 1) % len(NEW_far_plane_points)]), axes.c2p(*NEW_far_plane_points[i]),
                fill_color=BLUE, fill_opacity=0.1
            )
            # 转换每个侧面多边形
            animationlist2.append(Transform(sides[i], new_side_polygon))


        self.play(*animationlist2, run_time=3)
