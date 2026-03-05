# Torbox API Skill — Index & Routing Guide

Pure HTTP API for managing torrents, Usenet, web downloads, streaming, and cloud integrations through Torbox.

**Base URL:** `https://api.torbox.app`

---

## Load Order Rules

1. **Always load `auth-and-plans.md` first** before any authenticated operation — it contains plan checks, the Python API helper, and slot/limit guards.
2. **Load `quirks-and-errors.md`** alongside any service file when implementing or debugging.
3. **Gate Pro-only features** — check plan before loading `usenet.md` or `streaming.md`.

---

## Task → File Routing

| Task | Files to Load |
|------|---------------|
| Check user plan / verify API access | `auth-and-plans.md` |
| Add, delete, list, or download a torrent | `auth-and-plans.md` → `torrents.md` |
| Add, delete, list, or download a Usenet item | `auth-and-plans.md` → `usenet.md` ⚠️ Pro only |
| Add or manage a web download | `auth-and-plans.md` → `web-downloads.md` |
| Set up or manage RSS feeds | `auth-and-plans.md` → `rss.md` |
| Stream or play media in browser | `auth-and-plans.md` → `streaming.md` ⚠️ Pro only |
| Upload a download to Google Drive / Dropbox / etc. | `auth-and-plans.md` → `integrations.md` |
| Manage notifications | `auth-and-plans.md` → `notifications.md` |
| Manage account, tokens, search engines | `auth-and-plans.md` → `user-account.md` |
| Check API health, stats, speedtest (no auth) | `general-service.md` |
| Debug errors or unexpected behavior | `quirks-and-errors.md` |

---

## File Descriptions

- **`auth-and-plans.md`** — Bearer token setup, plan feature matrix, per-plan decision tree, Python `api_call()` helper.
- **`user-account.md`** — Get user info, refresh token, device OAuth, referrals, subscriptions, transactions, search engine config.
- **`torrents.md`** — Create (magnet/file), edit, control (delete/resume/reannounce), list, cache check, queued torrents, download link requests, torrent info.
- **`usenet.md`** — Create, control, list, download links, cache check, edit. **Pro plan required.**
- **`web-downloads.md`** — Create, control, list, download links, supported hosters, cache check, edit.
- **`rss.md`** — Add, control (pause/resume/delete), modify, get feeds and feed items.
- **`streaming.md`** — Create stream, get stream/playback data. Web Player UI is Pro-only.
- **`notifications.md`** — Fetch, clear (all or specific), test notifications.
- **`integrations.md`** — Upload to cloud (Google Drive, Dropbox, OneDrive, GoFile, 1Fichier, PixelDrain), OAuth registration, transfer job management.
- **`general-service.md`** — Unauthenticated endpoints: API status, all-time stats, speedtest files.
- **`quirks-and-errors.md`** — `seed` semantics, `post_processing` values, `file_id`/`zip_link` behavior, multi-hash formats, inconsistent ID field names, Content-Type requirements, error codes.
