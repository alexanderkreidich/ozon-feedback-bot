-- Table: processed_reviews (prevent duplicate responses)
CREATE TABLE IF NOT EXISTS processed_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id TEXT UNIQUE NOT NULL,
    sku INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    review_rating INTEGER,
    review_published_at DATETIME,
    comment_id TEXT,
    response_text TEXT,
    response_posted BOOLEAN DEFAULT FALSE,
    processed_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending', -- pending, posted, failed, skipped
    retry_count INTEGER DEFAULT 0,
    UNIQUE(review_id)
);

-- Table: products (track monitored SKUs)
CREATE TABLE IF NOT EXISTS monitored_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku INTEGER UNIQUE NOT NULL,
    product_name TEXT,
    last_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    total_reviews INTEGER DEFAULT 0,
    unprocessed_reviews INTEGER DEFAULT 0
);

-- Table: api_calls (monitor API usage)
CREATE TABLE IF NOT EXISTS api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reviews_sku ON processed_reviews(sku);
CREATE INDEX IF NOT EXISTS idx_reviews_status ON processed_reviews(status);
CREATE INDEX IF NOT EXISTS idx_products_active ON monitored_products(is_active, last_checked);