# Minesweeper CI/CD

Academic Minesweeper project built with `pygame`.

## What is implemented

This repository now includes the full CI/CD scope for the lab:

- unit tests for the application with `pytest`;
- code style checks with `flake8`;
- local CI script for running tests and lint together;
- `requirements.txt` with project and CI dependencies;
- GitHub Actions workflow that runs on every push and pull request;
- HTML reports for testing and linting as workflow artifacts.

## Project structure

- `src/` - game source code
- `tests/` - automated tests
- `.github/workflows/build.yml` - GitHub Actions pipeline
- `scripts/run_ci.ps1` - local CI pipeline script
- `.flake8` - flake8 configuration
- `pytest.ini` - pytest configuration

## Run the game

```powershell
python -m src.main
```

## Run tests

```powershell
python -m pytest tests
```

## Run lint

```powershell
python -m flake8 src tests --config=.flake8
```

## Run the local CI pipeline

```powershell
.\scripts\run_ci.ps1
```

The script generates local reports in:

- `reports/pytest/report.html`
- `reports/pytest/junit.xml`
- `reports/flake8/index.html`
- `reports/flake8/flake8.txt`

## GitHub Actions

The workflow automatically:

1. installs dependencies from `requirements.txt`;
2. runs `pytest`;
3. runs `flake8`;
4. generates HTML reports;
5. uploads reports as workflow artifacts.

## Notes

Generated files in `reports/` are ignored locally and should not be committed.
