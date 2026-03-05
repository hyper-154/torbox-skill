# Usenet

## Usenet Service

⚠️ **PRO PLAN ONLY** — Will fail with error on Free/Essential/Standard plans.

### Create Usenet Download

Creates a Usenet download from an NZB link or file. Uses `multipart/form-data`.

**⚠️ PRO PLAN ONLY** — Will fail with error on Free/Essential/Standard plans.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "link=https://example.com/file.nzb" \
  -F "name=My Download" \
  -F "post_processing=-1" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `link` | formData | string | No | NZB link (required if `file` not provided) |
| `file` | formData | file | No | NZB file (required if `link` not provided) |
| `name` | formData | string | No | Custom display name |
| `password` | formData | string | No | Extraction password for RAR archives |
| `post_processing` | formData | integer | No | `-1` (Repair/Extract/Delete), `0` (None), `1` (Repair), `2` (Repair/Unpack), `3` (Same as -1) |
| `as_queued` | formData | boolean | No | Instantly queue the download |
| `add_only_if_cached` | formData | boolean | No | Only add the download if it is already cached on TorBox |

### Control Usenet Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "usenet_id": 123, "all": false}' \
  https://api.torbox.app/v1/api/usenet/controlusenetdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `delete`, `pause`, or `resume` |
| `usenet_id` | body | integer | No | Usenet download ID (required unless `all=true`) |
| `all` | body | boolean | No | Apply operation to all downloads (default: `false`) |

### Get Usenet List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/mylist?offset=0&limit=50&bypass_cache=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `limit` | query | integer | No | Max items to return (default: `1000`) |
| `id` | query | integer | No | Filter by specific Usenet download ID (returns object) |
| `bypass_cache` | query | boolean | No | Force fresh info from database (default: `false`) |

### Request Usenet Download Link

**Note:** `token` is required as a query parameter for this endpoint.

```bash
curl "https://api.torbox.app/v1/api/usenet/requestdl?\
token=YOUR_TOKEN&\
usenet_id=123&\
file_id=0&\
zip_link=false&\
redirect=false&\
user_ip=YOUR_IP"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | Your API key |
| `usenet_id` | query | integer | Yes | The Usenet download ID |
| `file_id` | query | integer | No | Specific file ID |
| `zip_link` | query | boolean | No | Request as zip (required if `file_id` omitted) |
| `redirect` | query | boolean | No | Redirect to CDN link (default: `false`) |
| `user_ip` | query | string | No | User's IP to select closest CDN |

### Check Cached Usenet

**GET (comma-separated hashes):**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/checkcached?hash=abc123def456&format=list&list_files=true"
```

**POST (JSON list):**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123..."]}' \
  "https://api.torbox.app/v1/api/usenet/checkcached?format=object&list_files=false"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Comma-separated list of hashes (for GET) |
| `hashes` | body | array | No | Array of hashes (for POST) |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

### Edit Usenet Download Item

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

