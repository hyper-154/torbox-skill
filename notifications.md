# Torbox — Notifications Service

> **Prerequisite:** Load `auth-and-plans.md` first.

---

## Get Notifications

```bash
# JSON format (authenticated header)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/mynotifications

# RSS format (token in query string)
curl "https://api.torbox.app/v1/api/notifications/rss?token=YOUR_TOKEN"
```

**Example Response (JSON):**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "type": "download_complete",
      "message": "Torrent 'My File' has finished downloading",
      "created_at": "2024-01-15T10:30:00Z",
      "read": false
    }
  ]
}
```

---

## Clear Notifications

```bash
# Clear ALL notifications
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear

# Clear a SPECIFIC notification by ID
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear/123
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | string | Yes (specific) | Notification ID to clear |

---

## Test Notification

Sends a test notification to verify your notification settings. **Rate limited to 1 per minute.**

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/test
```
