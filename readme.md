# Potential Inc

## Django Boilerplate

---

# Django ASGI Application Setup Guide

This guide will walk you through setting up and running a Django application using ASGI (Asynchronous Server Gateway
Interface) both locally and with Docker Compose.

## Prerequisites

Before getting started, make sure you have the following installed:

- Python (3.10 recommended)
- Docker
- Docker Compose

## Local Setup

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/potentialInc/django_boilerplate.git
cd dir_name
```

### Step 2: Create a Virtual Environment

Create and activate a virtual environment to isolate your project dependencies:

```bash
python3 -m venv env
source env/bin/activate      # On Unix or MacOS
# OR
env\Scripts\activate         # On Windows
```

### Step 3: Install Dependencies

Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Django Application

Run the Django application using the ASGI server:

```bash
python manage.py runserver
```

## Docker Setup

### Step 1: Build the Docker Image

Build the Docker image using the provided Dockerfile:

```bash
docker build -t django-asgi-app .
```

### Step 2: Run the Docker Container

Run the Docker container based on the built image(Manually):

```bash
docker run -p 8000:8000 django-asgi-app
```

## Using Docker Compose

### Step 1: Start Docker Compose

Use Docker Compose to manage your application services. First, create a new file named `docker-compose.yml` if it
doesn't exist already, and then run the following command:

```bash
docker-compose up -d 
```

### Step 2: Access Your Application

Once the services are up and running, you can access your Django application at `http://localhost:8000`.

## Deployment Guide

To deploy your Django application using Docker Compose, follow these steps:

1. Prepare your server environment with Docker and Docker Compose installed.
2. Copy your project files to the server.
3. Modify the `docker-compose-example.yml` file as needed (e.g., update environment variables, ports).
4. Use `docker-compose` to start your application services on the server:

    ```bash
    docker-compose -f up -d
    ```

5. Ensure that your server's firewall allows traffic on the specified ports.
6. You can now access your deployed application using the server's IP address or domain name.

## Notes

...
---