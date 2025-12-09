import asyncio
from webperf.analyzer import analyze_urls


def test_analyze_urls_single() -> None:
    urls = ["https://example.com"]
    results = asyncio.run(analyze_urls(urls, concurrency=1, timeout=5))
    assert len(results) == 1
    assert results[0]["url"] == "https://example.com"
    assert "latency_ms" in results[0]
    assert "status" in results[0]


def test_analyze_urls_multiple() -> None:
    urls = ["https://example.com", "https://httpbin.org/get"]
    results = asyncio.run(analyze_urls(urls, concurrency=2, timeout=5))
    assert len(results) == 2
    for r in results:
        assert "url" in r
        assert "latency_ms" in r
        assert "status" in r
