
# Use offical python image
FROM python:3.11-bullseye AS base

LABEL org.opencontainers.image.authors="DMOrigin"
LABEL version="0.1"
LABEL description="Aquire data from a GoodWe Inverter and stores it to an influxdb."

# Install external libraries
RUN pip install goodwe
RUN pip install influxdb-client

# expose volume
VOLUME [ "/data" ]

# copy python data
ADD ./src/* /ipvgather/
ADD ./src/conf.docker.json /data/config.json

#ENTRYPOINT [ "python", "/ipvgather/ipvgather.py", "-c /etc/ipvgather.json", "--check" ]
ENTRYPOINT [ "python", "/ipvgather/test.py" ]
