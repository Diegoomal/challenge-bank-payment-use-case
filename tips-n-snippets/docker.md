# Docker

## Summary

Docker is a platform used to build, run, and distribute applications inside containers.

A container packages the application code, dependencies, runtime, and configuration, making the application run consistently across different environments.

Docker is commonly used for backend services, APIs, databases, microservices, local development, CI/CD pipelines, and cloud deployments.

## When to Use

Use Docker when you need to:

- Run applications in isolated environments
- Avoid dependency conflicts
- Standardize development and production environments
- Package an application with all required dependencies
- Run databases, queues, APIs, and services locally
- Deploy applications using containers

## Build Image

Build a Docker image from a `Dockerfile`:

```bash
docker build -t app-name .
```

## Run Container

Run a container from an image:

```bash
docker run app-name
```

Run exposing a port:

```bash
docker run -p 8080:8080 app-name
```

Run in detached mode:

```bash
docker run -d -p 8080:8080 app-name
```

## List Images

```bash
docker images
```

## List Running Containers

```bash
docker ps
```

## List All Containers

```bash
docker ps -a
```

## Stop Container

```bash
docker stop container_id
```

## Remove Container

```bash
docker rm container_id
```

## Remove Image

```bash
docker rmi image_id
```

## View Logs

```bash
docker logs container_id
```

Follow logs in real time:

```bash
docker logs -f container_id
```

## Execute Command Inside Container

```bash
docker exec -it container_id bash
```

Or:

```bash
docker exec -it container_id sh
```

## Docker Compose

Start services defined in `docker-compose.yml`:

```bash
docker compose up
```

Start in detached mode:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

Rebuild services:

```bash
docker compose up --build
```

## Clean Docker Resources

Remove stopped containers, unused networks, images, and cache:

```bash
docker system prune
```

Remove build cache:

```bash
docker builder prune
```

Remove all unused images:

```bash
docker image prune -a
```

## Practical Example

```bash
docker build -t my-api .
docker run -d -p 8080:8080 my-api
docker logs -f container_id
```