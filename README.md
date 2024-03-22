# akvmodel: A Python Tool for Social Network Simulations in the Alvim-Knight-Valencia Model

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10695209.svg)](https://doi.org/10.5281/zenodo.10695209)

Formal models for social networks aim to capture the crucial aspects of the evolution of agents' beliefs over time, as communication occurs in a network. The Alvim-Knight-Valencia (AKV) social network model (2019) works on the dynamics of belief updates using a quantitative spectrum of belief values, and an influence graph representing the relationships between agents. Previous work on the AKV model developed belief update functions representing a range of belief update methods.

This package implements the AKV model and a catalog of its belief updates, initial configurations, and update functions from the literature, creating a general tool that incorporates a wide range of possible approaches to belief updates. In addition, we allow the AKV model to have multiple outcomes (or truth values) for the proposition used in the model. This tool facilitates future research using the AKV model without the need to reimplement it also allowing its reproducibility.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install akvmodel.

```bash
pip install akvmodel
```

## Usage

The full reference of the package can be found in `DOCUMENTATION.md`.

```python
import numpy as np
from akvmodel import *

# Create model with 10 agents, mildly polarized initial configuration, faintly communicating influence graph, and confirmation bias belief update.
akvmodel = AKV(
    belief_state=InitialConfigurations.mildly(10),
    influence_graph=InfluenceGraphs.faintly(10),
    update_function=UpdateFunctions.confirmation_bias,
)

# Update the model 100 times
for _ in range(100):
    akvmodel.update()

# Get polarization
p = akvmodel.get_polarization()

# Plot polarization evolution for the first outcome in the domain
plt.plot(p[0])
```

Full example can be found in the Jupyter Notebook `example.ipynb`.

## Trying the package with Docker

This project includes a `Dockerfile` that builds an image with Jupyter
Notebook and necessary requirements to run the example.

Build the image:
```bash
docker build -t akvmodel-test .
```

Run the image:`
```bash
docker run -p 8888:8888 akvmodel-test
```

Open `localhost:8888` on your browser, use the password `test` and open the file
`example.ipynb`. Changes on `example.ipynb` will not be saved.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)