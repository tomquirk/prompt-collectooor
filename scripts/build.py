#!/usr/bin/env python3
"""Generate RSS, JSON Feed, and a readable catalog using Python's standard library."""

import argparse
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ATOM = "http://www.w3.org/2005/Atom"
ET.register_namespace("atom", ATOM)


def validate(data):
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported schema_version")
    for key in ("title", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"Missing {key}")
    if not isinstance(data.get("prompts"), list):
        raise ValueError("prompts must be a list")
    seen = set()
    for p in data["prompts"]:
        for key in ("id", "title", "category", "use_when", "prompt", "added_on"):
            if not isinstance(p.get(key), str) or not p[key].strip():
                raise ValueError(f"Missing {key} in prompt")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", p["id"]) or p["id"] in seen:
            raise ValueError(f"Invalid or duplicate id: {p['id']}")
        seen.add(p["id"])
        date.fromisoformat(p["added_on"])
        if p.get("scope") not in ("project", "machine"):
            raise ValueError(f"Invalid scope: {p['id']}")
        if p.get("text_kind", "collected") not in ("collected", "summary"):
            raise ValueError(f"Invalid text_kind: {p['id']}")
        tags = p.get("tags")
        if not isinstance(tags, list) or not tags or any(not isinstance(t, str) or not t.strip() for t in tags):
            raise ValueError(f"Invalid tags: {p['id']}")
        source = p.get("source", {})
        if source.get("status") not in ("missing", "unverified", "verified"):
            raise ValueError(f"Invalid source status: {p['id']}")
        if source["status"] == "missing":
            if source.get("url") is not None or source.get("author") is not None:
                raise ValueError("Missing source must have null url and author")
        else:
            url = source.get("url")
            if not isinstance(url, str) or urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                raise ValueError(f"Source must have an absolute HTTPS URL: {p['id']}")
            if not isinstance(source.get("author"), str) or not source["author"].strip():
                raise ValueError(f"Source must have an author: {p['id']}")
        related_urls = source.get("related_urls", [])
        if not isinstance(related_urls, list):
            raise ValueError("related_urls must be a list")
        for related in related_urls:
            url = related.get("url")
            if not isinstance(url, str) or urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                raise ValueError("Related source must have an absolute HTTPS URL")
            if not isinstance(related.get("label"), str) or not related["label"].strip():
                raise ValueError("Related source must have a label")
            if related.get("status") not in ("unverified", "verified"):
                raise ValueError("Invalid related source status")


def published(p):
    # Collection date at midnight UTC; never inferred from a tweet ID.
    return datetime.combine(date.fromisoformat(p["added_on"]), datetime.min.time(), timezone.utc)


