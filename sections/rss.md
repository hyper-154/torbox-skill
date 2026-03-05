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
    "rss_type": "torrent"
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
| `scan_interval` | body | integer| No | Scan interval in minutes (default: `60`) |
| `rss_type` | body | string | No | `torrent` or `usenet` (default: `torrent`) |

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
| `operation` | body | string | Yes | `delete`, `pause`, or `resume` |
| `rss_feed_id` | body | integer | Yes | RSS feed ID |

### Modify RSS Feed

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
    "rss_type": "torrent",
    "torrent_seeding": 1
  }' \
  https://api.torbox.app/v1/api/rss/modifyrss
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `rss_feed_id` | body | integer | Yes | RSS feed ID |
| `name` | body | string | No | New feed name |
| `do_regex` | body | string | No | Include pattern regex |
| `dont_regex` | body | string | No | Exclude pattern regex |
| `scan_interval` | body | integer | No | Scan interval in minutes (default: `60`) |
| `dont_older_than` | body | integer | No | Skip items older than N days |
| `rss_type` | body | string | No | `torrent` or `usenet` (default: `torrent`) |
| `torrent_seeding` | body | integer | No | Seed ratio limit (default: `1`) |

### Get RSS Feeds & Items

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/rss/getfeeds"
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/rss/getfeeditems?rss_feed_id=123"
```
