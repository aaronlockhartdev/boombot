## BUILD STAGE ##
FROM python:3.10 AS build

# create venv and add to path
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# set working directory
WORKDIR /usr/src/boombot

# build python requirements
COPY . .

RUN apt-get update && apt-get install -y \
    git \
    gcc \
  && pip install -U pip \
  && pip install -U wheel \
  && pip install -r requirements.txt

## RUN STAGE ##
FROM python:3.10

# install package requirements
#RUN apt-get update && apt-get install -y \
#    ffmpeg

# copy prepared venv and add to PATH
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# run application
COPY ./src/app.py .
ENTRYPOINT ["python", "-OO", "app.py"]
