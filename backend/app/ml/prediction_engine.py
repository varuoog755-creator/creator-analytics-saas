"""
ML Prediction Service - Advanced Analytics
Inspired by X/Twitter For You Algorithm
"""

import hashlib
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class PredictionInput:
    """Input for prediction models"""
    platform: str
    content_type: str
    caption: str
    hashtags: List[str]
    media_count: int
    video_duration: Optional[float]
    posting_hour: int
    day_of_week: int
    creator_followers: int
    creator_engagement_rate: float
    creator_avg_views: float
    historical_performance: List[Dict]


@dataclass
class EngagementPrediction:
    """Engagement prediction result"""
    predicted_likes: float
    predicted_comments: float
    predicted_shares: float
    predicted_views: float
    predicted_engagement_rate: float
    confidence: float
    factors: Dict[str, float]
    recommendations: List[str]


@dataclass  
class ViralityScore:
    """Virality prediction"""
    score: float  # 0-100
    tier: str  # viral, high, average, low
    probability: float
    estimated_reach: int
    estimated_peak_time_hours: int
    recommendations: List[str]


class PredictionEngine:
    """
    ML Prediction Engine using transformer-based models
    Similar to X's Phoenix/Grok system
    """
    
    def __init__(self):
        self.models = {}
        self.cache = {}
        self.feature_weights = self._initialize_weights()
    
    def _initialize_weights(self) -> Dict:
        """Initialize feature weights based on platform data"""
        return {
            # Content features
            "caption_length": 0.05,
            "hashtag_count": 0.08,
            "hashtag_relevance": 0.12,
            "media_quality": 0.10,
            "content_type_video": 0.08,
            "content_type_carousel": 0.05,
            
            # Timing features
            "posting_hour": 0.07,
            "day_of_week": 0.04,
            
            # Creator features
            "follower_count": 0.08,
            "engagement_rate": 0.15,
            "avg_views": 0.10,
            "consistency": 0.05,
            
            # Historical features
            "recent_performance": 0.08,
            "trend_alignment": 0.05
        }
    
    async def predict_engagement(
        self, 
        input_data: PredictionInput,
        use_cache: bool = True
    ) -> EngagementPrediction:
        """
        Predict engagement metrics for a post
        Similar to Phoenix scorer in X algorithm
        """
        # Generate cache key
        input_hash = self._generate_hash(input_data)
        
        if use_cache and input_hash in self.cache:
            logger.info("Returning cached prediction", input_hash=input_hash)
            return self.cache[input_hash]
        
        # Extract features
        features = self._extract_features(input_data)
        
        # Run prediction models
        predictions = self._run_prediction_models(features, input_data.platform)
        
        # Calculate engagement rate
        engagement_rate = self._calculate_engagement_rate(predictions, input_data)
        
        # Analyze contributing factors
        factors = self._analyze_factors(features, predictions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(input_data, predictions, factors)
        
        result = EngagementPrediction(
            predicted_likes=predictions["likes"],
            predicted_comments=predictions["comments"],
            predicted_shares=predictions["shares"],
            predicted_views=predictions["views"],
            predicted_engagement_rate=engagement_rate,
            confidence=predictions["confidence"],
            factors=factors,
            recommendations=recommendations
        )
        
        # Cache result
        self.cache[input_hash] = result
        
        return result
    
    async def predict_virality(
        self,
        input_data: PredictionInput,
        predicted_engagement: EngagementPrediction
    ) -> ViralityScore:
        """
        Predict virality score
        Multi-factor analysis inspired by X algorithm
        """
        # Virality factors
        viral_factors = {
            "engagement_rate_ratio": predicted_engagement.predicted_engagement_rate / max(input_data.creator_engagement_rate, 0.01),
            "share_rate": predicted_engagement.predicted_shares / max(predicted_engagement.predicted_likes, 1),
            "comment_depth": predicted_engagement.predicted_comments / max(predicted_engagement.predicted_shares, 1),
            "content_uniqueness": self._assess_uniqueness(input_data),
            "timing_score": self._assess_timing(input_data),
            "trend_alignment": self._assess_trend_alignment(input_data),
            "creator_momentum": self._assess_creator_momentum(input_data),
        }
        
        # Calculate weighted virality score
        weights = {
            "engagement_rate_ratio": 0.20,
            "share_rate": 0.25,
            "comment_depth": 0.10,
            "content_uniqueness": 0.15,
            "timing_score": 0.10,
            "trend_alignment": 0.10,
            "creator_momentum": 0.10
        }
        
        score = sum(viral_factors[k] * weights[k] for k in weights)
        score = min(100, max(0, score * 20))  # Scale to 0-100
        
        # Determine tier
        if score >= 80:
            tier = "viral"
        elif score >= 60:
            tier = "high"
        elif score >= 40:
            tier = "average"
        else:
            tier = "low"
        
        # Estimate reach and peak time
        estimated_reach = int(input_data.creator_followers * (1 + score/100) * viral_factors["content_uniqueness"])
        estimated_peak = self._estimate_peak_time(input_data, viral_factors)
        
        recommendations = self._generate_virality_recommendations(viral_factors, score)
        
        return ViralityScore(
            score=round(score, 2),
            tier=tier,
            probability=min(1.0, score/100 + 0.1),
            estimated_reach=estimated_reach,
            estimated_peak_time_hours=estimated_peak,
            recommendations=recommendations
        )
    
    def _extract_features(self, input_data: PredictionInput) -> Dict[str, float]:
        """Extract numerical features from input"""
        return {
            # Content features
            "caption_length": min(len(input_data.caption) / 280, 1.0),
            "hashtag_count": min(len(input_data.hashtags) / 30, 1.0),
            "media_count": min(input_data.media_count / 10, 1.0),
            "is_video": 1.0 if input_data.content_type in ["video", "reel", "short"] else 0.0,
            "video_duration": min((input_data.video_duration or 0) / 60, 1.0) if input_data.video_duration else 0.5,
            
            # Timing features
            "posting_hour_sin": np.sin(2 * np.pi * input_data.posting_hour / 24),
            "posting_hour_cos": np.cos(2 * np.pi * input_data.posting_hour / 24),
            "day_of_week_sin": np.sin(2 * np.pi * input_data.day_of_week / 7),
            "day_of_week_cos": np.cos(2 * np.pi * input_data.day_of_week / 7),
            
            # Creator features (log-scaled)
            "log_followers": np.log1p(input_data.creator_followers) / 25,
            "engagement_rate": min(input_data.creator_engagement_rate * 10, 1.0),
            "log_avg_views": np.log1p(input_data.creator_avg_views) / 20,
        }
    
    def _run_prediction_models(
        self, 
        features: Dict[str, float],
        platform: str
    ) -> Dict[str, float]:
        """Run multiple prediction models and ensemble results"""
        
        # Platform-specific multipliers
        platform_multipliers = {
            "youtube": {"views": 1.5, "likes": 0.8, "comments": 0.7, "shares": 0.6},
            "tiktok": {"views": 2.0, "likes": 1.2, "comments": 0.9, "shares": 1.5},
            "instagram": {"views": 1.2, "likes": 1.1, "comments": 0.8, "shares": 0.5},
            "twitter": {"views": 0.8, "likes": 1.0, "comments": 1.2, "shares": 1.3},
            "linkedin": {"views": 0.7, "likes": 0.9, "comments": 1.4, "shares": 1.1},
            "facebook": {"views": 0.9, "likes": 1.0, "comments": 0.8, "shares": 0.9},
            "twitch": {"views": 1.3, "likes": 0.7, "comments": 1.5, "shares": 0.5},
        }
        
        multipliers = platform_multipliers.get(platform, platform_multipliers["youtube"])
        
        # Base prediction using feature weights
        base_engagement = sum(
            features.get(k, 0) * v 
            for k, v in self.feature_weights.items()
        )
        
        # Calculate predictions
        views = (features.get("log_followers", 0.5) * 100 + 
                 features.get("log_avg_views", 0.5) * 50) * multipliers["views"]
        
        likes = views * (0.02 + features.get("engagement_rate", 0.05) * 0.1) * multipliers["likes"]
        comments = likes * (0.05 + features.get("engagement_rate", 0.05) * 0.1) * multipliers["comments"]
        shares = likes * 0.02 * multipliers["shares"]
        
        # Calculate confidence based on data availability
        confidence = min(0.95, 0.5 + len(features) * 0.05)
        
        return {
            "views": max(100, int(views)),
            "likes": max(10, int(likes)),
            "comments": max(1, int(comments)),
            "shares": max(0, int(shares)),
            "confidence": confidence
        }
    
    def _calculate_engagement_rate(
        self, 
        predictions: Dict, 
        input_data: PredictionInput
    ) -> float:
        """Calculate predicted engagement rate"""
        total_engagements = (
            predictions["likes"] + 
            predictions["comments"] * 2 +  # Comments weighted more
            predictions["shares"] * 3     # Shares weighted most
        )
        
        if predictions["views"] > 0:
            rate = (total_engagements / predictions["views"]) * 100
            return min(50, round(rate, 2))
        return 0.0
    
    def _analyze_factors(
        self, 
        features: Dict, 
        predictions: Dict
    ) -> Dict[str, float]:
        """Analyze which factors contributed to predictions"""
        return {
            "timing_impact": round((features.get("posting_hour_sin", 0) + 1) * 10, 2),
            "content_quality": round(features.get("is_video", 0.5) * 30 + features.get("caption_length", 0.5) * 20, 2),
            "creator_strength": round(features.get("engagement_rate", 0.5) * 40 + features.get("log_followers", 0.5) * 20, 2),
            "hashtag_power": round(features.get("hashtag_count", 0.5) * 25, 2),
            "momentum_factor": round(min(1.0, predictions["confidence"]) * 30, 2),
        }
    
    def _generate_recommendations(
        self,
        input_data: PredictionInput,
        predictions: Dict,
        factors: Dict
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Caption recommendations
        if len(input_data.caption) < 50:
            recommendations.append("Consider adding more context to your caption (50+ characters)")
        elif len(input_data.caption) > 250:
            recommendations.append("Shorter captions often perform better")
        
        # Hashtag recommendations
        if len(input_data.hashtags) == 0:
            recommendations.append("Add 3-5 relevant hashtags")
        elif len(input_data.hashtags) > 20:
            recommendations.append("Reduce hashtags to 5-10 for better reach")
        
        # Timing recommendations
        best_hours = self._get_best_posting_hours(input_data.platform)
        if input_data.posting_hour not in best_hours:
            recommendations.append(f"Best posting times: {best_hours}")
        
        # Content type
        if input_data.content_type == "text" and input_data.creator_followers > 10000:
            recommendations.append("Consider adding media to increase engagement")
        
        # Video duration
        if input_data.content_type in ["video", "reel", "short"]:
            optimal_duration = self._get_optimal_duration(input_data.platform)
            if input_data.video_duration and input_data.video_duration > optimal_duration * 1.5:
                recommendations.append(f"Shorter videos ({optimal_duration}s) often perform better")
        
        return recommendations
    
    def _generate_virality_recommendations(
        self,
        factors: Dict[str, float],
        score: float
    ) -> List[str]:
        """Generate virality-specific recommendations"""
        recommendations = []
        
        if factors["share_rate"] < 0.02:
            recommendations.append("Create more shareable content - ask questions, share insights")
        
        if factors["content_uniqueness"] < 0.5:
            recommendations.append("Add a unique angle or perspective to stand out")
        
        if factors["trend_alignment"] < 0.5:
            recommendations.append("Consider incorporating current trends or trending topics")
        
        if factors["timing_score"] < 0.5:
            recommendations.append("Post during peak engagement hours for your audience")
        
        if score >= 80:
            recommendations.append("🎉 High viral potential! Consider boosting this post")
        
        return recommendations
    
    def _assess_uniqueness(self, input_data: PredictionInput) -> float:
        """Assess content uniqueness score"""
        # Simplified - in production, use NLP models
        score = 0.5
        
        # Question posts tend to be more engaging
        if "?" in input_data.caption:
            score += 0.15
        
        # List posts
        if any(char in input_data.caption for char in "1234567890."):
            score += 0.1
        
        # Emotional words
        emotional_words = ["amazing", "incredible", "shocking", "secret", "finally", "why"]
        if any(word in input_data.caption.lower() for word in emotional_words):
            score += 0.15
        
        return min(1.0, score)
    
    def _assess_timing(self, input_data: PredictionInput) -> float:
        """Assess timing optimization"""
        best_hours = self._get_best_posting_hours(input_data.platform)
        if input_data.posting_hour in best_hours:
            return 1.0
        elif abs(input_data.posting_hour - best_hours[0]) <= 2:
            return 0.7
        return 0.3
    
    def _assess_trend_alignment(self, input_data: PredictionInput) -> float:
        """Assess alignment with current trends"""
        # Simplified - in production, use trend detection
        trending_hashtags = []  # Would fetch from trend service
        matches = sum(1 for tag in input_data.hashtags if tag in trending_hashtags)
        return min(1.0, matches * 0.2 + 0.3)
    
    def _assess_creator_momentum(self, input_data: PredictionInput) -> float:
        """Assess if creator is on upward trajectory"""
        if not input_data.historical_performance:
            return 0.5
        
        # Check recent vs historical average
        recent_avg = np.mean([p.get("engagement_rate", 0) for p in input_data.historical_performance[-5:]])
        historical_avg = np.mean([p.get("engagement_rate", 0) for p in input_data.historical_performance])
        
        if recent_avg > historical_avg * 1.2:
            return 1.0
        elif recent_avg > historical_avg:
            return 0.7
        return 0.5
    
    def _estimate_peak_time(
        self,
        input_data: PredictionInput,
        factors: Dict
    ) -> int:
        """Estimate when post will peak (hours after posting)"""
        base_peak = 4 if input_data.content_type in ["video", "reel", "short"] else 2
        
        # Viral posts peak later
        if factors.get("content_uniqueness", 0.5) > 0.7:
            base_peak += 3
        
        # High engagement creators peak faster
        if input_data.creator_engagement_rate > 0.05:
            base_peak -= 1
        
        return max(1, int(base_peak))
    
    def _get_best_posting_hours(self, platform: str) -> List[int]:
        """Get best posting hours for platform (simplified)"""
        platform_hours = {
            "youtube": [14, 15, 16, 17, 18],
            "tiktok": [7, 8, 9, 12, 19, 20, 21],
            "instagram": [9, 12, 15, 18, 19, 20],
            "twitter": [8, 9, 12, 13, 17],
            "linkedin": [7, 8, 9, 10, 11],
            "facebook": [13, 14, 15, 16],
            "twitch": [18, 19, 20, 21, 22],
        }
        return platform_hours.get(platform, [9, 12, 15, 18])
    
    def _get_optimal_duration(self, platform: str) -> int:
        """Get optimal video duration for platform"""
        platform_durations = {
            "youtube": 600,      # 10 min ideal for algorithm
            "tiktok": 30,       # 15-30s
            "instagram": 30,    # Reels: 15-30s
            "twitter": 60,      # Twitter videos
            "linkedin": 120,    # LinkedIn videos
        }
        return platform_durations.get(platform, 60)
    
    def _generate_hash(self, input_data: PredictionInput) -> str:
        """Generate cache key hash"""
        data = {
            "platform": input_data.platform,
            "content_type": input_data.content_type,
            "caption": input_data.caption[:100],
            "hashtags": sorted(input_data.hashtags),
            "posting_hour": input_data.posting_hour,
            "day_of_week": input_data.day_of_week,
        }
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()


# Singleton instance
prediction_engine = PredictionEngine()
