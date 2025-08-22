"""
AI-powered search engine using OpenRouter and tool calling.
"""

import json
import requests
from typing import List, Dict, Any, Optional, Callable
from .config import config
from .wordpress_client import WordPressClient, WordPressAPIError


class AISearchEngine:
    """AI-powered search engine using OpenRouter with tool calling."""
    
    def __init__(self):
        self.wordpress_client = WordPressClient()
        self.base_url = config.openrouter_base_url
        self.headers = config.get_openrouter_headers()
        self.current_model = config.ai_model
        self.fallback_models = config.fallback_models
        
        # Tool definition for WordPress search
        self.search_tool = {
            "type": "function",
            "function": {
                "name": "search_wordpress",
                "description": "Search WordPress content intelligently. Returns all available content for AI analysis - the AI will determine relevance based on semantic understanding, not just keyword matching.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query. Note: This tool returns all content - the AI analyzes relevance, not the tool."
                        },
                        "maxResults": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    
    def search(self, user_query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """
        Perform AI-powered search using natural language query.
        
        Args:
            user_query: Natural language search query
            max_results: Maximum number of results to return
            
        Returns:
            Search results with AI analysis
        """
        if max_results is None:
            max_results = config.max_results
        
        # Try primary model first, then fallbacks
        for model in [self.current_model] + self.fallback_models:
            try:
                return self._search_with_model(user_query, max_results, model)
            except Exception as e:
                if config.verbose_logging:
                    print(f"Model {model} failed: {e}")
                continue
        
        # If all models fail, fall back to direct WordPress search
        return self._fallback_search(user_query, max_results)
    
    def _search_with_model(self, user_query: str, max_results: int, model: str) -> Dict[str, Any]:
        """
        Search using a specific AI model.
        
        Args:
            user_query: Natural language search query
            max_results: Maximum number of results
            model: AI model to use
            
        Returns:
            Search results with AI analysis
        """
        # Prepare the chat completion request
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant that searches WordPress content intelligently. 
                    
                    When a user asks a question:
                    1. Use the search_wordpress tool to retrieve content
                    2. Analyze ALL returned content for relevance, even if it doesn't contain exact keywords
                    3. Look for semantic relationships, related concepts, and contextual relevance
                    4. Consider synonyms, related terms, and broader topics
                    5. If content is tangentially related or could be helpful, include it
                    6. Always provide accurate citations and source links
                    
                    Be flexible in your search - don't require exact keyword matches. Think about what the user is really looking for."""
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            "tools": [self.search_tool],
            "tool_choice": "auto",
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return self._process_ai_response(result, user_query, max_results)
            
        except requests.exceptions.RequestException as e:
            raise AIError(f"OpenRouter API request failed: {e}")
    
    def _process_ai_response(self, ai_response: Dict[str, Any], user_query: str, max_results: int) -> Dict[str, Any]:
        """
        Process AI response and execute tool calls if needed.
        
        Args:
            ai_response: Response from OpenRouter API
            user_query: Original user query
            max_results: Maximum number of results
            
        Returns:
            Processed search results
        """
        try:
            message = ai_response['choices'][0]['message']
            
            # Check if AI wants to use the search tool
            if 'tool_calls' in message:
                tool_calls = message['tool_calls']
                
                for tool_call in tool_calls:
                    if tool_call['function']['name'] == 'search_wordpress':
                        # Execute WordPress search
                        args = json.loads(tool_call['function']['arguments'])
                        search_query = args.get('query', user_query)
                        search_max_results = args.get('maxResults', max_results)
                        
                        wordpress_results = self.wordpress_client.search_content(
                            search_query, 
                            search_max_results
                        )
                        
                        # Format results for AI
                        formatted_results = self._format_results_for_ai(wordpress_results)
                        
                        # Get AI analysis of results
                        analysis = self._get_ai_analysis(user_query, formatted_results)
                        
                        return {
                            'query': user_query,
                            'results': wordpress_results,
                            'analysis': analysis,
                            'model_used': ai_response['model'],
                            'total_results': len(wordpress_results)
                        }
            
            # If no tool calls, return AI's direct response
            return {
                'query': user_query,
                'results': [],
                'analysis': message.get('content', 'No relevant content found.'),
                'model_used': ai_response['model'],
                'total_results': 0
            }
            
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise AIError(f"Failed to process AI response: {e}")
    
    def _format_results_for_ai(self, results: List[Dict[str, Any]]) -> str:
        """
        Format WordPress results for AI analysis.
        
        Args:
            results: List of WordPress content items
            
        Returns:
            Formatted string for AI
        """
        if not results:
            return "No content found."
        
        formatted = []
        for i, item in enumerate(results, 1):
            formatted.append(f"""
Result {i}:
Title: {item['title']}
Excerpt: {item['excerpt'][:200]}...
URL: {item['url']}
Author: {item['author']}
Date: {item['date']}
""")
        
        return "\n".join(formatted)
    
    def _get_ai_analysis(self, user_query: str, formatted_results: str) -> str:
        """
        Get AI analysis of search results.
        
        Args:
            user_query: Original user query
            formatted_results: Formatted search results
            
        Returns:
            AI analysis of the results
        """
        payload = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are a helpful assistant that analyzes search results intelligently.
                    
                    When analyzing results:
                    1. Consider ALL content for relevance, not just exact keyword matches
                    2. Look for semantic relationships and contextual relevance
                    3. Include content that might be tangentially related or helpful
                    4. Consider synonyms, related concepts, and broader topics
                    5. If content could be useful to the user, mention it
                    6. Provide clear, concise answers with proper citations
                    
                    Be flexible and helpful - think about what would actually be useful to the user."""
                },
                {
                    "role": "user",
                    "content": f"""User Query: {user_query}

Search Results:
{formatted_results}

Please provide a helpful answer based on these search results. Include relevant citations and source links."""
                }
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException:
            return "Unable to analyze results at this time."
    
    def _fallback_search(self, user_query: str, max_results: int) -> Dict[str, Any]:
        """
        Fallback search when AI models are unavailable.
        
        Args:
            user_query: Search query
            max_results: Maximum number of results
            
        Returns:
            Basic search results
        """
        try:
            results = self.wordpress_client.search_content(user_query, max_results)
            return {
                'query': user_query,
                'results': results,
                'analysis': f"Found {len(results)} results for your query. (Fallback search - AI analysis unavailable)",
                'model_used': 'fallback',
                'total_results': len(results)
            }
        except WordPressAPIError as e:
            return {
                'query': user_query,
                'results': [],
                'analysis': f"Search failed: {e}",
                'model_used': 'error',
                'total_results': 0
            }
    
    def test_ai_connection(self) -> bool:
        """
        Test connection to OpenRouter API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            payload = {
                "model": self.current_model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False


class AIError(Exception):
    """Exception raised for AI-related errors."""
    pass
