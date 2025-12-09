"""
Asynchronous URL analyzer using aiohttp.
Measures latency, HTTP status, and demonstrates task groups + callbacks.

AsyncIO Features (Assignment Step 6):
1. Coroutines: async/await for non-blocking I/O (_fetch, analyze_urls)
2. Event Loop: Managed via asyncio.run() in CLI
3. Task Groups: asyncio.TaskGroup() for structured concurrency
4. Callbacks: _log_callback() invoked after each fetch completes
5. Semaphore: Limits concurrent tasks to prevent resource exhaustion
"""

import asyncio
import time
from typing import List, Dict, Any, Callable, Optional
import pdb

import aiohttp


async def _fetch(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """Fetch a single URL and measure latency.

    COROUTINE: Uses async/await for non-blocking HTTP requests.
    CALLBACK: Invokes callback function after each fetch completes.

    Time Complexity: O(1) for the function logic itself.
    - Network I/O dominates: depends on server response time (external factor)
    - Dictionary operations: O(1)
    Space Complexity: O(1) - fixed size result dictionary
    """
    start = time.perf_counter()
    result: Dict[str, Any] = {"url": url, "status": None, "latency_ms": None}

    try:
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        async with session.get(url, timeout=timeout_obj, ssl=False) as response:
            await response.read()  # ensure body is consumed
            latency = (time.perf_counter() - start) * 1000
            result["status"] = response.status
            result["latency_ms"] = round(latency, 2)
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000

        # 🔴 DEBUG: Breakpoint for edge cases
        # (timeouts, connection errors, etc.)
        # Uncomment the line below to debug error handling
        # pdb.set_trace()

        result["status"] = f"ERROR: {type(e).__name__}"
        result["latency_ms"] = round(latency, 2)

    # Execute callback if provided
    if callback:
        callback(result)

    return result


async def analyze_urls(
    urls: List[str],
    concurrency: int = 10,
    timeout: int = 10,
) -> List[Dict[str, Any]]:
    """Analyze all URLs asynchronously with concurrency limit.

    ASYNCIO FEATURES:
    - COROUTINE: This function is a coroutine (async def)
    - TASK GROUPS: Uses asyncio.TaskGroup() for structured concurrency
    - SEMAPHORE: asyncio.Semaphore() limits concurrent execution
    - CALLBACKS: Passes _log_callback to track completion in real-time

    Time Complexity: O(n) where n is the number of URLs.
    - Task creation: O(n) - creates one task per URL
    - Task execution: Concurrent with max 'concurrency' tasks running at once
    - Result collection: O(n) - iterates through all tasks
    - Actual wall-clock time: O(n/c * t) where c is concurrency
      and t is avg response time

    Space Complexity: O(n)
    - Tasks list: O(n)
    - Results list: O(n)
    - Semaphore: O(1)

    Memory Management: For large batches (1000+ URLs), tasks are collected
    immediately after completion to allow garbage collection.
    """
    # ASYNCIO: Semaphore limits concurrent tasks (e.g., max 10 at once)
    semaphore = asyncio.Semaphore(concurrency)
    results: List[Dict[str, Any]] = []

    async def bound_fetch(url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Wrap _fetch with semaphore-based concurrency control."""
        async with semaphore:
            # Disable verbose logging for large batches
            # to reduce memory overhead
            callback = None if len(urls) > 100 else _log_callback
            return await _fetch(session, url, timeout, callback=callback)

    def _log_callback(item: Dict[str, Any]) -> None:
        """Invoked after each URL fetch completes."""
        status = item["status"]
        latency = item["latency_ms"]
        print(f"[DONE] {item['url']} → {status} in {latency} ms")

    # Configure connection pooling for better memory management
    connector = aiohttp.TCPConnector(
        limit=100,  # Max total connections
        limit_per_host=10,  # Max connections per host
        ttl_dns_cache=300,  # DNS cache TTL (5 minutes)
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        # ASYNCIO: Task Group manages concurrent coroutines
        # Ensures all tasks complete or fail together (structured concurrency)
        async with asyncio.TaskGroup() as tg:
            # Create tasks for each URL (all run concurrently)
            tasks = [tg.create_task(bound_fetch(url, session)) for url in urls]

        # Collect results immediately after TaskGroup completes
        # This allows completed tasks to be garbage collected
        for task in tasks:
            results.append(task.result())

    return results
