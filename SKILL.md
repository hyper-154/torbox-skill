---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, streaming, and cloud integrations. Use when managing downloads, checking cache status, creating streams, uploading to cloud storage, or automating Torbox workflows. Supports torrent creation/management, usenet downloads, web downloads, RSS feeds, queued downloads, user account operations, and integrations with Google Drive, Dropbox, OneDrive, and more.
---

# Torbox API Skill

API for managing torrents, Usenet, web downloads, and cloud integrations through Torbox.

## Base URL

```
https://api.torbox.app
```

## Authentication

All authenticated endpoints require an API key via Bearer token:

```bash
Authorization: Bearer <YOUR_API_KEY>
```

For unauthenticated endpoints (status, stats, changelogs), no token is needed.

---

## STEP 1: Check User Plan (CRITICAL)

**ALWAYS check the user's plan first** before performing operations. Different plans have different limitations.

### Get User Info

```bash
GET /v1/api/user/me?settings=true
```

```python
from torbox_api import TorboxApi
sdk = TorboxApi(access_token="YOUR_TOKEN")
user = sdk.user.get_user_data(settings=True)
print(user.plan)  # Check plan type
```

```typescript
const sdk = new TorboxApi({ token: 'YOUR_TOKEN' });
const { data } = await sdk.user.getUserData({ settings: true });
console.log(data.plan);  // Check plan type
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

### Plan Restriction Errors

If a user tries to use Pro features on lower plans:

```json
{
  "success": false,
  "error": "PLAN_RESTRICTION",
  "detail": "This feature requires Pro plan"
}
```

**Common plan errors:**
- Usenet on non-Pro: Returns permission/upgrade error
- Exceeding concurrent slots: New additions go to queue
- File too large: Rejected with size limit error

---

## Official SDKs

### Python SDK
```bash
pip install torbox_api
```

```python
from torbox_api import TorboxApi

sdk = TorboxApi(
    access_token="YOUR_ACCESS_TOKEN",
    base_url="https://api.torbox.app",
    timeout=10000
)

# Get API status
result = sdk.general.get_up_status()
print(result)

# Update token later
sdk.set_access_token("NEW_TOKEN")
```

### JavaScript/TypeScript SDK
```bash
npm install @torbox/torbox-api
# or
pnpm install @torbox/torbox-api
```

```typescript
import { TorboxApi } from '@torbox/torbox-api';

const sdk = new TorboxApi({
  token: 'YOUR_TOKEN',
  baseUrl: 'https://api.torbox.app'
});

// Get API status
const { data } = await sdk.general.getUpStatus();
console.log(data);
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
GET /
```

```python
result = sdk.general.get_up_status()
```

```typescript
const { data } = await sdk.general.getUpStatus();
```

### Get Stats
```bash
GET /v1/api/stats
GET /v1/api/stats/30days
```

### Get Changelogs
```bash
GET /v1/api/changelogs/rss     # RSS format
GET /v1/api/changelogs/json    # JSON format
```

### Speedtest Files
```bash
GET /v1/api/speedtest?test_length=short&region=all
```

Parameters:
- `test_length`: `short` or `long`
- `region`: CDN region (omit to get all available)

---

## Torrents Service

Works on all plans. Check concurrent slot availability.

### Create Torrent
Creates a torrent from magnet link or torrent file.

```bash
POST /v1/api/torrents/createtorrent
Content-Type: multipart/form-data
```

**Parameters:**
| Field | Type | Description |
|-------|------|-------------|
| `magnet` | string | Magnet link (optional if file provided) |
| `file` | file | .torrent file (optional if magnet provided) |
| `seed` | integer | Seed ratio limit (optional) |
| `allow_zip` | boolean | Allow zip output (default: true) |
| `name` | string | Custom name (optional) |
| `as_queued` | boolean | Add to queue (default: false) |
| `add_only_if_cached` | boolean | Only add if cached (default: false) |

**Performance Tip:** Use `add_only_if_cached=true` to avoid wasting slots on non-cached torrents on free/lower plans.

```python
# Check cache first (free plan optimization)
cache = sdk.torrents.get_torrent_cached_availability(hash=["abc123..."])
if cache.data:
    # Safe to add - won't waste slot
    result = sdk.torrents.create_torrent(magnet="magnet:?xt=urn:btih:...")
else:
    # May fail if no slots available on free plan
    print("Not cached - consider checking plan slots first")
