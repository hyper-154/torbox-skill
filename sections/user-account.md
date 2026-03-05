# User Account Service

## User Service

Manage user account, subscriptions, devices, and search engines.

### Account Policies
- **Multi-IP Usage:** TorBox accounts can be used from multiple different IP addresses worldwide at the same time.
- **Email Policy:** Most email addresses are allowed for sign-up (suspicious ones are blocked), but **email changes are strictly not allowed** once registered.

### Get User Data

Retrieves user profile information, plan details, and optionally settings.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/me?settings=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `settings` | query | boolean | No | Include user settings in the response (default: `false`) |

### Refresh Token

Generates a new API token using a session token.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"session_token": "YOUR_SESSION_TOKEN"}' \
  https://api.torbox.app/v1/api/user/refreshtoken
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `session_token` | body | string | Yes | Your current session token (found in local storage as `torbox_session_token` when logged into the website) |

### Device Authentication (OAuth)

Used for TV apps or CLI tools to login without entering passwords.

```bash
# 1. Start Device Auth
curl "https://api.torbox.app/v1/api/user/auth/device/start?app=My%20CLI%20App"

# Returns:
# {
#   "success": true,
#   "data": {
#     "device_code": "XXXXXXXXXXXXXXXXXXXXXXXXX",
#     "user_code": "XXXX-XXXX",
#     "verification_uri": "https://torbox.app/device",
#     "expires_in": 300,
#     "interval": 5
#   }
# }

# 2. Poll for Token (until user authorizes the user_code at verification_uri)
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"device_code": "XXXXXXXXXXXXXXXXXXXXXXXXX"}' \
  https://api.torbox.app/v1/api/user/auth/device/token
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `app` | query | string | No | App name displayed to the user during verification |
| `device_code` | body | string | Yes | The `device_code` returned from the start endpoint |

### Add Referral

Add a referral code to your account. Must be a valid UUID.

```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/addreferral?referral=REFERRAL_UUID"
```

### Referral Data

Get information about your referrals.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.torbox.app/v1/api/user/referraldata
```

### Subscriptions & Transactions

Manage billing and receipts.

```bash
# Get active subscriptions
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/subscriptions

# Get all transactions
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.torbox.app/v1/api/user/transactions

# Get transaction receipt as PDF
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/transaction/pdf?transaction_id=XYZ" -o receipt.pdf
```

### Search Engine Configuration

Configure external indexers (Prowlarr, Jackett, etc.) for integrated search.

```bash
# Get configured search engines
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/settings/searchengines?id=OPTIONAL_ID"

# Add search engine
curl -X PUT -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "type": "prowlarr",
    "url": "http://prowlarr:9696",
    "apikey": "YOUR_API_KEY",
    "download_type": "torrents"
  }' \
  https://api.torbox.app/v1/api/user/settings/addsearchengines

# Modify search engine
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "url": "http://new-prowlarr:9696"
  }' \
  https://api.torbox.app/v1/api/user/settings/modifysearchengines

# Control search engine (enable/disable/delete)
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"operation": "delete", "id": 1, "all": false}' \
  https://api.torbox.app/v1/api/user/settings/controlsearchengines
```

### Delete Account

