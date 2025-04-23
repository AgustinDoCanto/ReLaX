FROM python:3.11-slim

# Instalar LaTeX y utilidades
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    git \
    make \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Clonar el framework ReLaX dentro del contenedor
RUN git clone https://github.com/AgustinDoCanto/ReLaX.git /relax-framework

# Instalar ReLaX como CLI de Python
RUN pip install --no-cache-dir -e /relax-framework

# El contenedor trabajará directamente sobre esta ruta
WORKDIR /relax-docker

# Comando por defecto
CMD ["/bin/bash"]
