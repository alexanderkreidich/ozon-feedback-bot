import time
import logging
from datetime import datetime
from config import ConfigManager
from database.manager import DatabaseManager
from clients.ozon_client import OzonClient
from clients.deepseek_client import DeepSeekClient
from utils.logger import setup_logger

class OzonCommentBot:
    def __init__(self):
        self.config = ConfigManager()
        self.db = DatabaseManager(self.config.database_path)
        self.ozon_client = OzonClient(
            self.config.ozon_client_id, 
            self.config.ozon_api_key
        )
        self.deepseek_client = DeepSeekClient(self.config.deepseek_api_key)
        self.logger = setup_logger('ozon_bot')
        self.responses_posted_this_hour = 0
        self.last_hour_reset = datetime.now().hour
    
    def run(self):
        """Main bot execution loop"""
        self.logger.info("Ozon Comment Bot started")
        
        while True:
            try:
                self.reset_hourly_counters()
                self.process_reviews()
                
                sleep_time = self.config.bot_run_interval
                self.logger.info(f"Cycle completed. Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                self.logger.info("Bot stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Bot error: {e}", exc_info=True)
                time.sleep(60)  # Wait before retry
    
    def reset_hourly_counters(self):
        """Reset hourly rate limiting counters"""
        current_hour = datetime.now().hour
        if current_hour != self.last_hour_reset:
            self.responses_posted_this_hour = 0
            self.last_hour_reset = current_hour
    
    def process_reviews(self):
        """Process all unprocessed reviews"""
        if self.responses_posted_this_hour >= self.config.max_responses_per_hour:
            self.logger.info("Hourly response limit reached, skipping this cycle")
            return
        
        try:
            # Get all unprocessed reviews from Ozon
            reviews = self.ozon_client.get_all_unprocessed_reviews()
            self.logger.info(f"Found {len(reviews)} unprocessed reviews")
            
            for review in reviews:
                if self.responses_posted_this_hour >= self.config.max_responses_per_hour:
                    self.logger.info("Hourly limit reached during processing")
                    break
                
                self.process_single_review(review)
                time.sleep(2)  # Rate limiting between reviews
                
        except Exception as e:
            self.logger.error(f"Error processing reviews: {e}", exc_info=True)
    
    def process_single_review(self, review: dict):
        """Process a single review"""
        review_id = review['id']
        
        # Skip if already processed
        if self.db.is_review_processed(review_id):
            return
        
        try:
            # Get detailed review information
            detailed_review = self.ozon_client.get_review_details(review_id)
            
            # Generate AI response
            response_text = self.deepseek_client.generate_response(detailed_review)
            
            # Post response to Ozon
            result = self.ozon_client.post_comment_to_review(
                review_id=review_id,
                text=response_text,
                mark_as_processed=self.config.mark_as_processed
            )
            
            comment_id = result.get('comment_id')
            
            # Save to database
            self.db.save_processed_review(
                detailed_review, 
                response_text, 
                comment_id, 
                "posted"
            )
            
            self.responses_posted_this_hour += 1
            self.logger.info(f"Posted response to review {review_id}, comment_id: {comment_id}")
            
        except Exception as e:
            self.logger.error(f"Error processing review {review_id}: {e}")
            # Save failed attempt to database
            self.db.save_processed_review(review, "", None, "failed")

if __name__ == "__main__":
    bot = OzonCommentBot()
    bot.run()