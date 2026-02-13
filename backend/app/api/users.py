"""
Users API Routes - User Management
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.api.deps import get_current_user

router = APIRouter()

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    timezone: Optional[str] = None
    notifications: Optional[dict] = None


@router.get("/profile")
async def get_user_profile(current_user = Depends(get_current_user)):
    """
    Get current user profile.
    """
    return {
        "id": 1,
        "email": "demo@example.com",
        "full_name": "Demo User",
        "avatar_url": None,
        "timezone": "UTC",
        "plan": "pro",
        "created_at": "2024-01-01T00:00:00Z",
        "settings": {
            "notifications": {
                "email": True,
                "push": True,
                "weekly_report": True,
                "milestone_alerts": True
            },
            "privacy": {
                "show_follower_count": True,
                "show_revenue": False
            }
        }
    }


@router.patch("/profile")
async def update_user_profile(
    updates: UserUpdate,
    current_user = Depends(get_current_user)
):
    """
    Update user profile.
    """
    return {
        "updated": True,
        "profile": {
            **current_user,
            **updates.dict(exclude_unset=True)
        }
    }


@router.get("/subscription")
async def get_subscription(current_user = Depends(get_current_user)):
    """
    Get current subscription details.
    """
    return {
        "plan": "pro",
        "status": "active",
        "billing_cycle": "monthly",
        "current_period_end": "2024-02-01T00:00:00Z",
        "features": {
            "platforms": 5,
            "historical_data": "1 year",
            "predictions": True,
            "competitor_tracking": True,
            "api_access": True
        },
        "limits": {
            "platforms_used": 3,
            "reports_generated": 15,
            "api_calls": 10000
        }
    }


@router.post("/subscription/upgrade")
async def upgrade_subscription(plan: str, current_user = Depends(get_current_user)):
    """
    Upgrade subscription plan.
    """
    return {
        "plan": plan,
        "status": "pending",
        "message": f"Upgraded to {plan} plan. Payment required."
    }


@router.get("/usage")
async def get_usage_stats(current_user = Depends(get_current_user)):
    """
    Get usage statistics for current billing period.
    """
    return {
        "period": {
            "start": "2024-01-01",
            "end": "2024-01-31"
        },
        "usage": {
            "platforms": {"used": 3, "limit": 5},
            "storage": {"used": "2.5GB", "limit": "10GB"},
            "api_calls": {"used": 2500, "limit": 10000},
            "reports": {"used": 15, "limit": 50}
        },
        "percentages": {
            "platforms": 60,
            "storage": 25,
            "api_calls": 25,
            "reports": 30
        }
    }
