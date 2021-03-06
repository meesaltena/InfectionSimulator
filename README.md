# InfectionSimulator
Python implementation of a simple model for simulating the spread of an infectious disease. Shows a graph of an SIR-model of the disease.

Uses [John Zelles graphics.py package](https://pypi.org/project/graphics.py/) to visualise every person as a circle that randomly moves around.
Uses [Matplotlib](https://matplotlib.org/) to generate a graph containing information about the spread of the disease.

When an susceptible person gets within the 'sphere of influence' of an infected person, they get infected.

![Demo gif](demo.gif)
