# Streaming

## Streaming Service

⚠️ **PRO PLAN ONLY** — The Web Player feature (in-browser streaming) requires Pro plan. The streaming endpoints work on all plans, but the Web Player UI is Pro-only.

### Create Stream

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/stream/createstream?id=123&type=torrent&file_id=0"
```

**Parameters (`createstream`):**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | query | integer | **Yes**| Item ID |
| `file_id` | query | integer | No | File index (default: `0`) |
| `type` | query | string | No | `torrent`, `usenet`, or `webdl` (default: `torrent`) |
| `chosen_subtitle_index` | query | integer | No | Subtitle track index |
| `chosen_audio_index` | query | integer | No | Audio track index (default: `0`) |
| `chosen_resolution_index` | query | integer | No | Resolution index |
| `scrobbling_enabled` | query | boolean | No | Enable scrobbling (default: `true`) |

### Get Stream Data (Playback URL)

```bash
curl "https://api.torbox.app/v1/api/stream/getstreamdata?token=YOUR_TOKEN&presigned_token=abc123def456"
```

**Parameters (`getstreamdata`):**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | query | string | **Yes**| API key |
| `presigned_token` | query | string | **Yes**| From createstream response |
| `chosen_subtitle_index` | query | integer | No | Same as createstream |
| `chosen_audio_index` | query | integer | No | Same as createstream |
| `chosen_resolution_index` | query | integer | No | Same as createstream |
| `scrobbling_enabled` | query | boolean | No | Same as createstream |
