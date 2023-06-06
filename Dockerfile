FROM python:3.11.3-slim

# Copy your Django project files
COPY ./django/ /app/

WORKDIR /app

# os-level installs
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    libpq-dev \
    gcc \
    make \
    nginx

# venv & installs
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r /app/requirements.txt

# purge unused
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x ./config/entrypoint.sh
CMD ["./config/entrypoint.sh"]