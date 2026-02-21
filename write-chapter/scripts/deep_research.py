#!/usr/bin/env python3
"""Deep research utility for chapter writing. Runs multiple search queries across
different source types and produces a consolidated research brief.

Usage:
    python3 deep_research.py "topic 1" "topic 2" ... [--output FILE]

Searches for each topic across: general web, academic papers (arxiv/scholar),
tech blogs, and industry reports. Outputs a JSON research brief.

Requirements: pip3 install ddgs
"""
import argparse
import json
import sys
import time

def search(query: str, max_results: int = 8):
    from ddgs import DDGS
    ddgs = DDGS()
    raw = ddgs.text(query, max_results=max_results)
    results = []
    for r in raw:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("href", r.get("url", "")),
            "snippet": r.get("body", r.get("excerpt", ""))[:400]
        })
    return results

def research_topic(topic: str) -> dict:
    """Run multiple search angles for a single topic."""
    queries = {
        "academic": f"site:arxiv.org OR site:scholar.google.com {topic} survey paper",
        "blogs_tech": f"{topic} architecture best practices blog 2024 2025",
        "industry": f"{topic} enterprise production real-world case study",
        "general": topic
    }

    topic_results = {"topic": topic, "sources": {}}
    for category, query in queries.items():
        try:
            results = search(query, max_results=5)
            topic_results["sources"][category] = results
            time.sleep(1)  # rate limit
        except Exception as e:
            topic_results["sources"][category] = [{"error": str(e)}]
    return topic_results

def main():
    parser = argparse.ArgumentParser(description="Deep research for chapter topics")
    parser.add_argument("topics", nargs="+", help="Topics to research")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    try:
        from ddgs import DDGS
    except ImportError:
        print("Error: ddgs package not installed. Run: pip3 install ddgs", file=sys.stderr)
        sys.exit(1)

    brief = {"research_brief": [], "total_sources": 0}
    for topic in args.topics:
        print(f"Researching: {topic}...", file=sys.stderr)
        result = research_topic(topic)
        brief["research_brief"].append(result)
        for cat, sources in result["sources"].items():
            brief["total_sources"] += len([s for s in sources if "error" not in s])

    output = json.dumps(brief, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Research brief written to {args.output} ({brief['total_sources']} sources)", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
