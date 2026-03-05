# Torbox — Usenet Service

> ⚠️ **PRO PLAN ONLY** — All endpoints in this file will return a `PLAN_RESTRICTION` error on Free, Essential, and Standard plans. Always verify `user.plan == "pro"` before calling any of these endpoints.

> **Prerequisite:** Load `auth-and-plans.md` first. Load `quirks-and-errors.md` when debugging.

---

## Create Usenet Download

Uses `multipart/form-data`. Provide either an NZB link or an `.nzb` file.

```bash
# Via NZB link
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "link=https://example.com/file.nzb" \
  -F "name=My Download" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload

# Via NZB file
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/file.nzb" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `link` | formData | string | No | NZB URL (required if `file` not provided) |
| `file` | formData | file | No | NZB file (required if `link` not provided) |
| `name` | formData | string | No | Custom name |
| `password` | formData | string | No | Archive password |
| `post_processing` | formData | integer | No | See post-processing options below (default: `-1`) |
| `as_queued` | formData | boolean | No | Add to queue (default: `false`) |

**`post_processing` values:**
| Value | Behavior |
|-------|----------|
| `-1` | Repair, extract, delete originals (**Recommended**) |
| `0` | Raw download only — no repair or extraction |
| `1` | Repair using PAR2, no extraction |
| `2` | Repair and extract, keep originals |
| `3` | Repair, extract, and delete originals (same as `-1`) |

---

## Control Usenet Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "usenet_id": 123}' \
  https://api.torbox.app/v1/api/usenet/controlusenetdownload
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `delete`, `pause`, or `resume` |
| `usenet_id` | body | integer | No | Usenet download ID (omit if `all=true`) |
| `all` | body | boolean | No | Apply to all (default: `false`) |

---

## Get Usenet List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/mylist?offset=0&limit=50"
```

---

## Request Usenet Download Link

```bash
curl "https://api.torbox.app/v1/api/usenet/requestdl?\
token=YOUR_TOKEN&\
usenet_id=123&\
file_id=0&\
zip_link=false&\
redirect=false"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | API key |
| `usenet_id` | query | integer | Yes | Usenet download ID |
| `file_id` | query | integer | No | File index (default: `0`) |
| `zip_link` | query | boolean | No | Return as zip (default: `false`) |
| `redirect` | query | boolean | No | Return direct URL (default: `false`) |

> ⚠️ Note: Usenet uses `usenet_id` here, but `usenet_download_id` in the edit endpoint. See `quirks-and-errors.md`.

---

## Check Cached Usenet

```bash
# POST (recommended for multiple hashes)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123..."]}' \
  "https://api.torbox.app/v1/api/usenet/checkcached?format=object"

# GET (single or comma-separated hashes)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/checkcached?hash=abc123&format=object"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hashes` | body | array | Yes (POST) | Array of hashes (max 100) |
| `hash` | query | string | Yes (GET) | Hash or repeated `hash=` params |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

---

## Edit Usenet Download

```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "usenet_download_id": 123,
    "name": "New Name",
    "tags": ["tag1", "tag2"],
    "alternative_hashes": ["hash1", "hash2"]
  }' \
  https://api.torbox.app/v1/api/usenet/editusenetdownload
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `usenet_download_id` | body | integer | Yes | Usenet download ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | Array of tag strings |
| `alternative_hashes` | body | array | No | Array of alternative hash strings |
