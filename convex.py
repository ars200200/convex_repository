from deq import Deq
from r2point import R2Point


class Figure:
    """Абстрактная фигура"""

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    # Площадь пересечения двух треугольников
    @staticmethod
    def intersects(a, b=None):
        if b is not None:
            c = []
            for i in range(3):
                flag = 1
                for j in range(3):
                    inter = R2Point.intersect(
                        a[i], a[(i + 1) % 3], b[j], b[(j + 1) % 3]
                    )
                    if R2Point.area(b[j], b[(j + 1) % 3], a[i]) <= 0:
                        flag = 0
                    if inter is not None:
                        c.append(inter)
                if flag:
                    c.append(a[i])
            f = Void(0)
            square = 0
            for i in range(len(c)):
                f = f.add(c[i])
            if isinstance(f, Polygon):
                for i in range(len(f.points.array) - 2):
                    square += abs(
                        R2Point.area(
                            f.points.array[i],
                            f.points.array[i + 1],
                            f.points.array[i + 2],
                        )
                    )
            return square

        else:
            pass

    def intersection_square(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, flag):
        self.flag = flag
        self._intersection = 0.0

    def add(self, p):
        return Point(p, self.flag)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, flag):
        self.p = p
        self.flag = flag
        self._intersection = 0.0

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.flag)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, flag):
        self.p, self.q = p, q
        self.flag = flag
        self._intersection = 0.0

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.flag)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r, self.flag)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.flag)
        else:
            return self


class Polygon(Figure):
    """Многоугольник"""

    def __init__(self, a, b, c, flag):
        self.points = Deq()
        self.flag = flag
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        if flag:
            zz = [self.points.array[0], self.points.array[1]]
            zzz = [self.points.array[2]]
            self._intersection = Figure.intersects(Figure.tr, zz + zzz)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            ppp = self.points.first()
            self._area += abs(R2Point.area(t, self.points.last(), ppp))
            if self.flag:
                self._intersection += Figure.intersects(
                    Figure.tr, [t, self.points.first(), self.points.last()]
                )

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if self.flag:
                    self._intersection += Figure.intersects(
                        Figure.tr, [t, self.points.first(), p]
                    )

                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if self.flag:
                    self._intersection += Figure.intersects(
                        Figure.tr, [t, p, self.points.last()]
                    )
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            xx = t.dist(self.points.last())
            self._perimeter += t.dist(self.points.first()) + xx
            self.points.push_first(t)

        return self
