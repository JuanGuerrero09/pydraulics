from pydraulics.open_flow import RectangularChannel, TrapezoidalChannel, TriangularChannel, CircularChannel
from math import isclose
# from pydraulics.pipe_flow import Pipe

Q = 1.5
n = 0.013
b = 2
So = 0.0075
z = 1.5
D = 3
y = 0.5

rectangular_channel = RectangularChannel(n=n, So=So,  b=b, Q=Q)
circular_channel = CircularChannel(n=n, So=So,  D=D, Q=Q)
trapezoidal_channel = TrapezoidalChannel(n=n, So=So,  b=b, Q=Q, z=z)
triangular_channel = TriangularChannel(n=n, So=So,  z=z, Q=Q)

print(RectangularChannel(Q=3, n=0.013, So=0.0075, b=2).__dict__)

# class TestRectangular:
#     def calc_flow(self):
#         self.rectangular_channel = RectangularChannel(Q=3, n=0.013, So=0.0075, b=2)
#         assert self.rectangular_chanel.yc == 0.61

def test_flow_rectangular():
    yc = round(rectangular_channel.yc, 2)
    Sc = round(rectangular_channel.Sc, 4)
    y = round(rectangular_channel.y, 2)
    assert isclose(yc, 0.39, rel_tol=1e-3)
    assert isclose(Sc, 0.0035, rel_tol=1e-3)
    assert isclose(y, 0.3, rel_tol=1e-3)

def test_flow_circular():
    yc = round(circular_channel.yc, 2)
    Sc = round(circular_channel.Sc, 4)
    y = round(circular_channel.y, 2)
    assert isclose(yc, 0.39, rel_tol=1e-3)
    assert isclose(Sc, 0.0035, rel_tol=1e-3)
    assert isclose(y, 0.3, rel_tol=1e-3)

def test_flow_trapezoidal():
    yc = round(trapezoidal_channel.yc, 2)
    Sc = round(trapezoidal_channel.Sc, 4)
    y = round(trapezoidal_channel.y, 2)
    assert isclose(yc, 0.39, rel_tol=1e-3)
    assert isclose(Sc, 0.0035, rel_tol=1e-3)
    assert isclose(y, 0.3, rel_tol=1e-3)

def test_flow_triangular():
    yc = round(triangular_channel.yc, 2)
    Sc = round(triangular_channel.Sc, 4)
    y = round(triangular_channel.y, 2)
    assert isclose(yc, 0.39, rel_tol=1e-3)
    assert isclose(Sc, 0.0035, rel_tol=1e-3)
    assert isclose(y, 0.3, rel_tol=1e-3)


test_flow_rectangular()

