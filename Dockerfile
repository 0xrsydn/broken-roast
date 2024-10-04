# Use a more recent Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Upgrade pip and install build dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    apt-get update && \
    apt-get install -y build-essential

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
