# Use a stable and minimal base image for Python 3.10
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
ENV ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Use multi-stage build to reduce final image size
FROM base AS builder

# Set the working directory
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY Requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r Requirements.txt

# Copy the application code
COPY . .

# Final stage
FROM base AS final

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code from the builder stage
COPY --from=builder /app /app

# Expose the port Streamlit will run on
EXPOSE 8501

# Create the .streamlit directory
RUN mkdir -p ~/.streamlit

# Copy Streamlit configuration files if needed
# COPY config.toml ~/.streamlit/config.toml
# COPY credentials.toml ~/.streamlit/credentials.toml

# Set the entrypoint to run Streamlit
ENTRYPOINT ["streamlit", "run"]

# Set the default command to run the main.py script
CMD ["main.py"]