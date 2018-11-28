FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip
RUN pip3 install --upgrade pip==9.0.3 \
    && pip3 install setuptools

# for flask web server
EXPOSE 8082

# set working directory
#ADD ./ /app
# install required libraries
WORKDIR /app
VOLUME ["/app"]

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# This is the runtime command for the container
CMD python3 /app/ui/backend/app.py
#CMD sleep 100
#CMD tail -f anything
