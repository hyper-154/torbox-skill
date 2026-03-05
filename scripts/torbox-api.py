#!/usr/bin/env python3
"""Torbox API CLI helper - Simplified interface for common Torbox operations."""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from typing import Optional

BASE_URL = "https://api.torbox.app"


def api_call(method: str, endpoint: str, token: Optional[str] = None, 
             data=None, params=None, is_json=True) -> dict:
    """Make an API call to Torbox."""
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if data and is_json:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    elif data:
        # Form data
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = urllib.parse.urlencode(data).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        try:
            error_body = json.loads(e.read().decode())
            return error_body
        except:
            return {"success": False, "error": f"HTTP {e.code}", "detail": str(e)}
    except Exception as e:
        return {"success": False, "error": "REQUEST_FAILED", "detail": str(e)}


def cmd_status(_):
    """Get API status."""
    result = api_call("GET", "/")
    print(json.dumps(result, indent=2))


def cmd_stats(args):
    """Get Torbox stats."""
    endpoint = "/v1/api/stats/30days" if args.days30 else "/v1/api/stats"
    result = api_call("GET", endpoint)
    print(json.dumps(result, indent=2))


def cmd_user_info(args):
    """Get user information."""
    result = api_call("GET", "/v1/api/user/me", token=args.token, 
                     params={"settings": args.settings})
    print(json.dumps(result, indent=2))


def cmd_torrents_list(args):
    """List torrents."""
    params = {"offset": args.offset, "limit": args.limit}
    if args.id:
        params["id"] = args.id
    if args.bypass_cache:
        params["bypass_cache"] = True
    
    result = api_call("GET", "/v1/api/torrents/mylist", token=args.token, params=params)
    print(json.dumps(result, indent=2))


def cmd_torrents_create(args):
    """Create a torrent from magnet or file."""
    if not args.magnet and not args.file:
        print("Error: Either --magnet or --file is required", file=sys.stderr)
        sys.exit(1)
    
    data = {
        "allow_zip": args.allow_zip,
        "as_queued": args.queued,
        "add_only_if_cached": args.cached_only
    }
    if args.magnet:
        data["magnet"] = args.magnet
    if args.name:
        data["name"] = args.name
    if args.seed:
        data["seed"] = args.seed
    
    if args.file:
        # File upload requires multipart, use curl fallback
        print(f"File upload not supported via CLI. Use curl:")
        print(f"curl -X POST -H 'Authorization: Bearer {args.token}' \\")
        print(f"  -F 'file=@{args.file}' \\")
        if args.magnet:
            print(f"  -F 'magnet={args.magnet}' \\")
        print(f"  https://api.torbox.app/v1/api/torrents/createtorrent")
        return
    
    result = api_call("POST", "/v1/api/torrents/createtorrent", 
                     token=args.token, data=data, is_json=True)
    print(json.dumps(result, indent=2))


def cmd_torrents_control(args):
    """Control a torrent (pause/resume/delete)."""
    data = {
        "operation": args.operation,
        "all": args.all
    }
    if args.id:
        data["torrent_id"] = args.id
    
    result = api_call("POST", "/v1/api/torrents/controltorrent",
                     token=args.token, data=data, is_json=True)
    print(json.dumps(result, indent=2))


def cmd_torrents_cache(args):
    """Check if torrents are cached."""
    hashes = args.hashes.split(",")
    data = {"hashes": hashes}
    params = {
        "format": args.format,
        "list_files": args.list_files
    }
    
    result = api_call("POST", "/v1/api/torrents/checkcached",
                     token=args.token, data=data, params=params, is_json=True)
    print(json.dumps(result, indent=2))


def cmd_torrents_download(args):
    """Request download link for a torrent."""
    params = {
        "token": args.token,
        "torrent_id": args.id,
        "file_id": args.file_id,
        "zip_link": args.zip,
        "redirect": args.redirect
    }
    if args.user_ip:
        params["user_ip"] = args.user_ip
    
    result = api_call("GET", "/v1/api/torrents/requestdl", params=params)
    print(json.dumps(result, indent=2))


def cmd_torrents_info(args):
    """Get torrent info from hash."""
    if args.hash:
        params = {"hash": args.hash, "timeout": args.timeout, 
                 "use_cache_lookup": args.use_cache}
        result = api_call("GET", "/v1/api/torrents/torrentinfo", params=params)
    else:
        print("Error: --hash is required", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))


def cmd_webdl_list(args):
    """List web downloads."""
    params = {"offset": args.offset, "limit": args.limit}
    if args.id:
        params["id"] = args.id
    
    result = api_call("GET", "/v1/api/webdl/mylist", token=args.token, params=params)
    print(json.dumps(result, indent=2))


def cmd_webdl_create(args):
    """Create a web download."""
    data = {
        "link": args.link,
        "as_queued": args.queued,
        "add_only_if_cached": args.cached_only
    }
    if args.password:
        data["password"] = args.password
    if args.name:
        data["name"] = args.name
    
    result = api_call("POST", "/v1/api/webdl/createwebdownload",
                     token=args.token, data=data, is_json=False)
    print(json.dumps(result, indent=2))


