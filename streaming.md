# Torbox — Streaming Service

> ⚠️ **Web Player (in-browser streaming UI) requires Pro plan.** The streaming API endpoints themselves work on all plans, but the Web Player feature is Pro-only. Always verify plan before directing users to the Web Player.

> **Prerequisite:** Load `auth-and-plans.md` first.

---

## Overview

Streaming works in two steps:

1. **`createstream`** — Create a stream session for a specific file. Returns a `presigned_token`.
2. **`getstreamdata`** — Use the `presigned_token` to get the actual playback URL and stream metadata.

---

## Step 1: Create Stream

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/stream/createstream?id=123&type=torrent&file_id=0"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | query | integer | **Yes** | Item ID (torrent, usenet, or webdl) |
| `file_id` | query | integer | No | File index within the item (default: `0`) |
| `type` | query | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `chosen_subtitle_index` | query | integer | No | Subtitle track index |
| `chosen_audio_index` | query | integer | No | Audio track index (default: `0`) |
| `chosen_resolution_index` | query | integer | No | Resolution index |
| `scrobbling_enabled` | query | boolean | No | Enable watch progress tracking (default: `true`) |

**Returns:** A `presigned_token` used in the next step.

---

## Step 2: Get Stream Data (Playback URL)

```bash
curl "https://api.torbox.app/v1/api/stream/getstreamdata?\
token=YOUR_TOKEN&\
presigned_token=abc123def456"
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | **Yes** | Your API key |
| `presigned_token` | query | string | **Yes** | Token returned by `createstream` |
| `chosen_subtitle_index` | query | integer | No | Override subtitle track |
| `chosen_audio_index` | query | integer | No | Override audio track |
| `chosen_resolution_index` | query | integer | No | Override resolution |
| `scrobbling_enabled` | query | boolean | No | Override scrobbling setting |

**Returns:** Playback URL and stream metadata (subtitles, audio tracks, resolutions available).
