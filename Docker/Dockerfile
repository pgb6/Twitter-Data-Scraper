#set base image to Python 3.9.1
FROM python:3.9.1-buster

#set working directory in container
WORKDIR /code

#copy dependencies file to working directory
COPY requirements.txt .

#install dependencies
RUN pip install -r requirements.txt

#copy content of local src directory to working directory
COPY src/ .

#make a logs dir for the script to write to
RUN mkdir ./logs

#give logs dir permissions
RUN chmod 777 ./logs 

#run container as entrypoint to allow cmd args
ENTRYPOINT ["python","./twitterSearch.py"]
