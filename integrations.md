# Torbox — Integrations Service

Upload completed downloads to cloud storage. Supported providers: `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.

> **Prerequisite:** Load `auth-and-plans.md` first.

---

## Provider Token Field Names

Each provider requires its own token field in the upload request body:

| Provider | Token Field | Required |
|----------|-------------|----------|
| Google Drive | `google_token` | Yes |
| Dropbox | `dropbox_token` | Yes |
| OneDrive | `onedrive_token` | Yes |
| GoFile | `gofile_token` | Optional |
| 1Fichier | `onefichier_token` | Optional |
| PixelDrain | `pixeldrain_token` | Optional |

---

## Upload to Cloud

```bash
# Example: Upload to Google Drive
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "file_id": 0,
    "zip": false,
    "type": "torrent",
    "google_token": "GOOGLE_OAUTH_TOKEN"
  }' \
  https://api.torbox.app/v1/api/integration/googledrive
```

Replace `googledrive` in the URL with the target provider slug. Include the appropriate `{provider}_token` field.

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | body | integer | **Yes** | Download ID |
| `file_id` | body | integer | No | File index (default: `0`) |
| `zip` | body | boolean | No | Upload as zip (default: `false`) |
| `type` | body | string | No | `torrent`, `usenet`, or `webdl` |
| `{provider}_token` | body | string | **Yes** | OAuth token for the target provider |

---

## Manage Transfer Jobs

Check the status of ongoing cloud upload jobs.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/jobs
```

---

## OAuth Flow

Use this to connect a cloud storage provider via OAuth, or to register your own OAuth tokens.

### View Connected Integrations

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/me
```

### Start OAuth Flow (Redirect to Provider)

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive
```

The OAuth callback is handled by the provider, then routed back to Torbox:
```
GET/POST /v1/api/integration/oauth/{provider}/callback
```

### Get Token After Successful OAuth

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/success
```

### Register Your Own OAuth Tokens

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_oauth_access_token",
    "refresh_token": "your_oauth_refresh_token"
  }' \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/register
```

| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | body | string | Yes | OAuth access token |
| `refresh_token` | body | string | Yes | OAuth refresh token |

### Unregister OAuth Link

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/unregister
```

> Replace `googledrive` in all OAuth URLs with the target provider slug: `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.
