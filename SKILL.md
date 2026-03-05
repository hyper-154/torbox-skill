---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, streaming, and cloud integrations using pure HTTP API calls. Use when managing downloads, checking cache status, creating streams, uploading to cloud storage, or automating Torbox workflows. Supports torrent creation/management, usenet downloads, web downloads, RSS feeds, queued downloads, user account operations, and integrations with Google Drive, Dropbox, OneDrive, and more.
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

| Feature | Free | Essential ($3/mo) | Standard ($5/mo) | Pro ($10/mo) |
|---------|------|-------------------|------------------|--------------|
| **Concurrent Files** | 1-2 | 3 | 5 | 10 |
| **Max File Size** | Limited | 200GB | 200GB | 500GB |
| **Seed Time** | Very limited | 24 hours | 14 days | 30 days |
| **Max Speed** | Limited | 1 Gbit/s | 1 Gbit/s | 80 Gbit/s |
| **Usenet Access** | ❌ NO | ❌ NO | ❌ NO | ✅ Premium servers |
| **Web Downloads** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Storage** | Unlimited | Unlimited | Unlimited | Unlimited |
| **Bandwidth** | Unlimited | Unlimited | Unlimited | Unlimited |

### Plan-Based Decision Tree

```
IF user.plan == "free":
    - Max 1-2 concurrent downloads
    - CANNOT use Usenet endpoints (will fail)
    - Limited speed and seed time
    - Check cache before adding to save slots

IF user.plan == "essential":
    - Max 3 concurrent downloads
    - CANNOT use Usenet endpoints (will fail)
    - 24h seed time only
    - 200GB max file size

IF user.plan == "standard":
    - Max 5 concurrent downloads  
    - CANNOT use Usenet endpoints (will fail)
    - 14 days seed time
    - 200GB max file size

IF user.plan == "pro":
    - Max 10 concurrent downloads
    - ✅ CAN use Usenet endpoints
    - 30 days seed time
    - 500GB max file size
    - Premium Usenet servers
```

### Python Helper to Check Plan

```python
import urllib.request
import json

TORBOX_TOKEN = "your_token"

def api_call(method, endpoint, data=None, params=None):
    url = f"https://api.torbox.app{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TORBOX_TOKEN}")
    
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

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
| **Torrents** | Create, control, list, check cache, download | Any |
| **Usenet** | Create, control, list, check cache NZB | **Pro only** |
| **Web Downloads** | Create, control, list web downloads | Any |
| **Queued** | Manage queued downloads | Any |
| **User** | User info, referrals, subscriptions | Any |
| **RSS** | Manage RSS feeds | Any |
| **Integrations** | Upload to cloud storage | Any |
| **Notifications** | Get and clear notifications | Any |

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
with urllib.request.urlopen(req) as resp:
    print(json.loads(resp.read().decode()))
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

Parameters:
- `test_length`: `short` or `long`
- `region`: CDN region (omit to get all available)

---

## Torrents Service

Works on all plans. Check concurrent slot availability.

### Create Torrent

Creates a torrent from magnet link or torrent file.

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
| Field | Type | Description |
|-------|------|-------------|
| `magnet` | string | Magnet link (optional if file provided) |
| `file` | file | .torrent file (optional if magnet provided) |
| `seed` | integer | Seed ratio limit (optional) |
| `allow_zip` | boolean | Allow zip output (default: true) |
| `name` | string | Custom name (optional) |
| `as_queued` | boolean | Add to queue if slots full (default: false) |
| `add_only_if_cached` | boolean | Only add if cached (default: false) |

**Performance Tip:** Use `add_only_if_cached=true` to avoid wasting slots on non-cached torrents on free/lower plans.

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

**Operations:** `reannounce`, `delete`, `resume`

### Get Torrent List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50&bypass_cache=false"
```

**Download States:**
- `downloading` - Currently downloading
- `uploading` - Currently seeding
- `stalled (no seeds)` - No seeds available
- `paused` - Paused
- `completed` - Downloaded (use `cached` for completion status)
- `cached` - Available on server
- `metaDL` - Downloading metadata
- `checkingResumeData` - Checking resumable data

### Check Cached

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes": ["abc123...", "def456..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object&list_files=false"
```

**Notes:**
- Max ~100 hashes per request
- Fast lookup (<1s per 100 hashes)
- 1-hour cache on server
- Formats: `object` or `list`

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
- `token` - Your API key (can be passed in query instead of header)
- `torrent_id` - The torrent ID
- `file_id` - Specific file ID (0 for all files)
- `zip_link` - Return as zip (default: false)
- `redirect` - Return direct URL (default: false)
- `user_ip` - Your IP for CDN selection

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

---

## Usenet Service

⚠️ **PRO PLAN ONLY** - Will fail with error on Free/Essential/Standard plans.

### Pre-Flight Check

```python
import urllib.request
import json

TORBOX_TOKEN = "your_token"

req = urllib.request.Request(
    "https://api.torbox.app/v1/api/user/me",
    headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
)
with urllib.request.urlopen(req) as resp:
    user = json.loads(resp.read().decode())
    if user['data']['plan'] not in ['pro', 'premium']:
        print("ERROR: Usenet requires Pro plan")
        exit(1)
