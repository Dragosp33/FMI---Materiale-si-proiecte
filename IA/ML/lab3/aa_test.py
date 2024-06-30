import math
import numpy as np
def input_int(out):
    while True:
        try:
            return int(input(out))
        except Exception:
            print("Input invalid")

def zeros_matrix(rows, cols):

    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M

def copy_matrix(M):

    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC


def dete(a):
   x = (a[0][0] * a[1][1] * a[2][2]) + (a[1][0] * a[2][1] * a[0][2]) + (a[2][0] * a[0][1] * a[1][2])
   y = (a[0][2] * a[1][1] * a[2][0]) + (a[1][2] * a[2][1] * a[0][0]) + (a[2][2] * a[0][1] * a[1][0])
   return x - y

class Point:
    def __init__(self, x: float = None, y: float = None):
        self.x = x
        self.y = y

    def dist(self, point) -> float:
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def center(self, point):
        return Point((self.x + point.x) / 2, (self.y + point.y) / 2)

    def slope(self, point):
        if point.x - self.x == 0:
            return 1e9
        return (point.y - self.y) / (point.x - self.x)

    def extract(self, axis: str):
        if axis == 'x':
            return self.x
        return self.y

    @classmethod
    def read(cls, name="P"):
        print(f"Punctul {name}")
        x = input_int("x = ")
        y = input_int("y = ")
        return cls(x, y)


    @staticmethod
    def compute_turn(p, q, r):
        delta = [[1, 1, 1], [p.x, q.x, r.x], [p.y, q.y, r.y]]

        det = dete(delta)
        if det < 0:
            return -1
        if det > 0:
            return 1
        return 0

    @staticmethod
    def on_segment(p, q, r):
        if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
                (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    def __str__(self):
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"

    def __repr__(self):
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"


class Polygon:
    def __init__(self, edges: [Point]):
        self.size = len(edges)
        self.edges = edges

    @classmethod
    def read(cls):
        n = input_int("n = ")
        points = []
        for i in range(n):
            points.append(Point.read(str(i)))
        return cls(points)

    def __str__(self):
        return f"Polygon({', '.join([str(point) for point in self.edges])})"

    def __repr__(self):
        return f"Polygon({', '.join([str(point) for point in self.edges])})"


class Line:
    def __init__(self, A: Point, B: Point):
        self.A = A
        self.B = B

    def dist(self) -> float:
        return self.A.dist(self.B)

    def center(self) -> Point:
        return self.A.center(self.B)

    def slope(self):
        return self.A.slope(self.B)

    def intersect(self, line) -> bool:
        slope1 = self.slope()
        slope2 = line.slope()

        if slope1 == slope2:
            return False

        t1 = Point.compute_turn(self.A, self.B, line.A)
        t2 = Point.compute_turn(self.A, self.B, line.B)
        t3 = Point.compute_turn(line.A, line.B, self.A)
        t4 = Point.compute_turn(line.A, line.B, self.B)

        if (t1 != t2) and (t3 != t4):
            return True
        if (t1 == 0) and Point.on_segment(self.A, line.A, self.B):
            return True
        if (t2 == 0) and Point.on_segment(self.A, line.B, self.B):
            return True
        if (t3 == 0) and Point.on_segment(line.A, self.A, line.B):
            return True
        if (t4 == 0) and Point.on_segment(line.A, self.B, line.B):
            return True

        return False

    def __str__(self):
        return f"Line({self.A}, {self.B})"


def check_position(polygon: Polygon, start: Point):
    end = Point(999999, 9999999)
    intersections = 0

    for i in range(polygon.size):
        p1 = polygon.edges[i]
        p2 = polygon.edges[(i + 1) % polygon.size]
        if Point.compute_turn(p1, p2, start) == 0:
            return 0
        if Line(p1, p2).intersect(Line(start, end)):
            intersections += 1

    if intersections % 2 == 0:
        return -1
    return 1



n = int(input())


puncte = []

for i in range(n):
    list1 = [int(x) for x in input().split(" ")]
    (x, y) = (list1[0], list1[1])
    puncte.append(Point(x, y))



polygon = Polygon(puncte)


puncte2 = []
m = int(input())
for i in range(m):
    list1 = [int(x) for x in input().split(" ")]
    (x, y) = (list1[0], list1[1])
    puncte2.append(Point(x, y))

for i in puncte2:
    pos = check_position(polygon, i)
    if pos == 1:
        print("INSIDE")

    elif pos == -1:
        print("OUTSIDE")
    else:
        print("BOUNDARY")