def build(data, base_url, home_url=None, catalog_url=None):
    validate(data)
    parsed = urlsplit(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("base-url must be an absolute HTTP(S) URL without a query or fragment")
    base = base_url.rstrip("/")
    home = home_url or base + "/"
    catalog_url = catalog_url or base + "/PROMPTS.md"
    for url in (home, catalog_url):
        parsed_url = urlsplit(url)
        if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc or parsed_url.fragment:
            raise ValueError("home-url and catalog-url must be absolute HTTP(S) URLs without fragments")
    # Stable ordering within each collection date; builds do not invent new dates.
    entries = sorted(data["prompts"], key=lambda p: p["id"])
    entries.sort(key=lambda p: p["added_on"], reverse=True)
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": data["title"],
        "description": data["description"],
        "home_page_url": home,
        "feed_url": base + "/feed.json",
        "language": "en",
        "items": [],
    }
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for key, value in (("title", data["title"]), ("link", home), ("description", data["description"]), ("language", "en")):
        ET.SubElement(channel, key).text = value
    ET.SubElement(channel, f"{{{ATOM}}}link", href=base + "/feed.xml", rel="self", type="application/rss+xml")
    for p in entries:
        identity = "urn:prompt-collection:" + p["id"]
        url = catalog_url + "#" + p["id"]
        item = {
            "id": identity,
            "url": url,
            "title": p["title"],
            "content_text": p["prompt"],
            "summary": p["use_when"],
            "date_published": published(p).isoformat(),
            "tags": list(dict.fromkeys([p["category"], *p["tags"]])),
            "_prompt": {key: p[key] for key in ("id", "category", "use_when", "scope", "added_on", "source")},
        }
        item["_prompt"]["text_kind"] = p.get("text_kind", "collected")
        if p["source"]["url"]:
            item["external_url"] = p["source"]["url"]
            item["authors"] = [{"name": p["source"]["author"]}]
        feed["items"].append(item)
        xml_item = ET.SubElement(channel, "item")
        ET.SubElement(xml_item, "title").text = p["title"]
        ET.SubElement(xml_item, "link").text = url
        ET.SubElement(xml_item, "guid", isPermaLink="false").text = identity
        ET.SubElement(xml_item, "pubDate").text = format_datetime(published(p), usegmt=True)
        description = f"<p>{escape(p['use_when'])}</p><pre>{escape(p['prompt'])}</pre>"
        if p.get("text_kind") == "summary":
            description = "<p>Editorial summary; follow the source link for the full prompt.</p>" + description
        if p["source"]["url"]:
            description += f'<p>Source: <a href="{escape(p["source"]["url"], quote=True)}">{escape(p["source"]["author"])}</a> ({escape(p["source"]["status"])})</p>'
        else:
            description += "<p>Source: not provided.</p>"
        for related in p["source"].get("related_urls", []):
            description += f'<p>{escape(related["label"])}: <a href="{escape(related["url"], quote=True)}">{escape(related["url"])}</a> ({escape(related["status"])})</p>'
        ET.SubElement(xml_item, "description").text = description
        for tag in item["tags"]:
            ET.SubElement(xml_item, "category").text = tag
    ET.indent(rss, space="  ")
    catalog = ["# Prompt catalog", "", "Generated from `prompts.json`; edit that file and rebuild.", ""]
    for category in dict.fromkeys(p["category"] for p in data["prompts"]):
        catalog.extend([f"## {category}", ""])
        for p in data["prompts"]:
            if p["category"] != category:
                continue
            # Longer fences preserve prompts that themselves contain code fences.
            fence = "`" * max(3, max((len(m[0]) + 1 for m in re.finditer(r"`+", p["prompt"])), default=0))
            catalog.extend([f'<a id="{p["id"]}"></a>', "", f'### {p["title"]}', "", p["use_when"], "", fence + "text", p["prompt"], fence, ""])
            if p.get("text_kind") == "summary":
                catalog.extend(["Editorial summary; follow the source link for the full prompt.", ""])
            source = p["source"]
            label = f'[{source["author"]}]({source["url"]}) ({source["status"]})' if source["url"] else "not provided."
            catalog.extend(["Source: " + label, ""])
            for related in source.get("related_urls", []):
                catalog.extend([f'{related["label"]}: [{related["url"]}]({related["url"]}) ({related["status"]})', ""])
    return {
        "feed.json": json.dumps(feed, ensure_ascii=False, indent=2) + "\n",
        "feed.xml": ET.tostring(rss, encoding="unicode", xml_declaration=True) + "\n",
        "PROMPTS.md": "\n".join(catalog),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="Override the feed hosting root from feed-config.json")
    parser.add_argument("--home-url", help="Override the human-readable collection URL")
    parser.add_argument("--catalog-url", help="Override the readable catalog URL, without a fragment")
    args = parser.parse_args()
    data = json.loads((ROOT / "prompts.json").read_text())
    config = json.loads((ROOT / "feed-config.json").read_text())
    base = args.base_url or config["base_url"]
    home = args.home_url or (None if args.base_url else config.get("home_url"))
    catalog = args.catalog_url or (None if args.base_url else config.get("catalog_url"))
    for name, content in build(data, base, home, catalog).items():
        (ROOT / name).write_text(content, encoding="utf-8")
    print(f"Built {len(data['prompts'])} prompts into feed.xml, feed.json, and PROMPTS.md")


if __name__ == "__main__":
    main()
