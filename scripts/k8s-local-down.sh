#!/usr/bin/env bash
set -e

kubectl delete -f k8s/generated/ --ignore-not-found=true || true
