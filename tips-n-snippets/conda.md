# Conda

## Summary

Conda is a package and environment manager used to create isolated development environments.

It helps manage Python versions, dependencies, and project-specific packages without affecting the global system.

It is commonly used in data science, machine learning, AI projects, and Python applications that require reproducible environments.

## When to Use

Use Conda when you need to:

- Isolate dependencies per project
- Control the Python version
- Reproduce the same environment on another machine
- Manage libraries with native dependencies, such as TensorFlow, PyTorch, NumPy, Pandas, CUDA, etc.

## Create Environment

Create an environment from an `env.yml` file:

```bash
conda env create -f ./env.yml
```

## Update Environment

Update an existing environment using the `env.yml` file:

```bash
conda env update -f ./env.yml
```

To remove packages that are no longer listed in the file:

```bash
conda env update -f ./env.yml --prune
```

## Activate Environment

```bash
conda activate project-env
```

## Deactivate Environment

```bash
conda deactivate
```

## List Environments

```bash
conda env list
```

## Remove Environment

```bash
conda env remove -n project-env
```

Or:

```bash
conda remove -n project-env --all
```

## Export Environment

Generate an `env.yml` file from the current environment:

```bash
conda env export > env.yml
```

## Run Project

After activating the environment:

```bash
make run
```

## Practical Example

```bash
conda env create -f env.yml
conda activate project-env
make run
```