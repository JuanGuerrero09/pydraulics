from pydraulics import Channel, Rectangular
from pydraulics.utils import manning_Q

def main() -> None:
    print("Hello from pydraulics!")

    # Pure function (utils)
    Q = manning_Q(A=8.0, Rh=1.1, S=0.002, n=0.013)
    print("Q (utils):", Q)

    # Channel without section (pass A and Rh)
    ch = Channel(n=0.013, So=0.002)
    Q2 = ch.calc_manning(A=8.0, Rh=1.1)
    print("Q (channel no section):", Q2)

    # Channel with section (pass depth y)
    rect = Rectangular(b=3.0)
    ch2 = Channel(n=0.013, So=0.002, section=rect)
    # res = ch2.hidraulics_at(y=1.2)  # ← ojo, typo intencional para mostrar error
    # Debe ser: ch2.hydraulics_at(y=1.2)
    Q3 = ch2.calc_manning(y=1.2)
    print("hydraulics:", ch2.hydraulics_at(y=1.2))
    print("Q (channel with section):", Q3)

if __name__ == "__main__":
    main()
