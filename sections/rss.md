# Rss

## RSS Service

### Add RSS Feed

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://.../feed.rss",
    "name": "My Feed",
    "do_regex": "include_pattern",
    "dont_regex": "exclude_pattern",
    "scan_interval": 60,
    "dont_older_than": 7,
    "pass_check": false,
    "rss_type": "torrent",
    "torrent_seeding": 1
  }' \
  https://api.torbox.app/v1/api/rss/addrss
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `url` | body | string | **Yes** | RSS feed URL |
| `name` | body | string | **Yes** | Feed name |
| `do_regex` | body | string | No | Include pattern regex |
| `dont_regex` | body | string | No | Exclude pattern regex |
| `dont_older_than` | body | integer | No | Skip items older than N days |
| `scan_interval` | body | integer| No | Scan interval in minutes (min: `10`, default: `60`) |
| `pass_check` | body | boolean | No | Allow duplicate URLs (default: `false`) |
| `rss_type` | body | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `torrent_seeding` | body | integer | No | Seeding: `1` (auto), `2` (always), `3` (never). Default: `1`. |

### Control RSS Feed

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "rss_feed_id": 123}' \
  https://api.torbox.app/v1/api/rss/controlrss
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `update`, `delete`, `pause`, or `resume` |
| `rss_feed_id` | body | integer | Yes | RSS feed ID |

### Modify RSS Feed

Modifies an existing RSS feed's settings.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rss_feed_id": 123,
    "name": "Updated Feed Name",
    "do_regex": "include_pattern",
    "dont_regex": "exclude_pattern",
    "scan_interval": 60,
    "dont_older_than": 7,
    "pass_check": false,
    "rss_type": "torrent",
    "torrent_seeding": 1
  }' \
  https://api.torbox.app/v1/api/rss/modifyrss
```

**Parameters:** (Same as Add RSS Feed, with the addition of `rss_feed_id`)

### Get RSS Feeds & Items

```bash
# Get all feeds or a specific feed by ID
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/rss/getfeeds?id=123"

# Get items scraped from a specific feed
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/rss/getfeeditems?rss_feed_id=123"
```

