# set base image (host OS)
FROM python:alpine

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY app/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY app/src/ .

# define volume
VOLUME /media

# expose port
EXPOSE 5000

# command to run on container start
CMD [ "python", "./server.py" ] 