```

### Create Usenet Download

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
| Field | Type | Description |
|-------|------|-------------|
| `link` | string | NZB link (optional if file provided) |
| `file` | file | NZB file (optional if link provided) |
| `name` | string | Custom name (optional) |
| `password` | string | Password (optional) |
| `post_processing` | integer | Post-processing option (default: -1) |
| `as_queued` | boolean | Add to queue (default: false) |
| `add_only_if_cached` | boolean | Only add if cached (default: false) |

**Async:** `POST /v1/api/usenet/asynccreateusenetdownload`

### Control Usenet Download

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "usenet_id": 123}' \
  https://api.torbox.app/v1/api/usenet/controlusenetdownload
```

**Operations:** `delete`, `pause`, `resume`

### Get Usenet List

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/usenet/mylist?offset=0&limit=50"
```

### Request Download Link

```bash
curl "https://api.torbox.app/v1/api/usenet/requestdl?\
token=YOUR_TOKEN&\
usenet_id=123&\
file_id=0&\
zip_link=false&\
redirect=false"
```

---

## Web Downloads Service

Works on all plans. Premium hosters may require Pro for best speeds.

### Create Web Download

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
| Field | Type | Description |
|-------|------|-------------|
| `link` | string | **Required** - Download URL |
| `password` | string | Password (optional) |
| `name` | string | Custom name (optional) |
| `as_queued` | boolean | Add to queue (default: false) |
| `add_only_if_cached` | boolean | Only add if cached (default: false) |

### Get Supported Hosters

```bash
curl https://api.torbox.app/v1/api/webdl/hosters
```

---

## Queued Service

### Get Queued Downloads

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/queued/getqueued?type=torrent&offset=0&limit=50"
```

**Types:** `torrent`, `usenet`, `webdl`

### Control Queued

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "queued_id": 123}' \
  https://api.torbox.app/v1/api/queued/controlqueued
```

---

## User Service

### Get User Info

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/me?settings=true"
```

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

### Control RSS Feed

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operation": "delete", "rss_feed_id": 123}' \
  https://api.torbox.app/v1/api/rss/controlrss
```

**Operations:** `delete`, `pause`, `resume`

### Get RSS Feeds

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/rss/getfeeds"
```

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

### Upload to Dropbox

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "dropbox_token": "DROPBOX_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/dropbox
```

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

### For Free/Lower Plans

**1. Always check cache first:**
```bash
# Check cache before adding
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes":["ABC123..."]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object"

# Only add if cached (saves slots on free plans)
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:ABC123..." \
  -F "add_only_if_cached=true" \
  https://api.torbox.app/v1/api/torrents/createtorrent
```

**2. Monitor slot usage:**
```python
import urllib.request
import json

TORBOX_TOKEN = "your_token"

def get_available_slots():
    req = urllib.request.Request(
        "https://api.torbox.app/v1/api/user/me",
        headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        user = json.loads(resp.read().decode())
        return user['data']['max_downloads'] - user['data']['active_downloads']

print(f"Available slots: {get_available_slots()}")
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

### Polling Strategy

```python
import time
import urllib.request
import json

TORBOX_TOKEN = "your_token"

def wait_for_cached(torrent_id, timeout=300):
    """Wait for torrent to become cached."""
    start = time.time()
    while time.time() - start < timeout:
        req = urllib.request.Request(
            f"https://api.torbox.app/v1/api/torrents/mylist?id={torrent_id}",
            headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data['data']['download_state'] == 'cached':
                return data['data']
        time.sleep(10)
    return None
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
- `ENDPOINT_NOT_FOUND` - Invalid URL
- `VALIDATION_ERROR` - Invalid parameters
- `AUTHENTICATION_FAILED` - Invalid or missing token
- `RATE_LIMITED` - Too many requests
- `PLAN_RESTRICTION` - Feature requires higher plan
- `SLOTS_FULL` - Concurrent download limit reached
- `FILE_TOO_LARGE` - Exceeds plan size limit

---

## Rate Limits

- Test notification: 1 per minute
- Cache checks: No explicit limit, but be reasonable
- Download requests: Metered based on plan
- General API: Be polite, don't hammer

---

## Troubleshooting

### "Usenet not working"
- Check plan: Must be "pro"
- Non-Pro plans get permission errors
- Verify with: `GET /v1/api/user/me`

### "Cannot add more torrents"
- Check active downloads vs plan limit
- Use `as_queued=true` or delete old torrents
- Free plan: Max 1-2 concurrent

### "Download link expired"
- Links valid for 3 hours to START download
- Once started, unlimited time to complete
- Request new link or use permalinks

### "File too large"
- Essential/Standard: 200GB max
- Pro: 500GB max
- Check file size before adding

### Slow speeds
- Check plan speed tier (Free/Essential/Standard = 1Gbit/s, Pro = 80Gbit/s)
- Use speedtest endpoint: `GET /v1/api/speedtest`
- Try different CDN via `user_ip` parameter
