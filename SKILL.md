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

## Services Overview

| Service | Description |
|---------|-------------|
| **General** | API status, stats, changelogs, speedtest |
| **Torrents** | Create, control, list, check cache, download torrents |
| **Usenet** | Create, control, list, check cache NZB downloads |
| **Web Downloads** | Create, control, list web downloads, get hoster list |
| **Queued** | Manage queued downloads |
| **User** | User info, referrals, subscriptions, transactions |
| **RSS** | Manage RSS feeds |
| **Integrations** | Upload to cloud storage (Google Drive, Dropbox, etc.) |
| **Notifications** | Get and clear notifications |

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

```python
# Using magnet
result = sdk.torrents.create_torrent(magnet="magnet:?xt=urn:btih:...")

# Using file
with open("file.torrent", "rb") as f:
    result = sdk.torrents.create_torrent(file=f)
```

```typescript
const { data } = await sdk.torrents.createTorrent({
  magnet: 'magnet:?xt=urn:btih:...'
});
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

### Magnet to Torrent File

```bash
POST /v1/api/torrents/magnettofile
```

---

## Usenet Service

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
result = sdk.usenet.create_usenet_download(link="https://.../file.nzb")
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

Returns list of supported file hosters.

---

## Queued Service

### Get Queued Downloads

```bash
GET /v1/api/queued/getqueued?id=&type=torrent&bypass_cache=false&offset=0&limit=1000
```

**Types:** `torrent`, `usenet`, `webdl`

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
```

### Referrals

```bash
POST /v1/api/user/addreferral?referral=CODE
GET /v1/api/user/referraldata
```

### Subscriptions & Transactions

```bash
GET /v1/api/user/subscriptions
GET /v1/api/user/transactions
GET /v1/api/user/transaction/pdf?transaction_id=xyz
```

### Device Authorization (OAuth2 Device Flow)

```bash
GET /v1/api/user/auth/device/start?app=MyApp
POST /v1/api/user/auth/device/token
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

### Modify RSS Feed

```bash
POST /v1/api/rss/modifyrss
```

### Get RSS Feeds

```bash
GET /v1/api/rss/getfeeds?id=
```

### Get RSS Feed Items

```bash
GET /v1/api/rss/getfeeditems?rss_feed_id=123
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

### Upload to Dropbox

```bash
POST /v1/api/integration/dropbox
```

```json
{
  "id": 123,
  "dropbox_token": "DROPBOX_TOKEN"
}
```

### Upload to OneDrive

```bash
POST /v1/api/integration/onedrive
```

### Upload to GoFile

```bash
POST /v1/api/integration/gofile
```

Optional: `gofile_token` for authenticated uploads.

### Upload to 1Fichier

```bash
POST /v1/api/integration/1fichier
```

### Upload to Pixeldrain

```bash
POST /v1/api/integration/pixeldrain
```

### Manage Transfer Jobs

```bash
GET /v1/api/integration/jobs                 # List all jobs
GET /v1/api/integration/job/{job_id}         # Get job status
DELETE /v1/api/integration/job/{job_id}      # Cancel job
GET /v1/api/integration/jobs/{hash}          # Get jobs by hash
```

---

## Notifications Service

### Get Notifications

```bash
GET /v1/api/notifications/mynotifications    # JSON format
GET /v1/api/notifications/rss?token=APIKEY   # RSS format
```

### Clear Notifications

```bash
POST /v1/api/notifications/clear             # Clear all
POST /v1/api/notifications/clear/{id}        # Clear specific
```

### Test Notification

```bash
POST /v1/api/notifications/test              # Rate limited: 1/min
```

---

## Using the CLI Script

Use the provided script for easy API calls:

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

# Create web download
python3 ~/clawd/skills/torbox/scripts/torbox-api.py webdl create --link "https://..." --token YOUR_TOKEN

# List usenet downloads
python3 ~/clawd/skills/torbox/scripts/torbox-api.py usenet list --token YOUR_TOKEN

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

---

## Rate Limits

- Test notification: 1 per minute
- Cache checks: No explicit limit, but be reasonable
- Download requests: Metered based on plan

---

## Response Models Reference

Key response types you can expect:

| Model | Description |
|-------|-------------|
| `GetTorrentListOkResponse` | Torrent list with download states |
| `CreateTorrentOkResponse` | Created torrent details |
| `RequestDownloadLinkOkResponse` | Download URL or permalink |
| `GetTorrentCachedAvailabilityOkResponse` | Cache availability |
| `GetUsenetListOkResponse` | Usenet download list |
| `GetWebDownloadListOkResponse` | Web download list |
| `GetUserDataOkResponse` | User account info |
| `GetNotificationFeedOkResponse` | Notifications list |
| `GetAllJobsOkResponse` | Cloud upload jobs |
