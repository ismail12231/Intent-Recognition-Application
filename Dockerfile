# Use an official lightweight Python image
FROM python:3.9-slim

# Set environment variables to avoid Python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port Flask runs on
EXPOSE 8080

# Start the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
