# CI/CD

## Summary

CI/CD is a software engineering practice used to automate build, test, and deployment processes.

CI means Continuous Integration.

CD can mean Continuous Delivery or Continuous Deployment.

It helps teams deliver software faster, safer, and with fewer manual steps.

## When to Use

Use CI/CD when you need to:

- Automate tests
- Validate code before merging
- Build applications automatically
- Deploy applications safely
- Reduce manual deployment errors
- Improve release frequency
- Support DevOps practices

## CI - Continuous Integration

Continuous Integration means automatically validating code changes when developers push or open a pull request.

Common CI steps:

```text
Install dependencies
Run lint
Run unit tests
Run integration tests
Build application
Validate security checks
```

Example:

```text
Developer opens PR
    ↓
CI pipeline runs tests
    ↓
Code is approved
    ↓
Code is merged
```

## CD - Continuous Delivery

Continuous Delivery means the application is always ready to be deployed, but the final deployment usually requires manual approval.

Example:

```text
Merge to main
    ↓
Build artifact
    ↓
Run tests
    ↓
Prepare release
    ↓
Manual approval
    ↓
Deploy to production
```

## CD - Continuous Deployment

Continuous Deployment means every approved change is automatically deployed to production.

Example:

```text
Merge to main
    ↓
Run pipeline
    ↓
Deploy automatically to production
```

## Common Pipeline Flow

```text
Code
    ↓
Build
    ↓
Test
    ↓
Package
    ↓
Deploy
    ↓
Monitor
```

## Common Tools

```text
GitHub Actions
GitLab CI
Jenkins
Azure DevOps
CircleCI
Argo CD
Tekton
Docker
Kubernetes
Terraform
```

## Example GitHub Actions

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

## Benefits

- Faster delivery
- Fewer manual errors
- Safer deployments
- Better code quality
- Automated validation
- Easier rollback
- Better collaboration between development and operations

## Challenges

- Requires good test coverage
- Pipelines can become complex
- Flaky tests can block releases
- Secrets must be handled carefully
- Bad automation can deploy bugs faster
- Requires monitoring after deployment

## Related Concepts

```text
blue-green-deploy.md
canary-deploy.md
zero-downtime-migrations.md
docker.md
kubernetes.md
observability.md
```

## Simple Explanation

```text
CI/CD automates the path from code change to production.

CI checks if the code is correct.
CD prepares or performs the deployment.
```