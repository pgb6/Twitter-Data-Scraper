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

#run container as entrypoint to allow cmd args
ENTRYPOINT ["python","./twitterSearch.py"]
