# Use the specified Python base image
FROM python:3.10.14-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY ./src /app/src
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Remove unnecessary tools and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions
RUN chmod -R 755 /app

# Make port 8080 available to the world outside this container
EXPOSE 8502

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8502"]