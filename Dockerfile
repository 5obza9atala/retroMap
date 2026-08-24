# Use a lightweight official Python runtime
FROM python:3.11-slim

# Install C++ compilers and GIS system libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgdal-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency list and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
