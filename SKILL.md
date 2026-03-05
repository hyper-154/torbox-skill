---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, search engines, streaming, and cloud integrations using pure HTTP API calls. This is a modular skill - load only the sections you need. See the routing guide below.
---

# Torbox API Skill (Modular)

Pure HTTP API for managing torrents, Usenet, web downloads, search engines, streaming, and cloud integrations through Torbox. No SDK dependencies required.

---

## What is Torbox?

**Torbox is a debrid service** that downloads content on behalf of users and makes it available for direct download or streaming.

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Torrent Caching** | Add a magnet link or .torrent file. Torbox downloads it to their servers. You download directly from Torbox's CDN (not P2P). |
| **Usenet Downloads** | (Pro only) Download NZB files from Usenet servers. |
| **Web Downloads** | Debrid direct download URLs from supported file hosters. |
| **Streaming** | Stream video files directly in browser (Pro Web Player) or via API. |
| **Cloud Uploads** | Automatically upload completed downloads to Google Drive, Dropbox, etc. |
| **RSS Automation** | Auto-download from RSS feeds (torrent sites, Usenet indexers). |

### Key Concepts

**Caching:** When you add a torrent, Torbox checks if it's already cached (pre-downloaded by another user). Cached downloads are instant. Non-cached downloads take time to fetch from the swarm.

**Debrid:** Instead of downloading P2P (BitTorrent) yourself, Torbox does it for you. You get a clean HTTP/HTTPS download link from their CDN.

**Concurrent Slots:** Maximum simultaneous active downloads. Free=1, Essential=3, Standard=5, Pro=10. Additional downloads are queued.

**Seed Time:** How long Torbox seeds the torrent after downloading. Essential=24h, Standard=14d, Pro=30d.

**API Access:** Free plan has NO API access. Essential+ required to use this skill.

### Basic Workflow

1. **Add Content:** Send magnet/NZB/URL to Torbox via API
2. **Wait/Download:** Torbox fetches the content (instant if cached)
3. **Get Download Link:** Request CDN link when ready
4. **Download:** Download directly from Torbox's CDN

### Important Constraints

- **Free Plan:** 10 downloads/month, NO API access, no Usenet, no Web Player
- **Essential/Standard:** API access, NO Usenet, NO Web Player
- **Pro:** Full access including Usenet and Web Player streaming
- **Max File Sizes:** Free=10GB, Essential/Standard=200GB, Pro=1TB
- **Rate Limits:** Respect API limits; abusive use may result in bans

---

## ⚡ Quick Routing Guide

**Load the appropriate section based on your task:**

| Task | Load Section |
|------|--------------|
| Check plan, auth, or API limits | `auth-and-plans.md` |
| Get user info, tokens, subscriptions | `user-account.md` |
| Create/manage torrents | `torrents.md` |
| Usenet downloads (NZB) | `usenet.md` |
| Web downloads (URL debrid) | `web-downloads.md` |
| RSS feed automation | `rss.md` |
| Video streaming | `streaming.md` |
| Check notifications | `notifications.md` |
| Upload to cloud storage | `integrations.md` |
| API health, stats | `general-service.md` |
| Error codes, quirks | `quirks-and-errors.md` |

---

## Base URL

```
https://api.torbox.app
```

---

## Section Files

### 1. auth-and-plans.md
**Authentication, plan limits, decision tree, Python helper**

- Plan limitations table (Free/Essential/Standard/Pro)
- Plan-based decision tree
- API key authentication
- Python helper with error handling

**Use when:** Checking user plan, understanding limits, or need the api_call() helper function.

---

### 2. user-account.md
**User Service - Account management**

- Get user info (`/user/me`)
- Refresh tokens (`/user/refreshtoken`)
- Device authentication flow (`/user/auth/device/*`)
- Referrals (`/user/addreferral`, `/user/referraldata`)
- Subscriptions & transactions
- Search engines management (`/user/settings/searchengines`)

**Use when:** Managing user account, billing, or configuring search engines.

---

### 3. torrents.md
**Torrents Service - Torrent management**

