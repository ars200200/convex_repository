#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, "draw", void_draw)
setattr(Point, "draw", point_draw)
setattr(Segment, "draw", segment_draw)
setattr(Polygon, "draw", polygon_draw)


tk = TkDrawer()

tk.clean()

print("Введите координаты первой точки треугольника  ")
a = R2Point()
print("Введите координаты второй точки треугольника  ")
b = R2Point()
print("Введите координаты третьей точки треугольника  ")
c = R2Point()
print("________________________________________________\n\n")

if R2Point.area(a, b, c) == 0:
    print("Ошибка: введнные точки лежат на одной прямой")
else:
    if R2Point.area(a, b, c) < 0:
        a, b = b, a
    Figure.tr = [a, b, c]
    f = Void(1)
    try:
        while True:
            tk.draw_line2(a, b)
            tk.draw_line2(b, c)
            tk.draw_line2(a, c)
            f = f.add(R2Point())
            tk.clean()
            f.draw(tk)
            ttt = f._intersection
            print(
                f"S = {f.area()}, P = {f.perimeter()}, C = {ttt}\n"
            )
    except (EOFError, KeyboardInterrupt):
        print("\nStop")
        tk.close()
