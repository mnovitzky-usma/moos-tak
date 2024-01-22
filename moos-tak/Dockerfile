# Using official Python image from Docker Hub as a Base Image
FROM python:3.8-slim

# Setting working directory in the container
WORKDIR /app

# Copying the local directory contents to the container
COPY . /app/

# Installing the python packages from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python script
CMD ["python", "./loc2cotfin.py"]
