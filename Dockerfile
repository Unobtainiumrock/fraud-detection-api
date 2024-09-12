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

# Install Python dependencies
COPY requirements.txt /app/
# Install Jupyter and Uvicorn
RUN pip install --no-cache-dir \
    jupyterlab \
    uvicorn \
    -r requirements.txt

# Make port 8000 and 8888 available to the world outside this container
EXPOSE 8000
EXPOSE 8888

# Run the FastAPI app when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
