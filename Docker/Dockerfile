#set base image to Python 3.9.1
FROM python:3.9.1-buster

#set working directory in container
WORKDIR /code

#copy dependencies file to working directory
COPY requirements.txt .

<<<<<<< HEAD
#install dependencies
RUN pip install -r requirements.txt
=======
## Set Your AWS Access credentials
ARG AWS_ACCESS_KEY=HIDDEN
ENV AWS_ACCESS_KEY=$AWS_ACCESS_KEY
ARG AWS_SECRET_ACCESS_KEY=HIDDEN
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
>>>>>>> 45a1075 (Update Dockerfile)

#copy content of local src directory to working directory
COPY src/ .

#make a logs dir for the script to write to
RUN mkdir ./logs

#give logs dir permissions
RUN chmod 755 ./logs 

#run container as entrypoint to allow cmd args
ENTRYPOINT ["python","./twitterSearch.py"]
