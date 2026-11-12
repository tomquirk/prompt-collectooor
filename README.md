# prompt-collection

A feed of prompts collected from X, designed for RSS readers and bots that suggest useful prompts to a user.

Subscribe: [RSS](https://raw.githubusercontent.com/tomquirk/prompt-collection/main/feed.xml) · [JSON Feed](https://raw.githubusercontent.com/tomquirk/prompt-collection/main/feed.json)

| File | Purpose |
| --- | --- |
| [`prompts.json`](prompts.json) | Source of truth: prompt text, stable IDs, tags, context hints, and attribution |
| [`feed.json`](feed.json) | JSON Feed 1.1, with structured metadata for bots |
| [`feed.xml`](feed.xml) | RSS 2.0 for feed readers |
| [`PROMPTS.md`](PROMPTS.md) | Readable catalog generated from the same data |
| [`CONSUMING.md`](CONSUMING.md) | How a bot can select suggestions and remember what it has shown |
| [`feed-config.json`](feed-config.json) | Hosting URLs used by the default build |

The collection contains 20 entries. Formatting and obvious typos have been cleaned up. Most source posts have not been independently verified; one prompt has no source. Long external workflows may be represented by a labeled editorial summary linking to the full prompt. Context hints and tags are editorial additions to help consumers choose relevant prompts.

## Local preview

Requires Python 3.10 or newer; no packages to install. From this project directory:

```sh
python3 scripts/build.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Read RSS at <http://localhost:8000/feed.xml> or JSON Feed at <http://localhost:8000/feed.json>. A bot running locally can also read `feed.json` directly. The Markdown catalog is rendered by GitHub or a Markdown viewer; the basic local server serves it as a file.

The feed is a collection, not a running bot. A consumer chooses when to poll, which prompts fit the user's context, and when to suggest them. It does not automatically discover new tweets or send notifications. The public feeds are served from this repository; no recurring bot is scheduled.

## Add or update a prompt

Edit `prompts.json`, then run `python3 scripts/build.py`. Commit the source and generated files together when using Git.

- Give every prompt a unique, permanent `id`. Two prompts from the same tweet still need different IDs.
- Keep the prompt text in `prompt`; use `use_when` for an editorial context hint. For a summary linking to an external workflow, set `text_kind` to `summary`; otherwise it defaults to `collected`.
- Set `category`, `tags`, and `scope` (`project` or `machine`).
- Set `added_on` to the collection date in `YYYY-MM-DD` format. This is not the tweet's publication date. Feed dates use that date at midnight UTC.
- Use a source object with `url`, `author`, and `status`. Status is `unverified`, `verified`, or `missing`. For missing sources, use null for both URL and author.
- Optionally include `source.related_urls`: a list of objects with `url`, `label`, and `status` (`unverified` or `verified`) to preserve supporting links. Verification refers to checking the linked content, not endorsing the prompt's recommendations.
- Preserve IDs and collection dates when editing an entry so readers do not treat it as a new prompt. Keep separate update history if you need revision notifications.

Do not edit `feed.xml`, `feed.json`, or `PROMPTS.md` directly; they are generated. Rebuilding unchanged data produces unchanged files.

## Publishing updates

The default build uses `feed-config.json`: feed files are served from GitHub's raw URLs, while collection and catalog links open the readable GitHub pages. Rebuild and push the source and generated files together to update subscribers.

For another static host, update the configuration or override its URLs for a build:

```sh
python3 scripts/build.py --base-url https://example.org/prompt-collection
```

`example.org` is only a placeholder. Host `feed.xml`, `feed.json`, and `PROMPTS.md` under that root, then give the feed URL to a reader or bot. Use `--home-url` and `--catalog-url` when readable pages live elsewhere. For fully local links use `--base-url http://localhost:8000`; rebuild with no overrides before publishing again. Localhost URLs are only reachable on the same computer.

## Checks

```sh
python3 -m unittest discover -s tests
```

Formats: [RSS 2.0 specification](https://www.rssboard.org/rss-specification) and [JSON Feed 1.1](https://www.jsonfeed.org/version/1.1/).
