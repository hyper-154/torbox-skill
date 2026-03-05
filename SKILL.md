---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, and cloud integrations using pure HTTP API calls. Use when managing downloads, checking cache status, uploading to cloud storage, or automating Torbox workflows. Supports torrent creation/management, usenet downloads, web downloads, RSS feeds, queued downloads, user account operations, and integrations with Google Drive, Dropbox, OneDrive, and more.
---

# Torbox API Skill

Pure HTTP API for managing torrents, Usenet, web downloads, and cloud integrations through Torbox. No SDK dependencies required.

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
    - Limited to 10 downloads per month
    - Must upgrade to Essential+ for API access

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

# Use environment variable for security
TORBOX_TOKEN = os.environ.get("TORBOX_API_KEY")
if not TORBOX_TOKEN:
    raise RuntimeError("Set TORBOX_API_KEY environment variable")

def api_call(method, endpoint, data=None, params=None):
    """Make an API call with proper error handling."""
    url = f"https://api.torbox.app{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TORBOX_TOKEN}")
    
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
user = api_call("GET", "/v1/api/user/me", params={"settings": True})
print(f"Plan: {user['data']['plan']}")
print(f"Active: {user['data']['active_downloads']}/{user['data']['max_downloads']}")

if user['data']['plan'] != 'pro':
    print("WARNING: Usenet requires Pro plan")
```

---

## Services Overview

| Service | Description | Plan Required |
|---------|-------------|---------------|
| **General** | API status, stats, changelogs, speedtest | Any (unauth) |
| **Torrents** | Create, control, list, check cache, download | Essential+ |
| **Usenet** | Create, control, list, check cache NZB | **Pro only** |
| **Web Downloads** | Create, control, list web downloads | Essential+ |
| **Queued** | Manage queued downloads | Essential+ |
| **User** | User info, referrals, subscriptions | Essential+ |
| **RSS** | Manage RSS feeds | Essential+ (Pro=unlimited) |
| **Integrations** | Upload to cloud storage | Essential+ |
| **Notifications** | Get and clear notifications | Essential+ |

⚠️ **Free plan has NO API access** — Must upgrade to Essential ($3/mo) or higher.

---

## General Service

Unauthenticated endpoints for API health and info.

### Get API Status

```bash
curl https://api.torbox.app/
```

```python
import urllib.request
import json

req = urllib.request.Request("https://api.torbox.app/")
try:
    with urllib.request.urlopen(req) as resp:
        print(json.loads(resp.read().decode()))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
except urllib.error.URLError as e:
    print(f"Connection error: {e.reason}")
```

### Get Stats

```bash
# All-time stats
curl https://api.torbox.app/v1/api/stats

# Last 30 days
curl https://api.torbox.app/v1/api/stats/30days
```

### Get Changelogs

```bash
# RSS format
curl https://api.torbox.app/v1/api/changelogs/rss

# JSON format
curl https://api.torbox.app/v1/api/changelogs/json
```

### Speedtest Files

```bash
curl "https://api.torbox.app/v1/api/speedtest?test_length=short&region=all"
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `test_length` | string | No | `short` or `long` |
| `region` | string | No | CDN region (omit to get all available) |

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
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `magnet` | string | No | Magnet link (required if `file` not provided) |
| `file` | file | No | .torrent file (required if `magnet` not provided) |
| `seed` | integer | No | Seed ratio limit |
| `allow_zip` | boolean | No | Allow zip output (default: `true`) |
| `name` | string | No | Custom name |
| `as_queued` | boolean | No | Add to queue if slots full (default: `false`) |
| `add_only_if_cached` | boolean | No | Only add if cached (default: `false`) |

**Performance Tip:** Use `add_only_if_cached=true` to avoid wasting slots on non-cached torrents.

