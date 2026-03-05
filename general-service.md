# Torbox — General Service

Unauthenticated endpoints for API health, statistics, and speedtest files. No API key required.

---

## Get API Status

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

---

## Get All-Time Stats

```bash
curl https://api.torbox.app/v1/api/stats
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "total_users": 50000,
    "total_torrents": 1200000
  }
}
```

---

## Speedtest Files

Returns CDN file URLs for measuring download speed.

```bash
curl "https://api.torbox.app/v1/api/speedtest?test_length=short&region=all"
```

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| `test_length` | query | string | No | `short` or `long` |
| `region` | query | string | No | CDN region name (omit to get all available regions) |
