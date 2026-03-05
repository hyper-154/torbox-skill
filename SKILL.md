---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, search engines, streaming, and cloud integrations using pure HTTP API calls. Use when managing downloads, checking cache status, uploading to cloud storage, or automating Torbox workflows. Supports torrent creation/management, usenet downloads, web downloads, RSS feeds, queued downloads, user account operations, device auth, search engines, streaming, and integrations with Google Drive, Dropbox, OneDrive, and more.
---

# Torbox API Skill

Pure HTTP API for managing torrents, Usenet, web downloads, search engines, streaming, and cloud integrations through Torbox. No SDK dependencies required.

## Base URL

```
https://api.torbox.app
```

## Authentication

All authenticated endpoints require an API key via Bearer token header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.torbox.app/v1/api/user/me
```

⚠️ **Free plan does NOT have API access** — You must upgrade to Essential ($3/mo) or higher.

For unauthenticated endpoints (status, stats, changelogs), no token is needed.

---

## STEP 1: Check User Plan (CRITICAL)

**ALWAYS check the user's plan first** before performing operations. Different plans have different limitations.

### Get User Info

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/me?settings=true"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "active_downloads": 3,
    "max_downloads": 10,
    "storage_used": 1073741824
  }
}
```

### Plan Limitations

| Feature | Free ($0/mo) | Essential ($3/mo) | Standard ($5/mo) | Pro ($10/mo) |
|---------|--------------|-------------------|------------------|--------------|
| **Concurrent Slots** | 1 | 3 | 5 | 10 |
| **Downloads Per Month** | 10 | Unlimited | Unlimited | Unlimited |
| **Max File Size** | 10GB | 200GB | 200GB | 1TB |
| **Seed Time** | 24h cooldown | 24 hours | 14 days | 30 days |
| **Max Speed** | 250Mbps | 1Gbps | 1Gbps | 80Gbps |
| **Traffic Priority** | Reduced | Normal | Normal | High |
| **Usenet Downloads** | ❌ NO | ❌ NO | ❌ NO | ✅ Unlimited |
| **API Access** | ❌ NO | ✅ YES | ✅ YES | ✅ YES |
| **3rd Party Apps** | ❌ NO | ✅ YES | ✅ YES | ✅ YES |
| **Web Player** | ❌ NO | ❌ NO | ❌ NO | ✅ YES |
| **RSS Feeds** | ❌ NO | Limited | Limited | ✅ Unlimited |

### Plan-Based Decision Tree

```
IF user.plan == "free":
    - ❌ NO API ACCESS — Cannot use this skill
    - Limited to exactly 10 downloads per month
    - Must upgrade to Essential+ for API access and unlimited downloads

IF user.plan == "essential":
    - Max 3 concurrent downloads
    - Unlimited downloads per month
    - 200GB max file size
    - 24h seed time only
    - CANNOT use Usenet endpoints (will fail)
    - NO Web Player
    - Limited RSS

IF user.plan == "standard":
    - Max 5 concurrent downloads
    - Unlimited downloads per month
    - 200GB max file size
    - 14 days seed time
    - CANNOT use Usenet endpoints (will fail)
    - NO Web Player
    - Limited RSS

IF user.plan == "pro":
    - Max 10 concurrent downloads
    - Unlimited downloads per month
    - ✅ CAN use Usenet endpoints (unlimited)
    - 30 days seed time
    - 1TB max file size
    - ✅ Web Player enabled
    - ✅ Unlimited RSS feeds
    - 80Gbps speed
```

### Python Helper to Check Plan

```python
import os
import urllib.request
import urllib.parse
import json

def api_call(method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
    """
    Make an API call to Torbox with proper error handling.
    """
    torbox_token = os.environ.get("TORBOX_API_KEY")
    if not torbox_token:
        raise RuntimeError("Set TORBOX_API_KEY environment variable")

    url = f"https://api.torbox.app{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {torbox_token}")
    
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}")
        raise
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        raise

# Check plan before any operation
user = api_call("GET", "/v1/api/user/me", params={"settings": "true"})
print(f"Plan: {user['data']['plan']}")
print(f"Active: {user['data']['active_downloads']}/{user['data']['max_downloads']}")

if user['data']['plan'] != 'pro':
    print("WARNING: Usenet requires Pro plan")
```

---

## General Service

Unauthenticated endpoints for API health and info.

### Get API Status

```bash
curl https://api.torbox.app/
```
**Example Response:**
```json
{
  "success": true,
  "data": "API is online",
  "detail": "Welcome to Torbox API"
}
```

### Get Stats

```bash
# All-time stats
curl https://api.torbox.app/v1/api/stats
```
**Example Response:**
```json
{
  "success": true,
  "data": {
    "total_users": 50000,
    "total_torrents": 1200000
  }
}
```

### Speedtest Files

```bash
curl "https://api.torbox.app/v1/api/speedtest?test_length=short&region=all"
```

**Parameters:**
| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `test_length` | query | string | No | `short` or `long` |
| `region` | query | string | No | CDN region (omit to get all available) |

---

## User Service

Manage user account, subscriptions, devices, and search engines.

