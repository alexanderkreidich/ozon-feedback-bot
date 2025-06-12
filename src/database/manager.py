import sqlite3
import logging
from typing import Dict, List, Optional
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path: str = "data/bot.db"):
        self.db_path = db_path
        self.ensure_directory_exists()
        self.init_database()
    
    def ensure_directory_exists(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def init_database(self):
        """Initialize database with schema"""
        with sqlite3.connect(self.db_path) as conn:
            with open('src/database/schema.sql', 'r') as f:
                conn.executescript(f.read())
    
    def is_review_processed(self, review_id: str) -> bool:
        """Check if review has already been processed"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM processed_reviews WHERE review_id = ?",
                (review_id,)
            )
            return cursor.fetchone() is not None
    
    def save_processed_review(self, review_data: Dict, response_text: str, 
                            comment_id: str = None, status: str = "posted"):
        """Save processed review to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO processed_reviews 
                (review_id, sku, review_text, review_rating, review_published_at,
                 comment_id, response_text, response_posted, status, processed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review_data['id'],
                review_data.get('sku'),
                review_data.get('text', ''),
                review_data.get('rating'),
                review_data.get('published_at'),
                comment_id,
                response_text,
                comment_id is not None,
                status,
                datetime.now()
            ))
    
    def get_monitored_products(self) -> List[Dict]:
        """Get list of products to monitor"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM monitored_products WHERE is_active = 1"
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, 
                    response_time_ms: int, error_message: str = None):
        """Log API call for monitoring"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO api_calls 
                (endpoint, method, status_code, response_time_ms, error_message, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (endpoint, method, status_code, response_time_ms, error_message, datetime.now()))