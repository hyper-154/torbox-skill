# Integrations

## Integrations Service

Upload downloads to cloud storage. Supported platforms: `googledrive`, `dropbox`, `onedrive`, `gofile`, `1fichier`, `pixeldrain`.

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
| `file_id` | body | integer | No | File index (required if `zip` is `false`) |
| `zip` | body | boolean | No | Upload entire download as zip (default: `false`) |
| `type` | body | string | No | `torrent`, `usenet`, or `webdl` |
| `{provider}_token`| body | string | **Yes**| OAuth token for respective provider |

### Other Integrations

TorBox supports various external tools and applications:

- **FTP Access:** Access your downloads via FTP/SFTP. Recommended clients are **Filezilla** and **Cyberduck**.
- **JDownloader2:** Download your TorBox web downloads and torrent files directly in JDownloader2.
- **RDTClient:** Connect TorBox with **Radarr** and **Sonarr** using RDTClient (Docker-based).
- **Mobile Apps:** Community-developed mobile apps are available for both iOS and Android.
- **Ferrite:** iOS-only search engine for torrents integrated with TorBox.

### Manage Transfer Jobs

```bash
# Get all jobs
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/jobs

# Get jobs by download hash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/jobs/ABC123DEF456

# Get specific job details
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/job/JOB_ID

# Cancel/Delete a specific job
curl -X DELETE -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/integration/job/JOB_ID
```