### Refresh Token

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"session_token": "YOUR_SESSION_TOKEN"}' \
  https://api.torbox.app/v1/api/user/refreshtoken
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `session_token` | body | string | Yes | Your current session token |

**Example Response:**
```json
{
  "success": true,
  "data": "NEW_TOKEN_STRING"
}
```

### Device Authentication (OAuth)

Used for TV apps or CLI tools to login without entering passwords.

```bash
# 1. Start Device Auth
curl "https://api.torbox.app/v1/api/user/auth/device/start?app=MyApp"

# Returns {"data": {"device_code": "ABCDEF", "user_code": "12345", "verification_uri": "https://torbox.app/device"}}

# 2. Poll for Token (until user authorizes)
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"device_code": "ABCDEF"}' \
  https://api.torbox.app/v1/api/user/auth/device/token
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `app` | query | string | No | App name (default: "Third Party App") |
| `device_code` | body | string | Yes | Device code from start endpoint |

### Add Referral

```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/addreferral?referral=REFERRAL_CODE"
```

### Delete Account

```bash
# 1. Get confirmation code
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/getconfirmation

# 2. Confirm deletion
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_token": "YOUR_TOKEN", "confirmation_code": 123456}' \
  https://api.torbox.app/v1/api/user/deleteme
```

### Subscriptions & Transactions

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/subscriptions
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/transactions
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/user/transaction/pdf?transaction_id=xyz" -o receipt.pdf
```

### Search Engines

Configure search engines like Prowlarr, Jackett, or NZBHydra.

```bash
# Get Search Engines
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/user/settings/searchengines"

# Add Search Engine
curl -X PUT -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"type": "prowlarr", "url": "http://prowlarr:9696", "apikey": "key", "download_type": "torrents"}' \
  https://api.torbox.app/v1/api/user/settings/addsearchengines

# Modify Search Engine
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"id": 1, "type": "prowlarr", "url": "http://prowlarr:9696", "apikey": "key", "download_type": "torrents"}' \
  https://api.torbox.app/v1/api/user/settings/modifysearchengines

# Control Search Engine
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"operation": "enable", "id": 1, "all": false}' \
  https://api.torbox.app/v1/api/user/settings/controlsearchengines
```

---

## Torrents Service

Requires Essential+ plan. Check concurrent slot availability.

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
| `seed` | formData | integer | No | Seed ratio limit |
| `allow_zip` | formData | boolean | No | Allow zip output (default: `true`) |
| `name` | formData | string | No | Custom name |
| `as_queued` | formData | boolean | No | Add to queue if slots full (default: `false`) |
| `add_only_if_cached` | formData | boolean | No | Only add if cached (default: `false`) |

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

### Edit Torrent

```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"torrent_id": 123, "name": "New Name"}' \
  https://api.torbox.app/v1/api/torrents/edittorrent
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `torrent_id` | body | integer | Yes | Torrent ID |
| `name` | body | string | No | New name |
| `tags` | body | array | No | Tags list |
| `alternative_hashes` | body | array | No | Alternate hashes |

### Magnet to File

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"magnet": "magnet:?xt=urn:btih:..."}' \
  https://api.torbox.app/v1/api/torrents/magnettofile
```

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
| `operation` | body | string | Yes | `reannounce`, `delete`, or `resume` |
| `torrent_id` | body | integer | No | Torrent ID (omit if `all=true`) |
| `all` | body | boolean | No | Apply to all torrents (default: `false`) |

### Get Torrent List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50&bypass_cache=false"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `limit` | query | integer | No | Max items to return (default: `1000`, max: `1000`) |
| `id` | query | integer | No | Filter by specific torrent ID |
| `bypass_cache` | query | boolean | No | Skip cache (default: `false`) |

### Check Cached

Content-Type conflicts are solved via HTTP method context:
- `GET` uses query string lists.
- `POST` uses `application/json`.

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
| `hashes` | body | array | Yes | Array of torrent hashes (max 100) |
| `format` | query | string | No | `object` or `list` (default: `object`) |
| `list_files` | query | boolean | No | Include file list (default: `false`) |

### Get Queued Torrents

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/getqueued"
```

### Request Download Link

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
| `file_id` | query | integer | No | Specific file index (default: `0` = all files as zip if `zip_link=true`) |
| `zip_link` | query | boolean | No | Return as zip (default: `false`) |
| `redirect` | query | boolean | No | Return direct URL (default: `false`) |
| `user_ip` | query | string | No | Your IP for CDN selection |

**Example Response:**
```json
{
  "success": true,
  "data": "https://cdn1.torbox.app/download/..."
}
```

### Get Torrent Info

```bash
# By POST with magnet/file (multipart)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:..." \
  https://api.torbox.app/v1/api/torrents/torrentinfo

# By GET with hash (query)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/torrentinfo?hash=ABC123&timeout=30"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `hash` | query | string | No | Torrent hash (for GET) |
| `timeout` | query | integer | No | Timeout in seconds (for GET, default: `30`) |
| `use_cache_lookup` | query | boolean | No | Use cached data (for GET, default: `false`) |
| `magnet` | formData| string | No | Magnet link (for POST) |
| `file` | formData| file | No | .torrent file (for POST) |

