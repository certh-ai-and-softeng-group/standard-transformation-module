# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Install Python and dependencies
RUN apt update && apt install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

# Ensure Python3 is correctly installed
RUN python3 --version && which python3

# Create a virtual environment inside the container
RUN python3 -m venv /app/venv

# Ensure the virtual environment is used for all future commands
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip inside the virtual environment
RUN /app/venv/bin/python -m pip install --upgrade pip setuptools wheel

# Copy requirements.txt and install dependencies inside the virtual environment
COPY requirements.txt .
RUN /app/venv/bin/python -m pip install --no-cache-dir -r requirements.txt

# Force install Uvicorn inside the virtual environment
RUN /app/venv/bin/python -m pip install --no-cache-dir uvicorn

# Debugging: Check if Uvicorn is installed
RUN /app/venv/bin/python -m pip list | grep uvicorn

# Copy the rest of the application
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Ensure the command runs inside the virtual environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
