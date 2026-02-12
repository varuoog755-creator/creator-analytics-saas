"""
Analytics API Routes - Dashboard & Cross-Platform Analytics
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user)
):
    """
    Get dashboard overview with key metrics.
    
    Returns unified metrics across all connected platforms:
    - Total followers, views, engagements
    - Engagement rate trends
    - Top performing content
    - Growth trajectory
    """
    return {
        "period": f"last_{days}_days",
        "summary": {
            "total_followers": 125000,
            "total_views": 4500000,
            "total_engagements": 320000,
            "avg_engagement_rate": 7.1,
            "total_posts": 145,
            "growth_rate": 12.5
        },
        "platform_breakdown": [
            {
                "platform": "youtube",
                "followers": 45000,
                "views": 1800000,
                "engagements": 95000,
                "engagement_rate": 5.3,
                "posts": 25
            },
            {
                "platform": "tiktok",
                "followers": 52000,
                "views": 2100000,
                "engagements": 150000,
                "engagement_rate": 7.1,
                "posts": 65
            },
            {
                "platform": "instagram",
                "followers": 28000,
                "views": 600000,
                "engagements": 75000,
                "engagement_rate": 8.9,
                "posts": 55
            }
        ],
        "trends": {
            "followers": [{"date": "2024-01-01", "count": 100000}, {"date": "2024-02-01", "count": 112000}],
            "views": [{"date": "2024-01-01", "count": 3500000}, {"date": "2024-02-01", "count": 4500000}],
            "engagement": [{"date": "2024-01-01", "rate": 6.5}, {"date": "2024-02-01", "rate": 7.1}]
        },
        "top_content": [
            {
                "platform": "tiktok",
                "caption": "POV: When the beat drops 🎵",
                "views": 450000,
                "engagement_rate": 12.5,
                "type": "video"
            },
            {
                "platform": "youtube",
                "caption": "Day in my life as a creator",
                "views": 320000,
                "engagement_rate": 8.2,
                "type": "video"
            }
        ],
        "insights": [
            "Your TikTok engagement is 42% higher than average",
            "Best posting time: 7-9 PM on weekdays",
            "Video content gets 3x more engagement than images"
        ]
    }


@router.get("/audience")
async def get_audience_insights(
    platform: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Get detailed audience insights.
    
    Demographics, active hours, geography, interests.
    """
    return {
        "demographics": {
            "age_distribution": [
                {"range": "13-17", "percentage": 8},
                {"range": "18-24", "percentage": 35},
                {"range": "25-34", "percentage": 38},
                {"range": "35-44", "percentage": 12},
                {"range": "45+", "percentage": 7}
            ],
            "gender_split": {"male": 55, "female": 43, "other": 2}
        },
        "geography": {
            "top_countries": [
                {"country": "United States", "percentage": 42},
                {"country": "United Kingdom", "percentage": 12},
                {"country": "Canada", "percentage": 8},
                {"country": "Australia", "percentage": 6},
                {"country": "India", "percentage": 5}
            ],
            "cities": [
                {"city": "Los Angeles", "percentage": 8},
                {"city": "New York", "percentage": 7},
                {"city": "London", "percentage": 5}
            ]
        },
        "active_hours": {
            "weekday": [
                {"hour": 9, "activity": 65},
                {"hour": 12, "activity": 72},
                {"hour": 18, "activity": 85},
                {"hour": 21, "activity": 92}
            ],
            "weekend": [
                {"hour": 10, "activity": 60},
                {"hour": 14, "activity": 75},
                {"hour": 20, "activity": 95}
            ]
        },
        "interests": [
            {"interest": "Technology", "score": 85},
            {"interest": "Entertainment", "score": 78},
            {"interest": "Lifestyle", "score": 72},
            {"interest": "Gaming", "score": 65}
        ],
        "audience_quality": {
            "score": 82,
            "breakdown": {
                "authenticity": 88,
                "engagement_rate": 75,
                "growth_trend": 78,
                "demographic_fit": 85
            }
        }
    }


