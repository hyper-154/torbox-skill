---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, search engines, streaming, and cloud integrations using pure HTTP API calls. This is a modular skill - load only the sections you need. See the routing guide below.
---
# IMPORTANT: Do not assume any features or limiations without checking relevant files.
# Torbox API Skill (Modular)

Pure HTTP API for managing torrents, Usenet, web downloads, search engines, streaming, and cloud integrations through Torbox. No SDK dependencies required.

---

## What is Torbox?

**Torbox is a debrid service** that downloads content on behalf of users and makes it available for direct download or streaming.

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Torrent Caching** | Add a magnet link or .torrent file. Torbox downloads it via "satellites". You download directly from Torbox's CDN. Supports most **Private Trackers**. |
| **Usenet Downloads** | (Pro only) Download NZB files from Usenet servers. |
| **Web Downloads** | Debrid direct download URLs from supported hosters, including **Baidu** and **Bunkr**. |
| **Streaming** | Stream directly in browser (Pro Web Player) with **Intro Detection/Skip** or via API to VLC, MPV, Kodi, and Stremio. |
| **Cloud Uploads** | Automatically upload completed downloads to Google Drive, Dropbox, etc. |
| **RSS Automation** | Auto-download from RSS feeds (torrent sites, Usenet indexers). |
| **FTP Access** | Access your downloads via FTP/SFTP using clients like Filezilla or Cyberduck. |
| **API/Integrations** | Extensive support for **RDTClient** (Radarr/Sonarr), JDownloader2, and custom indexers (BYOI). |

### Key Concepts

**Caching:** When you add a torrent, Torbox checks if it's already cached. Cached downloads are instant. Inactive or unused files may be purged periodically to manage storage costs.

**Debrid:** Instead of downloading P2P yourself, Torbox does it for you. You get a clean HTTPS download link from their CDN.

**Concurrent Slots:** Maximum simultaneous active downloads. Free=1, Essential=3, Standard=5, Pro=10. Additional downloads are queued.

**Seed Time:** How long Torbox seeds the torrent after downloading. Essential=24h, Standard=14d, Pro=30d.

**API Access:** Free plan has NO API access. Essential+ required to use this skill.

**Safety:** Automatic virus detection is performed on downloads to ensure user safety.

**Multi-IP Usage:** TorBox accounts can be used from multiple different IP addresses simultaneously.

**Email Policy:** Users can sign up with nearly any email, but **email changes are strictly prohibited** once registered.

---

## 🤖 Developer & Agent Guide

This skill is designed for both human users and automated agents. When performing tasks as an agent, follow these mandatory best practices:

### 1. Unified Search Strategy (Crucial)
The Torbox Search API separates Torrent and Usenet indexes. **Always query both** to provide a complete view of available content.
- **Why?** High-quality "Remux" files (raw Blu-ray) are significantly more common on Usenet, while Torrents may have more variety in compressed formats.
- **Action:** Call `GET search-api.torbox.app/torrents/search/...` AND `GET search-api.torbox.app/usenet/search/...`.

### 2. Instant Streaming Workflow (Cache-First)
To provide the best experience (no download waiting), follow this sequence:
1. **Search with Cache Check:** Use `check_cache=true` on both search endpoints.
2. **Filter for Cached Results:** Prioritize items where `cached: true`.
3. **Add with Safeguard:** Use the `add_only_if_cached=true` flag when adding the content to the account. This prevents accidentally starting a slow download if the cache status changed.
4. **Stream Direct:** Request the download link with `zip_link=false` and `redirect=false` to get a direct URL for media players.

### 3. Identity Consistency
When searching for known media, **prefer IMDb IDs** (`imdb:tt...`) over raw query strings. This ensures matching across both protocol silos.

---

## ⚡ Quick Routing Guide

**Load the appropriate section based on your task:**

| Task | Load Section |
|------|--------------|
| **Search for movies/TV shows** | `search.md` ⭐ |
| Check plan, auth, or API limits | `auth-and-plans.md` |
| Get user info, tokens, subscriptions | `user-account.md` |
| Create/manage torrents | `torrents.md` |
| Usenet downloads (NZB) | `usenet.md` |
| Web downloads (URL debrid) | `web-downloads.md` |
| RSS feed automation | `rss.md` |
| Video streaming & Web Player | `streaming.md` |
| Check notifications | `notifications.md` |
| Upload to cloud storage | `integrations.md` |
| API health, stats | `general-service.md` |
| Error codes, quirks, storage | `quirks-and-errors.md` |

---

## Base URL

```
https://api.torbox.app
```

---

## Section Files

### 1. search.md ⭐
**Search API - Find torrents and Usenet content**

- Search torrents by query or ID
- Search Usenet/NZB by query or ID
- Metadata search
- Torznab/Newznab API compatibility
- Download Usenet results

**Use when:** Looking for movies, TV shows, or other content to download. This is the starting point for most workflows.

**Note:** Separate API at `https://search-api.torbox.app`

---

### 2. auth-and-plans.md
**Authentication, plan limits, decision tree, Python helper**

- Plan limitations table (Free/Essential/Standard/Pro)
- Plan-based decision tree
- API key authentication
- Python helper with error handling

**Use when:** Checking user plan, understanding limits, or need the api_call() helper function.

---

### 3. user-account.md
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
