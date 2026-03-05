# Web Downloads Service

## Web Downloads Service

### Create Web Download

Uses `application/x-www-form-urlencoded`.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "link=https://example.com/file.zip" \
  -d "password=optional" \
  -d "name=Custom Name" \
  https://api.torbox.app/v1/api/webdl/createwebdownload
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `link` | formData| string | **Yes**| Download URL |
| `password` | formData| string | No | Password |
| `name` | formData| string | No | Custom name |
| `as_queued` | formData| boolean| No | Add to queue (default: `false`) |

### Control Web Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "webdl_id": 123}' \
  https://api.torbox.app/v1/api/webdl/controlwebdownload
```

### Get Web Download List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/webdl/mylist?offset=0&limit=50"
```

### Request Web Download Link

```bash
curl "https://api.torbox.app/v1/api/webdl/requestdl?token=YOUR_TOKEN&web_id=123"
```

### Get Supported Hosters

```bash
curl https://api.torbox.app/v1/api/webdl/hosters
```

### Check Cached Web Download

```bash
# POST with JSON body
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123..."]}' \
  "https://api.torbox.app/v1/api/webdl/checkcached?format=object"

# GET with query params
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/webdl/checkcached?hash=abc123&format=object"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hashes` | body | array | Yes (POST) | Array of hashes (max 100) |
| `hash` | query | string/array | Yes (GET) | Hash or comma-separated hashes |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

### Edit Web Download

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
