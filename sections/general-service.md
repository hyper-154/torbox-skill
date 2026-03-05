# General Service

## General Service

Unauthenticated endpoints for API health and info.

### Get API Status

```bash
curl https://api.torbox.app/
```
**Example Response:**
```json
{
  "success": true,
  "data": "API is online",
  "detail": "Welcome to Torbox API"
}
```

### Get Stats

Returns platform-wide statistics.

```bash
# All-time stats
curl https://api.torbox.app/v1/api/stats

# 30-day stats
curl https://api.torbox.app/v1/api/stats/30days
```

### Changelogs

```bash
# Get changelogs in JSON format
curl https://api.torbox.app/v1/api/changelogs/json

# Get changelogs RSS feed
curl https://api.torbox.app/v1/api/changelogs/rss
```

### Speedtest Files

```bash
curl "https://api.torbox.app/v1/api/speedtest?test_length=short&region=us"
```

**Parameters:**
| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `test_length` | query | string | No | `short` or `long` |
| `region` | query | string | No | CDN region (e.g., `us`, `eu`, `asia`) |
| `user_ip` | query | string | No | User's IP to determine closest CDNs |

