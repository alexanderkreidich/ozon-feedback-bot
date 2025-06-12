import requests
import time
from typing import Dict, List, Optional

class OzonClient:
    def __init__(self, client_id: str, api_key: str):
        self.client_id = client_id
        self.api_key = api_key
        self.base_url = "https://api-seller.ozon.ru"
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """Setup required headers for Ozon API"""
        self.session.headers.update({
            'Client-Id': self.client_id,
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def get_reviews_list(self, limit: int = 100, last_id: str = None, 
                        status: str = "UNPROCESSED", sort_dir: str = "DESC") -> Dict:
        """
        Get list of reviews using POST /v1/review/list
        Only works with Premium Plus subscription
        """
        url = f"{self.base_url}/v1/review/list"
        
        payload = {
            "limit": max(20, min(100, limit)),  # Enforce 20-100 range
            "sort_dir": sort_dir,
            "status": status
        }
        
        if last_id:
            payload["last_id"] = last_id
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_review_details(self, review_id: str) -> Dict:
        """Get detailed review information using POST /v1/review/info"""
        url = f"{self.base_url}/v1/review/info"
        
        payload = {"review_id": review_id}
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def post_comment_to_review(self, review_id: str, text: str, 
                              mark_as_processed: bool = True, 
                              parent_comment_id: str = None) -> Dict:
        """
        Post a comment to a review using POST /v1/review/comment/create
        """
        url = f"{self.base_url}/v1/review/comment/create"
        
        payload = {
            "review_id": review_id,
            "text": text,
            "mark_review_as_processed": mark_as_processed
        }
        
        if parent_comment_id:
            payload["parent_comment_id"] = parent_comment_id
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_all_unprocessed_reviews(self) -> List[Dict]:
        """Fetch all unprocessed reviews with pagination"""
        all_reviews = []
        last_id = None
        
        while True:
            result = self.get_reviews_list(
                limit=100, 
                last_id=last_id, 
                status="UNPROCESSED"
            )
            
            reviews = result.get('reviews', [])
            all_reviews.extend(reviews)
            
            if not result.get('has_next', False):
                break
                
            last_id = result.get('last_id')
            time.sleep(0.5)  # Rate limiting
        
        return all_reviews
    
    def get_product_info(self, product_id: Optional[int] = None, 
                        sku: Optional[int] = None, 
                        offer_id: Optional[str] = None) -> Dict:
        """Get product information using POST /v2/product/info"""
        url = f"{self.base_url}/v2/product/info"
        
        payload = {}
        if product_id:
            payload["product_id"] = product_id
        elif sku:
            payload["sku"] = sku
        elif offer_id:
            payload["offer_id"] = offer_id
        else:
            raise ValueError("At least one of product_id, sku, or offer_id must be provided")
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Simple health check to verify API connectivity"""
        try:
            # Use a simple endpoint to check connectivity
            self.get_reviews_list(limit=1)
            return True
        except Exception:
            return False