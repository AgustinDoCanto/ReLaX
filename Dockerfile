FROM python:3.11-bookworm

# Evitá interacciones
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-lang-english \
    texlive-lang-spanish \
    git make \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

 # Clonar ReLaX
RUN git clone https://github.com/AgustinDoCanto/ReLaX.git /relax-framework

# Instalar ReLaX como CLI
RUN pip3 install --no-cache-dir -e /relax-framework

# Ruta de trabajo
WORKDIR /relax-docker

CMD ["/bin/bash"]