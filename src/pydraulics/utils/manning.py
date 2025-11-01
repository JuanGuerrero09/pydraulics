from typing import overload, Literal, Final

K_SI: Final[float] = 1.0
K_IP: Final[float] = 1.49

@overload
def manning(*, A: float, Rh: float, S: float, n: float, k: float = K_SI, solve_for: Literal["Q"] = "Q") -> float: ...
@overload
def manning(*, Q: float, A: float, Rh: float, n: float, k: float = K_SI, solve_for: Literal["S"]) -> float: ...
@overload
def manning(*, Q: float, A: float, Rh: float, S: float, k: float = K_SI, solve_for: Literal["n"]) -> float: ...

def manning(*,
            A: float | None = None,
            Rh: float | None = None,
            S: float | None = None,
            n: float | None = None,
            Q: float | None = None,
            k: float = K_SI,
            solve_for: Literal["Q", "S", "n"] = "Q") -> float:

    if k <= 0:
        raise ValueError("k must be > 0.")

    if solve_for == "Q":
        if A is None or Rh is None or S is None or n is None:
            raise ValueError("Provide A, Rh, S and n to solve for Q.")
        if A <= 0 or Rh <= 0 or n <= 0 or S < 0:
            raise ValueError("Invalid parameters: A, Rh, n > 0 and S >= 0.")
        A_, Rh_, S_, n_ = A, Rh, S, n
        return k / n_ * A_ * (Rh_ ** (2/3)) * (S_ ** 0.5)

    elif solve_for == "S":
        if Q is None or A is None or Rh is None or n is None:
            raise ValueError("Provide Q, A, Rh and n to solve for S.")
        if Q <= 0 or A <= 0 or Rh <= 0 or n <= 0:
            raise ValueError("Invalid parameters: Q, A, Rh, n must be > 0.")
        Q_, A_, Rh_, n_ = Q, A, Rh, n
        return (Q_ * n_ / (k * A_ * (Rh_ ** (2/3)))) ** 2

    elif solve_for == "n":
        if Q is None or A is None or Rh is None or S is None:
            raise ValueError("Provide Q, A, Rh and S to solve for n.")
        if Q <= 0 or A <= 0 or Rh <= 0 or S < 0:
            raise ValueError("Invalid parameters: Q, A, Rh > 0 and S >= 0.")
        Q_, A_, Rh_, S_ = Q, A, Rh, S
        return k * A_ * (Rh_ ** (2/3)) * (S_ ** 0.5) / Q_

    else:
        raise ValueError("solve_for must be 'Q', 'S', or 'n'.")

# Optional: keep the simple helpers delegating to the unified API
def manning_Q(A: float, Rh: float, S: float, n: float, k: float = K_SI) -> float:
    return manning(A=A, Rh=Rh, S=S, n=n, k=k, solve_for="Q")

def manning_n(Q: float, A: float, Rh: float, S: float, k: float = K_SI) -> float:
    return manning(Q=Q, A=A, Rh=Rh, S=S, k=k, solve_for="n")
