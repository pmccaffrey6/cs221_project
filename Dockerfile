FROM conda/miniconda3

RUN apt-get update \
  && apt-get install -y make automake gcc g++ gfortran libblas3 liblapack3 liblapack-dev libblas-dev \
  && pip install pandas flask scipy \
  && conda install -y -c conda-forge rdkit deepchem==2.6.1 \

COPY /flask_app /

ENTRYPOINT python3 /app.py
