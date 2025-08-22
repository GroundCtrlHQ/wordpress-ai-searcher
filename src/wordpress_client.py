"""
WordPress API client for content search and retrieval.
"""

import requests
import time
from typing import List, Dict, Any, Optional
from requests.auth import HTTPBasicAuth
from .config import config


class WordPressClient:
    """Client for interacting with WordPress REST API."""
    
    def __init__(self):
        self.base_url = config.wordpress_api_url
        self.auth = HTTPBasicAuth(*config.get_wordpress_auth())
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.timeout = config.request_timeout
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    def _rate_limit(self):
        """Implement basic rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def search_content(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search WordPress content using the provided API endpoint.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of content items with metadata
        """
        if max_results is None:
            max_results = config.max_results
            
        self._rate_limit()
        
        try:
            # Use the specific API endpoint provided
            params = {
                'content_format': 'plain',
                'per_page': min(max_results, 100)  # API limit
            }
            
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            # Parse and filter results based on query
            all_content = response.json()
            filtered_content = self._filter_content_by_query(all_content, query)
            
            return filtered_content[:max_results]
            
        except requests.exceptions.RequestException as e:
            raise WordPressAPIError(f"WordPress API request failed: {e}")
        except ValueError as e:
            raise WordPressAPIError(f"Invalid response from WordPress API: {e}")
    
    def _filter_content_by_query(self, content: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Return all content and let AI handle relevance filtering.
        
        Args:
            content: List of content items from API
            query: Search query string (not used for filtering)
            
        Returns:
            All content items for AI to analyze
        """
        # Return all content and let the AI determine relevance
        return [self._format_content_item(item) for item in content]
    
    def _format_content_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a WordPress content item for consistent output.
        
        Args:
            item: Raw content item from WordPress API
            
        Returns:
            Formatted content item
        """
        # Handle the actual API response format
        author_info = item.get('author', {})
        if isinstance(author_info, dict):
            author_name = author_info.get('name', 'Unknown')
        else:
            author_name = 'Unknown'
            
        return {
            'id': item.get('id'),
            'title': item.get('title', 'Untitled'),
            'excerpt': item.get('excerpt', ''),
            'content': item.get('content', ''),
            'url': item.get('url', ''),
            'date': item.get('date', ''),
            'author': author_name,
            'type': item.get('type', 'post'),
            'slug': item.get('slug', '')
        }
    
    def get_content_by_id(self, content_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific content by ID.
        
        Args:
            content_id: WordPress content ID
            
        Returns:
            Content item or None if not found
        """
        self._rate_limit()
        
        try:
            response = self.session.get(
                f"{self.base_url}/{content_id}",
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            return self._format_content_item(response.json())
            
        except requests.exceptions.RequestException:
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to WordPress API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._rate_limit()
            response = self.session.get(
                self.base_url,
                params={'per_page': 1},
                timeout=config.request_timeout
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False


class WordPressAPIError(Exception):
    """Exception raised for WordPress API errors."""
    pass
