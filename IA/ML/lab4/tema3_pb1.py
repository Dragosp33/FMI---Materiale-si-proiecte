def dete(a):
    x = (a[0][0] * a[1][1] * a[2][2]) + (a[1][0] * a[2][1] * a[0][2]) + (a[2][0] * a[0][1] * a[1][2])
    y = (a[0][2] * a[1][1] * a[2][0]) + (a[1][2] * a[2][1] * a[0][0]) + (a[2][2] * a[0][1] * a[1][0])
    return x - y


def getMatrixMinor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def getMatrixDeterminant(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * getMatrixDeterminant(getMatrixMinor(m, 0, c))
    return determinant


eps = 1e-12


def testeaza_viraj(P, Q, R):
    a = [[1, 1, 1],
         [P[0], Q[0], R[0]],
         [P[1], Q[1], R[1]]]

    det_a = dete(a)

    if det_a == 0:
        return "pe dreapta"
    elif det_a < 0:
        return "viraj dreapta"
    return "viraj stanga"


def th(x_a, y_a, x_b, y_b, x_c, y_c, x_d, y_d):
    theta = [[x_a, y_a, x_a * x_a + y_a * y_a, 1],
             [x_b, y_b, x_b * x_b + y_b * y_b, 1],
             [x_c, y_c, x_c * x_c + y_c * y_c, 1],
             [x_d, y_d, x_d * x_d + y_d * y_d, 1]]

    res = getMatrixDeterminant(theta)
    if -eps <= res <= eps:
        return 0
    else:
        return res


# citire
x_a, y_a = map(int, input().split())
x_b, y_b = map(int, input().split())
x_c, y_c = map(int, input().split())
x_d, y_d = map(int, input().split())



semn = 1

if not testeaza_viraj((x_a,y_a), (x_b,y_b), (x_c,y_c)) == "viraj stanga":
    semn = -1


res = th(x_a,y_a,x_b,y_b,x_c,y_c,x_d,y_d) * semn
print(res)
if  res > 0:
    print("inauntru")
elif res == 0:
    print("pe cerc")
else:
    print("in afara")