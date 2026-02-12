"""
Prediction API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.ml.prediction_engine import PredictionEngine, PredictionInput
from app.api.deps import get_current_user

router = APIRouter()

prediction_engine = PredictionEngine()


class EngagementPredictRequest(BaseModel):
    """Request for engagement prediction"""
    platform: str = Field(..., description="Platform: youtube, tiktok, instagram, twitter, linkedin, facebook, twitch")
    content_type: str = Field(..., description="Content type: video, image, text, carousel, reel, short")
    caption: str = Field("", description="Post caption/text")
    hashtags: List[str] = Field(default_factory=list, description="Hashtags")
    media_count: int = Field(1, ge=0, le=10, description="Number of media items")
    video_duration: Optional[float] = Field(None, ge=0, description="Video duration in seconds")
    posting_hour: int = Field(12, ge=0, le=23, description="Hour of day to post (0-23)")
    day_of_week: int = Field(0, ge=0, le=6, description="Day of week (0=Monday)")
    creator_followers: int = Field(1000, ge=0, description="Number of followers")
    creator_engagement Field(0.02, ge=_rate: float =0, le=1, description="Average engagement rate")
    creator_avg_views: float = Field(1000, ge=0, description="Average views per post")
    historical_performance: Optional[List[Dict[str, Any]]] = Field(None, description="Recent posts performance")


class ViralityPredictRequest(BaseModel):
    """Request for virality prediction"""
    engagement_prediction: EngagementPredictRequest


class PredictionResponse(BaseModel):
    """Prediction response"""
    predicted_likes: float
    predicted_comments: float
    predicted_shares: float
    predicted_views: float
    predicted_engagement_rate: float
    confidence: float
    factors: Dict[str, float]
    recommendations: List[str]


class ViralityResponse(BaseModel):
    """Virality prediction response"""
    score: float
    tier: str
    probability: float
    estimated_reach: int
    estimated_peak_time_hours: int
    recommendations: List[str]


@router.post("/engagement", response_model=PredictionResponse)
async def predict_engagement(
    request: EngagementPredictRequest,
    current_user = Depends(get_current_user)
):
    """
    Predict engagement metrics for a post before publishing.
    
    Uses ML model inspired by X's For You algorithm to predict:
    - Expected likes, comments, shares, views
    - Overall engagement rate
    - Key contributing factors
    - Actionable recommendations
    """
    try:
        # Convert request to prediction input
        input_data = PredictionInput(
            platform=request.platform,
            content_type=request.content_type,
            caption=request.caption,
            hashtags=request.hashtags,
            media_count=request.media_count,
            video_duration=request.video_duration,
            posting_hour=request.posting_hour,
            day_of_week=request.day_of_week,
            creator_followers=request.creator_followers,
            creator_engagement_rate=request.creator_engagement_rate,
            creator_avg_views=request.creator_avg_views,
            historical_performance=request.historical_performance or []
        )
        
        # Get prediction
        prediction = await prediction_engine.predict_engagement(input_data)
        
        return PredictionResponse(
            predicted_likes=prediction.predicted_likes,
            predicted_comments=prediction.predicted_comments,
            predicted_shares=prediction.predicted_shares,
            predicted_views=prediction.predicted_views,
            predicted_engagement_rate=prediction.predicted_engagement_rate,
            confidence=prediction.confidence,
            factors=prediction.factors,
            recommendations=prediction.recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/virality", response_model=ViralityResponse)
async def predict_virality(
    request: ViralityPredictRequest,
    current_user = Depends(get_current_user)
):
    """
    Predict virality score for a post.
    
    Calculates:
    - Virality score (0-100)
    - Tier (viral, high, average, low)
    - Probability of going viral
    - Estimated reach
    - Recommendations for maximizing virality
    """
    try:
        # First get engagement prediction
        input_data = PredictionInput(
            platform=request.engagement_prediction.platform,
            content_type=request.engagement_prediction.content_type,
            caption=request.engagement_prediction.caption,
            hashtags=request.engagement_prediction.hashtags,
            media_count=request.engagement_prediction.media_count,
            video_duration=request.engagement_prediction.video_duration,
            posting_hour=request.engagement_prediction.posting_hour,
            day_of_week=request.engagement_prediction.day_of_week,
            creator_followers=request.engagement_prediction.creator_followers,
            creator_engagement_rate=request.engagement_prediction.creator_engagement_rate,
            creator_avg_views=request.engagement_prediction.creator_avg_views,
            historical_performance=request.engagement_prediction.historical_performance or []
        )
        
        engagement = await prediction_engine.predict_engagement(input_data)
        virality = await prediction_engine.predict_virality(input_data, engagement)
        
        return ViralityResponse(
            score=virality.score,
            tier=virality.tier,
            probability=virality.probability,
            estimated_reach=virality.estimated_reach,
            estimated_peak_time_hours=virality.estimated_peak_time_hours,
            recommendations=virality.recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Virality prediction failed: {str(e)}")


@router.get("/best-time/{platform}")
async def get_best_posting_time(
    platform: str,
    current_user = Depends(get_current_user)
):
    """
    Get optimal posting times for a platform.
    
    Returns best hours for posting based on platform-specific research.
    """
    best_hours = prediction_engine._get_best_posting_hours(platform)
    
    return {
        "platform": platform,
        "best_hours": best_hours,
        "recommendation": f"Post between {min(best_hours)}:00 and {max(best_hours)}:00 for best engagement"
    }


@router.post("/batch")
async def batch_predict(
    requests: List[EngagementPredictRequest],
    current_user = Depends(get_current_user)
):
    """
    Batch predict engagement for multiple post variations.
    
    Useful for A/B testing different captions, hashtags, or timing.
    """
    results = []
    
    for i, req in enumerate(requests):
        input_data = PredictionInput(
            platform=req.platform,
            content_type=req.content_type,
            caption=req.caption,
            hashtags=req.hashtags,
            media_count=req.media_count,
            video_duration=req.video_duration,
            posting_hour=req.posting_hour,
            day_of_week=req.day_of_week,
            creator_followers=req.creator_followers,
            creator_engagement_rate=req.creator_engagement_rate,
            creator_avg_views=req.creator_avg_views,
            historical_performance=req.historical_performance or []
        )
        
        prediction = await prediction_engine.predict_engagement(input_data)
        
        results.append({
            "variant": f"variant_{i + 1}",
            "predicted_engagement_rate": prediction.predicted_engagement_rate,
            "predicted_views": prediction.predicted_views,
            "confidence": prediction.confidence,
            "top_factor": max(prediction.factors.items(), key=lambda x: x[1])[0] if prediction.factors else None
        })
    
    # Sort by engagement rate
    results.sort(key=lambda x: x["predicted_engagement_rate"], reverse=True)
    
    return {
        "predictions": results,
        "best_variant": results[0] if results else None,
        "improvement_tip": f"Variant 1 shows {((results[0]['predicted_engagement_rate'] / results[-1]['predicted_engagement_rate']) - 1) * 100:.1f}% higher engagement than worst variant" if len(results) > 1 else None
    }
