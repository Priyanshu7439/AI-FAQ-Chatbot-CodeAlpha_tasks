"""
API Client Module
Handles secure API requests using credentials from config
Integrates with Google APIs to enhance FAQ answers
"""

import requests
import json
from config import GOOGLE_API_KEY

class GoogleAPIClient:
    """
    Secure client for Google APIs
    Uses API key from environment variables (never hardcoded)
    """
    
    # Google API endpoints
    KNOWLEDGE_GRAPH_API = "https://kgsearch.googleapis.com/v1/entities:search"
    CUSTOM_SEARCH_API = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self):
        """Initialize API client with key from config"""
        self.api_key = GOOGLE_API_KEY
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not configured in .env file")
    
    def search_knowledge_graph(self, query, limit=3):
        """
        Search Google Knowledge Graph for enhanced FAQ information
        
        Args:
            query (str): Search query
            limit (int): Number of results to return
            
        Returns:
            dict: Knowledge Graph results
        """
        try:
            params = {
                'query': query,
                'key': self.api_key,
                'limit': limit
            }
            
            response = self.session.get(self.KNOWLEDGE_GRAPH_API, params=params, timeout=5)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying Knowledge Graph: {str(e)}")
            return {'element_list': []}
    
    def extract_knowledge_info(self, query):
        """
        Extract additional information from Knowledge Graph
        
        Args:
            query (str): FAQ question/topic
            
        Returns:
            str: Additional information or empty string if not found
        """
        try:
            result = self.search_knowledge_graph(query, limit=1)
            
            if result.get('element_list'):
                element = result['element_list'][0]
                description = element.get('description', '')
                
                if description:
                    return f"\n📚 **Additional Information:** {description}"
            
            return ''
        
        except Exception as e:
            print(f"Error extracting knowledge info: {str(e)}")
            return ''
    
    def validate_api_key(self):
        """
        Test if API key is valid by making a simple request
        
        Returns:
            bool: True if API key works, False otherwise
        """
        try:
            params = {
                'query': 'test',
                'key': self.api_key,
                'limit': 1
            }
            
            response = self.session.get(
                self.KNOWLEDGE_GRAPH_API,
                params=params,
                timeout=5
            )
            
            return response.status_code == 200
        
        except Exception as e:
            print(f"API key validation failed: {str(e)}")
            return False


# Initialize global API client
try:
    api_client = GoogleAPIClient()
    API_AVAILABLE = True
except ValueError as e:
    print(f"⚠️  API not configured: {str(e)}")
    print("   Chatbot will work normally without enhanced features")
    api_client = None
    API_AVAILABLE = False


def get_enhanced_answer(faq_answer, faq_question):
    """
    Enhance FAQ answer with additional information from Google APIs
    
    Args:
        faq_answer (str): Original FAQ answer
        faq_question (str): FAQ question for context
        
    Returns:
        str: Enhanced answer with additional information
    """
    if not API_AVAILABLE or not api_client:
        return faq_answer
    
    try:
        additional_info = api_client.extract_knowledge_info(faq_question)
        return faq_answer + additional_info
    
    except Exception as e:
        print(f"Error enhancing answer: {str(e)}")
        return faq_answer