```bash
# Check cache first, then add
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes":["ABC123..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object"

# If cached, safe to add
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:ABC123..." \
  -F "add_only_if_cached=true" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**Async version:** `POST /v1/api/torrents/asynccreatetorrent` (returns immediately, processes in background)

### Control Torrent

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "torrent_id": 123, "all": false}' \
  https://api.torbox.app/v1/api/torrents/controltorrent
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `reannounce`, `delete`, or `resume` |
| `torrent_id` | integer | No | Torrent ID (omit if `all=true`) |
| `all` | boolean | No | Apply to all torrents (default: `false`) |

### Get Torrent List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50&bypass_cache=false"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `offset` | integer | No | Pagination offset (default: `0`) |
| `limit` | integer | No | Max items to return (default: `1000`, max: `1000`) |
| `id` | integer | No | Filter by specific torrent ID |
| `bypass_cache` | boolean | No | Skip cache (default: `false`) |

**Download States:**
- `downloading` — Currently downloading
- `uploading` — Currently seeding
- `stalled (no seeds)` — No seeds available
- `paused` — Paused
- `completed` — Downloaded (use `cached` for completion status)
- `cached` — Available on server
- `metaDL` — Downloading metadata (qBittorrent state)
- `checkingResumeData` — Checking resumable data (qBittorrent state)

### Check Cached

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123...", "def456..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object&list_files=false"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hashes` | array | Yes | Array of torrent hashes (max 100) |
| `format` | string | No | `object` or `list` (default: `object`) |
| `list_files` | boolean | No | Include file list (default: `false`) |

**Notes:**
- Max ~100 hashes per request
- Fast lookup (<1s per 100 hashes)
- 1-hour cache on server

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
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | Yes | Your API key |
| `torrent_id` | integer | Yes | The torrent ID |
| `file_id` | integer | No | Specific file index (default: `0` = all files as zip if `zip_link=true`) |
| `zip_link` | boolean | No | Return as zip (default: `false`) |
| `redirect` | boolean | No | Return direct URL (default: `false`) |
| `user_ip` | string | No | Your IP for CDN selection |

**Important:** `file_id=0` with `zip_link=false` returns the first file only. Use `zip_link=true` to get all files as a zip.

**Permalink for direct access:**
```
https://api.torbox.app/v1/api/torrents/requestdl?\
  token=YOUR_TOKEN&\
  torrent_id=NUMBER&\
  file_id=NUMBER&\
  redirect=true
```

- Link valid for 3 hours to START download
- Once started, unlimited time to complete
- Use `redirect=true` for permanent permalinks

### Get Torrent Info

```bash
# By hash
curl "https://api.torbox.app/v1/api/torrents/torrentinfo?\
hash=ABC123...&\
timeout=30&\
use_cache_lookup=false"

# By POST with magnet/file
curl -X POST \
  -F "magnet=magnet:?xt=urn:btih:..." \
  https://api.torbox.app/v1/api/torrents/torrentinfo
```

**Parameters (GET):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hash` | string | Yes | Torrent hash |
| `timeout` | integer | No | Timeout in seconds (default: `30`) |
| `use_cache_lookup` | boolean | No | Use cached data (default: `false`) |

### Export Torrent Data

```bash
# Export as magnet link
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/exportdata?torrent_id=123&type=magnet"

# Export as .torrent file
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/exportdata?torrent_id=123&type=file" \
  -o download.torrent
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `torrent_id` | integer | Yes | Torrent ID |
| `type` | string | Yes | `magnet` or `file` |

---

## Usenet Service

⚠️ **PRO PLAN ONLY** — Will fail with error on Free/Essential/Standard plans.

### Pre-Flight Check

```python
import os
import urllib.request
import urllib.error
import json

TORBOX_TOKEN = os.environ.get("TORBOX_API_KEY")
if not TORBOX_TOKEN:
    raise RuntimeError("Set TORBOX_API_KEY environment variable")

def check_pro_plan():
    req = urllib.request.Request(
        "https://api.torbox.app/v1/api/user/me",
        headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            user = json.loads(resp.read().decode())
            if user['data']['plan'] not in ['pro', 'premium']:
                print("ERROR: Usenet requires Pro plan")
                return False
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        return False
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        return False

if not check_pro_plan():
    exit(1)
```

### Create Usenet Download

Uses `multipart/form-data` for NZB file uploads.

**Using NZB Link:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "link=https://example.com/file.nzb" \
  -F "name=My Download" \
  -F "password=optional" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload
