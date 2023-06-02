# Use an official Python runtime based on Debian 10 "buster" as a parent image
FROM python:3.8-slim-buster

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

# create root directory for our project in the container
RUN mkdir /techtrends

# Set the working directory to /techtrends
WORKDIR /techtrends

# Copy the current directory contents into the container at /techtrends
ADD . /techtrends/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "init_db.py" ]
CMD [ "python", "app.py" ]

# Expose the port the app runs in 
EXPOSE 3111


