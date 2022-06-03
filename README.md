# CS 221 Project

# Organization of Codebase
The codebase consists of three main elements:

## Primary Data Source acquisition
The Jupyter Notebook entitled `cs221_project_dataset_creation.ipynb` contains the code to extract data from the BRENDA database as well as from PubChem (for compounds) and UniProt (for proteins) using their metered APIs. These separate data sources are collected and joined together in this notebook.

## Secondary Analysis
The Jupyter Notebook entitled `cs221_project_secondary_analysis.ipynb` contains the code to profile the sparsity of the source data and to create distance matrices for chemical and enzymatic entities. This notebook also includes the code used to calculate the MAPK evaluation metric.

## Search Application Code
all code for the search application itself is contained within the `flask_app` directory. Specific instructions as to how to build and run the Docker container are below.

# Running the Search App
The application can be run using a Docker container which can be built using the Dockerfile contained in this repo. To build the container, run:

`docker build . -t enzyme-search`

And then to run the application itself, run:

`docker run -p 5445:5445 enzyme-search`

And then navigate in your browser to http://0.0.0.0:5445