```

**Using NZB File:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/file.nzb" \
  https://api.torbox.app/v1/api/usenet/createusenetdownload
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `link` | string | No | NZB link (required if `file` not provided) |
| `file` | file | No | NZB file (required if `link` not provided) |
| `name` | string | No | Custom name |
| `password` | string | No | Password |
| `post_processing` | integer | No | Post-processing option (default: `-1`) |
| `as_queued` | boolean | No | Add to queue (default: `false`) |
| `add_only_if_cached` | boolean | No | Only add if cached (default: `false`) |

**Async:** `POST /v1/api/usenet/asynccreateusenetdownload`

### Control Usenet Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "usenet_id": 123}' \
  https://api.torbox.app/v1/api/usenet/controlusenetdownload
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `delete`, `pause`, or `resume` |
| `usenet_id` | integer | No | Usenet download ID |
| `all` | boolean | No | Apply to all (default: `false`) |

### Get Usenet List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/mylist?offset=0&limit=50"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `offset` | integer | No | Pagination offset (default: `0`) |
| `limit` | integer | No | Max items (default: `1000`) |
| `id` | integer | No | Filter by specific ID |

### Request Download Link

```bash
curl "https://api.torbox.app/v1/api/usenet/requestdl?\
token=YOUR_TOKEN&\
usenet_id=123&\
file_id=0&\
zip_link=false&\
redirect=false"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | Yes | API key |
| `usenet_id` | integer | Yes | Usenet download ID |
| `file_id` | integer | No | File index (default: `0`) |
| `zip_link` | boolean | No | Return as zip (default: `false`) |
| `redirect` | boolean | No | Return direct URL (default: `false`) |

---

## Web Downloads Service

Requires Essential+ plan.

### Create Web Download

Uses `application/x-www-form-urlencoded` (different from Torrents/Usenet which use `multipart/form-data` for file uploads).

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
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `link` | string | **Yes** | Download URL |
| `password` | string | No | Password |
| `name` | string | No | Custom name |
| `as_queued` | boolean | No | Add to queue (default: `false`) |
| `add_only_if_cached` | boolean | No | Only add if cached (default: `false`) |

**Note:** Web Downloads use `application/x-www-form-urlencoded` because they don't support file uploads (unlike Torrents and Usenet which accept `.torrent` and `.nzb` files).

### Get Supported Hosters

```bash
curl https://api.torbox.app/v1/api/webdl/hosters
```

### Control Web Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "webdl_id": 123}' \
  https://api.torbox.app/v1/api/webdl/controlwebdownload
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `delete`, `pause`, or `resume` |
| `webdl_id` | integer | No | Web download ID |
| `all` | boolean | No | Apply to all (default: `false`) |

### Get Web Download List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/webdl/mylist?offset=0&limit=50"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `offset` | integer | No | Pagination offset (default: `0`) |
| `limit` | integer | No | Max items (default: `1000`) |
| `id` | integer | No | Filter by specific ID |
| `bypass_cache` | boolean | No | Skip cache (default: `false`) |

### Request Download Link

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
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | Yes | API key |
| `web_id` | integer | Yes | Web download ID |
| `file_id` | integer | No | File index (default: `0`) |
| `zip_link` | boolean | No | Return as zip (default: `false`) |
| `redirect` | boolean | No | Return direct URL (default: `false`) |
| `user_ip` | string | No | Your IP for CDN selection |

---

## Queued Service

### Get Queued Downloads

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/queued/getqueued?type=torrent&offset=0&limit=50"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `offset` | integer | No | Pagination offset (default: `0`) |
| `limit` | integer | No | Max items (default: `1000`) |
| `id` | integer | No | Filter by specific ID |
| `bypass_cache` | boolean | No | Skip cache (default: `false`) |

### Control Queued

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "queued_id": 123}' \
  https://api.torbox.app/v1/api/queued/controlqueued
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `delete`, `pause`, or `resume` |
| `queued_id` | integer | No | Queued item ID |
| `all` | boolean | No | Apply to all (default: `false`) |

---

## User Service

### Get User Info

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/me?settings=true"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `settings` | boolean | No | Include settings (default: `false`) |

**Key Fields in Response:**
```json
{
  "success": true,
  "data": {
    "id": 12345,
    "email": "user@example.com",
    "plan": "pro",              // "free", "essential", "standard", "pro"
    "active_downloads": 3,
    "max_downloads": 10,        // Plan limit
    "storage_used": 1073741824  // Bytes used
  }
}
```

### Subscriptions & Transactions

