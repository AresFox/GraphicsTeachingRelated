


import numpy as np

from manimlib import *
from scipy.stats import qmc


class CoordinateSystemExample(Scene):

    def clamp(self, x, min_value, max_value):
        return max(min(x, max_value), min_value)
    def construct(self):
        axes = Axes(
            # x轴的范围从-1到10，步长为1
            x_range=(-2, 8,1),
            # y轴的范围从-2到2，步长为0.5y-axis ranges from -2 to 10 with a step size of 0.5
            y_range=(-1, 5,1 ),
            # 坐标系将会伸缩来匹配指定的height和width
            height=6,
            width=10,
            # Axes由两个NumberLine组成，你可以通过axis_config来指定它们的样式
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            },
            # 或者，你也可以像这样分别指定各个坐标轴的样式
            y_axis_config={
                "include_tip": False,
            }
        )
        # add_coordinate_labels方法的关键字参数可以传入DecimalNumber来指定它的样式
        # axes.add_coordinate_labels(
        #     # font_size=20,
        #     # num_decimal_places=1,
        # )
        self.add(axes)

        debug_mode = True
        # 定义n=4
        n = 4.0
        # point数组
        # 数量
        if(debug_mode):
            count = 5
        else:
            count = 10
        points = []
        pointDots = []
        far = 8.0
        k=0.5 # 斜率
        trick = 0.6
        trickP1 = 1-trick
        trickP1C = trickP1/2
        for i in range(count + 1):
            x = n + (far - n)  * i / count
            for(j) in range(count + 1):
                y = 0 + k * x * j / count
                points.append([x, y])
        # draw points
        for point in points:
            # x for R， y for G
            U = (point[0]-n) * 1.0 / (far-n)
            V = (point[1]-0) * 1.0 / (k*far)

            U -= 0.5
            V -= 0.5

            #U = U * trick + trickP1C
            #V = V * trick + trickP1C
            Y = 0.5
            # R = Y + 1.402 * (V - 0.5)
            # G = Y - 0.344136 * (U - 0.5) - 0.714136 * (V - 0.5)
            # B = Y + 1.772 * (U - 0.5)
            R = 1.164 * Y + 1.596 * V
            G = 1.164 * Y - 0.392 * U - 0.813 * V
            B = 1.164 * Y + 2.017 * U
            R = self.clamp(R, 0.0, 1.0)
            G = self.clamp(G, 0.0, 1.0)
            B = self.clamp(B, 0.0, 1.0)


            # print(R, G, B)
            # print(r, g, b)
            color_point = np.array([R,G,B], dtype=np.float64)
            # print(color_point)
            color_to_paint = rgb_to_color(color_point)
            # self.play(ShowCreation(Dot(axes.c2p(point[0], point[1]), fill_color=color_to_paint, radius=0.03)), run_time=0.03)
            dot = Dot(axes.c2p(point[0], point[1]), fill_color=color_to_paint, radius=0.03)
            show_dot_transparent = Dot(axes.c2p(point[0], point[1]), fill_color=color_to_paint, radius=0.03, fill_opacity=0.3)
            self.add(show_dot_transparent)
            pointDots.append(dot)
            self.add(dot)

        perspect_points = []
        # 计算变换后的坐标
        for point in points:
            x = point[0]
            y = point[1]
            x1 = -(n+far)-n*far/(-x)
            x1=-x1
            y1 = y * n / x
            # print(x1, y1)
            # self.play(ShowCreation(Dot(axes.c2p(x1, y1), fill_color=color_to_paint, radius=0.03)), run_time=0.03)
            perspect_points.append([x1, y1])

        # 将对应坐标的points数组变换到perspect_points数组
        # self.play lambda
        animation_list = []
        # for i in range(len(points)):
        #     animation_list.append(pointDots[i].animate.move_to(axes.c2p(perspect_points[i][0], perspect_points[i][1])))
        # self.play(AnimationGroup(*animation_list), run_time=2)


        z = 5.0
        y = 1.6
        y1 = (n/z)*y

        f=8
        z1 = -(n+f)-n*f/(-z)
        z1=-z1

        # Axes从CoordinateSystem类派生而来，意思是可以调用Axes.coords_to_point
        # （缩写为Axes.c2p）将一组坐标与一个点相关联，如下所示：
        dot = Dot(color=RED)
        # 画一条竖线，过（2，0）点  这是近平面
        # self.play(ShowCreation(DashedLine(axes.c2p(2, -2), axes.c2p(2, 3))))
        self.play(ShowCreation(Line(axes.c2p(4, 0), axes.c2p(4, 2))), run_time=0.1)

        # 棱台start-------------------------------------


        #画点M（8, 4）
        DotFar = Dot(axes.c2p(far,4), color=WHITE)
        self.play(ShowCreation(DotFar), run_time=0.1)
        # 连接原点和点M（8, 3）
        LineLengTai = Line(axes.c2p(0, 0), DotFar, color=WHITE)
        self.play(ShowCreation(LineLengTai), run_time=0.1)
        # 棱台END-------------------------------------

        # 这是远平面
        # farLine = Line(axes.c2p(far, 0), axes.c2p(far, 4), color=WHITE)
        # self.play(ShowCreation(farLine), run_time=0.1)
        #  #让这个是实线
        far_line = always_redraw(lambda: axes.get_v_line(DotFar.get_bottom()))
        self.add(far_line)

        # 画底下的点
        f0point = Dot(axes.c2p(far, 0), color=RED)
        self.play(ShowCreation(f0point), run_time=0.1)
        # 文字
        f0pointText = Text("-f", font_size=20)
        f0point1 = f0point.get_center() + np.array([-0.2, -0.0, 0])
        f0pointText.next_to(f0point1, DOWN)
        self.add(f0pointText)

        # 画底下的点
        C0point = Dot(axes.c2p(n, 0), color=RED)
        self.play(ShowCreation(C0point), run_time=0.1)
        # 文字
        C0pointText = Text("-n", font_size=20)
        C0point1 = C0point.get_center() + np.array([-0.2, -0.0, 0])
        C0pointText.next_to(C0point1, DOWN)
        self.add(C0pointText)
        # self.play(
        #     ShowCreation(far_line),
        # )


        # 我们从压缩前的棱台观察体中随机取一个点$A(x,y,z)$,将它与相机连线，与近平面相交于$C(x',y',-n)$这个点上
        # 画点A
        pointA = Dot(axes.c2p(z, y), color=BLUE)
        self.play(ShowCreation(pointA), run_time=0.1)
        # ApointText = Text("A(x,y,z)", font_size=20)
        ApointText = Text("A(z,y)", font_size=20)
        ApointText.next_to(pointA, RIGHT)
        # ApointText.rotate(PI / 2, axis=RIGHT)
        self.add(ApointText)

        # 连接原点和点A（7, 2）,画出与相机连线，且画出与近平面相交的点C
        #记录线段
        LineAC = Line(axes.c2p(0, 0), pointA,color=BLUE)
        self.play(ShowCreation(LineAC), run_time=0.1)
        # lineAC虚线
        LineAC1 = DashedLine(axes.c2p(0, 0), pointA, color=BLUE)
        self.play(ShowCreation(LineAC1), run_time=0.1)

        pointC = Dot(axes.c2p(n, y1), color=RED)
        self.play(ShowCreation(pointC), run_time=0.1)
        # CpointText = Text("C(x',y',-n)", font_size=20)
        CpointText = Text("C(-n,y')", font_size=20)
        # CpointText.next_to(pointC, UP)
        #Text改为在他的左上方
        pointCLeftUp = pointC.get_center() + np.array([-0.0, 0.2, 0])
        CpointText.next_to(pointCLeftUp,LEFT)

        # CpointText.rotate(PI / 2, axis=RIGHT)
        self.add(CpointText)

        # 压缩-------------------------------------
        # 开始压缩 从透视投影压缩到正交投影

        # lineLenttai变为平行于坐标轴的线段
        lineLentTaiNEW = Line(axes.c2p(0, 2), axes.c2p(8, 2), color=WHITE)
        # self.play(ReplacementTransform(LineLengTai, lineLentTaiNEW), run_time=0.6)

        # 将线段AC压缩，将其变为平行于坐标轴的线段，即旋转为与z轴平行
        lineACNEW = Line(axes.c2p(0, y1), axes.c2p(z1, y1),color=RED)
        # 将线段AC压缩，将其变为平行于坐标轴的线段，即旋转为lineACNEW
        # self.play(ReplacementTransform(LineAC, lineACNEW), run_time=0.6)


        # animation_list.append(ReplacementTransform(farLine, lineLenTaiFarNew))
        animation_list.append(ReplacementTransform(LineLengTai, lineLentTaiNEW))
        animation_list.append(DotFar.animate.move_to(axes.c2p(far, n / far * 4)))

        for i in range(len(points)):
            animation_list.append(pointDots[i].animate.move_to(axes.c2p(perspect_points[i][0], perspect_points[i][1])))


        animation_list.append(ReplacementTransform(LineAC, lineACNEW))

        self.play(AnimationGroup(*animation_list), run_time=2)


        # 移动points点


        # 因此点A压缩后对应的点$B(x',y',z')$的$x'$与$y'$与C是一致的。
        # 画点B
        self.play(ShowCreation(Dot(axes.c2p(z1, y1), color=BLUE)), run_time=0.1)
        # BpointText = Text("B(x',y',z')", font_size=20)
        BpointText = Text("B(z',y')", font_size=20)
        BpointText.next_to(axes.c2p(z1, y1), RIGHT)
        # BpointText.rotate(PI / 2, axis=RIGHT)
        self.add(BpointText)


        # 压缩结束-------------------------------------




        v_line = always_redraw(lambda: axes.get_v_line(pointA.get_bottom()))
        self.play(
            ShowCreation(v_line),
            run_time=0.1,
        )

        # self.play(LineAC.animate.rotate(PI / 2, axis=RIGHT), run_time=0.6)
        # self.play(LineAC.animate.move_to(axes.c2p(0, 8/7), axes.c2p(4, 8/7)), run_time=0.6)



        # 画Z，0
        A0point = Dot(axes.c2p(z, 0), color=BLUE)
        self.play(ShowCreation(A0point), run_time=0.1)
        #文字
        A0pointText = Text("z", font_size=20)
        A0pointText.next_to(A0point,DOWN)
        self.add(A0pointText)


        # 绘制O C C0 三角形
        Opoint = Dot(axes.c2p(0, 0), color=WHITE)
        TriangleOCC0 = Polygon(axes.c2p(0, 0), axes.c2p(n, 0), axes.c2p(n, y1), color=WHITE, fill_color=BLUE, fill_opacity=0.5)
        # TriangleOCC0 = Polygon(Opoint.__doc__, C0point.__doc__, pointC.__doc__, color=WHITE, fill_color=BLUE, fill_opacity=0.5)
        self.play(ShowCreation(TriangleOCC0), run_time=0.1)

        # 绘制O A A0 三角形
        # TriangleOAA0 = Polygon(Opoint, A0point, pointA, color=WHITE, fill_color=BLUE_C, fill_opacity=0.5)
        TriangleOAA0 = Polygon(axes.c2p(0, 0), axes.c2p(z, 0), axes.c2p(z, y), color=WHITE, fill_color=BLUE_C, fill_opacity=0.5)
        self.play(ShowCreation(TriangleOAA0), run_time=0.1)


        # y^\prime = -\frac{n}{z}y 写出 y’ / y = -n / z  ，用latex格式
        # ybili = Text(r"\frac{y'}{y} = -\frac{n}{z}", font_size=20, color=WHITE, t2c={"y": RED, "n": GREEN, "z": BLUE})
        ybili = Tex("\\frac{y'}{y} = \\frac{-n}{z}", font_size=30, color=WHITE)
        # ybili = Text("y’ / y = -n / z", font_size=20)
        ybili.next_to(axes.c2p(3, 5), DOWN)
        self.add(ybili)

        ybili2 = Tex("y' = -\\frac{ny}{z}", font_size=30, color=WHITE)
        ybili2.next_to(axes.c2p(3, 4), DOWN)
        self.add(ybili2)

        # ybili = MathTex(r"\frac{y'}{y} = -\frac{n}{z}")

        # 导出gif
        # equation = MathTex(
        #     r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots"
        # )
        # equation.set_color_by_tex("x", YELLOW)
        # self.add(equation)



        return

        dot.move_to(axes.c2p(4, 2))
        self.play(FadeIn(dot, scale=0.5))


        return
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        # 同样，你可以调用Axes.point_to_coords（缩写Axes.p2c）
        # print(axes.p2c(dot.get_center()))

        # 我们可以从轴上画线，以便更好地标记给定点的坐标在这里
        # always_redraw命令意味着在每一个新帧上重新绘制线来保证线始终跟随着点移动
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        # 如果我们把这个点固定在一个特定的坐标上，当我们移动轴时，它也会跟随坐标系移动
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))

        # manim还有一些其它的坐标系统：ThreeDAxes，NumberPlane，ComplexPlane