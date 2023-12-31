# pydraulics

pydraulics is a Python package designed to facilitate hydraulic calculations and analysis. It provides a range of functionalities for open channel flow and pipe flow calculations.

## Features

### Open Channel Flow
- Depth Calculation: Estimate the depth of flow in open channels based on input parameters such as flow rate, channel geometry, and Manning's roughness coefficient.
- Flow Calculation: Determine the flow rate in open channels using various methods by using Manning's equation.
- Critical Flow and Critical Slope Calculation: Calculate the critical flow rate and critical slope in open channels to determine the specific conditions at which flow transitions occur.

### Pipe Flow
- Losses Calculation: Calculate the friction losses and other energy losses in pipes for different flow conditions and material roughness.
- Reynolds Number and Darcy Coefficient: Utilize a third-party package to calculate the Reynolds number and Darcy coefficient, providing valuable information about the flow regime and the hydraulic resistance of the pipe.

## Installation

To install pydraulics, you can use pip, the Python package manager. Simply run the following command:

```
pip install pydraulics
```

## Getting Started

Here's an example of how to use pydraulics for open channel and pipe flow calculations:

```python
from open_flow import TrapezoidalChannel, TriangularChannel, CircularChannel, RectangularChannel
from pipe_flow import Pipe

# Calculate friction losses in a pipe

#Example with Darcy (default)
pipe1 = Pipe(Q=10, D=0.2, e=0.005, L=100)
print(pipe1.__dict__)
#Example with azen-Williams
pipe2 = Pipe(Q=1, D=0.9, L=100, method='Hazen-Williams', C=140)
print(pipe2.__dict__)

# Calculate depth in an open channel
print(RectangularChannel(b=2, n=0.0013, So=0.0075, Q = 3.5).__dict__)
print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, Q = 3.5, z=1.5).__dict__)
print(CircularChannel(D=1, n=0.013, So=0.0075, Q = 2.1).__dict__)
print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, Q = 3.5).__dict__)

# Calculate flow rate in an open channel using Manning's equation
print(RectangularChannel(b=2, n=0.0013, So=0.0075, y = .1177).__dict__)
print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, y = 0.426, z=1.5).__dict__)
print(CircularChannel(D=1, n=0.0013, So=0.0075, y = 0.2777).__dict__)
print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, y = 0.354).__dict__)
```


## Contributing

Contributions to pydraulics are welcome! If you have any ideas, bug fixes, or new features, feel free to open an issue or submit a pull request on GitHub.

## License

pydraulics is licensed under the MIT License. See the [LICENSE](https://github.com/your-username/pydraulics/blob/main/LICENSE) file for more information.

We hope pydraulics proves to be a valuable tool for your hydraulic analysis and calculations. Happy coding!