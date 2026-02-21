#!/usr/bin/env python3
"""Web search utility for chapter research. Uses DuckDuckGo via the ddgs library.

Usage:
    python3 web_search.py "search query" [--max-results N] [--news]

Output: JSON array of results with title, url, and snippet.

Requirements: pip3 install ddgs
"""
import argparse
import json
import sys

def search(query: str, max_results: int = 10, news: bool = False):
    try:
        from ddgs import DDGS
    except ImportError:
        print("Error: ddgs package not installed. Run: pip3 install ddgs", file=sys.stderr)
        sys.exit(1)

    ddgs = DDGS()
    if news:
        raw = ddgs.news(query, max_results=max_results)
    else:
        raw = ddgs.text(query, max_results=max_results)

    results = []
    for r in raw:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("href", r.get("url", "")),
            "snippet": r.get("body", r.get("excerpt", ""))[:300]
        })
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web search for chapter research")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--max-results", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--news", action="store_true", help="Search news instead of web")
    args = parser.parse_args()

    results = search(args.query, args.max_results, args.news)
    print(json.dumps(results, indent=2))
