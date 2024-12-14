# Welcome Again

## How to build the docker container 

### First create a docker file that installs the requirements of the api and python 3.9
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN python -m venv venv

RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

EXPOSE 3000

ENV FLASK_APP=library.py
ENV FLASK_ENV=development

CMD ["./venv/bin/python", "library.py"]

###### Like this in the code you are ready to create a docker container and run it ,  the most important thing to make the host 0.0.0.0 in python to ensure that the api works correctly
###### Run this to create the container
docker build -t flask-library-api .
###### Then run this to run the container
docker run -d -p 3000:3000 flask-library-api
###### Then you can open postman to run your apis 

## How to access swagger documentation for the api
### go to http://localhost:3000/apidocs


# Thank you all