def cmd_webdl_download(args):
    """Request download link for a web download."""
    params = {
        "token": args.token,
        "web_id": args.id,
        "file_id": args.file_id,
        "zip_link": args.zip,
        "redirect": args.redirect
    }
    if args.user_ip:
        params["user_ip"] = args.user_ip
    
    result = api_call("GET", "/v1/api/webdl/requestdl", params=params)
    print(json.dumps(result, indent=2))


def cmd_usenet_list(args):
    """List usenet downloads."""
    params = {"offset": args.offset, "limit": args.limit}
    if args.id:
        params["id"] = args.id
    
    result = api_call("GET", "/v1/api/usenet/mylist", token=args.token, params=params)
    print(json.dumps(result, indent=2))


def cmd_usenet_create(args):
    """Create a usenet download."""
    data = {
        "as_queued": args.queued,
        "add_only_if_cached": args.cached_only
    }
    if args.link:
        data["link"] = args.link
    if args.name:
        data["name"] = args.name
    if args.password:
        data["password"] = args.password
    
    if args.file:
        print(f"NZB file upload not supported via CLI. Use curl:")
        print(f"curl -X POST -H 'Authorization: Bearer {args.token}' \\")
        print(f"  -F 'file=@{args.file}' \\")
        print(f"  https://api.torbox.app/v1/api/usenet/createusenetdownload")
        return
    
    result = api_call("POST", "/v1/api/usenet/createusenetdownload",
                     token=args.token, data=data, is_json=True)
    print(json.dumps(result, indent=2))


def cmd_queued_list(args):
    """List queued downloads."""
    params = {
        "offset": args.offset, 
        "limit": args.limit,
        "type": args.type
    }
    if args.id:
        params["id"] = args.id
    
    result = api_call("GET", "/v1/api/queued/getqueued", token=args.token, params=params)
    print(json.dumps(result, indent=2))


def cmd_notifications(args):
    """Get notifications."""
    result = api_call("GET", "/v1/api/notifications/mynotifications", token=args.token)
    print(json.dumps(result, indent=2))


