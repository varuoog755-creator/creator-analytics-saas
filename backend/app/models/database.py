"""
SQLAlchemy Database Models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class PlatformEnum(enum.Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    TWITCH = "twitch"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    plan = Column(String(50), default="free")  # free, pro, agency
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    platforms = relationship("UserPlatform", back_populates="user")
    accounts = relationship("CreatorAccount", back_populates="user")
    reports = relationship("Report", back_populates="user")


class UserPlatform(Base):
    """Connected platform accounts"""
    __tablename__ = "user_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String(50), nullable=False)
    platform_user_id = Column(String(255))
    username = Column(String(255))
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    profile_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    last_synced_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="platforms")
    posts = relationship("Post", back_populates="platform_account")
    analytics = relationship("PlatformAnalytics", back_populates="platform")


class CreatorAccount(Base):
    """Creator account being tracked (can be same as connected or others)"""
    __tablename__ = "creator_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String(50), nullable=False)
    platform_user_id = Column(String(255))
    username = Column(String(255))
    display_name = Column(String(255))
    profile_image_url = Column(String(512))
    bio = Column(Text)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    score = Column(Float, default=0.0)  # Creator score (0-100)
    is_verified = Column(Boolean, default=False)
    is_competitor = Column(Boolean, default=False)
    last_analyzed_at = Column(DateTime)
    profile_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    posts = relationship("Post", back_populates="creator")
    analytics = relationship("CreatorAnalytics", back_populates="creator")


class Post(Base):
    """Post/Content model"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_accounts.id"))
    platform_account_id = Column(Integer, ForeignKey("user_platforms.id"))
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255))
    content_type = Column(String(50))  # video, image, text, carousel, reel, short
    caption = Column(Text)
    media_urls = Column(JSON)
    hashtags = Column(JSON)
    permalink = Column(String(512))
    
    # Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    
    # Predictions (ML)
    predicted_engagement = Column(Float)
    predicted_virality = Column(Float)
    virality_score = Column(Float)  # Calculated post-performance
    
    published_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    creator = relationship("CreatorAccount", back_populates="posts")
    platform_account = relationship("UserPlatform", back_populates="posts")
    analytics = relationship("PostAnalytics", back_populates="post")
    sentiments = relationship("SentimentAnalysis", back_populates="post")


class PostAnalytics(Base):
    """Time-series analytics for posts"""
    __tablename__ = "post_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    date = Column(DateTime)
    
    # Metrics snapshot
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="analytics")


class SentimentAnalysis(Base):
    """AI sentiment analysis for posts"""
    __tablename__ = "sentiment_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    sentiment = Column(String(50))  # positive, negative, neutral
    sentiment_score = Column(Float)  # -1 to 1
    emotions = Column(JSON)  # joy, sadness, anger, etc.
    topics = Column(JSON)  # detected topics
    keywords = Column(JSON)  # extracted keywords
    
    confidence = Column(Float)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="sentiments")


class PlatformAnalytics(Base):
    """Daily aggregated platform analytics"""
    __tablename__ = "platform_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(Integer, ForeignKey("user_platforms.id"))
    date = Column(DateTime)
    
    # Metrics
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_followers = Column(Integer, default=0)
    new_followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    avg_engagement_per_post = Column(Float, default=0.0)
    posts_published = Column(Integer, default=0)
    
    # Derived
    growth_rate = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    platform = relationship("UserPlatform", back_populates="analytics")


class CreatorAnalytics(Base):
    """Cross-platform creator analytics"""
    __tablename__ = "creator_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_accounts.id"))
    date = Column(DateTime)
    
    # Unified metrics
    total_followers = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_engagements = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    posts_count = Column(Integer, default=0)
    
    # Scores
    influence_score = Column(Float, default=0.0)
    growth_score = Column(Float, default=0.0)
    content_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Demographics
    audience_data = Column(JSON)  # age, gender, location
    active_hours = Column(JSON)  # best posting times
    top_countries = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    creator = relationship("CreatorAccount", back_populates="analytics")


class Report(Base):
    """Generated reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String(100))  # weekly, monthly, custom, competitor
    title = Column(String(255))
    description = Column(Text)
    parameters = Column(JSON)
    file_path = Column(String(512))
    file_url = Column(String(512))
    status = Column(String(50), default="pending")  # pending, generating, completed, failed
    generated_at = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")


class PredictionCache(Base):
    """Cached ML predictions"""
    __tablename__ = "prediction_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100))
    input_hash = Column(String(255), index=True)
    prediction = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime)
