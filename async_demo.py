#!/usr/bin/env python3
"""
AsyncIO Demonstration - Assignment Step 6

Demonstrates:
1. Event Loop usage
2. Coroutines (async/await)
3. Task Groups for structured concurrency
4. Callbacks for real-time logging

This script showcases the async architecture used in the web analyzer.
"""

import asyncio
import time
from typing import List, Dict, Any


# ========== DEMONSTRATION: Callbacks ==========


class StatsTracker:
    """Callback handler that tracks statistics in real-time."""

    def __init__(self):
        self.total_requests = 0
        self.successful = 0
        self.failed = 0
        self.total_latency = 0.0

    def on_request_complete(self, result: Dict[str, Any]) -> None:
        """Callback invoked after each fetch completes."""
        self.total_requests += 1

        if isinstance(result["status"], int) and result["status"] < 400:
            self.successful += 1
        else:
            self.failed += 1

        if result["latency_ms"]:
            self.total_latency += result["latency_ms"]

        # Real-time logging
        status_icon = (
            "✅"
            if isinstance(result["status"], int) and result["status"] < 400
            else "❌"
        )
        print(
            f"{status_icon} [{self.total_requests:3d}] {result['url'][:50]:50s} "
            f"→ {str(result['status']):20s} {result['latency_ms']:7.2f}ms"
        )

    def print_summary(self) -> None:
        """Print final statistics."""
        avg_latency = (
            self.total_latency / self.total_requests if self.total_requests > 0 else 0
        )
        print("\n" + "=" * 80)
        print("📊 CALLBACK STATS SUMMARY")
        print("=" * 80)
        print(f"Total Requests:    {self.total_requests}")
        print(f"Successful:        {self.successful}")
        print(f"Failed:            {self.failed}")
        print(f"Average Latency:   {avg_latency:.2f}ms")
        print("=" * 80)


# ========== DEMONSTRATION: Coroutines ==========


async def fetch_url_demo(url: str, delay: float, stats: StatsTracker) -> Dict[str, Any]:
    """
    Coroutine that simulates fetching a URL.

    Demonstrates:
    - async/await syntax
    - Non-blocking I/O simulation
    - Callback invocation
    """
    start = time.perf_counter()

    # Simulate network I/O (non-blocking)
    await asyncio.sleep(delay)

    latency = (time.perf_counter() - start) * 1000
    result = {"url": url, "status": 200, "latency_ms": round(latency, 2)}

    # Invoke callback
    stats.on_request_complete(result)

    return result


# ========== DEMONSTRATION: Task Groups ==========


async def analyze_with_task_groups(
    urls: List[str], concurrency: int, stats: StatsTracker
) -> List[Dict[str, Any]]:
    """
    Demonstrates Task Groups (Python 3.11+) for structured concurrency.

    Features:
    - Creates multiple coroutines as tasks
    - Limits concurrency with semaphore
    - Automatic exception handling
    - Clean resource management
    """
    semaphore = asyncio.Semaphore(concurrency)
    results: List[Dict[str, Any]] = []

    async def bounded_fetch(url: str, delay: float):
        """Fetch with semaphore-based concurrency control."""
        async with semaphore:
            return await fetch_url_demo(url, delay, stats)

    # Task Group ensures all tasks complete or fail together
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(bounded_fetch(url, delay)) for url, delay in urls]

    # Collect results after all tasks complete
    for task in tasks:
        results.append(task.result())

    return results


# ========== DEMONSTRATION: Event Loop ==========


def main():
    """
    Demonstrates Event Loop usage.

    The event loop:
    1. Schedules coroutines for execution
    2. Manages concurrent tasks
    3. Handles I/O operations efficiently
    4. Provides structured concurrency
    """
    print("\n" + "=" * 80)
    print("  AsyncIO Demonstration - Event Loop, Coroutines, Task Groups, Callbacks")
    print("=" * 80)

    # Test data: (url, simulated_delay_seconds)
    test_urls = [
        ("https://example.com", 0.5),
        ("https://httpbin.org/get", 1.0),
        ("https://httpbin.org/delay/1", 1.5),
        ("https://github.com", 0.8),
        ("https://python.org", 0.6),
        ("https://stackoverflow.com", 0.7),
        ("https://reddit.com", 0.9),
        ("https://news.ycombinator.com", 0.4),
    ]

    concurrency = 3

    print(f"\n🔄 Testing {len(test_urls)} URLs with concurrency={concurrency}")
    print("=" * 80)
    print(f"{'STATUS':^6} {'#':^5} {'URL':^50} {'HTTP':^20} {'LATENCY':^10}")
    print("=" * 80)

    # Create stats tracker (callback handler)
    stats = StatsTracker()

    # Run the event loop
    # asyncio.run() creates event loop, runs coroutine, and cleans up
    start_time = time.time()
    results = asyncio.run(analyze_with_task_groups(test_urls, concurrency, stats))
    elapsed = time.time() - start_time

    # Print summary from callback stats
    stats.print_summary()

    print(f"\n⏱️  Total wall-clock time: {elapsed:.2f}s")
    print(f"   Sequential would take: {sum(delay for _, delay in test_urls):.2f}s")
    print(f"   Speedup: {sum(delay for _, delay in test_urls) / elapsed:.1f}x")
    print("\n" + "=" * 80)

    # Show what the analyzer uses
    print("\n📚 Key AsyncIO Features Demonstrated:")
    print("   1. Event Loop:     asyncio.run() manages the event loop")
    print("   2. Coroutines:     async def + await for non-blocking operations")
    print("   3. Task Groups:    asyncio.TaskGroup() for structured concurrency")
    print(
        "   4. Callbacks:      StatsTracker.on_request_complete() for real-time logging"
    )
    print("   5. Semaphore:      asyncio.Semaphore() limits concurrent tasks")
    print("=" * 80)

    print("\n💡 The web analyzer (src/webperf/analyzer.py) uses these same patterns!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