def cmd_rss_list(args):
    """List RSS feeds."""
    result = api_call("GET", "/v1/api/rss/getfeeds", token=args.token)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Torbox API CLI")
    parser.add_argument("--token", help="API token (or set TORBOX_TOKEN env var)")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status
    subparsers.add_parser("status", help="Get API status")
    
    # Stats
    stats_parser = subparsers.add_parser("stats", help="Get Torbox stats")
    stats_parser.add_argument("--days30", action="store_true", help="Get 30-day stats")
    stats_parser.set_defaults(func=cmd_stats)
    
    # User
    user_parser = subparsers.add_parser("user", help="User operations")
    user_sub = user_parser.add_subparsers(dest="user_cmd")
    
    user_info = user_sub.add_parser("info", help="Get user info")
    user_info.add_argument("--settings", action="store_true", help="Include settings")
    user_info.set_defaults(func=cmd_user_info)
    
    # Torrents
    torrents_parser = subparsers.add_parser("torrents", help="Torrent operations")
    torrents_sub = torrents_parser.add_subparsers(dest="torrents_cmd")
    
    # torrents list
    torrents_list = torrents_sub.add_parser("list", help="List torrents")
    torrents_list.add_argument("--offset", type=int, default=0)
    torrents_list.add_argument("--limit", type=int, default=100)
    torrents_list.add_argument("--id", type=int)
    torrents_list.add_argument("--bypass-cache", action="store_true")
    torrents_list.set_defaults(func=cmd_torrents_list)
    
    # torrents create
    torrents_create = torrents_sub.add_parser("create", help="Create torrent")
    torrents_create.add_argument("--magnet", help="Magnet link")
    torrents_create.add_argument("--file", help="Torrent file path")
    torrents_create.add_argument("--name", help="Custom name")
    torrents_create.add_argument("--seed", type=int, help="Seed ratio")
    torrents_create.add_argument("--allow-zip", action="store_true", default=True)
    torrents_create.add_argument("--queued", action="store_true", help="Add to queue")
    torrents_create.add_argument("--cached-only", action="store_true", help="Only if cached")
    torrents_create.set_defaults(func=cmd_torrents_create)
    
    # torrents control
    torrents_control = torrents_sub.add_parser("control", help="Control torrent")
    torrents_control.add_argument("operation", choices=["delete", "pause", "resume"])
    torrents_control.add_argument("--id", type=int, help="Torrent ID")
    torrents_control.add_argument("--all", action="store_true", help="Apply to all")
    torrents_control.set_defaults(func=cmd_torrents_control)
    
    # torrents cache
    torrents_cache = torrents_sub.add_parser("cache", help="Check cache status")
    torrents_cache.add_argument("hashes", help="Comma-separated hashes")
    torrents_cache.add_argument("--format", default="object", choices=["object", "list"])
    torrents_cache.add_argument("--list-files", action="store_true")
    torrents_cache.set_defaults(func=cmd_torrents_cache)
    
    # torrents download
    torrents_dl = torrents_sub.add_parser("download", help="Request download link")
    torrents_dl.add_argument("--id", type=int, required=True, help="Torrent ID")
    torrents_dl.add_argument("--file-id", type=int, default=0)
    torrents_dl.add_argument("--zip", action="store_true")
    torrents_dl.add_argument("--redirect", action="store_true")
    torrents_dl.add_argument("--user-ip", help="User IP for CDN")
    torrents_dl.set_defaults(func=cmd_torrents_download)
    
    # torrents info
    torrents_info = torrents_sub.add_parser("info", help="Get torrent info")
    torrents_info.add_argument("--hash", required=True, help="Torrent hash")
    torrents_info.add_argument("--timeout", type=int, default=30)
    torrents_info.add_argument("--use-cache", action="store_true")
    torrents_info.set_defaults(func=cmd_torrents_info)
    
    # Web downloads
    webdl_parser = subparsers.add_parser("webdl", help="Web download operations")
    webdl_sub = webdl_parser.add_subparsers(dest="webdl_cmd")
    
    # webdl list
    webdl_list = webdl_sub.add_parser("list", help="List web downloads")
    webdl_list.add_argument("--offset", type=int, default=0)
    webdl_list.add_argument("--limit", type=int, default=100)
    webdl_list.add_argument("--id", type=int)
    webdl_list.set_defaults(func=cmd_webdl_list)
    
    # webdl create
    webdl_create = webdl_sub.add_parser("create", help="Create web download")
    webdl_create.add_argument("--link", required=True, help="Download URL")
    webdl_create.add_argument("--password", help="Password if required")
    webdl_create.add_argument("--name", help="Custom name")
    webdl_create.add_argument("--queued", action="store_true")
    webdl_create.add_argument("--cached-only", action="store_true")
    webdl_create.set_defaults(func=cmd_webdl_create)
    
    # webdl download
    webdl_dl = webdl_sub.add_parser("download", help="Request download link")
    webdl_dl.add_argument("--id", type=int, required=True)
    webdl_dl.add_argument("--file-id", type=int, default=0)
    webdl_dl.add_argument("--zip", action="store_true")
    webdl_dl.add_argument("--redirect", action="store_true")
    webdl_dl.add_argument("--user-ip")
    webdl_dl.set_defaults(func=cmd_webdl_download)
    
    # Usenet
    usenet_parser = subparsers.add_parser("usenet", help="Usenet operations")
    usenet_sub = usenet_parser.add_subparsers(dest="usenet_cmd")
    
    # usenet list
    usenet_list = usenet_sub.add_parser("list", help="List usenet downloads")
    usenet_list.add_argument("--offset", type=int, default=0)
    usenet_list.add_argument("--limit", type=int, default=100)
    usenet_list.add_argument("--id", type=int)
    usenet_list.set_defaults(func=cmd_usenet_list)
    
    # usenet create
    usenet_create = usenet_sub.add_parser("create", help="Create usenet download")
    usenet_create.add_argument("--link", help="NZB link")
    usenet_create.add_argument("--file", help="NZB file path")
    usenet_create.add_argument("--name", help="Custom name")
    usenet_create.add_argument("--password", help="Password")
    usenet_create.add_argument("--queued", action="store_true")
    usenet_create.add_argument("--cached-only", action="store_true")
    usenet_create.set_defaults(func=cmd_usenet_create)
    
    # Queued
    queued_parser = subparsers.add_parser("queued", help="Queued operations")
    queued_sub = queued_parser.add_subparsers(dest="queued_cmd")
    
    # queued list
    queued_list = queued_sub.add_parser("list", help="List queued downloads")
    queued_list.add_argument("--offset", type=int, default=0)
    queued_list.add_argument("--limit", type=int, default=100)
    queued_list.add_argument("--id", type=int)
    queued_list.add_argument("--type", default="torrent")
    queued_list.set_defaults(func=cmd_queued_list)
    
    # Notifications
    subparsers.add_parser("notifications", help="Get notifications")
    
    # RSS
    rss_parser = subparsers.add_parser("rss", help="RSS operations")
    rss_sub = rss_parser.add_subparsers(dest="rss_cmd")
    rss_list = rss_sub.add_parser("list", help="List RSS feeds")
    rss_list.set_defaults(func=cmd_rss_list)
    
    args = parser.parse_args()
    
    # Get token from env if not provided
    if not args.token:
        import os
        args.token = os.environ.get("TORBOX_TOKEN")
    
    if args.command in ["user", "torrents", "webdl", "usenet", "queued", "rss"]:
        if not args.token:
            print("Error: API token required. Use --token or set TORBOX_TOKEN", file=sys.stderr)
            sys.exit(1)
    
    if args.command == "status":
        cmd_status(args)
    elif args.command == "notifications":
        cmd_notifications(args)
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
