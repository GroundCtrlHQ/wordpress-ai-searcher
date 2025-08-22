"""
Configuration management for WordPress AI Search Terminal.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for WordPress AI Search Terminal."""
    
    def __init__(self):
        # AI Model Configuration
        self.openrouter_api_key: str = self._get_required_env("OPENROUTER_API_KEY")
        self.ai_model: str = self._get_env("AI_MODEL", "z-ai/glm-4.5-air:free")
        
        # WordPress API Configuration
        self.wordpress_api_url: str = self._get_required_env("WORDPRESS_API_URL")
        self.wordpress_username: str = self._get_required_env("WORDPRESS_USERNAME")
        self.wordpress_password: str = self._get_required_env("WORDPRESS_PASSWORD")
        
        # Application Configuration
        self.max_results: int = int(self._get_env("MAX_RESULTS", "5"))
        self.request_timeout: int = int(self._get_env("REQUEST_TIMEOUT", "30"))
        self.verbose_logging: bool = self._get_env("VERBOSE_LOGGING", "false").lower() == "true"
        
        # OpenRouter Configuration
        self.openrouter_base_url: str = "https://openrouter.ai/api/v1"
        
        # Fallback models
        self.fallback_models: list[str] = [
            "z-ai/glm-4.5-air:free",
            "qwen/qwen3-coder:free", 
            "moonshotai/kimi-k2:free"
        ]
    
    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def _get_env(self, key: str, default: str) -> str:
        """Get an environment variable with a default value."""
        return os.getenv(key, default)
    
    def get_wordpress_auth(self) -> tuple[str, str]:
        """Get WordPress authentication credentials."""
        return (self.wordpress_username, self.wordpress_password)
    
    def get_openrouter_headers(self) -> dict[str, str]:
        """Get OpenRouter API headers."""
        return {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://wordpress-ai-search-terminal",
            "X-Title": "WordPress AI Search Terminal"
        }
    
    def validate(self) -> bool:
        """Validate configuration."""
        try:
            # Check required fields
            assert self.openrouter_api_key, "OpenRouter API key is required"
            assert self.wordpress_api_url, "WordPress API URL is required"
            assert self.wordpress_username, "WordPress username is required"
            assert self.wordpress_password, "WordPress password is required"
            
            # Validate numeric fields
            assert self.max_results > 0, "Max results must be positive"
            assert self.request_timeout > 0, "Request timeout must be positive"
            
            return True
        except AssertionError as e:
            print(f"Configuration validation failed: {e}")
            return False


# Global configuration instance
config = Config()
