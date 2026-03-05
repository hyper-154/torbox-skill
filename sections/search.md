---
name: torbox-search
description: Torbox Search API for finding torrents and Usenet content. Use when searching for movies, TV shows, or other content to download. This is separate from the main Torbox API and requires authentication.
---

# Torbox Search API

**Base URL:** `https://search-api.torbox.app`

**Note:** This is a **separate API** from the main Torbox API (`https://api.torbox.app`). The Search API requires authentication and provides torrent/Usenet search functionality.

## Authentication

The Search API uses the same OAuth2 authentication as the main API:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/torrents/search/Mad%20Max"
```

## Custom Search Engines (BYOI)

TorBox allows you to "Bring Your Own Indexers" (BYOI). You can configure your own external search engines (like Prowlarr, Jackett, or NZBHydra) in your TorBox account settings and use them within the Search API and Stremio integration.

To use your custom engines in a search, set `search_user_engines=true` in your search query.

**Note:** Configuration of these engines is done via the **User Service** (see `user-account.md`).

## 🤖 Agent Strategy: Unified Search

Automated agents should **always combine results** from both Torrent and Usenet search endpoints to ensure the best content availability. High-fidelity raw Blu-ray data (Remux) is significantly more prevalent on Usenet.

### Recommended Logic:
1. Call both search endpoints with `check_cache=true`.
2. Aggregate the `torrents` and `nzbs` lists.
3. Prioritize items where `cached: true`.

### Using the CLI Helper:
The included `scripts/torbox-api.py` handles this aggregation automatically:
```bash
python3 scripts/torbox-api.py unified-search "Mad Max Fury Road" --metadata
```

## Search Endpoints

### Search Torrents

Search for torrents by query string.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/torrents/search/Mad%20Max%20Fury%20Road?metadata=true&check_cache=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `query` | path | string | **Yes** | Search query (URL-encoded) |
| `metadata` | query | boolean | No | Include metadata (default: `false`) |
| `check_cache` | query | boolean | No | Check if cached on Torbox (default: `false`) |
| `check_owned` | query | boolean | No | Check if owned by user (default: `false`) |
| `search_user_engines` | query | boolean | No | Search user's configured engines (default: `false`) |
| `cached_only` | query | boolean | No | Return only cached results (default: `false`) |

### Search Torrents by ID

Search for torrents using a metadata ID.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/torrents/imdb:tt1392190?metadata=true&season=1&episode=1"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | string | **Yes** | Format: `id_type:id`. Supported types: `imdb`, `tmdb`, `tvdb`, `mal`, `anilist`. |
| `metadata` | query | boolean | No | Include metadata (default: `false`) |
| `season` | query | integer | No | Season number (for TV shows) |
| `episode` | query | integer | No | Episode number (for TV shows) |
| `check_cache` | query | boolean | No | Check if cached (default: `false`) |
| `check_owned` | query | boolean | No | Check if owned (default: `false`) |
| `cached_only` | query | boolean | No | Return only cached (default: `false`) |

### Search Usenet (NZB)

Search for Usenet/NZB content.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/usenet/search/Mad%20Max%20Fury%20Road?metadata=true"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `query` | path | string | **Yes** | Search query (URL-encoded) |
| `metadata` | query | boolean | No | Include metadata (default: `false`) |
| `check_cache` | query | boolean | No | Check if cached (default: `false`) |
| `check_owned` | query | boolean | No | Check if owned (default: `false`) |
| `search_user_engines` | query | boolean | No | Search user's configured engines (default: `false`) |
| `cached_only` | query | boolean | No | Return only cached (default: `false`) |

**Note:** Usenet search requires **Pro plan**.

### Search Usenet by ID

Search Usenet using a metadata ID.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/usenet/imdb:tt1392190?season=1&episode=1"
```

**Parameters:** Same as torrents by ID.

### Download Usenet Result

Download a specific Usenet result after searching.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://search-api.torbox.app/usenet/download/12345/abc-guid-here"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | integer | **Yes** | Result ID from search |
| `guid` | path | string | **Yes** | GUID from search result |