```bash
# Get subscriptions
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/user/subscriptions

# Get transactions
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/user/transactions

# Get transaction as PDF
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/transaction/pdf?transaction_id=xyz" \
  -o receipt.pdf
```

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
    "dont_older_than": 7,
    "pass_check": false,
    "scan_interval": 60,
    "rss_type": "torrent",
    "torrent_seeding": 1
  }' \
  https://api.torbox.app/v1/api/rss/addrss
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | **Yes** | RSS feed URL |
| `name` | string | **Yes** | Feed name |
| `do_regex` | string | No | Include pattern regex |
| `dont_regex` | string | No | Exclude pattern regex |
| `dont_older_than` | integer | No | Skip items older than N days |
| `pass_check` | boolean | No | Pass password check (default: `false`) |
| `scan_interval` | integer | No | Scan interval in minutes (default: `60`) |
| `rss_type` | string | No | `torrent` or `usenet` (default: `torrent`) |
| `torrent_seeding` | integer | No | Seed ratio limit (default: `1`) |

### Control RSS Feed

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "rss_feed_id": 123}' \
  https://api.torbox.app/v1/api/rss/controlrss
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `delete`, `pause`, or `resume` |
| `rss_feed_id` | integer | Yes | RSS feed ID |

### Get RSS Feeds

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/rss/getfeeds?id="
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | No | Filter by specific feed ID |

### Get RSS Feed Items

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/rss/getfeeditems?rss_feed_id=123"
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rss_feed_id` | integer | **Yes** | RSS feed ID |

---

## Integrations Service

Upload downloads to cloud storage.

### Upload to Google Drive

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

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | **Yes** | Torrent/Usenet/Web download ID |
| `file_id` | integer | No | File index (default: `0` = all files) |
| `zip` | boolean | No | Upload as zip (default: `false`) |
| `type` | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `google_token` | string | **Yes** | Google OAuth token |

### Upload to Dropbox

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "dropbox_token": "DROPBOX_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/dropbox
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | **Yes** | Download ID |
| `file_id` | integer | No | File index (default: `0`) |
| `zip` | boolean | No | Upload as zip (default: `false`) |
| `type` | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `dropbox_token` | string | **Yes** | Dropbox OAuth token |

### Upload to OneDrive

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "onedrive_token": "ONEDRIVE_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/onedrive
```

**Request Body:** Same as Dropbox with `onedrive_token`.

### Upload to GoFile

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "gofile_token": "GOFILE_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/gofile
```

**Note:** `gofile_token` is optional (for authenticated uploads).

### Upload to 1Fichier

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "onefichier_token": "ONEFICHIER_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/1fichier
```

### Upload to Pixeldrain

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "pixeldrain_token": "PIXELDRAIN_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/pixeldrain
```

**Note:** `pixeldrain_token` is optional.

### Manage Transfer Jobs

```bash
# List all jobs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/jobs

# Get job status
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/job/123

# Cancel job
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/job/123

# Get jobs by hash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/jobs/ABC123...
```

---

## Notifications Service

### Get Notifications

```bash
# JSON format
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/mynotifications

# RSS format
curl "https://api.torbox.app/v1/api/notifications/rss?token=YOUR_TOKEN"
```

### Clear Notifications

```bash
# Clear all
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear

# Clear specific
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear/123
```

---

## Performance Optimization

### For Essential/Standard Plans

While Essential+ plans have unlimited downloads, they have limited concurrent slots (3 for Essential, 5 for Standard). Use cache checks to avoid wasting slots on non-cached torrents.

**1. Always check cache first:**
```bash
# Check cache before adding
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes":["ABC123..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object"

# Only add if cached (saves slots)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:ABC123..." \
  -F "add_only_if_cached=true" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**2. Monitor slot usage with error handling:**
```python
import os
import urllib.request
import urllib.parse
import urllib.error
import json

TORBOX_TOKEN = os.environ.get("TORBOX_API_KEY")
if not TORBOX_TOKEN:
    raise RuntimeError("Set TORBOX_API_KEY environment variable")

def get_available_slots():
    """Get number of available concurrent download slots."""
    req = urllib.request.Request(
        "https://api.torbox.app/v1/api/user/me",
        headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            user = json.loads(resp.read().decode())
            return user['data']['max_downloads'] - user['data']['active_downloads']
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        return None

slots = get_available_slots()
if slots is not None:
    print(f"Available slots: {slots}")
```

