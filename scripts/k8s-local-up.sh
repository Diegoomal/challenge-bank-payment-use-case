#!/usr/bin/env bash
set -e

minikube start --driver=docker
kubectl get nodes

eval $(minikube docker-env)

docker compose build

rm -rf k8s/generated
mkdir -p k8s/generated

kompose convert -f docker-compose.yml -o k8s/generated/

find k8s/generated -type f -name "*.yaml" -exec perl -0pi -e 's/^([ \t]*)image: (.*)$/\1image: \2\n\1imagePullPolicy: IfNotPresent/mg' {} \;

kubectl apply --dry-run=client -f k8s/generated/
kubectl apply -f k8s/generated/

kubectl get pods
kubectl get services
kubectl get deployments
