FROM python:3.10

RUN apt update && apt install -y \
    sudo \
    ffmpeg \
    libzmq3-dev

RUN pip3 install \
    Flask \
    pyzmq \
    uwsgi \
    openai

# add sudo user
RUN groupadd -g 1000 developer && \
    useradd  -g      developer -G sudo -m -s /bin/bash nomura && \
    echo 'nomura:robo2006' | chpasswd
RUN echo 'Defaults visiblepw'             >> /etc/sudoers
RUN echo 'nomura ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER nomura
WORKDIR /home/nomura