**3. Use queue for overflow:**
```bash
# If slots full, add to queue instead
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:..." \
  -F "as_queued=true" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

### Batch Operations

```bash
# Batch cache checks (max 100 hashes)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes":["hash1","hash2",...,"hash100"]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached"
```

### Polling Strategy with Error Handling

```python
import os
import time
import urllib.request
import urllib.error
import json

TORBOX_TOKEN = os.environ.get("TORBOX_API_KEY")
if not TORBOX_TOKEN:
    raise RuntimeError("Set TORBOX_API_KEY environment variable")

def wait_for_cached(torrent_id, timeout=300, interval=10):
    """Wait for torrent to become cached.
    
    Args:
        torrent_id: The torrent ID to check
        timeout: Maximum time to wait in seconds (default: 300)
        interval: Seconds between checks (default: 10)
    
    Returns:
        Torrent data dict when cached
    
    Raises:
        TimeoutError: If timeout reached before cached
        HTTPError: If API returns error
        URLError: If connection fails
    """
    start = time.time()
    attempt = 0
    
    while time.time() - start < timeout:
        attempt += 1
        try:
            req = urllib.request.Request(
                f"https://api.torbox.app/v1/api/torrents/mylist?id={torrent_id}",
                headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                
                # Validate response structure
                if 'data' not in data:
                    raise ValueError(f"Unexpected response: {data}")
                
                # Handle list response (mylist returns a list even with id filter)
                torrent_list = data['data']
                if isinstance(torrent_list, list):
                    if len(torrent_list) == 0:
                        raise ValueError(f"Torrent {torrent_id} not found")
                    torrent_data = torrent_list[0]
                else:
                    torrent_data = torrent_list
                
                # Check download state
                if torrent_data.get('download_state') == 'cached':
                    return torrent_data
                
                print(f"Attempt {attempt}: State is {torrent_data.get('download_state')}, waiting...")
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error on attempt {attempt}: {e.code}")
            raise
        except urllib.error.URLError as e:
            print(f"Connection error on attempt {attempt}: {e.reason}")
            raise
        
        # Exponential backoff with jitter
        sleep_time = min(interval * (1.5 ** (attempt - 1)), 60)
        time.sleep(sleep_time)
    
    raise TimeoutError(f"Torrent {torrent_id} did not become cached within {timeout} seconds")

# Usage
try:
    result = wait_for_cached(12345, timeout=600)
    print(f"Torrent cached: {result}")
except TimeoutError as e:
    print(f"Timeout: {e}")
except Exception as e:
    print(f"Error: {e}")
```

---

## Response Format

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

---

## Rate Limits

| Endpoint | Limit | Notes |
|----------|-------|-------|
| Test notification | 1/minute | Hard limit |
| Cache checks | 5/second | Be reasonable; cache results for 1 hour |
| List endpoints | 1/second | Avoid rapid polling |
| Download requests | Metered | Based on plan; respect `Retry-After` header |
| General API | - | Be polite; implement exponential backoff on 429 |

**Handling 429 Responses:**
```python
import time

def api_call_with_backoff(req, max_retries=3):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Get Retry-After header if available
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            raise
    raise Exception("Max retries exceeded")
```

---

## Troubleshooting

### "Usenet not working"
- Check plan: Must be `pro`
- Non-Pro plans get permission errors
- Verify with: `GET /v1/api/user/me`

### "Cannot add more torrents"
- Check active downloads vs plan limit
- Use `as_queued=true` or delete old torrents
- Essential: Max 3 concurrent
- Standard: Max 5 concurrent
- Pro: Max 10 concurrent

### "Download link expired"
- Links valid for 3 hours to START download
- Once started, unlimited time to complete
- Request new link or use permalinks with `redirect=true`

### "File too large"
- Free: 10GB max
- Essential/Standard: 200GB max
- Pro: 1TB max
- Check file size before adding

### Slow speeds
- Free: 250Mbps
- Essential/Standard: 1Gbps
- Pro: 80Gbps
- Use speedtest endpoint: `GET /v1/api/speedtest`
- Try different CDN via `user_ip` parameter

### "API authentication failed"
- Free plan has NO API access
- Must upgrade to Essential ($3/mo) or higher
- Check plan: `GET /v1/api/user/me`

### "Connection refused" or timeout
- Check if TorBox API is up: `GET /`
- Check your internet connection
- Verify firewall/proxy settings
