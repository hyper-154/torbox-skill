# Authentication And Plans

## Authentication

All authenticated endpoints require an API key via Bearer token header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.torbox.app/v1/api/user/me
```

⚠️ **Free plan does NOT have API access** — You must upgrade to Essential ($3/mo) or higher.

For unauthenticated endpoints (status, stats, changelogs), no token is needed.

---

## STEP 1: Check User Plan (CRITICAL)

**ALWAYS check the user's plan first** before performing operations. Different plans have different limitations.

### Get User Info

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.torbox.app/v1/api/user/me?settings=true"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "active_downloads": 3,
    "max_downloads": 10,
    "storage_used": 1073741824
  }
}
```

### Plan Limitations

| Feature | Free ($0/mo) | Essential ($3/mo) | Standard ($5/mo) | Pro ($10/mo) |
|---------|--------------|-------------------|------------------|--------------|
| **Concurrent Slots** | 1 | 3 | 5 | 10 |
| **Downloads Per Month** | 10 | Unlimited | Unlimited | Unlimited |
| **Max File Size** | 10GB | 200GB | 200GB | 1TB |
| **Seed Time** | 24h cooldown | 24 hours | 14 days | 30 days |
| **Max Speed** | 250Mbps | 1Gbps | 1Gbps | 80Gbps |
| **Traffic Priority** | Reduced | Normal | Normal | High |
| **Usenet Downloads** | ❌ NO | ❌ NO | ❌ NO | ✅ Unlimited |
| **API Access** | ❌ NO | ✅ YES | ✅ YES | ✅ YES |
| **3rd Party Apps** | ❌ NO | ✅ YES | ✅ YES | ✅ YES |
| **Web Player** | ❌ NO | ❌ NO | ❌ NO | ✅ YES |
| **RSS Feeds** | ❌ NO | Limited | Limited | ✅ Unlimited |

### Plan-Based Decision Tree

```
IF user.plan == "free":
    - ❌ NO API ACCESS — Cannot use this skill
    - Limited to exactly 10 downloads per month
    - Must upgrade to Essential+ for API access and unlimited downloads

IF user.plan == "essential":
    - Max 3 concurrent downloads
    - Unlimited downloads per month
    - 200GB max file size
    - 24h seed time only
    - CANNOT use Usenet endpoints (will fail)
    - NO Web Player
    - Limited RSS

IF user.plan == "standard":
    - Max 5 concurrent downloads
    - Unlimited downloads per month
    - 200GB max file size
    - 14 days seed time
    - CANNOT use Usenet endpoints (will fail)
    - NO Web Player
    - Limited RSS

IF user.plan == "pro":
    - Max 10 concurrent downloads
    - Unlimited downloads per month
    - ✅ CAN use Usenet endpoints (unlimited)
    - 30 days seed time
    - 1TB max file size
    - ✅ Web Player enabled (stream cached torrents in browser, no apps needed)
    - ✅ Unlimited RSS feeds
    - 80Gbps speed
```

### Python Helper to Check Plan

```python
import os
import urllib.request
import urllib.parse
import json

def api_call(method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
    """
    Make an API call to Torbox with proper error handling.
    """
    torbox_token = os.environ.get("TORBOX_API_KEY")
    if not torbox_token:
        raise RuntimeError("Set TORBOX_API_KEY environment variable")

    url = f"https://api.torbox.app{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {torbox_token}")
    
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}")
        raise
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        raise

# Check plan before any operation
user = api_call("GET", "/v1/api/user/me", params={"settings": "true"})
print(f"Plan: {user['data']['plan']}")
print(f"Active: {user['data']['active_downloads']}/{user['data']['max_downloads']}")

if user['data']['plan'] != 'pro':
    print("WARNING: Usenet requires Pro plan")
```
