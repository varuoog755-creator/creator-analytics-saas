"""
Platform API Routes - Manage Platform Connections
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.api.deps import get_current_user

router = APIRouter()


@router.get("")
async def get_connected_platforms(current_user = Depends(get_current_user)):
    """
    Get all connected platform accounts.
    """
    return {
        "platforms": [
            {
                "id": "1",
                "platform": "youtube",
                "username": "@mychannel",
                "connected": True,
                "last_synced": "2024-01-20T10:30:00Z",
                "followers": 45000,
                "posts": 125
            },
            {
                "id": "2",
                "platform": "tiktok",
                "username": "@mytiktok",
                "connected": True,
                "last_synced": "2024-01-20T10:30:00Z",
                "followers": 52000,
                "posts": 250
            },
            {
                "id": "3",
                "platform": "instagram",
                "username": "@myinsta",
                "connected": True,
                "last_synced": "2024-01-20T10:30:00Z",
                "followers": 28000,
                "posts": 180
            },
            {
                "id": "4",
                "platform": "twitter",
                "username": "@mytwitter",
                "connected": False,
                "last_synced": "2024-01-15T10:30:00Z",
                "followers": 15000,
                "posts": 890
            }
        ],
        "available_platforms": [
            {"id": "youtube", "name": "YouTube", "connected": True},
            {"id": "tiktok", "name": "TikTok", "connected": True},
            {"id": "instagram", "name": "Instagram", "connected": True},
            {"id": "twitter", "name": "Twitter/X", "connected": False},
            {"id": "linkedin", "name": "LinkedIn", "connected": False},
            {"id": "facebook", "name": "Facebook", "connected": False},
            {"id": "twitch", "name": "Twitch", "connected": False}
        ]
    }


@router.post("/connect/{platform}")
async def connect_platform(
    platform: str,
    current_user = Depends(get_current_user)
):
    """
    Initiate platform connection flow.
    
    Returns OAuth URL for platform authorization.
    """
    platform_configs = {
        "youtube": {
            "auth_url": "https://accounts.google.com/o/oauth2/auth",
            "scope": "https://www.googleapis.com/auth/youtube.readonly"
        },
        "tiktok": {
            "auth_url": "https://www.tiktok.com/auth/authorize/",
            "scope": "user.info.basic,video.list"
        },
        "instagram": {
            "auth_url": "https://api.instagram.com/oauth/authorize",
            "scope": "user_profile,user_media"
        },
        "twitter": {
            "auth_url": "https://twitter.com/i/oauth2/authorize",
            "scope": "tweet.read users.read"
        }
    }
    
    if platform not in platform_configs:
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
    
    return {
        "platform": platform,
        "auth_url": platform_configs[platform]["auth_url"],
        "state": "random_state_token",
        "message": f"Visit the auth URL to connect your {platform} account"
    }


@router.post("/connect/{platform}/callback")
async def handle_oauth_callback(
    platform: str,
    code: str,
    state: str,
    current_user = Depends(get_current_user)
):
    """
    Handle OAuth callback from platform.
    """
    # In production, exchange code for access token
    return {
        "platform": platform,
        "connected": True,
        "username": f"@{platform}_user"
    }


@router.delete("/{platform_id}")
async def disconnect_platform(
    platform_id: str,
    current_user = Depends(get_current_user)
):
    """
    Disconnect a platform account.
    """
    return {
        "platform_id": platform_id,
        "disconnected": True,
        "message": "Platform disconnected successfully"
    }


@router.post("/{platform_id}/sync")
async def sync_platform_data(
    platform_id: str,
    current_user = Depends(get_current_user)
):
    """
    Trigger manual data sync for a platform.
    """
    return {
        "platform_id": platform_id,
        "status": "syncing",
        "started_at": "2024-01-20T10:30:00Z",
        "estimated_completion": "2 minutes"
    }
