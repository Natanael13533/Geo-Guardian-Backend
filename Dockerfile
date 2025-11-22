# Import base image
FROM python:3.13.9-slim-bookworm

# Set working directory
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Set Work Directory
WORKDIR /app

# Install dependecies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project
COPY . .