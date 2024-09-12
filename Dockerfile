# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, Node.js, and npm
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libatlas-base-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    git \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN npm install -g bash-language-server sql-language-server yaml-language-server typescript typescript-language-server

# Copy the current directory contents into the container at /app
COPY . /app

ENV PYTHON_EXECUTABLE=/usr/local/bin/python

# Install Python dependencies
COPY requirements.txt /app/
# Install Jupyter and Uvicorn
RUN pip install --no-cache-dir \
    jupyterlab \
    uvicorn \
    ipykernel \
    -r requirements.txt

# Add the Python 3.9 environment as a Jupyter kernel
RUN python -m ipykernel install --name=python3 --display-name "Python 3.9"

# Make port 8000 available to the world outside this container
EXPOSE 8000
Expose 8888

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
