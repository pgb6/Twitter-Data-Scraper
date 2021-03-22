# Twitter Data Scraper
This python file serves as a command line script that will allow the user to
store a users' most recent 100 tweets into an NDJSON file. It can also search
the first 100 tweets with a specified hashtag and display associated distinct hashtags as
well as the count of each distinct hashtag. This script is useful for identifying and analyzing trends on Twitter through tweets and hashtags.
# Approach
This code was designed to be scalable and reusable.
I took the liberty to provide the user with a docker build environment so that the user could simply build an image and run it regardless of their OS! However, if they do not want to use Docker, they can proceed to the boring way of
running the code, which is through the Windows/Linux command-line.

# Directory Contents
```bash
├───Desktop
│   │   hidden.py
│   │   twitterSearch.py
│   │
│   └───logs
└───Docker
    │   Dockerfile
    │   requirements.txt
    │
    └───src
            hidden.py
            twitterSearch.py

```

# Running the Script

This script uses argparse to allow the user to specify which function they would like to run. Users simply add the following args (excluding -h) to the script to call a function. Users may list both args, or either arg.

The '-t' arg will use Twitter's user_timeline API to output a JSON file of a users' 100 recent tweets to the 'logs' folder.

The '-H' arg (uppercase!) arg will search a hashtags first 100 tweets and print a dataframe of distinct hashtags and their 
occurences. This argument also outputs a CSV file to the 'logs' folder.

The '-h' arg is for listing the available args as well as what their purposes are.
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

# WIP:
1. Automating this process by adding the docker image to AWS ECR and running it on a daily basis. Store the output contents in an S3.

