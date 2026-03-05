# Integrations

## Integrations Service

Upload downloads to cloud storage. Supported platforms: `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.

### Integration OAuth & Token Acquisition

1. **OAuth Flow Overview**:
   - `GET /v1/api/integration/oauth/me` - Get connected OAuth integrations
   - `GET /v1/api/integration/oauth/{provider}` - Start OAuth redirect
   - `POST/GET /v1/api/integration/oauth/{provider}/callback` - OAuth callback
   - `GET /v1/api/integration/oauth/{provider}/success` - Get token after success
   - `POST /v1/api/integration/oauth/{provider}/register` - Register OAuth token
   - `DELETE /v1/api/integration/oauth/{provider}/unregister` - Remove OAuth link

2. **Token Field Names** (from integration_schemas.json):
   - Google Drive: `google_token` (required)
   - Dropbox: `dropbox_token` (required)
   - OneDrive: `onedrive_token` (required)
   - GoFile: `gofile_token` (optional)
   - 1Fichier: `onefichier_token` (optional)
   - PixelDrain: `pixeldrain_token` (optional)

3. **OAuth Register Request Body**:
   ```json
   {
     "token": "oauth_access_token",
     "refresh_token": "oauth_refresh_token"
   }
   ```

### Upload to Cloud

```bash
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

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | body | integer | **Yes**| Download ID |
| `file_id` | body | integer | No | File index (default: `0`) |
| `zip` | body | boolean | No | Upload as zip (default: `false`) |
| `type` | body | string | No | `torrent`, `usenet`, or `webdl` |
| `{provider}_token`| body | string | **Yes**| OAuth token for respective provider |

### Manage Transfer Jobs

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/jobs
```

### Integration OAuth & Token Acquisition

TorBox provides OAuth flows for connecting cloud storage providers. You can either use TorBox's built-in OAuth redirects or register your own OAuth tokens.

**Token Field Names by Provider:**
| Provider | Token Field | Required |
|----------|-------------|----------|
| Google Drive | `google_token` | Yes |
| Dropbox | `dropbox_token` | Yes |
| OneDrive | `onedrive_token` | Yes |
| GoFile | `gofile_token` | No |
| 1Fichier | `onefichier_token` | No |
| PixelDrain | `pixeldrain_token` | No |

**OAuth Endpoints:**

```bash
# Get connected OAuth integrations
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/me

# Start OAuth flow (redirects to provider)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive

# OAuth callback (handled by provider, then TorBox)
# GET/POST /v1/api/integration/oauth/{provider}/callback

# Get token after successful OAuth (success page)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/success

# Register your own OAuth tokens
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_oauth_access_token",
    "refresh_token": "your_oauth_refresh_token"
  }' \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/register

# Unregister OAuth link
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/integration/oauth/googledrive/unregister
```

**OAuth Register Request Body:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `token` | body | string | Yes | OAuth access token |
| `refresh_token` | body | string | Yes | OAuth refresh token |

**Note:** Providers are `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.