@router.get("/growth")
async def get_growth_metrics(
    period: str = Query("month", regex="^(week|month|quarter|year)$"),
    current_user = Depends(get_current_user)
):
    """
    Get growth metrics over time.
    
    Follower growth, view growth, engagement trends.
    """
    return {
        "period": period,
        "follower_growth": {
            "total": 25000,
            "percentage": 12.5,
            "daily_avg": 833,
            "trend": "up",
            "projected_monthly": 30000
        },
        "view_growth": {
            "total": 1500000,
            "percentage": 25.0,
            "daily_avg": 50000,
            "trend": "up"
        },
        "engagement_growth": {
            "total": 45000,
            "percentage": 8.0,
            "engagement_rate_change": 0.5,
            "trend": "up"
        },
        "milestones": [
            {"metric": "followers", "target": 150000, "current": 125000, "eta": "2 weeks"},
            {"metric": "views", "target": 5000000, "current": 4500000, "eta": "1 month"}
        ],
        "velocity": {
            "follower_velocity": 1.2,  # 1.2x faster than previous period
            "engagement_velocity": 0.95,
            "reach_velocity": 1.35
        }
    }


@router.get("/content-performance")
async def get_content_performance(
    platform: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user)
):
    """
    Get content performance analytics.
    
    Best/worst posts, format comparisons, hashtag performance.
    """
    return {
        "posts": [
            {
                "id": "1",
                "platform": "tiktok",
                "caption": "POV: When the beat drops 🎵",
                "type": "video",
                "published_at": "2024-01-15T18:30:00Z",
                "views": 450000,
                "likes": 52000,
                "comments": 2300,
                "shares": 4500,
                "engagement_rate": 12.5,
                "virality_score": 85
            },
            {
                "id": "2",
                "platform": "youtube",
                "caption": "Day in my life as a creator",
                "type": "video",
                "published_at": "2024-01-10T14:00:00Z",
                "views": 320000,
                "likes": 18000,
                "comments": 2100,
                "shares": 1200,
                "engagement_rate": 8.2,
                "virality_score": 72
            }
        ],
        "format_comparison": {
            "video": {"avg_engagement": 9.5, "count": 85},
            "image": {"avg_engagement": 5.2, "count": 45},
            "carousel": {"avg_engagement": 7.8, "count": 25},
            "text": {"avg_engagement": 3.1, "count": 15}
        },
        "hashtag_performance": [
            {"hashtag": "#creator", "avg_engagement": 8.5, "usage_count": 45},
            {"hashtag": "#viral", "avg_engagement": 11.2, "usage_count": 28},
            {"hashtag": "#fyp", "avg_engagement": 9.8, "usage_count": 62}
        ],
        "best_performing_day": "Tuesday",
        "best_performing_hour": "19:00"
    }


@router.get("/competitors")
async def get_competitor_analysis(
    limit: int = Query(10, ge=1, le=50),
    current_user = Depends(get_current_user)
):
    """
    Get competitor tracking and benchmarking.
    
    Compare performance with tracked competitors.
    """
    return {
        "competitors": [
            {
                "id": "1",
                "username": "competing_creator",
                "platform": "tiktok",
                "followers": 85000,
                "engagement_rate": 6.8,
                "avg_views": 120000,
                "growth_rate": 15.2,
                "compared_to_you": {
                    "followers_diff": +33000,
                    "engagement_diff": -0.3,
                    "views_diff": -50000
                }
            }
        ],
        "benchmarks": {
            "your_avg_engagement": 7.1,
            "industry_avg": 5.5,
            "percentile": 78,
            "rating": "Above Average"
        },
        "industry_trends": [
            {"trend": "Short-form video", "growth": "+25%", "recommendation": "Increase TikTok/Reels output"},
            {"trend": "Live streaming", "growth": "+18%", "recommendation": "Consider weekly live sessions"}
        ],
        "opportunities": [
            "Your YouTube Shorts engagement is 40% lower than TikTok - optimize for short-form",
            "Carousel posts on Instagram show 25% higher engagement - test more carousels"
        ]
    }


@router.get("/revenue")
async def get_revenue_analytics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Get revenue and sponsorship analytics.
    """
    return {
        "total_revenue": 15000,
        "revenue_by_platform": [
            {"platform": "youtube", "revenue": 8000, "percentage": 53},
            {"platform": "tiktok", "revenue": 3500, "percentage": 23},
            {"platform": "instagram", "revenue": 2500, "percentage": 17},
            {"platform": "sponsorships", "revenue": 1000, "percentage": 7}
        ],
        "sponsorships": [
            {
                "brand": "TechBrand",
                "campaign": "Product Review",
                "platform": "youtube",
                "revenue": 5000,
                "views": 250000,
                "engagement_rate": 8.5,
                "roi": 3.2
            }
        ],
        "cpm_trend": {"avg": 4.50, "trend": "+5%"},
        "cpe_trend": {"avg": 0.15, "trend": "+8%"},
        "projected_monthly": 18000
    }
