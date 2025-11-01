import math
from pydraulics.utils import manning_Q, manning_n
from pydraulics.utils.manning import manning


def test_manning_Q_roundtrip_with_n():
    # Given
    A, Rh, S = 8.0, 1.1, 0.002
    n = 0.013

    # When
    Q = manning_Q(A=A, Rh=Rh, S=S, n=n)
    n_back = manning_n(Q=Q, A=A, Rh=Rh, S=S)

    # Then
    assert math.isclose(n, n_back, rel_tol=1e-12)

def test_manning_Q_invalid_params():
    A, Rh, S, n = 8.0, 1.1, 0.002, 0.013
    # S < 0
    try:
        manning_Q(A, Rh, -0.1, n)
        assert False, "Expected ValueError for negative S"
    except ValueError:
        pass

    # n <= 0
    try:
        manning_Q(A, Rh, S, 0.0)
        assert False, "Expected ValueError for zero n"
    except ValueError:
        pass

def test_manning_unified_modes():
    A, Rh, S, n = 8.0, 1.1, 0.002, 0.013
    Q = manning(A=A, Rh=Rh, S=S, n=n, solve_for="Q")
    S_back = manning(Q=Q, A=A, Rh=Rh, n=n, solve_for="S")
    n_back = manning(Q=Q, A=A, Rh=Rh, S=S, solve_for="n")
    assert abs(S - S_back) / S < 1e-12
    assert abs(n - n_back) / n < 1e-12