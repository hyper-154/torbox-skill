# Torbox — API Quirks & Error Handling

Load this file alongside any service file when implementing or debugging Torbox API calls.

---

## Known Quirks

### 1. `seed` Parameter Semantics (Create Torrent)

The `seed` field is a **behavioral setting**, not a ratio number:

| Value | Behavior |
|-------|----------|
| `1` | Auto — follows default account settings |
| `2` | Always — forces indefinite seeding (prevents Hit and Runs on private trackers) |
| `3` | Never — stops seeding immediately after download completes |

### 2. `post_processing` for Usenet

Controls PAR2 repair and archive extraction (default: `-1`):

| Value | Behavior |
|-------|----------|
| `-1` | Repair, extract, delete originals (**Recommended**) |
| `0` | Raw download only — no repair or extraction |
| `1` | Repair using PAR2, no extraction |
| `2` | Repair and extract, keep originals |
| `3` | Repair, extract, delete originals (same as `-1`) |

### 3. `file_id` and `zip_link` Semantics

Applies to all `requestdl` endpoints (Torrents, Usenet, Web Downloads):

- **`zip_link=true`**: Returns a `.zip` of the entire download. `file_id` is ignored.
- **`zip_link=false`**: Returns a direct link to a single file. Must provide a valid `file_id` (default `0` = first file).
- **For streaming** (e.g. Stremio): Always use `zip_link=false` with a specific `file_id`.

### 4. Multi-Hash Format Differs by HTTP Method

For all `checkcached` endpoints:

- **GET**: Repeat the query param — `?hash=HASH1&hash=HASH2`
- **POST**: JSON array in body — `{"hashes": ["HASH1", "HASH2"]}`

### 5. Inconsistent ID Field Names

ID field names vary by service and endpoint type — do not assume they are the same:

| Service | Endpoint Type | Field Name |
|---------|--------------|------------|
| Torrents | All | `torrent_id` |
| Usenet | Control & requestdl | `usenet_id` |
| Usenet | Edit | `usenet_download_id` |
| Web Downloads | requestdl | `web_id` |
| Web Downloads | Control & edit | `webdl_id` |
| Queued | Control | `queued_id` |
| RSS | All | `rss_feed_id` |

### 6. Content-Type Requirements

Each create endpoint has a specific required Content-Type:

| Endpoint | Required Content-Type |
|----------|----------------------|
| `POST /torrents/createtorrent` | `multipart/form-data` |
| `POST /usenet/createusenetdownload` | `multipart/form-data` |
| `POST /webdl/createwebdownload` | `application/x-www-form-urlencoded` |
| All JSON body endpoints | `application/json` |

---

## Error Response Format

All responses follow this structure:

```json
{
  "success": false,
  "error": "ERROR_CODE",
  "detail": "Human-readable description"
}
```

## Common Error Codes

| Code | Description |
|------|-------------|
| `ENDPOINT_NOT_FOUND` | Invalid URL or path |
| `VALIDATION_ERROR` | Missing or invalid parameters |
| `AUTHENTICATION_FAILED` | Invalid or missing Bearer token |
| `RATE_LIMITED` | Too many requests |
| `PLAN_RESTRICTION` | Feature requires a higher plan |
| `SLOTS_FULL` | Concurrent download limit reached for this plan |
| `FILE_TOO_LARGE` | File exceeds plan's max size limit |

## Handling Errors in Python

```python
import urllib.error
import json

try:
    result = api_call("POST", "/v1/api/torrents/createtorrent", ...)
except urllib.error.HTTPError as e:
    body = json.loads(e.read().decode())
    code = body.get("error", "UNKNOWN")
    detail = body.get("detail", "")

    if code == "PLAN_RESTRICTION":
        print("Upgrade your plan to use this feature.")
    elif code == "SLOTS_FULL":
        print("All download slots are in use. Wait or delete an active download.")
    elif code == "AUTHENTICATION_FAILED":
        print("Check your TORBOX_API_KEY environment variable.")
    else:
        print(f"API error {code}: {detail}")
```
