#!/usr/bin/env python3

"""
CLI entry point for the async web performance analyzer.
"""

import argparse
import asyncio
from pathlib import Path

from webperf.analyzer import analyze_urls
from webperf.io_utils import load_urls
from webperf.stats import summarize


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the web analyzer."""
    parser = argparse.ArgumentParser(description="Async Web Performance Analyzer")
    parser.add_argument(
        "--input",
        required=True,
        type=str,
        help="Path to JSON or CSV file containing URLs.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Maximum number of concurrent requests.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout (seconds) for each HTTP request.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI.

    Overall Time Complexity: O(n) where n is the number of URLs.
    - load_urls: O(n)
    - analyze_urls: O(n) for task setup, execution is concurrent
    - summarize: O(n)
    - printing results: O(n)
    Total: O(n) + O(n) + O(n) + O(n) = O(n) linear complexity

    Space Complexity: O(n) to store URLs and results in memory.
    """
    args = parse_args()
    input_path = Path(args.input)

    urls = load_urls(input_path)

    results = asyncio.run(
        analyze_urls(urls, concurrency=args.concurrency, timeout=args.timeout)
    )

    # Generate aggregated statistics
    summary = summarize(results)

    print("\n=== Web Performance Summary ===")
    print(f"Total Requests: {summary['total_requests']}")
    print(f"Successful: {summary['successful_requests']}")
    print(f"Failed: {summary['failed_requests']}")
    print(f"Average Latency: {summary['average_latency_ms']} ms")

    print("\n=== Individual Results ===")
    for item in results:
        print(
            f"URL: {item['url']} | Status: {item['status']} | "
            f"Latency: {item['latency_ms']} ms"
        )


if __name__ == "__main__":
    main()
