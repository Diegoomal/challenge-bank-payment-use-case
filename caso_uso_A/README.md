<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# User Management - Ports and Adapters Architecture

A small Python service that demonstrates Ports and Adapters Architecture, also
known as Hexagonal Architecture.

The service implements user CRUD operations. Data is stored in memory, and the
application prevents creating or updating two users with the same email address.

## Architecture

- `src`: application hexagon.
- `domain`: pure business entities.
- `application/ports`: operations offered to external actors and resources
  required by the application.
- `application/services`: application services that implement driving
  ports.
- `adapters`: concrete adapters for CLI, persistence, and
  messaging.
- `configurator.py`: dependency wiring.
- `main.py`: executable entry point.

The application core depends only on its domain and interfaces. Adapters depend
inward on the application core.

## Project Structure

```text
root/
├── src/
│   ├── configurator.py
│   ├── main.py
│   ├── domain/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   └── adapters/
│       ├── cli/
│       ├── persistence/
│       └── messaging/
├── tests/
└── requirements.txt
```

## Environment

Create the Conda environment:

```bash
conda env create -n ports-adapters-env -f env.yml
```

Activate the environment:

```bash
conda activate ports-adapters-env
```

## Commands

- `make run`: runs the CLI example with `python3`.
- `make test`: runs the test suite.
- `make lint`: checks code style.
- `make docs`: generates the `docs/` directory.
- `make check`: runs lint and tests.

## Guides

- [Ports and Adapters](/tips-n-snippets/ports-and-adapters.md)
- [Unit tests](/tips-n-snippets/unity-test.md)
- [Flake8](/tips-n-snippets/flake8.md)
- [pdoc](/tips-n-snippets/pdoc.md)
- [Makefile](/tips-n-snippets/make.md)

[author](https://github.com/Diegoomal)
