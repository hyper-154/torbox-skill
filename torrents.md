# Torbox — Torrents Service

Requires **Essential plan or higher**. Always check concurrent slot availability before creating.

> **Prerequisite:** Load `auth-and-plans.md` first. Load `quirks-and-errors.md` when debugging.

---

## Create Torrent

Uses `multipart/form-data`. Provide either a magnet link or a `.torrent` file.

**Via Magnet Link:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:ABC123..." \
  -F "seed=2" \
  -F "allow_zip=true" \
  -F "name=My Torrent" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**Via Torrent File:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/file.torrent" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `magnet` | formData | string | No | Magnet link (required if `file` not provided) |
| `file` | formData | file | No | .torrent file (required if `magnet` not provided) |
| `seed` | formData | integer | No | Seeding behavior: `1`=Auto, `2`=Always, `3`=Never |
| `allow_zip` | formData | boolean | No | Allow zip output (default: `true`) |
| `name` | formData | string | No | Custom name |
| `as_queued` | formData | boolean | No | Queue if slots full (default: `false`) |
| `add_only_if_cached` | formData | boolean | No | Skip if not cached (default: `false`) |

**Example Response:**
```json
{
  "success": true,
  "data": { "torrent_id": 98765, "name": "My Torrent", "hash": "abc123def456" }
}
```

**Async version:** `POST /v1/api/torrents/asynccreatetorrent` — returns immediately, same parameters.

---

## Edit Torrent

```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"torrent_id": 123, "name": "New Name"}' \
  https://api.torbox.app/v1/api/torrents/edittorrent
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `torrent_id` | body | integer | Yes | Torrent ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | Tags list |
| `alternative_hashes` | body | array | No | Alternate hashes |

---

## Control Torrent

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "torrent_id": 123, "all": false}' \
  https://api.torbox.app/v1/api/torrents/controltorrent
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `reannounce`, `delete`, or `resume` |
| `torrent_id` | body | integer | No | Torrent ID (omit if `all=true`) |
| `all` | body | boolean | No | Apply to all torrents (default: `false`) |

---

## Get Torrent List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50&bypass_cache=false"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `limit` | query | integer | No | Max items (default: `1000`, max: `1000`) |
| `id` | query | integer | No | Filter by specific torrent ID |
| `bypass_cache` | query | boolean | No | Skip cache (default: `false`) |

---

## Check Cached

```bash
# POST (recommended for multiple hashes)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123...", "def456..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object&list_files=false"

# GET (single or multiple hashes)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/checkcached?hash=abc123&hash=def456&format=object"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hashes` | body | array | Yes (POST) | Array of torrent hashes (max 100) |
| `hash` | query | string | Yes (GET) | Hash or repeated `hash=` params |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

---

## Get Queued Torrents

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/getqueued"
```

---

## Request Download Link

```bash
curl "https://api.torbox.app/v1/api/torrents/requestdl?\
token=YOUR_TOKEN&\
torrent_id=123&\
file_id=0&\
zip_link=false&\
redirect=false&\
user_ip=YOUR_IP"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | Your API key |
| `torrent_id` | query | integer | Yes | The torrent ID |
| `file_id` | query | integer | No | Specific file index (default: `0`) |
| `zip_link` | query | boolean | No | Return as zip (default: `false`) |
| `redirect` | query | boolean | No | Return direct URL (default: `false`) |
| `user_ip` | query | string | No | Your IP for CDN selection |

**Example Response:**
```json
{ "success": true, "data": "https://cdn1.torbox.app/download/..." }
```

> For streaming (e.g. Stremio), always use `zip_link=false` with a valid `file_id`.

---

## Get Torrent Info

```bash
# By hash (GET)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/torrentinfo?hash=ABC123&timeout=30"

# By magnet or file (POST, multipart)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:..." \
  https://api.torbox.app/v1/api/torrents/torrentinfo
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Torrent hash (GET only) |
| `timeout` | query | integer | No | Timeout in seconds (default: `30`) |
| `use_cache_lookup` | query | boolean | No | Use cached data (default: `false`) |
| `magnet` | formData | string | No | Magnet link (POST only) |
| `file` | formData | file | No | .torrent file (POST only) |

---

## Magnet to File

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"magnet": "magnet:?xt=urn:btih:..."}' \
  https://api.torbox.app/v1/api/torrents/magnettofile
```

---

## Export Torrent Data

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/exportdata?torrent_id=123&type=magnet"
```
