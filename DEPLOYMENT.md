# Packaging & Deployment Guide

This guide covers packaging, installation, and deployment options for the Web Performance Analyzer.

---

## Table of Contents
1. [Package Structure](#package-structure)
2. [Installation Methods](#installation-methods)
3. [Building the Package](#building-the-package)
4. [Docker Deployment](#docker-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)

---

## Package Structure

```
web_analyzer/
├── src/webperf/          # Source code
├── tests/                # Test suite
├── pyproject.toml        # Package configuration (PEP 621)
├── requirements.txt      # Dependency lockfile
├── Dockerfile            # Container definition
└── .github/workflows/    # CI/CD automation
    └── ci.yml
```

### Package Configuration

**pyproject.toml** (modern Python packaging):
- Build system: `setuptools` with `build` backend
- Package metadata: name, version, dependencies
- Tool configurations: black, ruff, mypy, pytest
- Entry point: `webperf` command

---

## Installation Methods

### Method 1: Install from Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd web_analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
webperf --help
```

### Method 2: Install from Built Package

```bash
# Build the package
python -m build

# Install the wheel
pip install dist/webperf-0.1.0-py3-none-any.whl

# Or install the source distribution
pip install dist/webperf-0.1.0.tar.gz
```

### Method 3: Install from Requirements

```bash
# Install runtime dependencies only
pip install -r requirements.txt

# Install the package
pip install -e .
```

---

## Building the Package

### Prerequisites
```bash
pip install build twine
```

### Build Steps

1. **Build distribution packages:**
   ```bash
   python -m build
   ```
   
   This creates:
   - `dist/webperf-0.1.0-py3-none-any.whl` (wheel - binary distribution)
   - `dist/webperf-0.1.0.tar.gz` (source distribution)

2. **Verify the build:**
   ```bash
   twine check dist/*
   ```

3. **Test the built package:**
   ```bash
   pip install dist/webperf-0.1.0-py3-none-any.whl
   webperf --input urls.json
   ```

### Publishing to PyPI (Optional)

```bash
# Test upload to TestPyPI
twine upload --repository testpypi dist/*

# Production upload to PyPI
twine upload dist/*
```

---

## Docker Deployment

### Building the Docker Image

The Dockerfile uses multi-stage builds for optimal size:

```bash
# Build the image
docker build -t webperf:latest .

# Build with custom tag
docker build -t webperf:0.1.0 .
```

### Running with Docker

**Basic usage:**
```bash
docker run --rm webperf:latest --help
```

**Analyze URLs (mount volume):**
```bash
docker run --rm \
  -v $(pwd)/urls.json:/app/urls.json \
  webperf:latest --input /app/urls.json --concurrency 10
```

**Interactive mode:**
```bash
docker run -it --rm webperf:latest bash
```

### Docker Features

- **Multi-stage build**: Smaller final image (~150MB vs 1GB)
- **Non-root user**: Runs as user `webperf` for security
- **Health check**: Verifies package import works
- **Volume support**: Mount local files for analysis

### Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  webperf:
    build: .
    image: webperf:latest
    volumes:
      - ./urls.json:/app/urls.json
      - ./results:/app/results
    command: --input /app/urls.json --concurrency 20
```

Run:
```bash
docker-compose up
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

Located at `.github/workflows/ci.yml`

### Pipeline Stages

#### 1. **Lint and Test** (Matrix: Python 3.11, 3.12)
- ✅ Lint with `ruff`
- ✅ Lint with `flake8`
- ✅ Type-check with `mypy`
- ✅ Run tests with `pytest`

#### 2. **Build Package**
- ✅ Build wheel and source distribution
- ✅ Validate with `twine check`
- ✅ Upload artifacts

#### 3. **Build Docker**
- ✅ Build Docker image
- ✅ Test Docker image (`--help`)
- ✅ Upload image artifact

### Triggering CI/CD

**Automatic:**
- Push to `main` branch
- Pull requests to `main`

**Manual:**
```bash
# Push changes
git add .
git commit -m "feat: add feature"
git push origin main
```

### Local CI Testing

Run the same checks locally:

```bash
# Linting
ruff check src tests
flake8 src tests

# Type checking
mypy src

# Tests
pytest tests/ -v

# Build
python -m build

# Docker
docker build -t webperf:latest .
docker run --rm webperf:latest --help
```

---

## Quality Checks

### Code Quality Tools

**Ruff** (Fast linter):
```bash
ruff check src tests
ruff format src tests  # Auto-format
```

**Flake8** (Style guide enforcement):
```bash
flake8 src tests --count --show-source
```

**MyPy** (Static type checking):
```bash
mypy src --strict
```

**Black** (Code formatter):
```bash
black src tests
```

### Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Coverage report
pytest --cov=webperf --cov-report=html
```

---

## Deployment Checklist

Before deploying:

- [ ] All tests pass: `pytest`
- [ ] Linting passes: `ruff check src tests`
- [ ] Type checking passes: `mypy src`
- [ ] Package builds: `python -m build`
- [ ] Docker builds: `docker build -t webperf .`
- [ ] Docker runs: `docker run --rm webperf --help`
- [ ] Version updated in `pyproject.toml`
- [ ] README updated
- [ ] CHANGELOG updated (if applicable)

---

## Troubleshooting

### Package Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'webperf'`

**Solution**:
```bash
pip install -e .  # Install in editable mode
```

### Docker Build Issues

**Problem**: Docker build fails on dependency installation

**Solution**:
```bash
# Clear Docker cache
docker build --no-cache -t webperf:latest .
```

### CI/CD Failures

**Problem**: mypy type-checking fails

**Solution**:
```bash
# Run mypy locally to see errors
mypy src --show-error-codes

# Fix type hints or add type ignores
```

---

## Additional Resources

- **setuptools docs**: https://setuptools.pypa.io/
- **pyproject.toml spec**: https://peps.python.org/pep-0621/
- **Docker best practices**: https://docs.docker.com/develop/dev-best-practices/
- **GitHub Actions**: https://docs.github.com/en/actions
