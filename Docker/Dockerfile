FROM ubuntu:20.10

## Some utilities
RUN apt-get update -y && \
    apt-get install -y build-essential fuse sshfs libfuse-dev libcurl4-openssl-dev libxml2-dev pkg-config libssl-dev mime-support automake libtool wget tar git unzip
RUN apt-get install lsb-release -y  && apt-get install zip -y && apt-get install vim -y

## Install Python
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \  
    && pip3 install --upgrade pip \
    && apt-get clean

## Install S3 Fuse
RUN rm -rf /usr/src/s3fs-fuse
RUN git clone https://github.com/s3fs-fuse/s3fs-fuse/ /usr/src/s3fs-fuse
WORKDIR /usr/src/s3fs-fuse 
RUN ./autogen.sh && ./configure && make && make install

## Create workdir and logs folder (for mounting)
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ . 
RUN mkdir logs
RUN chmod 755 ./logs

## Set Your AWS Access credentials
ARG AWS_ACCESS_KEY=youraccesskey
ENV AWS_ACCESS_KEY=$AWS_ACCESS_KEY
ARG AWS_SECRET_ACCESS_KEY=yoursecretkey
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

## Set the directory where you want to mount your s3 bucket
ARG S3_MOUNT_DIRECTORY=/code/logs
ENV S3_MOUNT_DIRECTORY=$S3_MOUNT_DIRECTORY
ARG S3_BUCKET_NAME=twitterdatascraper-bucket
ENV S3_BUCKET_NAME=$S3_BUCKET_NAME 

## S3fs-fuse credential config
RUN echo $AWS_ACCESS_KEY:$AWS_SECRET_ACCESS_KEY > /root/.passwd-s3fs && \
    chmod 600 /root/.passwd-s3fs

## Run s3fs
WORKDIR /
#ADD start-script.sh /start-script.sh
#RUN chmod 755 /start-script.sh 
#RUN chmod +x /start-script.sh
#CMD ["/bin/bash","/start-script.sh"]
RUN s3fs $S3_BUCKET_NAME $S3_MOUNT_DIRECTORY 
#Run command above doesn't work due to s3fs?



## Entry Point
#WORKDIR /code
#ENTRYPOINT ["python3","./twitterSearch.py"]
