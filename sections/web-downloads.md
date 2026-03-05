# Web Downloads Service

## Web Downloads Service

TorBox supports debriding links from various file hosters, including:
- **Baidu (Pan.Baidu.Com):** Free debriding for Baidu links.
- **Bunkr:** Fast, anonymous downloading and streaming from Bunkr links.

### Create Web Download

Creates a web download from a direct link. Uses `application/x-www-form-urlencoded`.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "link=https://example.com/file.zip" \
  -d "password=optional" \
  -d "name=Custom Name" \
  -d "as_queued=true" \
  https://api.torbox.app/v1/api/webdl/createwebdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `link` | formData| string | **Yes**| Direct link to the file |
| `password` | formData| string | No | File password if required |
| `name` | formData| string | No | Custom display name |
| `as_queued` | formData| boolean| No | Instantly queue the download |
| `add_only_if_cached` | formData| boolean| No | Only add the download if it is already cached on TorBox |

### Control Web Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "webdl_id": 123, "all": false}' \
  https://api.torbox.app/v1/api/webdl/controlwebdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `operation` | body | string | Yes | `delete` |
| `webdl_id` | body | integer | No | Web download ID (required unless `all=true`) |
| `all` | body | boolean | No | Apply operation to all web downloads (default: `false`) |

### Get Web Download List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/webdl/mylist?offset=0&limit=50&bypass_cache=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `limit` | query | integer | No | Max items to return (default: `1000`) |
| `id` | query | integer | No | Filter by specific web download ID (returns object) |
| `bypass_cache` | query | boolean | No | Force fresh info from database (default: `false`) |

### Request Web Download Link

**Note:** `token` is required as a query parameter for this endpoint.

```bash
curl "https://api.torbox.app/v1/api/webdl/requestdl?\
token=YOUR_TOKEN&\
web_id=123&\
file_id=0&\
zip_link=false&\
redirect=false&\
user_ip=YOUR_IP"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | Yes | Your API key |
| `web_id` | query | integer | Yes | The web download ID |
| `file_id` | query | integer | No | Specific file ID |
| `zip_link` | query | boolean | No | Request as zip (required if `file_id` omitted) |
| `redirect` | query | boolean | No | Redirect to CDN link (default: `false`) |
| `user_ip` | query | string | No | User's IP to select closest CDN |

### Get Supported Hosters

Returns a list of debrid-supported file hosters.

```bash
curl https://api.torbox.app/v1/api/webdl/hosters
```

### Check Cached Web Download

**GET (comma-separated hashes):**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/webdl/checkcached?hash=abc123def456&format=list"
```

**POST (JSON list):**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123..."]}' \
  "https://api.torbox.app/v1/api/webdl/checkcached?format=object"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Comma-separated list of hashes (for GET) |
| `hashes` | body | array | No | Array of hashes (for POST) |
| `format` | query | string | No | `object` or `list` (default: `object`) |

### Edit Web Download Item

```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "webdl_id": 123,
    "name": "New Name",
    "tags": ["tag1", "tag2"],
    "alternative_hashes": ["hash1", "hash2"]
  }' \
  https://api.torbox.app/v1/api/webdl/editwebdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `webdl_id` | body | integer | Yes | Web download ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | Array of tag strings |
| `alternative_hashes` | body | array | No | Array of alternative hash strings |

