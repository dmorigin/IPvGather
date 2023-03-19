
# Use offical python image
FROM python:3.11-bullseye AS base

LABEL org.opencontainers.image.authors="DMOrigin"
LABEL version="0.1"
LABEL description="Aquire data from a GoodWe Inverter and stores it into influxdb."

# Install external libraries
RUN pip install goodwe=0.2.20
RUN pip install influxdb-client=1.36.1

# expose volume
VOLUME [ "/data" ]

# copy python data
ADD ./src/* /ipvgather/
ADD ./src/conf.docker.json /data/config.json

#ENTRYPOINT [ "python", "/ipvgather/ipvgather.py", "-c /data/config.json", "--check" ]
ENTRYPOINT [ "python", "/ipvgather/test.py" ]
