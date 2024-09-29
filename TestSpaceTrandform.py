


import numpy as np

from manimlib import *
from scipy.stats import qmc


class CoordinateSystemExample(Scene):
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

        # 定义n=4
        n = 4.0
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
        self.play(ShowCreation(Line(axes.c2p(4, -2), axes.c2p(4, 2))), run_time=0.1)

        # 棱台start-------------------------------------

        # 这是远平面
        # self.play(ShowCreation(DashedLine(axes.c2p(5, -2), axes.c2p(5, 3))))
        self.play(ShowCreation(Line(axes.c2p(8, -2), axes.c2p(8, 4))), run_time=0.1)

        #画点M（8, 3）
        self.play(ShowCreation(Dot(axes.c2p(8, 4), color=WHITE)), run_time=0.1)
        # 连接原点和点M（8, 3）
        LineLengTai = Line(axes.c2p(0, 0), axes.c2p(8, 4), color=WHITE)
        self.play(ShowCreation(LineLengTai), run_time=0.1)
        # 棱台END-------------------------------------


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

        # 两个线段一起压缩
        self.play(
            ReplacementTransform(LineLengTai, lineLentTaiNEW),
            ReplacementTransform(LineAC, lineACNEW),
            run_time=0.6
        )

        # 因此点A压缩后对应的点$B(x',y',z')$的$x'$与$y'$与C是一致的。
        # 画点B
        self.play(ShowCreation(Dot(axes.c2p(z1, y1), color=BLUE)), run_time=0.1)
        # BpointText = Text("B(x',y',z')", font_size=20)
        BpointText = Text("B(z',y')", font_size=20)
        BpointText.next_to(axes.c2p(z1, y1), RIGHT)
        # BpointText.rotate(PI / 2, axis=RIGHT)
        self.add(BpointText)


        # 压缩结束-------------------------------------

        # 画底下的点
        C0point = Dot(axes.c2p(n, 0), color=RED)
        self.play(ShowCreation(C0point), run_time=0.1)
        # 文字
        C0pointText = Text("-n", font_size=20)
        C0point1 = C0point.get_center() + np.array([-0.2, -0.0, 0])
        C0pointText.next_to(C0point1, DOWN)
        self.add(C0pointText)


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
        ybili.next_to(axes.c2p(4, 4), DOWN)
        self.add(ybili)

        ybili2 = Tex("y' = -\\frac{ny}{z}", font_size=30, color=WHITE)
        ybili2.next_to(axes.c2p(4, 3), DOWN)
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