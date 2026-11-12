import copy
from html import unescape
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build", ROOT / "scripts" / "build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class FeedTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "prompts.json").read_text())
        self.outputs = builder.build(self.data, "https://example.org/prompts")
        self.feed = json.loads(self.outputs["feed.json"])
        self.rss = ET.fromstring(self.outputs["feed.xml"])

    def test_every_prompt_survives_both_formats(self):
        originals = {p["id"]: p for p in self.data["prompts"]}
        self.assertEqual(len(self.feed["items"]), len(originals))
        self.assertEqual(len(self.rss.findall("channel/item")), len(originals))
        rss = {i.findtext("guid"): i for i in self.rss.findall("channel/item")}
        for item in self.feed["items"]:
            prompt = originals[item["_prompt"]["id"]]
            self.assertEqual(item["content_text"], prompt["prompt"])
            self.assertEqual(item["_prompt"]["source"], prompt["source"])
            self.assertEqual(item["external_url"] if "external_url" in item else None, prompt["source"]["url"])
            self.assertEqual(item["title"], rss[item["id"]].findtext("title"))
            self.assertIn(prompt["prompt"], unescape(rss[item["id"]].findtext("description")))
            self.assertEqual(rss[item["id"]].find("guid").attrib["isPermaLink"], "false")

    def test_shared_tweet_has_distinct_ids(self):
        items = [i for i in self.feed["items"] if i.get("external_url", "").endswith("2117400205314421058")]
        self.assertEqual(len(items), 3)
        self.assertEqual(len({i["id"] for i in items}), 3)

    def test_linked_workflow_keeps_summary_label_and_both_sources(self):
        item = next(i for i in self.feed["items"] if i["_prompt"]["id"] == "read-only-codebase-simplification-audit")
        self.assertEqual(item["_prompt"]["text_kind"], "summary")
        source = item["_prompt"]["source"]
        self.assertEqual(source["status"], "verified")
        self.assertEqual(source["related_urls"][0]["status"], "unverified")
        description = next(i.findtext("description") for i in self.rss.findall("channel/item") if i.findtext("guid") == item["id"])
        for url in (source["url"], source["related_urls"][0]["url"]):
            self.assertIn(url, description)
            self.assertIn(url, self.outputs["PROMPTS.md"])
        self.assertIn("Editorial summary", description)

    def test_builds_and_ids_are_stable(self):
        self.assertEqual(self.outputs, builder.build(self.data, "https://example.org/prompts"))
        changed = copy.deepcopy(self.data)
        changed["prompts"][0]["prompt"] += " Edited."
        other = json.loads(builder.build(changed, "https://another.example/collection")["feed.json"])
        self.assertEqual([i["id"] for i in self.feed["items"]], [i["id"] for i in other["items"]])
        self.assertEqual([i["date_published"] for i in self.feed["items"]], [i["date_published"] for i in other["items"]])

    def test_hosted_feeds_link_to_readable_github_catalog(self):
        config = json.loads((ROOT / "feed-config.json").read_text())
        outputs = builder.build(self.data, config["base_url"], config["home_url"], config["catalog_url"])
        feed = json.loads(outputs["feed.json"])
        rss = ET.fromstring(outputs["feed.xml"])
        self.assertEqual(feed["feed_url"], config["base_url"] + "/feed.json")
        self.assertEqual(feed["home_page_url"], config["home_url"])
        self.assertEqual(rss.findtext("channel/link"), config["home_url"])
        self.assertEqual(rss.find("channel/{http://www.w3.org/2005/Atom}link").attrib["href"], config["base_url"] + "/feed.xml")
        for item in feed["items"]:
            self.assertEqual(item["url"], config["catalog_url"] + "#" + item["_prompt"]["id"])
        self.assertNotIn("localhost", outputs["feed.json"])
        self.assertNotIn("localhost", outputs["feed.xml"])

    def test_xml_escaping_preserves_literal_content(self):
        self.data["prompts"][0]["prompt"] = '<module> & "quotes" → café\n```python\nx = 1\n```'
        outputs = builder.build(self.data, "https://example.org")
        rss = ET.fromstring(outputs["feed.xml"])
        description = next(i.findtext("description") for i in rss.findall("channel/item") if i.findtext("guid").endswith(":browser-testing"))
        self.assertIn("&lt;module&gt; &amp;", description)
        self.assertIn(self.data["prompts"][0]["prompt"], unescape(description))
        self.assertIn("````text", outputs["PROMPTS.md"])

    def test_rejects_ambiguous_ids_and_invalid_metadata(self):
        variants = []
        duplicate = copy.deepcopy(self.data)
        duplicate["prompts"].append(duplicate["prompts"][0])
        variants.append(duplicate)
        bad_date = copy.deepcopy(self.data)
        bad_date["prompts"][0]["added_on"] = "yesterday"
        variants.append(bad_date)
        bad_source = copy.deepcopy(self.data)
        bad_source["prompts"][0]["source"]["status"] = "missing"
        variants.append(bad_source)
        bad_related = copy.deepcopy(self.data)
        bad_related["prompts"][0]["source"]["related_urls"] = [{"url": "javascript:alert(1)", "label": "Tweet", "status": "verified"}]
        variants.append(bad_related)
        bad_kind = copy.deepcopy(self.data)
        bad_kind["prompts"][0]["text_kind"] = "unknown"
        variants.append(bad_kind)
        for variant in variants:
            with self.assertRaises(ValueError):
                builder.build(variant, "https://example.org")
        with self.assertRaises(ValueError):
            builder.build(self.data, "relative/path")


if __name__ == "__main__":
    unittest.main()