- Create torrent (magnet/file)
- Async create torrent
- Control torrent (pause/resume/delete)
- Get torrent list
- Check cached
- Get queued torrents
- Request download link
- Get torrent info
- Export torrent data (magnet/file)
- Edit torrent

**Use when:** Working with torrents - adding, controlling, checking cache, downloading.

---

### 4. usenet.md
**Usenet Service - NZB downloads (⚠️ Pro Plan Only)**

- Create Usenet download (link/file)
- Async create
- Control Usenet download
- Get Usenet list
- Request download link
- Check cached
- Edit Usenet download

**Use when:** Working with NZB downloads on Pro plan.

---

### 5. web-downloads.md
**Web Downloads Service - URL debrid**

- Create web download
- Async create
- Control web download
- Get web download list
- Request download link
- Get supported hosters
- Check cached
- Edit web download

**Use when:** Debriding direct download URLs.

---

### 6. rss.md
**RSS Service - Feed automation**

- Add RSS feed
- Control RSS feed (pause/resume/delete)
- Modify RSS feed
- Get RSS feeds
- Get RSS feed items

**Use when:** Setting up automated RSS feed monitoring.

---

### 7. streaming.md
**Streaming Service - Video playback (⚠️ Pro Web Player)**

- Create stream
- Get stream data (playback URL)

**Use when:** Streaming video content (Pro plan Web Player feature).

---

### 8. notifications.md
**Notifications Service**

- Get notifications (JSON/RSS)
- Clear notifications (all/specific)
- Test notification

**Use when:** Checking or managing user notifications.

---

### 9. integrations.md
**Integrations Service - Cloud storage uploads**

- Upload to Google Drive
- Upload to Dropbox
- Upload to OneDrive
- Upload to GoFile
- Upload to 1Fichier
- Upload to PixelDrain
- Manage transfer jobs
- OAuth flows for authentication

**Use when:** Uploading downloads to cloud storage.

---

### 10. general-service.md
**General Service - Unauthenticated endpoints**

- API status
- Get stats (all-time/30-day)
- Speedtest files

**Use when:** Checking API health or getting platform statistics.

---

### 11. quirks-and-errors.md
**Implementation details, quirks, error handling**

- `seed` parameter values (1/2/3)
- `post_processing` values (-1/0/1/2/3)
- `file_id` and `zip_link` semantics
- Check cached multi-hash format
- Inconsistent ID naming across services
- Content-Type requirements
- Error codes and handling

**Use when:** Troubleshooting, understanding API quirks, or handling errors.

---

## Plan Summary

| Plan | Price | Slots | Downloads/Month | Max Size | Usenet | API | Web Player |
|------|-------|-------|-----------------|----------|--------|-----|------------|
| Free | $0 | 1 | 10 | 10GB | ❌ | ❌ | ❌ |
| Essential | $3 | 3 | Unlimited | 200GB | ❌ | ✅ | ❌ |
| Standard | $5 | 5 | Unlimited | 200GB | ❌ | ✅ | ❌ |
| Pro | $10 | 10 | Unlimited | 1TB | ✅ | ✅ | ✅ |

---

## Quick Start

1. **First, check your plan:**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.torbox.app/v1/api/user/me
   ```

2. **Load the relevant section file** based on your task (see routing guide above).

3. **Use the Python helper** from `auth-and-plans.md` for consistent error handling.

---

## Common Patterns

### Adding a Torrent
1. Check cache (`torrents.md` - Check Cached)
2. Create torrent (`torrents.md` - Create Torrent)
3. Poll list until cached (`torrents.md` - Get Torrent List)
4. Request download link (`torrents.md` - Request Download Link)

### Uploading to Cloud
1. Get OAuth token (`integrations.md` - OAuth section)
2. Upload file (`integrations.md` - Upload endpoints)
3. Monitor job (`integrations.md` - Manage Transfer Jobs)

---

## Links

- **Repository:** https://github.com/hyper-154/torbox-skill
- **API Base:** https://api.torbox.app
- **OpenAPI Spec:** https://api.torbox.app/openapi.json

---

*Load only the sections you need to minimize context usage.*
