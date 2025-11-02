"""
SQLAlchemy ORM models for E-commerce Price Intelligence
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, DECIMAL,
    ForeignKey, JSON, UniqueConstraint, Index, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Platform(Base):
    __tablename__ = 'platforms'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    base_url = Column(String(500))
    country = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    products = relationship('Product', back_populates='platform')
    logs = relationship('ScrapingLog', back_populates='platform')


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(255), unique=True, nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    name = Column(String(500), nullable=False)
    brand = Column(String(255))
    model = Column(String(255))
    sku = Column(String(255))
    url = Column(String(1000), nullable=False)
    image_url = Column(String(1000))
    
    current_price = Column(DECIMAL(12, 2))
    currency = Column(String(10), default='KES')
    
    min_price = Column(DECIMAL(12, 2))
    max_price = Column(DECIMAL(12, 2))
    avg_price = Column(DECIMAL(12, 2))
    
    in_stock = Column(Boolean, default=True)
    stock_count = Column(Integer)
    
    seller_name = Column(String(255))
    seller_rating = Column(DECIMAL(3, 2))
    
    description = Column(Text)
    specifications = Column(JSON)
    
    rating = Column(DECIMAL(3, 2))
    review_count = Column(Integer, default=0)
    
    sentiment_score = Column(DECIMAL(3, 2))
    sentiment_label = Column(String(20))
    
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    last_price_check = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    platform = relationship('Platform', back_populates='products')
    category = relationship('Category', back_populates='products')
    price_history = relationship('PriceHistory', back_populates='product', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='product', cascade='all, delete-orphan')
    forecasts = relationship('PriceForecast', back_populates='product', cascade='all, delete-orphan')
    watchlists = relationship('UserWatchlist', back_populates='product', cascade='all, delete-orphan')
    alerts = relationship('PriceAlert', back_populates='product', cascade='all, delete-orphan')


class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    price = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(10), default='KES')
    
    was_on_sale = Column(Boolean, default=False)
    discount_percentage = Column(DECIMAL(5, 2))
    original_price = Column(DECIMAL(12, 2))
    
    in_stock = Column(Boolean, default=True)
    stock_count = Column(Integer)
    
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship('Product', back_populates='price_history')


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    title = Column(String(500))
    content = Column(Text)
    rating = Column(DECIMAL(3, 2))
    
    reviewer_name = Column(String(255))
    verified_purchase = Column(Boolean, default=False)
    
    sentiment_score = Column(DECIMAL(3, 2))
    sentiment_label = Column(String(20))
    
    helpful_count = Column(Integer, default=0)
    review_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship('Product', back_populates='reviews')


class PriceForecast(Base):
    __tablename__ = 'price_forecasts'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    forecast_date = Column(Date, nullable=False)
    predicted_price = Column(DECIMAL(12, 2), nullable=False)
    lower_bound = Column(DECIMAL(12, 2))
    upper_bound = Column(DECIMAL(12, 2))
    
    confidence = Column(DECIMAL(5, 2))
    model_used = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship('Product', back_populates='forecasts')


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20))
    telegram_id = Column(String(100))
    
    notification_preferences = Column(JSON)
    alert_threshold = Column(DECIMAL(5, 2), default=10.0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    watchlists = relationship('UserWatchlist', back_populates='user', cascade='all, delete-orphan')
    alerts = relationship('PriceAlert', back_populates='user', cascade='all, delete-orphan')


class UserWatchlist(Base):
    __tablename__ = 'user_watchlists'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    target_price = Column(DECIMAL(12, 2))
    notes = Column(Text)
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='watchlists')
    product = relationship('Product', back_populates='watchlists')
    
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='uq_user_product_watchlist'),)


class PriceAlert(Base):
    __tablename__ = 'price_alerts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    alert_type = Column(String(50))
    old_price = Column(DECIMAL(12, 2))
    new_price = Column(DECIMAL(12, 2))
    price_change_percent = Column(DECIMAL(5, 2))
    
    message = Column(Text)
    
    sent_at = Column(DateTime, default=datetime.utcnow)
    was_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    
    user = relationship('User', back_populates='alerts')
    product = relationship('Product', back_populates='alerts')


class ScrapingLog(Base):
    __tablename__ = 'scraping_logs'
    
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    category = Column(String(100))
    
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    status = Column(String(20))
    
    products_scraped = Column(Integer, default=0)
    products_new = Column(Integer, default=0)
    products_updated = Column(Integer, default=0)
    prices_recorded = Column(Integer, default=0)
    
    error_message = Column(Text)
    metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    platform = relationship('Platform', back_populates='logs')