## Metadata Endpoints

### Search Meta Tutorial

```bash
curl https://search-api.torbox.app/meta
```

### Query Search Meta

Search for metadata by query.

```bash
curl "https://search-api.torbox.app/meta/search/Inception?type=media"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `query` | path | string | **Yes** | Search query |
| `type` | query | string | No | `file` or `media` (default: `media`) |

### Get Meta by ID

```bash
curl "https://search-api.torbox.app/meta/imdb:tt1392190?media_type=movies"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `id` | path | string | **Yes** | Format: `id_type:id`. Supported types: `imdb`, `tmdb`, `tvdb`, `mal`, `anilist`. |
| `media_type` | query | string | No | `movies` or `series` (default: `movies`) |


## Standard APIs

### Torznab API (Torrents)

Standard Torznab API compatible with Sonarr, Radarr, etc.

```bash
curl "https://search-api.torbox.app/torznab/api?apikey=YOUR_TOKEN&t=search&q=Mad+Max"
```

**Parameters:**
| Field | In | Type | Required | Description |
|-------|----|------|----------|-------------|
| `apikey` | query | string | **Yes** | Your API key |
| `t` | query | string | **Yes** | Action type (`search`, `tvsearch`, `movie`, etc.) |
| `q` | query | string | No | Search query |
| `season` | query | integer | No | Season number |
| `ep` | query | integer | No | Episode number |
| `imdbid` | query | string | No | IMDb ID |
| `tmdbid` | query | integer | No | TMDb ID |
| `tvdbid` | query | integer | No | TVDB ID |
| `offset` | query | integer | No | Pagination offset (default: `0`) |
| `o` | query | string | No | Output format `xml` or `json` (default: `xml`) |

### Newznab API (Usenet)

Standard Newznab API compatible with NZB applications.

```bash
curl "https://search-api.torbox.app/newznab/api?apikey=YOUR_TOKEN&t=search&q=Mad+Max"
```

**Parameters:** Same as Torznab API.

## Tutorial Endpoints

### Torrents Tutorial

```bash
curl https://search-api.torbox.app/torrents
```

### Usenet Tutorial

```bash
curl https://search-api.torbox.app/usenet
```

## Example Workflow

**Search for a movie and add to Torbox:**

```python
import urllib.request
import json

TORBOX_TOKEN = "your_token"

# 1. Search for torrents
req = urllib.request.Request(
    "https://search-api.torbox.app/torrents/search/Mad%20Max%20Fury%20Road?check_cache=true",
    headers={"Authorization": f"Bearer {TORBOX_TOKEN}"}
)
with urllib.request.urlopen(req) as resp:
    results = json.loads(resp.read().decode())
    
# 2. Find a cached result
for result in results['data']:
    if result.get('cached'):
        print(f"Found cached: {result['title']}")
        print(f"Magnet: {result['magnet']}")
        
        # 3. Add to Torbox (using main API)
        # POST /v1/api/torrents/createtorrent with the magnet
        break
```

## Plan Requirements

| Feature | Free | Essential | Standard | Pro |
|---------|------|-----------|----------|-----|
| **Torrent Search** | ❌ | ✅ | ✅ | ✅ |
| **Usenet Search** | ❌ | ❌ | ❌ | ✅ |
| **Torznab/Newznab** | ❌ | ✅ | ✅ | ✅ |

## Important Notes

1. **Separate API**: This search API is at `search-api.torbox.app`, NOT `api.torbox.app`

2. **Authentication Required**: Unlike the article suggesting it's public, the API spec shows OAuth2 authentication is required for most endpoints

3. **Pro Required for Usenet**: Usenet search requires Pro plan

4. **Cached Results**: Use `check_cache=true` to see if content is already cached on Torbox (instant download)

5. **Integration with Main API**: 
   - Search here to find content
   - Then use main API (`api.torbox.app`) to add torrents/Usenet downloads

---

**See Also:**
- Main Torbox API: `torbox` skill sections
- Base URL: https://search-api.torbox.app
