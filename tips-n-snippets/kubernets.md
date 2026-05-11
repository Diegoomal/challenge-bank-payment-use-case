# Kubernetes

## Summary

Kubernetes is a container orchestration platform used to deploy, manage, scale, and monitor containerized applications.

It is commonly used to run applications in production using containers, especially when the system has multiple services, replicas, environments, and deployment strategies.

Kubernetes helps manage infrastructure concerns such as scaling, service discovery, load balancing, self-healing, and rolling deployments.

## When to Use

Use Kubernetes when you need to:

- Run containers in production
- Scale services automatically
- Manage microservices
- Deploy applications with zero downtime
- Restart failed containers automatically
- Balance traffic between replicas
- Manage configuration and secrets
- Standardize deployments across environments

## Core Concepts

### Cluster

A group of machines where Kubernetes runs applications.

```text
Kubernetes Cluster
 ├── Control Plane
 └── Worker Nodes
```

### Node

A machine inside the cluster responsible for running workloads.

```text
Node = server that runs containers
```

### Pod

The smallest deployable unit in Kubernetes.

A pod usually runs one container.

```text
Pod
 └── Container
```

### Deployment

Defines how an application should be deployed and updated.

```text
Deployment manages replicas of pods
```

### Service

Exposes pods through a stable network address.

```text
Service routes traffic to pods
```

### ConfigMap

Stores non-sensitive configuration.

```text
APP_ENV=production
LOG_LEVEL=info
```

### Secret

Stores sensitive configuration.

```text
DATABASE_PASSWORD
API_KEY
JWT_SECRET
```

### Namespace

Separates resources inside the same cluster.

```text
dev
staging
production
```

## Basic Commands

List pods:

```bash
kubectl get pods
```

List services:

```bash
kubectl get services
```

List deployments:

```bash
kubectl get deployments
```

Apply a Kubernetes manifest:

```bash
kubectl apply -f deployment.yml
```

Delete a resource:

```bash
kubectl delete -f deployment.yml
```

View pod logs:

```bash
kubectl logs pod-name
```

Follow logs:

```bash
kubectl logs -f pod-name
```

Execute command inside a pod:

```bash
kubectl exec -it pod-name -- sh
```

Describe a resource:

```bash
kubectl describe pod pod-name
```

## Example Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-api
  template:
    metadata:
      labels:
        app: payment-api
    spec:
      containers:
        - name: payment-api
          image: payment-api:latest
          ports:
            - containerPort: 8080
```

## Example Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payment-api-service
spec:
  selector:
    app: payment-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

## Benefits

- Automatic scaling
- Self-healing
- Load balancing
- Rolling updates
- Better infrastructure standardization
- Good fit for microservices
- Supports cloud-native deployments

## Challenges

- Higher operational complexity
- Requires knowledge of networking
- Requires monitoring and observability
- YAML configuration can become large
- Debugging can be harder than simple Docker usage

## Practical Use Cases

- Microservices
- APIs
- Event-driven systems
- Backend platforms
- AI services
- Batch jobs
- Scalable web applications
- Cloud-native systems

## Simple Explanation

```text
Docker runs containers.

Kubernetes manages many containers across many machines.
```