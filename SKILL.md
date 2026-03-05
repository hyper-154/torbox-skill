---
name: torbox
description: Interact with Torbox API for torrents, Usenet, web downloads, streaming, and cloud integrations. This is the index file - load specific sections as needed for on-demand context.
---

# Torbox API Skill - Index

This skill is organized into modular sections for on-demand loading. Only load the sections relevant to your current task to minimize context usage.

## Quick Reference

| Task | Load Section |
|------|--------------|
| Check plan, authenticate, understand limits | `auth-and-plans.md` |
| Get user info, manage account, device auth | `user-account.md` |
| Create/manage torrents, check cache, download | `torrents.md` |
| Usenet downloads (NZB) — **Pro only** | `usenet.md` |
| Web downloads from hosters | `web-downloads.md` |
| RSS feed automation | `rss.md` |
| Streaming/Web Player — **Pro only** | `streaming.md` |
| Get/clear notifications | `notifications.md` |
| Upload to Google Drive, Dropbox, etc. | `integrations.md` |
| Check API status, stats, speedtest | `general-service.md` |
| API quirks, error codes, troubleshooting | `quirks-and-errors.md` |

## Base URL

```
https://api.torbox.app
```

## Section Files

All sections are in the `sections/` directory:

- `sections/auth-and-plans.md` — Authentication, plan limits, decision tree, Python helper
- `sections/user-account.md` — User info, tokens, device auth, referrals, subscriptions, search engines
- `sections/torrents.md` — Torrent creation, control, list, cache check, download links
- `sections/usenet.md` — Usenet downloads (Pro only)
- `sections/web-downloads.md` — Web downloads, hosters, cache check
- `sections/rss.md` — RSS feeds management
- `sections/streaming.md` — Streaming endpoints (Web Player is Pro-only)
- `sections/notifications.md` — Notification management
- `sections/integrations.md` — Cloud uploads, OAuth flows
- `sections/general-service.md` — Unauthenticated endpoints (status, stats)
- `sections/quirks-and-errors.md` — API quirks, ID naming, error handling

## Plan Requirements Quick Reference

| Feature | Free | Essential | Standard | Pro |
|---------|------|-----------|----------|-----|
| API Access | ❌ | ✅ | ✅ | ✅ |
| Torrents | ❌ | ✅ | ✅ | ✅ |
| Web Downloads | ❌ | ✅ | ✅ | ✅ |
| Usenet | ❌ | ❌ | ❌ | ✅ |
| Web Player (Streaming UI) | ❌ | ❌ | ❌ | ✅ |
| RSS Feeds | ❌ | Limited | Limited | Unlimited |
| Concurrent Slots | 1 | 3 | 5 | 10 |

## Quick Start

1. **Always start with `auth-and-plans.md`** to understand authentication and check the user's plan
2. Load the specific service section for your task (torrents, usenet, web-downloads, etc.)
3. Reference `quirks-and-errors.md` for troubleshooting and edge cases

---

*For detailed API documentation, load the appropriate section file above.*
