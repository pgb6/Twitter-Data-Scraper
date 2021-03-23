#set base image to Python 3.9.1
FROM python:3.9.1-buster

#set working directory in container
WORKDIR /code

#copy dependencies file to working directory
COPY requirements.txt .

#install dependencies
RUN pip install -r requirements.txt

## Set Your AWS Access credentials
ARG AWS_ACCESS_KEY_ID=HIDDEN
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY=HIDDEN
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION=us-east-1
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
RUN aws ecr get-login --no-include-email | bash


#copy content of local src directory to working directory
COPY src/ .

#make a logs dir for the script to write to
RUN mkdir ./logs

#give logs dir permissions
RUN chmod 755 ./logs 

#run container as entrypoint to allow cmd args
ENTRYPOINT ["python","./twitterSearch.py"]