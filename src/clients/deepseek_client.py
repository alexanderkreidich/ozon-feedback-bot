from openai import OpenAI
from typing import Dict

class DeepSeekClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
    
    def generate_response(self, review_data: Dict) -> str:
        """Generate human-like response to customer review"""
        
        # Extract review details
        rating = review_data.get('rating', 0)
        text = review_data.get('text', '')
        sku = review_data.get('sku', '')
        
        # Build context-aware prompt
        prompt = self._build_response_prompt(rating, text, sku)
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a professional customer service representative for an online marketplace seller. 
                        Generate helpful, empathetic, and human-like responses to customer reviews. 
                        Keep responses concise (50-150 words), professional, and focused on customer satisfaction."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.7,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response for API failures
            return self._get_fallback_response(rating)
    
    def _build_response_prompt(self, rating: int, text: str, sku: str) -> str:
        """Build context-aware prompt based on review details"""
        
        if rating >= 4:
            # Positive review
            return f"""
            Customer left a positive review (rating: {rating}/5):
            "{text}"
            
            Generate a grateful response that:
            - Thanks the customer for their positive feedback
            - Encourages them to shop again
            - Is warm and appreciative
            Product SKU: {sku}
            """
        elif rating >= 3:
            # Neutral review
            return f"""
            Customer left a neutral review (rating: {rating}/5):
            "{text}"
            
            Generate a helpful response that:
            - Acknowledges their feedback
            - Offers assistance if needed
            - Shows commitment to improvement
            Product SKU: {sku}
            """
        else:
            # Negative review
            return f"""
            Customer left a negative review (rating: {rating}/5):
            "{text}"
            
            Generate an empathetic response that:
            - Acknowledges their concerns
            - Apologizes for any inconvenience
            - Offers to resolve the issue
            - Provides contact information if needed
            Product SKU: {sku}
            """
    
    def _get_fallback_response(self, rating: int) -> str:
        """Provide fallback responses when AI fails"""
        if rating >= 4:
            return "Thank you for your positive review! We're delighted that you're satisfied with your purchase. We look forward to serving you again!"
        elif rating >= 3:
            return "Thank you for your feedback. We appreciate your review and are always working to improve our products and service."
        else:
            return "Thank you for your feedback. We sincerely apologize for any inconvenience. Please contact our customer service team so we can resolve this issue for you."