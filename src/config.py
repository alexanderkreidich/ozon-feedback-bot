import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()
        self.validate_config()
    
    @property
    def ozon_client_id(self) -> str:
        return os.getenv('OZON_CLIENT_ID')
    
    @property
    def ozon_api_key(self) -> str:
        return os.getenv('OZON_API_KEY')
    
    @property
    def deepseek_api_key(self) -> str:
        return os.getenv('DEEPSEEK_API_KEY')
    
    @property
    def database_path(self) -> str:
        return os.getenv('DATABASE_PATH', '.data/bot.db')
    
    @property
    def bot_run_interval(self) -> int:
        return int(os.getenv('BOT_RUN_INTERVAL', 3600))
    
    @property
    def max_responses_per_hour(self) -> int:
        return int(os.getenv('MAX_RESPONSES_PER_HOUR', 10))
    
    @property
    def mark_as_processed(self) -> bool:
        return os.getenv('MARK_AS_PROCESSED', 'true').lower() == 'true'
    
    def validate_config(self):
        """Validate required configuration"""
        required_vars = [
            'OZON_CLIENT_ID', 
            'OZON_API_KEY', 
            'DEEPSEEK_API_KEY'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Required environment variable {var} is missing")