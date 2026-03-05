# Torrents

## Torrents Service

Requires Essential+ plan. Check concurrent slot availability.

### Infrastructure & Compatibility
- **Satellites:** TorBox uses its own network of "satellites" to download content. Performance may vary during high-load periods.
- **Private Trackers:** Nearly all private trackers (including very restrictive ones) are compatible with TorBox.

### Create Torrent

Creates a torrent from magnet link or torrent file. Uses `multipart/form-data` for file uploads.

**Using Magnet Link:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:ABC123..." \
  -F "seed=2" \
  -F "allow_zip=true" \
  -F "name=My Torrent" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**Using Torrent File:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/file.torrent" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `magnet` | formData | string | No | Magnet link (required if `file` not provided) |
| `file` | formData | file | No | .torrent file (required if `magnet` not provided) |
| `seed` | formData | integer | No | Seeding preference: 1 (auto), 2 (seed), 3 (don't seed). Default: 1. |
| `allow_zip` | formData | boolean | No | Allow zip output for 100+ files (default: `true`) |
| `name` | formData | string | No | Custom display name |
| `as_queued` | formData | boolean | No | Instantly queue the torrent (bypassed on Free plan) |
| `add_only_if_cached` | formData | boolean | No | Only add the download if it is already cached on TorBox |

**Example Response:**
```json
{
  "success": true,
  "data": {
    "torrent_id": 98765,
    "name": "My Torrent",
    "hash": "abc123def456"
  }
}
```

**Async version:** `POST /v1/api/torrents/asynccreatetorrent` (returns immediately, processes in background. Same parameters.)

### Edit Torrent Item

```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"torrent_id": 123, "name": "New Name", "tags": ["movie", "4k"], "alternative_hashes": ["def456..."]}' \
  https://api.torbox.app/v1/api/torrents/edittorrent
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `torrent_id` | body | integer | Yes | Torrent ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | List of tags to apply |
| `alternative_hashes` | body | array | No | List of alternative hashes for the same content |

### Control Torrent

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "torrent_id": 123, "all": false}' \
  https://api.torbox.app/v1/api/torrents/controltorrent
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `reannounce`, `delete`, `pause`, or `resume` |
| `torrent_id` | body | integer | No | Torrent ID (required unless `all=true`) |
| `all` | body | boolean | No | Apply operation to all torrents (default: `false`) |

### Get Torrent List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50&bypass_cache=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `limit` | query | integer | No | Max items to return (default: `1000`) |
| `id` | query | integer | No | Filter by specific torrent ID (returns object) |
| `bypass_cache` | query | boolean | No | Force fresh info from database (default: `false`) |

### Check Cached

Check if torrents are already available on TorBox servers for instant download.

**GET (comma-separated hashes):**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/checkcached?hash=abc123def456,fed654cba321&format=list&list_files=true"
```

**POST (JSON list):**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123...", "def456..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object&list_files=false"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Comma-separated list of hashes (for GET) |
| `hashes` | body | array | No | Array of torrent hashes (for POST) |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

### Get Queued Torrents

Returns torrents that are currently in the download queue.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/getqueued"
```

### Request Download Link

**Note:** `token` is required as a query parameter for this endpoint.

```bash
curl "https://api.torbox.app/v1/api/torrents/requestdl?\
token=YOUR_TOKEN&\
torrent_id=123&\
file_id=0&\
zip_link=false&\
redirect=false&\
user_ip=YOUR_IP"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | Your API key |
| `torrent_id` | query | integer | Yes | The torrent ID |
| `file_id` | query | integer | No | Specific file ID |
| `zip_link` | query | boolean | No | Request as zip (required if `file_id` omitted) |
| `redirect` | query | boolean | No | Redirect to CDN link (default: `false`) |
| `user_ip` | query | string | No | User's IP to select closest CDN |

### Get Torrent Info

**By POST with magnet/file:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:..." \
  -F "peers_only=true" \
  https://api.torbox.app/v1/api/torrents/torrentinfo
```

**By GET with hash:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/torrentinfo?hash=ABC123&timeout=30&use_cache_lookup=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Torrent hash (for GET) |
| `timeout` | query | integer | No | Time to search on P2P network (default: `10`) |
| `use_cache_lookup` | query | boolean | No | Use pre-cached request if available (default: `false`) |
| `magnet` | formData| string | No | Magnet link (for POST) |
| `file` | formData| file | No | .torrent file (for POST) |
| `peers_only` | formData| boolean | No | Quick lookup for seeds/peers only (no metadata) |


### Export Torrent Data

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/exportdata?torrent_id=123&type=magnet"
```
