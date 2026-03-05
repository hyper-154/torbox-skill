# Notifications

## Notifications Service

Get and manage user notifications.

### Get Notifications

```bash
# JSON format (authenticated)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/mynotifications

# RSS format (token in query)
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

### Clear Notifications

```bash
# Clear all notifications
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear

# Clear specific notification
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/clear/123
```

**Parameters (for specific clear):**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | string | Yes | Notification ID |

### Test Notification

Sends a test notification to verify your notification settings. Rate limited to 1 per minute.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/notifications/test
```
