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

All endpoints require an API key via Bearer token:

```bash
Authorization: Bearer <YOUR_API_KEY>
```

For unauthenticated endpoints (status, stats), no token is needed.

## Core Services

### 1. User Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/user/me` | GET | Get user info |
| `/v1/api/user/refreshtoken` | POST | Refresh API token |
| `/v1/api/user/addreferral` | POST | Add referral code |
| `/v1/api/user/referraldata` | GET | Get referral data |
| `/v1/api/user/subscriptions` | GET | Get subscriptions |
| `/v1/api/user/transactions` | GET | Get transactions |

### 2. Torrents

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/torrents/createtorrent` | POST | Create from magnet/file |
| `/v1/api/torrents/asynccreatetorrent` | POST | Async create |
| `/v1/api/torrents/controltorrent` | POST | Control (pause/resume/delete) |
| `/v1/api/torrents/mylist` | GET | List torrents |
| `/v1/api/torrents/checkcached` | POST/GET | Check cache status |
| `/v1/api/torrents/requestdl` | GET | Request download link |
| `/v1/api/torrents/torrentinfo` | POST/GET | Get torrent info |
| `/v1/api/torrents/edittorrent` | PUT | Edit torrent metadata |

**Create Torrent Body (multipart/form-data):**
- `magnet` - Magnet link (optional)
- `file` - .torrent file (optional)
- `seed` - Seed ratio (optional)
- `allow_zip` - Allow zip output (default: true)
- `name` - Custom name (optional)
- `as_queued` - Add to queue (default: false)
- `add_only_if_cached` - Only add if cached (default: false)

**Control Torrent Body:**
```json
{
  "operation": "delete" | "pause" | "resume",
  "torrent_id": 123,
  "all": false
}
```

### 3. Usenet Downloads

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/usenet/createusenetdownload` | POST | Create from NZB/link |
| `/v1/api/usenet/asynccreateusenetdownload` | POST | Async create |
| `/v1/api/usenet/controlusenetdownload` | POST | Control download |
| `/v1/api/usenet/mylist` | GET | List downloads |
| `/v1/api/usenet/checkcached` | POST/GET | Check cache |
| `/v1/api/usenet/requestdl` | GET | Request download link |

### 4. Web Downloads

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/webdl/createwebdownload` | POST | Create from URL |
| `/v1/api/webdl/asynccreatewebdownload` | POST | Async create |
| `/v1/api/webdl/controlwebdownload` | POST | Control download |
| `/v1/api/webdl/mylist` | GET | List downloads |
| `/v1/api/webdl/checkcached` | POST/GET | Check cache |
| `/v1/api/webdl/requestdl` | GET | Request download link |
| `/v1/api/webdl/hosters` | GET | List supported hosters |

**Create Web Download Body:**
```json
{
  "link": "https://example.com/file.zip",
  "password": "optional",
  "name": "custom name",
  "as_queued": false,
  "add_only_if_cached": false
}
```

### 5. Request Download Link

**Query Parameters:**
- `token` - Your API key
- `torrent_id` | `usenet_id` | `web_id` - Item ID
- `file_id` - Specific file ID (0 for all)
- `zip_link` - Return as zip (default: false)
- `user_ip` - User IP for CDN selection
- `redirect` - Return direct URL (default: false)

### 6. RSS Feeds

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/rss/addrss` | POST | Add RSS feed |
| `/v1/api/rss/controlrss` | POST | Control feed |
| `/v1/api/rss/modifyrss` | POST | Modify feed |
| `/v1/api/rss/getfeeds` | GET | List feeds |
| `/v1/api/rss/getfeeditems` | GET | Get feed items |

### 7. Streaming

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/stream/createstream` | GET | Create stream |
| `/v1/api/stream/getstreamdata` | GET | Get stream data |

### 8. Cloud Integrations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/integration/googledrive` | POST | Upload to Google Drive |
| `/v1/api/integration/dropbox` | POST | Upload to Dropbox |
| `/v1/api/integration/onedrive` | POST | Upload to OneDrive |
| `/v1/api/integration/gofile` | POST | Upload to GoFile |
| `/v1/api/integration/1fichier` | POST | Upload to 1Fichier |
| `/v1/api/integration/pixeldrain` | POST | Upload to Pixeldrain |
| `/v1/api/integration/jobs` | GET | List transfer jobs |
| `/v1/api/integration/job/{job_id}` | GET/DELETE | Get/cancel job |

### 9. General

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status |
| `/v1/api/stats` | GET | Torbox stats |
| `/v1/api/stats/30days` | GET | 30-day stats |
| `/v1/api/speedtest` | GET | Speedtest files |
| `/v1/api/notifications/mynotifications` | GET | Get notifications |
| `/v1/api/notifications/clear` | POST | Clear all notifications |

### 10. Queued Downloads

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/api/queued/getqueued` | GET | List queued items |
| `/v1/api/queued/controlqueued` | POST | Control queued item |

## Using the API Script

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
```

## Example cURL Commands

```bash
# Get user info
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/user/me

# Create torrent from magnet
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -F "magnet=magnet:?xt=urn:btih:..." \
  https://api.torbox.app/v1/api/torrents/createtorrent

# List torrents
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/torrents/mylist?offset=0&limit=50"

# Check if cached
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashes":["hash1","hash2"]}' \
  "https://api.torbox.app/v1/api/torrents/checkcached?format=object"

# Request download link
curl "https://api.torbox.app/v1/api/torrents/requestdl?token=YOUR_TOKEN&torrent_id=123&file_id=0"
```

## Common Operations

**Check if torrent is cached:**
```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  -d '{"hashes":["ABC123..."]}' \
  https://api.torbox.app/v1/api/torrents/checkcached
```

**Add torrent and get download link:**
1. Create torrent: POST `/v1/api/torrents/createtorrent`
2. Poll list until downloaded: GET `/v1/api/torrents/mylist`
3. Request download: GET `/v1/api/torrents/requestdl`

**Upload to Google Drive:**
```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id":123,"google_token":"GTOKEN","zip":false}' \
  https://api.torbox.app/v1/api/integration/googledrive
```

## Response Format

All responses are JSON with this structure:
```json
{
  "success": true,
  "data": { ... },
  "detail": "optional message"
}
```

Errors return:
```json
{
  "success": false,
  "error": "ERROR_CODE",
  "detail": "Error description"
}
```
