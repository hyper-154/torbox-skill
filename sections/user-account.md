# User Account Service

## User Service

Manage user account, subscriptions, devices, and search engines.

### Refresh Token

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"session_token": "YOUR_SESSION_TOKEN"}' \
  https://api.torbox.app/v1/api/user/refreshtoken
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `session_token` | body | string | Yes | Your current session token |

**Example Response:**
```json
{
  "success": true,
  "data": "NEW_TOKEN_STRING"
}
```

### Device Authentication (OAuth)

Used for TV apps or CLI tools to login without entering passwords.

```bash
# 1. Start Device Auth
curl "https://api.torbox.app/v1/api/user/auth/device/start?app=MyApp"

# Returns {"data": {"device_code": "ABCDEF", "user_code": "12345", "verification_uri": "https://torbox.app/device"}}

# 2. Poll for Token (until user authorizes)
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"device_code": "ABCDEF"}' \
  https://api.torbox.app/v1/api/user/auth/device/token
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `app` | query | string | No | App name (default: "Third Party App") |
| `device_code` | body | string | Yes | Device code from start endpoint |

### Add Referral

```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/addreferral?referral=REFERRAL_CODE"
```

### Delete Account

```bash
# 1. Get confirmation code
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/getconfirmation

# 2. Confirm deletion
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_token": "YOUR_TOKEN", "confirmation_code": 123456}' \
  https://api.torbox.app/v1/api/user/deleteme
```

### Subscriptions & Transactions

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/subscriptions
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/transactions
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/user/transaction/pdf?transaction_id=xyz" -o receipt.pdf
```

### Search Engines

Configure search engines like Prowlarr, Jackett, or NZBHydra.

```bash
# Get Search Engines
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.torbox.app/v1/api/user/settings/searchengines"

# Add Search Engine
curl -X PUT -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"type": "prowlarr", "url": "http://prowlarr:9696", "apikey": "key", "download_type": "torrents"}' \
  https://api.torbox.app/v1/api/user/settings/addsearchengines

# Modify Search Engine
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"id": 1, "type": "prowlarr", "url": "http://prowlarr:9696", "apikey": "key", "download_type": "torrents"}' \
  https://api.torbox.app/v1/api/user/settings/modifysearchengines

# Control Search Engine
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"operation": "enable", "id": 1, "all": false}' \
  https://api.torbox.app/v1/api/user/settings/controlsearchengines
```
