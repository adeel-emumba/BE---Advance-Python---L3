#!/usr/bin/env python3
"""
Profiling script for the async web performance analyzer.
Generates both cProfile (CPU) and memray (memory) profiling data.

Usage:
    # CPU profiling with cProfile (small batch)
    python profile_analyzer.py

    # CPU profiling with large batch
    python profile_analyzer.py --large

    # Memory profiling with memray (large batch recommended)
    python -m memray run -o memray_output.bin profile_analyzer.py --large
    python -m memray flamegraph memray_output.bin -o flamegraph.html
    python -m memray stats memray_output.bin
"""

import sys
import cProfile
import pstats
import asyncio
from pathlib import Path
from webperf.analyzer import analyze_urls
from webperf.io_utils import load_urls

# Determine batch size from command line
USE_LARGE_BATCH = "--large" in sys.argv

if USE_LARGE_BATCH:
    # Load 1250 URLs from file for memory profiling
    urls = load_urls(Path("urls_large.json"))
    CONCURRENCY = 20
else:
    # Small batch for quick CPU profiling
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/get",
        "https://example.com",
        "https://httpbin.org/status/200",
    ] * 10  # 50 URLs
    CONCURRENCY = 5


def run_analysis():
    """Run the async URL analysis."""
    batch_type = "Large Batch" if USE_LARGE_BATCH else "Small Batch"
    print(f"🔄 Starting profiling run ({batch_type})...")
    print(f"📊 Analyzing {len(urls)} URLs with concurrency={CONCURRENCY}")
    print("=" * 60)

    results = asyncio.run(analyze_urls(urls, concurrency=CONCURRENCY, timeout=10))

    success = sum(
        1 for r in results if isinstance(r["status"], int) and r["status"] < 400
    )
    print(f"\n✅ Analysis complete! Processed {len(results)} URLs")
    print(f"   Successful: {success}, Failed: {len(results) - success}")
    return results


def profile_with_cprofile():
    """Profile using cProfile and save detailed stats."""
    print("\n" + "=" * 60)
    print("  cProfile - CPU Timing Analysis")
    print("=" * 60 + "\n")

    profiler = cProfile.Profile()
    profiler.enable()

    # Run the analysis
    run_analysis()

    profiler.disable()

    # Save raw profile data
    profiler.dump_stats("cprofile_output.prof")
    print("\n💾 Saved: cprofile_output.prof")

    # Print human-readable stats
    print("\n" + "=" * 60)
    print("  Top 20 Functions by Cumulative Time")
    print("=" * 60)

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats(20)

    # Save detailed stats to file
    with open("cprofile_output.txt", "w", encoding="utf-8") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats(50)
    print("\n💾 Saved: cprofile_output.txt")

    return stats


def main():
    """Main entry point for profiling."""
    print("\n" + "=" * 60)
    print("  Web Performance Analyzer - Profiling")
    print("=" * 60)

    # Run cProfile
    profile_with_cprofile()

    print("\n" + "=" * 60)
    print("  Memory Profiling with memray")
    print("=" * 60)
    print("\nFor memory profiling (use --large for 1250 URLs):")
    print("\n  python -m memray run -o memray_output.bin profile_analyzer.py --large")
    print("  python -m memray stats memray_output.bin")
    print("  python -m memray flamegraph memray_output.bin -o flamegraph.html")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