```

**Async version:** `POST /v1/api/torrents/asynccreatetorrent` (returns immediately, processes in background)

### Control Torrent

```bash
POST /v1/api/torrents/controltorrent
```

**Operations:** `reannounce`, `delete`, `resume`

```json
{
  "operation": "delete",
  "torrent_id": 123,
  "all": false
}
```

```python
result = sdk.torrents.control_torrent(
    operation="delete",
    torrent_id=123
)
```

### Get Torrent List

```bash
GET /v1/api/torrents/mylist?offset=0&limit=1000&id=&bypass_cache=false
```

```python
result = sdk.torrents.get_torrent_list(offset=0, limit=50)
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
POST /v1/api/torrents/checkcached?format=object&list_files=false
```

```json
{
  "hashes": ["abc123...", "def456..."]
}
```

**Notes:**
- Max ~100 hashes per request
- Fast lookup (<1s per 100 hashes)
- 1-hour cache
- Formats: `object` or `list`

**Performance Tip:** Batch hash checks. Cache the results for 1 hour to avoid redundant API calls.

```python
result = sdk.torrents.get_torrent_cached_availability(
    hash=["abc123...", "def456..."],
    format="object",
    list_files=True
)
```

### Request Download Link

```bash
GET /v1/api/torrents/requestdl?token=APIKEY&torrent_id=123&file_id=0&zip_link=false&redirect=false&user_ip=
```

**Permalink for direct access:**
```
https://api.torbox.app/v1/api/torrents/requestdl?token=APIKEY&torrent_id=NUMBER&file_id=NUMBER&redirect=true
```

- Link valid for 3 hours to start download
- Once started, unlimited time to complete
- Use `redirect=true` for permanent permalinks

### Get Torrent Info

```bash
GET /v1/api/torrents/torrentinfo?hash=ABC123&timeout=30&use_cache_lookup=false
POST /v1/api/torrents/torrentinfo  # For file/magnet upload
```

```python
result = sdk.torrents.get_torrent_info(hash="abc123...")
```

### Export Torrent Data

```bash
GET /v1/api/torrents/exportdata?torrent_id=123&type=magnet
GET /v1/api/torrents/exportdata?torrent_id=123&type=file  # Returns .torrent file
```

---

## Usenet Service

⚠️ **PRO PLAN ONLY** - Will fail with error on Free/Essential/Standard plans.

### Pre-Flight Check

```python
user = sdk.user.get_user_data()
if user.plan not in ["pro", "premium"]:
    print("ERROR: Usenet requires Pro plan")
    print(f"Current plan: {user.plan}")
    return
```

### Create Usenet Download

```bash
POST /v1/api/usenet/createusenetdownload
Content-Type: multipart/form-data
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

```python
# Check plan first
user = sdk.user.get_user_data()
if user.plan == "pro":
    result = sdk.usenet.create_usenet_download(link="https://.../file.nzb")
else:
    print("Usenet requires Pro plan")
```

**Async:** `POST /v1/api/usenet/asynccreateusenetdownload`

### Control Usenet Download

```bash
POST /v1/api/usenet/controlusenetdownload
```

```json
{
  "operation": "delete" | "pause" | "resume",
  "usenet_id": 123,
  "all": false
}
```

### Get Usenet List

```bash
GET /v1/api/usenet/mylist?offset=0&limit=1000&id=
```

### Check Cached

```bash
POST /v1/api/usenet/checkcached?format=object&list_files=false
```

### Request Download Link

```bash
GET /v1/api/usenet/requestdl?token=APIKEY&usenet_id=123&file_id=0&zip_link=false&redirect=false
```

---

## Web Downloads Service

Works on all plans. Premium hosters may require Pro for best speeds.

### Create Web Download

```bash
POST /v1/api/webdl/createwebdownload
Content-Type: application/x-www-form-urlencoded
```

**Parameters:**
| Field | Type | Description |
|-------|------|-------------|
| `link` | string | **Required** - Download URL |
| `password` | string | Password (optional) |
| `name` | string | Custom name (optional) |
| `as_queued` | boolean | Add to queue (default: false) |
| `add_only_if_cached` | boolean | Only add if cached (default: false) |

```python
result = sdk.web_downloads_debrid.create_web_download(link="https://example.com/file.zip")
```

### Get Supported Hosters

```bash
GET /v1/api/webdl/hosters
```

Returns list of supported file hosters. Premium hosters marked separately.

---

## Queued Service

### Get Queued Downloads

```bash
GET /v1/api/queued/getqueued?id=&type=torrent&bypass_cache=false&offset=0&limit=1000
```

**Types:** `torrent`, `usenet`, `webdl`

```python
# Check how many items are waiting (free plan optimization)
queued = sdk.queued.get_queued_download_list()
print(f"{len(queued.data)} items in queue")
```

### Control Queued

```bash
POST /v1/api/queued/controlqueued
```

```json
{
  "operation": "delete",
  "queued_id": 123,
  "all": false
}
```

---

## User Service

### Get User Info

```bash
GET /v1/api/user/me?settings=false
```

```python
result = sdk.user.get_user_data(settings=True)
# Key fields:
# - result.plan: "free", "essential", "standard", "pro"
# - result.active_downloads: Current active count
# - result.max_downloads: Plan limit
# - result.storage_used: Bytes used
```

### Subscriptions & Transactions

