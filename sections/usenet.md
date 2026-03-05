# Usenet

## Usenet Service

⚠️ **PRO PLAN ONLY** — Will fail with error on Free/Essential/Standard plans.

### Create Usenet Download

Uses `multipart/form-data` for NZB file uploads.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "link=https://example.com/file.nzb" \
  -F "name=My Download" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `link` | formData | string | No | NZB link (required if `file` not provided) |
| `file` | formData | file | No | NZB file (required if `link` not provided) |
| `name` | formData | string | No | Custom name |
| `password` | formData | string | No | Password |
| `post_processing` | formData | integer | No | Post-processing option (default: `-1`) |
| `as_queued` | formData | boolean | No | Add to queue (default: `false`) |

### Control Usenet Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "usenet_id": 123}' \
  https://api.torbox.app/v1/api/usenet/controlusenetdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `delete`, `pause`, or `resume` |
| `usenet_id` | body | integer | No | Usenet download ID |
| `all` | body | boolean | No | Apply to all (default: `false`) |

### Get Usenet List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/mylist?offset=0&limit=50"
```

### Request Usenet Download Link

```bash
curl "https://api.torbox.app/v1/api/usenet/requestdl?\
token=YOUR_TOKEN&\
usenet_id=123&\
file_id=0&\
zip_link=false&\
redirect=false"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | API key |
| `usenet_id` | query | integer | Yes | Usenet download ID |
| `file_id` | query | integer | No | File index (default: `0`) |
| `zip_link` | query | boolean | No | Return as zip (default: `false`) |
| `redirect` | query | boolean | No | Return direct URL (default: `false`) |

### Check Cached Usenet

```bash
# POST with JSON body
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123..."]}' \
  "https://api.torbox.app/v1/api/usenet/checkcached?format=object"

# GET with query params
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/checkcached?hash=abc123&format=object"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hashes` | body | array | Yes (POST) | Array of hashes (max 100) |
| `hash` | query | string/array | Yes (GET) | Hash or comma-separated hashes |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

### Edit Usenet Download

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

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `usenet_download_id` | body | integer | Yes | Usenet download ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | Array of tag strings |
| `alternative_hashes` | body | array | No | Array of alternative hash strings |
