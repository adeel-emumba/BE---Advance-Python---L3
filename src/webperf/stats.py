"""
Utility helpers for aggregating statistics from fetched URL results.
"""

from typing import List, Dict, Any


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute high‑level statistics from the analyzer results.

    Time Complexity: O(n) where n is the number of results.
    - Counting success/failures: O(n) - single pass through results
    - Computing average latency: O(n) - filter latencies + sum
    Overall: O(n) - linear scan with constant-time operations

    Space Complexity: O(n) for latencies list (worst case).
    """

    total = len(results)
    success = sum(
        1 for r in results if isinstance(r["status"], int) and r["status"] < 400
    )
    failures = total - success

    latencies = [r["latency_ms"] for r in results if r["latency_ms"] is not None]
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else None

    return {
        "total_requests": total,
        "successful_requests": success,
        "failed_requests": failures,
        "average_latency_ms": avg_latency,
    }


__all__ = ["summarize"]