### Export Torrent Data

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/exportdata?torrent_id=123&type=magnet"
```

---

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

---

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

---

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

---

## Streaming Service

### Create Stream & Get Data

```bash
# 1. Create Stream
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/stream/createstream?id=123&type=torrent&file_id=0"

# 2. Get Stream Data (Playback URL)
curl "https://api.torbox.app/v1/api/stream/getstreamdata?token=YOUR_TOKEN&presigned_token=abc123def456"
```

---

## Notifications Service

Get and manage user notifications.

### Get Notifications

```bash
# JSON format (authenticated)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/mynotifications

# RSS format (token in query)
curl "https://api.torbox.app/v1/api/notifications/rss?token=YOUR_TOKEN"
```

**Example Response (JSON):**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "type": "download_complete",
      "message": "Torrent 'My File' has finished downloading",
      "created_at": "2024-01-15T10:30:00Z",
      "read": false
    }
  ]
}
```

### Clear Notifications

```bash
# Clear all notifications
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear

# Clear specific notification
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear/123
```

**Parameters (for specific clear):**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | string | Yes | Notification ID |

### Test Notification

Sends a test notification to verify your notification settings. Rate limited to 1 per minute.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/test
```

---

## Integrations Service

Upload downloads to cloud storage. Supported platforms: `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.

### Upload to Cloud

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "google_token": "GOOGLE_OAUTH_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/googledrive
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | body | integer | **Yes**| Download ID |
| `file_id` | body | integer | No | File index (default: `0`) |
| `zip` | body | boolean | No | Upload as zip (default: `false`) |
| `type` | body | string | No | `torrent`, `usenet`, or `webdl` |
| `{provider}_token`| body | string | **Yes**| OAuth token for respective provider |

### Manage Transfer Jobs

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/jobs
```

---

## API Implementation Details & Quirks

When implementing the TorBox API, be aware of the following undocumented or easily confused behaviors:

### 1. `seed` Parameter in Create Torrent
The `seed` parameter is not a ratio limit, but a **behavioral setting** for seeding on private trackers:
- **`1` (Auto)**: Follows default account settings.
- **`2` (Always)**: Forces the torrent to continue seeding indefinitely (prevents Hit and Runs).
- **`3` (Never)**: Stops seeding immediately after download completes.

### 2. `post_processing` in Usenet
Determines PAR2 repair and archive extraction behavior (default is `-1`):
- **`-1` (Default)**: Repair, extract, and delete original archives (Recommended).
- **`0` (None)**: Download raw files only; no repair or extraction.
- **`1` (Repair)**: Verify and repair using PAR2, but do not extract.
- **`2` (Repair & Unpack)**: Repair and extract, keeping original archives.
- **`3` (Repair, Unpack, & Delete)**: Same as `-1`.

### 3. `file_id` and `zip_link` Semantics
Across all `requestdl` endpoints (Torrents, Usenet, Webdl):
- **`zip_link=true`**: Returns a `.zip` archive of the entire download package. `file_id` is generally ignored.
- **`zip_link=false`**: Returns a direct link to a single file. You **must** specify a valid `file_id` (defaults to `0`, which is usually the first file). For streaming (e.g., in Stremio), always use `zip_link=false`.

### 4. Check Cached Multi-Hash
The `checkcached` endpoints support multiple hashes, but the format differs by HTTP method:
- **GET**: Use multiple query parameters: `?hash=HASH1&hash=HASH2`
- **POST**: Pass a JSON array in the body: `{"hashes": ["HASH1", "HASH2"]}`

### 5. Inconsistent ID Naming
ID fields vary depending on the service and the specific endpoint being called:
- **Torrents**: `torrent_id` (used everywhere for torrents).
- **Usenet**: `usenet_id` (used in control and requestdl), `usenet_download_id` (used in edit).
- **Web Downloads**: `web_id` (used in requestdl), `webdl_id` (used in control and edit).
- **Queued / RSS**: `queued_id`, `rss_feed_id`.

### 6. Content-Type Requirements
Pay close attention to required Content-Types when creating downloads:
- **Torrents (`createtorrent`)**: Requires `multipart/form-data` (to support optional `.torrent` file uploads).
- **Usenet (`createusenetdownload`)**: Requires `multipart/form-data` (to support optional `.nzb` file uploads).
- **Web Downloads (`createwebdownload`)**: Requires `application/x-www-form-urlencoded`.

---

## Error Handling

All responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "detail": "optional message"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "ERROR_CODE",
  "detail": "Error description"
}
```

**Common Error Codes:**
| Code | Description |
|------|-------------|
| `ENDPOINT_NOT_FOUND` | Invalid URL |
| `VALIDATION_ERROR` | Invalid parameters |
| `AUTHENTICATION_FAILED` | Invalid or missing token |
| `RATE_LIMITED` | Too many requests (see Rate Limits) |
| `PLAN_RESTRICTION` | Feature requires higher plan |
| `SLOTS_FULL` | Concurrent download limit reached |
| `FILE_TOO_LARGE` | Exceeds plan size limit |