```bash
GET /v1/api/user/subscriptions
GET /v1/api/user/transactions
GET /v1/api/user/transaction/pdf?transaction_id=xyz
```

**Check subscription status:**
```python
subs = sdk.user.get_subscriptions()
for sub in subs.data:
    print(f"Plan: {sub.plan}, Status: {sub.status}, Expires: {sub.expires}")
```

---

## RSS Service

### Add RSS Feed

```bash
POST /v1/api/rss/addrss
```

```json
{
  "url": "https://.../feed.rss",
  "name": "My Feed",
  "do_regex": "include_pattern",
  "dont_regex": "exclude_pattern",
  "dont_older_than": 7,
  "pass_check": false,
  "scan_interval": 60,
  "rss_type": "torrent",
  "torrent_seeding": 1
}
```

### Control RSS Feed

```bash
POST /v1/api/rss/controlrss
```

**Operations:** `delete`, `pause`, `resume`

### Get RSS Feeds

```bash
GET /v1/api/rss/getfeeds?id=
```

---

## Integrations Service

Upload downloads to cloud storage.

### Upload to Google Drive

```bash
POST /v1/api/integration/googledrive
```

```json
{
  "id": 123,
  "file_id": 0,
  "zip": false,
  "type": "torrent",
  "google_token": "GOOGLE_OAUTH_TOKEN"
}
```

### Manage Transfer Jobs

```bash
GET /v1/api/integration/jobs                 # List all jobs
GET /v1/api/integration/job/{job_id}         # Get job status
DELETE /v1/api/integration/job/{job_id}      # Cancel job
```

**Monitor upload progress:**
```python
job = sdk.integrations.get_job_status(job_id=123)
print(f"Progress: {job.data.progress}%")
```

---

## Performance Optimization

### For Free/Lower Plans

1. **Always check cache first** before adding:
```python
def smart_add_torrent(sdk, magnet_hash):
    cache = sdk.torrents.get_torrent_cached_availability(hash=[magnet_hash])
    if magnet_hash in cache.data:
        return sdk.torrents.create_torrent(magnet=f"magnet:?xt=urn:btih:{magnet_hash}")
    else:
        # Not cached - might use slot without success
        return {"success": False, "error": "NOT_CACHED"}
```

2. **Monitor slot usage**:
```python
def get_available_slots(sdk):
    user = sdk.user.get_user_data()
    torrents = sdk.torrents.get_torrent_list()
    active = len([t for t in torrents.data if t.download_state == "downloading"])
    return user.max_downloads - active
```

3. **Use queue for overflow**:
```python
# If slots full, add as_queued=True
if get_available_slots(sdk) == 0:
    result = sdk.torrents.create_torrent(magnet=magnet, as_queued=True)
```

### Batch Operations

```python
# Batch cache checks (max 100 hashes)
hashes = ["hash1", "hash2", ..., "hash100"]
cache = sdk.torrents.get_torrent_cached_availability(hash=hashes)
```

### Polling Strategy

```python
import time

def wait_for_cached(sdk, torrent_id, timeout=300):
    """Wait for torrent to become cached."""
    start = time.time()
    while time.time() - start < timeout:
        torrents = sdk.torrents.get_torrent_list()
        for t in torrents.data:
            if t.id == torrent_id and t.download_state == "cached":
                return t
        time.sleep(10)
    return None
```

---

## Using the CLI Script

```bash
# Get API status
python3 ~/clawd/skills/torbox/scripts/torbox-api.py status

# List torrents
python3 ~/clawd/skills/torbox/scripts/torbox-api.py torrents list --token YOUR_TOKEN

# Create torrent from magnet
python3 ~/clawd/skills/torbox/scripts/torbox-api.py torrents create --magnet "magnet:?xt=..." --token YOUR_TOKEN

# Check cache
python3 ~/clawd/skills/torbox/scripts/torbox-api.py torrents cache --hashes "hash1,hash2" --token YOUR_TOKEN

# Request download link
python3 ~/clawd/skills/torbox/scripts/torbox-api.py torrents download --id 123 --token YOUR_TOKEN

# Set token via environment variable
export TORBOX_TOKEN="your_token"
python3 ~/clawd/skills/torbox/scripts/torbox-api.py torrents list
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
- Check plan: `user.plan` must be "pro"
- Non-Pro plans get permission errors

### "Cannot add more torrents"
- Check active downloads vs plan limit
- Use `as_queued=True` or delete old torrents
- Check: `len(active_downloads) >= max_downloads`

### "Download link expired"
- Links valid for 3 hours to START download
- Request new link or use permalinks with `redirect=true`

### "File too large"
- Essential/Standard: 200GB max
- Pro: 500GB max
- Free: Very limited

### Slow speeds
- Check plan speed tier
- Use speedtest endpoint to verify CDN
- Try different region: `?user_ip=` or different CDN
