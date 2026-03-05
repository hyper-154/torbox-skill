# Quirks And Errors

## API Implementation Details & Quirks

When implementing the TorBox API, be aware of the following undocumented or easily confused behaviors:

### 1. `seed` Parameter in Create Torrent
The `seed` parameter is not a ratio limit, but a **behavioral setting** for seeding on private trackers:
- **`1` (Auto)**: Follows default account settings.
- **`2` (Always)**: Forces the torrent to continue seeding indefinitely (prevents Hit and Runs).
- **`3` (Never)**: Stops seeding immediately after download completes.

### 2. `post_processing` in Usenet
Determines PAR2 repair and archive extraction behavior (default is `-1`):
- **`-1` (Default)**: Repair, extract, and delete original archives (Recommended).
- **`0` (None)**: Download raw files only; no repair or extraction.
- **`1` (Repair)**: Verify and repair using PAR2, but do not extract.
- **`2` (Repair & Unpack)**: Repair and extract, keeping original archives.
- **`3` (Repair, Unpack, & Delete)**: Same as `-1`.

### 3. `file_id` and `zip_link` Semantics
Across all `requestdl` endpoints (Torrents, Usenet, Webdl):
- **`zip_link=true`**: Returns a `.zip` archive of the entire download package. `file_id` is generally ignored.
- **`zip_link=false`**: Returns a direct link to a single file. You **must** specify a valid `file_id` (defaults to `0`, which is usually the first file). For streaming (e.g., in Stremio), always use `zip_link=false`.

### 4. Check Cached Multi-Hash
The `checkcached` endpoints support multiple hashes, but the format differs by HTTP method:
- **GET**: Use multiple query parameters: `?hash=HASH1&hash=HASH2`
- **POST**: Pass a JSON array in the body: `{"hashes": ["HASH1", "HASH2"]}`

### 5. Inconsistent ID Naming
ID fields vary depending on the service and the specific endpoint being called:
- **Torrents**: `torrent_id` (used everywhere for torrents).
- **Usenet**: `usenet_id` (used in control and requestdl), `usenet_download_id` (used in edit).
- **Web Downloads**: `web_id` (used in requestdl), `webdl_id` (used in control and edit).
- **Queued / RSS**: `queued_id`, `rss_feed_id`.

### 6. Content-Type Requirements
Pay close attention to required Content-Types when creating downloads:
- **Torrents (`createtorrent`)**: Requires `multipart/form-data` (to support optional `.torrent` file uploads).
- **Usenet (`createusenetdownload`)**: Requires `multipart/form-data` (to support optional `.nzb` file uploads).
- **Web Downloads (`createwebdownload`)**: Requires `application/x-www-form-urlencoded`.

### 7. File Storage and Purging
- **Caching:** TorBox stores and caches files for users, but it does **not** claim to store them indefinitely.
- **Purge Behavior:** Since storage is expensive, inactive or unused files are eventually purged from the cache.
- **Inactive Downloads:** If a download is not being used or accessed, it may be marked as inactive and cleared to make room for new content.

---

## Error Handling

All responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "detail": "optional message"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "ERROR_CODE",
  "detail": "Error description"
}
```

**Common Error Codes:**
| Code | Description |
|------|-------------|
| `ENDPOINT_NOT_FOUND` | Invalid URL |
| `VALIDATION_ERROR` | Invalid parameters |
| `AUTHENTICATION_FAILED` | Invalid or missing token |
| `RATE_LIMITED` | Too many requests (see Rate Limits) |
| `PLAN_RESTRICTION` | Feature requires higher plan |
| `SLOTS_FULL` | Concurrent download limit reached |
| `FILE_TOO_LARGE` | Exceeds plan size limit |
