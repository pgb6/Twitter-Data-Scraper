# Twitter Data Scraper
This python file serves as a command line script that will allow the user to
store a users' most recent 100 tweets into an NDJSON file. It can also search
the first 100 tweets with a specified hashtag and display associated distinct hashtags as
well as the count of each distinct hashtag. This script is useful for identifying and analyzing trends on Twitter through tweets and hashtags. 
# Approach
This code was designed to be scalable and reusable.
I took the liberty to provide the user with a docker build environment so that the user could simply build an image and run it regardless of their OS! However, if they do not want to use Docker, they can proceed to the boring way of
running the code, which is through the Windows/Linux command-line.

The main use of this script is for AWS-the script is essentially a scheduled task in AWS Elastic Container Service, and the output goes directly to a specified S3 bucket. With the data in S3, the user can run queries (data must be transformed) with RDS and perform data analysis on Twitter trends over the course of time.

# Directory Contents
```bash
├───AWS
│   │   Dockerfile
│   │   requirements.txt
│   │
│   └───src
│           twitterSearch.py
│
├───Desktop
│       twitterSearch.py
│
└───Docker
    │   Dockerfile
    │   requirements.txt
    │
    └───src
            twitterSearch.py

```

# Running the Script

This script uses argparse to allow the user to specify which function they would like to run. Users simply add the following args (excluding -h) to the script to call a function. Users may list both args, or either arg.

The '-t' arg will use Twitter's user_timeline API to output a JSON file of a users' 100 recent tweets to the 'logs' folder.

The '-H' arg (uppercase!) arg will search a hashtags first 100 tweets and print a dataframe of distinct hashtags and their 
occurences. This argument also outputs a CSV file to the 'logs' folder.

The '-h' arg is for listing the available args as well as what their purposes are.

If implementing this script for AWS, the '-b' arg must be used to specify which S3 bucket will be used to collect the script output.

## Using AWS (ECS and S3)
Make sure Docker is installed on your system!
https://docs.docker.com/get-docker/
1. Navigate to the AWS folder in the command line
2. Change the Dockerfile to include your IAM users' keys
3. Build the docker image with: 
	```bash
	docker build -t <desired image name> .
	```
3. Create an AWS ECR repository and tag this docker image with the repo URI
4. Push the image to ECR
5. Navigate to AWS ECS and create a cluster with >= t2.large instances. Choose one AZ for the subnet.
6. Create an S3 bucket for gathering script output. This buckets' AZ should be the same as the one chosen in the cluster.
7. Create a task definition with default execution roles and 1024 Task memory and Task CPU each. In the container definitions, create a container with the image URI. For the details, the container must be in Privileged mode and the Command must look like: 
	```bash 
	["--timeline",<user name in quotes>,"--hashtag",<hashtag name in quotes>,"--bucket",<S3 bucket name in quotes>]
	```
8. Launch a scheduled task in the cluster using the task definition previously created, the S3 bucket should now collect script output for later analysis!


## Using Docker
Make sure Docker is installed on your system!
https://docs.docker.com/get-docker/
1. Navigate to the Docker folder in the command line 
2. Build the docker image with: 
	```bash
	docker build -t <desired image name> .
	```
3. Run the docker image you created using the following command, using whichever arguments are desired:
	```bash
	docker run -it --rm -v ${PWD}/logs:/code/logs <image name> <arg> <arg>
	```
4. Explore the created logs folder accordingly

## Using Windows/Linux
REQUIRES PYTHON >= 3.9

1. Navigate to the Desktop folder (provided with this README) in the command line
2. Install the scripts' dependencies like so:
	```bash
	pip install -r requirements.txt
	```
3. Run the script:
	```bash
	python twitterSearch.py <arg> <arg>
	```
4. Explore the logs folder accordingly



