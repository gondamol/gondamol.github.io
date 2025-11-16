-- E-commerce Price Intelligence Database Schema
-- PostgreSQL 14+

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist
DROP TABLE IF EXISTS price_alerts CASCADE;
DROP TABLE IF EXISTS user_watchlists CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS price_forecasts CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS platforms CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS scraping_logs CASCADE;

-- Platforms table
CREATE TABLE platforms (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    base_url VARCHAR(500),
    country VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_slug ON categories(slug);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) UNIQUE NOT NULL,
    platform_id INTEGER REFERENCES platforms(id),
    category_id INTEGER REFERENCES categories(id),
    
    -- Product Info
    name VARCHAR(500) NOT NULL,
    brand VARCHAR(255),
    model VARCHAR(255),
    sku VARCHAR(255),
    url VARCHAR(1000) NOT NULL,
    image_url VARCHAR(1000),
    
    -- Current Price
    current_price DECIMAL(12, 2),
    currency VARCHAR(10) DEFAULT 'KES',
    
    -- Price Stats
    min_price DECIMAL(12, 2),
    max_price DECIMAL(12, 2),
    avg_price DECIMAL(12, 2),
    
    -- Availability
    in_stock BOOLEAN DEFAULT TRUE,
    stock_count INTEGER,
    
    -- Seller Info
    seller_name VARCHAR(255),
    seller_rating DECIMAL(3, 2),
    
    -- Product Details
    description TEXT,
    specifications JSONB,
    
    -- Reviews
    rating DECIMAL(3, 2),
    review_count INTEGER DEFAULT 0,
    
    -- Sentiment
    sentiment_score DECIMAL(3, 2),
    sentiment_label VARCHAR(20),
    
    -- Tracking
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_price_check TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_platform ON products(platform_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_price ON products(current_price);
CREATE INDEX idx_products_active ON products(is_active);

-- Price history table
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    
    price DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'KES',
    
    -- Additional info
    was_on_sale BOOLEAN DEFAULT FALSE,
    discount_percentage DECIMAL(5, 2),
    original_price DECIMAL(12, 2),
    
    in_stock BOOLEAN DEFAULT TRUE,
    stock_count INTEGER,
    
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_price_history_product ON price_history(product_id);
CREATE INDEX idx_price_history_recorded ON price_history(recorded_at DESC);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    
    -- Review Content
    title VARCHAR(500),
    content TEXT,
    rating DECIMAL(3, 2),
    
    -- Reviewer
    reviewer_name VARCHAR(255),
    verified_purchase BOOLEAN DEFAULT FALSE,
    
    -- Sentiment
    sentiment_score DECIMAL(3, 2),
    sentiment_label VARCHAR(20),
    
    -- Metadata
    helpful_count INTEGER DEFAULT 0,
    review_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_rating ON reviews(rating DESC);

-- Price forecasts table
CREATE TABLE price_forecasts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    
    forecast_date DATE NOT NULL,
    predicted_price DECIMAL(12, 2) NOT NULL,
    lower_bound DECIMAL(12, 2),
    upper_bound DECIMAL(12, 2),
    
    confidence DECIMAL(5, 2),
    model_used VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecasts_product ON price_forecasts(product_id);
CREATE INDEX idx_forecasts_date ON price_forecasts(forecast_date);

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id UUID DEFAULT uuid_generate_v4() UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    telegram_id VARCHAR(100),
    
    -- Preferences
    notification_preferences JSONB,
    alert_threshold DECIMAL(5, 2) DEFAULT 10.0,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- User watchlists table
CREATE TABLE user_watchlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    
    target_price DECIMAL(12, 2),
    notes TEXT,
    
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, product_id)
);

CREATE INDEX idx_watchlist_user ON user_watchlists(user_id);
CREATE INDEX idx_watchlist_product ON user_watchlists(product_id);

-- Price alerts table
CREATE TABLE price_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    
    alert_type VARCHAR(50),  -- price_drop, target_price, back_in_stock
    old_price DECIMAL(12, 2),
    new_price DECIMAL(12, 2),
    price_change_percent DECIMAL(5, 2),
    
    message TEXT,
    
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    was_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP
);

CREATE INDEX idx_alerts_user ON price_alerts(user_id);
CREATE INDEX idx_alerts_sent ON price_alerts(sent_at DESC);

-- Scraping logs table
CREATE TABLE scraping_logs (
    id SERIAL PRIMARY KEY,
    platform_id INTEGER REFERENCES platforms(id),
    category VARCHAR(100),
    
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status VARCHAR(20),
    
    products_scraped INTEGER DEFAULT 0,
    products_new INTEGER DEFAULT 0,
    products_updated INTEGER DEFAULT 0,
    prices_recorded INTEGER DEFAULT 0,
    
    error_message TEXT,
    metadata JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_platform ON scraping_logs(platform_id);
CREATE INDEX idx_logs_started ON scraping_logs(started_at DESC);

-- Insert platforms
INSERT INTO platforms (code, name, base_url, country) VALUES
    ('jumia', 'Jumia Kenya', 'https://www.jumia.co.ke', 'Kenya'),
    ('kilimall', 'Kilimall Kenya', 'https://www.kilimall.co.ke', 'Kenya'),
    ('amazon', 'Amazon', 'https://www.amazon.com', 'USA')
ON CONFLICT (code) DO NOTHING;

-- Insert categories
INSERT INTO categories (name, slug) VALUES
    ('Electronics', 'electronics'),
    ('Mobile Phones', 'mobile-phones'),
    ('Laptops', 'laptops'),
    ('TVs & Audio', 'tvs-audio'),
    ('Home Appliances', 'home-appliances'),
    ('Fashion', 'fashion'),
    ('Books', 'books')
ON CONFLICT (name) DO NOTHING;

-- Create views

CREATE OR REPLACE VIEW product_price_trends AS
SELECT 
    p.id as product_id,
    p.name,
    p.current_price,
    COUNT(ph.id) as price_points,
    MIN(ph.price) as historical_min,
    MAX(ph.price) as historical_max,
    AVG(ph.price) as historical_avg,
    STDDEV(ph.price) as price_volatility,
    (p.current_price - AVG(ph.price)) / AVG(ph.price) * 100 as price_vs_avg_percent
FROM products p
LEFT JOIN price_history ph ON p.id = ph.product_id
WHERE p.is_active = TRUE
GROUP BY p.id, p.name, p.current_price;

CREATE OR REPLACE VIEW best_deals AS
SELECT 
    p.id,
    p.name,
    p.brand,
    p.current_price,
    p.rating,
    p.review_count,
    pl.name as platform,
    c.name as category,
    ROUND(((p.avg_price - p.current_price) / p.avg_price * 100), 2) as discount_from_avg
FROM products p
JOIN platforms pl ON p.platform_id = pl.id
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = TRUE 
  AND p.in_stock = TRUE
  AND p.avg_price > p.current_price
ORDER BY discount_from_avg DESC;

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_platforms_updated_at BEFORE UPDATE ON platforms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();






