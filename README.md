# Web Performance Analyzer

Async web performance analyzer built with Python's AsyncIO and aiohttp. Measures URL response times with concurrency control, generates statistics, and demonstrates advanced async patterns.

---

## Features

✅ **Asynchronous URL Fetching** - Uses aiohttp for non-blocking I/O  
✅ **Concurrency Control** - Semaphore-based rate limiting  
✅ **Task Groups** - Structured concurrency with auto-cleanup  
✅ **Callbacks** - Real-time progress tracking  
✅ **Memory Efficient** - 16.9MB for 1250 URLs  
✅ **Connection Pooling** - Reuses TCP connections  
✅ **DNS Caching** - 5-minute TTL  
✅ **Profiled & Optimized** - cProfile + Memray analysis  
✅ **Type-Checked** - Passes mypy strict mode  
✅ **Production Ready** - Dockerized with CI/CD  

---

## Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd web_analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .
```

### Usage

```bash
# Analyze URLs from JSON file
webperf --input urls.json

# With custom concurrency
webperf --input urls.json --concurrency 20 --timeout 15
```

**Input File Format (urls.json):**
```json
[
  "https://example.com",
  "https://httpbin.org/delay/1",
  "https://google.com"
]
```

**Output:**
```
Analyzing 3 URLs with concurrency=10, timeout=10s...
[DONE] https://example.com → 200 in 245.32 ms
[DONE] https://httpbin.org/delay/1 → 200 in 1125.67 ms
[DONE] https://google.com → 200 in 89.12 ms

=== Summary Statistics ===
Total Requests: 3
Successful: 3
Failed: 0
Average Latency: 486.70 ms
```

---

## Project Structure

```
web_analyzer/
├── src/webperf/
│   ├── __init__.py
│   ├── analyzer.py      # Core async URL fetching
│   ├── cli.py           # Command-line interface
│   ├── io_utils.py      # JSON/CSV loading
│   └── stats.py         # Statistics aggregation
├── tests/
│   ├── test_analyzer.py
│   └── test_io_utils.py
├── profile_analyzer.py  # Profiling script
├── async_demo.py        # AsyncIO patterns demo
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── Dockerfile           # Container definition
├── .github/workflows/
│   └── ci.yml           # CI/CD pipeline
├── PROFILING_RESULTS.md # Performance analysis
└── DEPLOYMENT.md        # Deployment guide
```

---

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality Checks

```bash
# Formatting
black src/ tests/

# Linting
flake8 src/ tests/
ruff check src/ tests/

# Type checking
mypy src/ tests/
```

### Profiling

**CPU Profiling (cProfile):**
```bash
python profile_analyzer.py
# Generates: cprofile_output.txt, cprofile_output.prof
```

**Memory Profiling (Memray):**
```bash
python profile_analyzer.py --large
memray run --output memray_output.bin profile_analyzer.py --large
memray flamegraph memray_output.bin -o flamegraph_memray.svg
```

---

## Docker

### Build Image

```bash
docker build -t webperf .
```

### Run Container

```bash
# Analyze URLs
docker run --rm -v $(pwd)/urls.json:/data/urls.json webperf --input /data/urls.json

# Interactive shell
docker run -it --rm webperf /bin/bash
```

---

## AsyncIO Patterns

This project demonstrates key AsyncIO concepts:

1. **Coroutines** - `async def` functions with `await`
2. **Event Loop** - Managed via `asyncio.run()`
3. **Task Groups** - `asyncio.TaskGroup()` for structured concurrency
4. **Semaphore** - `asyncio.Semaphore()` for concurrency limits
5. **Callbacks** - Real-time progress tracking

See `async_demo.py` for detailed examples.

---

## Performance

### Time Complexity: **O(n)**
- Linear scaling with number of URLs
- Wall-clock time: O(n/c × t) where c=concurrency, t=avg response time

### Space Complexity: **O(n)**
- Results stored in memory
- Peak: 16.9MB for 1250 URLs

### Optimizations Applied:
- Connection pooling (100 total, 10 per host)
- DNS caching (5-minute TTL)
- Conditional logging for large batches
- Immediate result collection for GC

See `PROFILING_RESULTS.md` for detailed analysis.

---

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):

- **Lint & Test** - Python 3.11, 3.12 matrix
- **Build Package** - Wheel + source dist with twine validation
- **Docker Build** - Multi-stage container with health check

---

## Requirements

- Python 3.11+
- aiohttp 3.8+
- pytest 6.0+ (dev)
- mypy, black, ruff (dev)
- memray, py-spy (profiling)

---

## License

MIT

---

## Assignment Completion Checklist

✅ Functional Asynchronous CLI with concurrency limits  
✅ Big O time complexity comments in all major functions  
✅ Evidence of pdb debugging (analyzer.py:53)  
✅ cProfile profiling (cprofile_output.txt)  
✅ Memray memory analysis (flamegraph_memray.svg)  
✅ Profiling write-up (PROFILING_RESULTS.md)  
✅ Advanced AsyncIO patterns (Task Groups, callbacks, semaphore)  
✅ Distribution-ready package (pyproject.toml, pip installable)  
✅ Dockerized version (Dockerfile)  
✅ CI/CD workflow (.github/workflows/ci.yml)  
✅ Code passes all quality checks (black, flake8, ruff, mypy)  
