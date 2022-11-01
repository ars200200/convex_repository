#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void, Figure

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
            f = f.add(R2Point())
            fff = f._intersection
            print(f"S = {f.area()}, P = {f.perimeter()}, C = {fff}")
    except (EOFError, KeyboardInterrupt):
        print("\nStop")
