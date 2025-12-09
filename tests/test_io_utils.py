from pathlib import Path
from webperf.io_utils import load_urls


def test_load_urls_json(tmp_path: Path) -> None:
    # Create a JSON file
    p = tmp_path / "urls.json"
    data = ["https://example.com", "https://httpbin.org/get"]
    p.write_text(str(data).replace("'", '"'), encoding="utf-8")

    urls = load_urls(p)
    assert len(urls) == 2
    assert "https://example.com" in urls
    assert "https://httpbin.org/get" in urls


def test_load_urls_csv(tmp_path: Path) -> None:
    p = tmp_path / "urls.csv"
    csv_content = "url\nhttps://example.com\nhttps://httpbin.org/get\n"
    p.write_text(csv_content, encoding="utf-8")

    urls = load_urls(p)
    assert len(urls) == 2
    assert "https://example.com" in urls
    assert "https://httpbin.org/get" in urls
