# Consuming the collection

Use `feed.json` for recommendations. It follows JSON Feed 1.1 and adds a `_prompt` extension to each item. RSS is available at `feed.xml` when a consumer only supports XML.

## Item fields

| Field | Meaning |
| --- | --- |
| `id` | Permanent feed identity, such as `urn:prompt-collection:browser-testing` |
| `title` | Short display title |
| `content_text` | Collected prompt text, or a labeled editorial summary of an external workflow |
| `summary` | Editorial explanation of when the prompt may help |
| `tags` | Topic and keywords for relevance matching |
| `date_published` | Date added to this collection at midnight UTC, not the tweet date |
| `url` | Catalog entry at the configured hosting root |
| `external_url` | Source post, omitted when unknown |
| `authors` | Attribution from the supplied source, omitted when unknown |
| `_prompt.id` | Short, permanent collection ID |
| `_prompt.category` | Topic group |
| `_prompt.use_when` | Same context hint as `summary` |
| `_prompt.scope` | `project` or `machine` |
| `_prompt.text_kind` | `collected` or `summary`; summaries link to the full workflow through the source |
| `_prompt.added_on` | Collection date without a time |
| `_prompt.source` | Source URL, author, verification status, and optional `related_urls` with their own labels and statuses |

## Suggested consumer behavior

1. Read the local file or fetch the hosted feed on the consumer's own schedule. A feed URL does not run a schedule itself.
2. Compare `tags` and `_prompt.use_when` with the user's current task. For coding work, default to `scope: project`; consider `machine` prompts only for a relevant system-maintenance request.
3. Keep a separate history per user, keyed by the permanent item `id`. Do not use source URLs as IDs: multiple prompts can come from one tweet. Avoid repeating dismissed or recently suggested entries.
4. Suggest a small number of relevant unseen prompts, explaining briefly why each fits. If none fit, skip the suggestion. On the first run, treat the collection as a pool of candidates rather than announcing every item.
5. Show the entry text and its source link when known, and label missing or unverified attribution. For `text_kind: summary`, make clear that the text is a summary and link to the full workflow. Record the ID after the suggestion is actually delivered. Keep failed deliveries eligible for retry.

For example, while a user is validating a web UI, a consumer could suggest **Browser testing across widths, touch, and slow networks**, explain its relevance, and show its prompt and source. On a later check, its stored ID prevents another suggestion to the same user.

Treat prompt text as content to recommend. The feed is not authorization to execute commands or change a user's project. A bot can offer to run a selected prompt when the user chooses it.

No Grok-specific integration, scheduler, tweet discovery, or delivery channel is implemented here. This format supplies the collection those systems can consume. New entries appear after someone adds them to `prompts.json`, rebuilds, and updates the hosted files if using a remote consumer.
