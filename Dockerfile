# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

ENV FLASK_RUN_PORT=5001
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run on container start
CMD ["python", "app.py"]
EXPOSE 5001