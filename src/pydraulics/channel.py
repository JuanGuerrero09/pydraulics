# pydraulics/channel.py
from __future__ import annotations

from typing import Protocol, runtime_checkable
from .utils.manning import manning_Q  

@runtime_checkable
class Section(Protocol):
    """Minimal interface for a channel cross-section."""
    def area(self, y: float) -> float: ...
    def wetted_perimeter(self, y: float) -> float: ...
    def top_width(self, y: float) -> float: ...

class Rectangular:
    """Rectangular section with bottom width b."""
    def __init__(self, b: float) -> None:
        if b <= 0:
            raise ValueError("b must be > 0.")
        self.b = b

    def area(self, y: float) -> float:
        return self.b * y

    def wetted_perimeter(self, y: float) -> float:
        # For y == 0, this returns b. Caller should avoid y <= 0 for hydraulics.
        return self.b + 2.0 * y

    def top_width(self, y: float) -> float:
        return self.b

class Channel:
    """
    Channel with Manning roughness n and slope So.
    Can work with or without a Section:
      - If section is provided, you can compute Q from a depth y.
      - If not, you can compute Q from A and Rh directly.
    """
    def __init__(self, n: float, So: float, section: Section | None = None) -> None:
        if n <= 0:
            raise ValueError("n must be > 0.")
        if So < 0:
            raise ValueError("So cannot be negative.")
        self.n = n
        self.So = So
        self.section = section

    @property
    def has_section(self) -> bool:
        return self.section is not None

    def calc_manning(self, *,
                     y: float | None = None,
                     A: float | None = None,
                     Rh: float | None = None) -> float:
        """
        Compute discharge via Manning.
        Modes:
          1) If section and y are provided: derive A, Rh and compute Q.
          2) If A and Rh are provided: compute Q directly.
        Raises:
          ValueError if inputs are invalid or insufficient.
        """
        # Mode 1: with section + y
        if self.section is not None and y is not None:
            if y <= 0:
                raise ValueError("y must be > 0.")
            A_ = self.section.area(y)
            P_ = self.section.wetted_perimeter(y)
            if P_ <= 0:
                raise ValueError("Wetted perimeter must be > 0.")
            Rh_ = A_ / P_
            return manning_Q(A_, Rh_, self.So, self.n)

        # Mode 2: direct A and Rh
        if A is not None and Rh is not None:
            if A <= 0 or Rh <= 0:
                raise ValueError("A and Rh must be > 0.")
            return manning_Q(A, Rh, self.So, self.n)

        raise ValueError("Provide either (section + y) or (A and Rh).")

    def hydraulics_at(self, y: float) -> dict[str, float]:
        """
        Return A, P, Rh, Q at a given depth y using the section.
        """
        if self.section is None:
            raise ValueError("No section is set on this Channel.")
        if y <= 0:
            raise ValueError("y must be > 0.")

        A = self.section.area(y)
        P = self.section.wetted_perimeter(y)
        if P <= 0:
            raise ValueError("Wetted perimeter must be > 0.")
        Rh = A / P
        Q = manning_Q(A, Rh, self.So, self.n)
        return {"A": A, "P": P, "Rh": Rh, "Q": Q}
