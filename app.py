"""
FAQ Chatbot Flask Application
Backend server for FAQ chatbot with NLP-based similarity matching
Enhanced with Google API integration for additional information
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from similarity import SimilarityMatcher
from config import GOOGLE_API_KEY, SIMILARITY_THRESHOLD, DEBUG
from api_client import get_enhanced_answer, API_AVAILABLE

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Configuration
FAQ_FILE = 'faq_dataset.json'
SIMILARITY_THRESHOLD_OVERRIDE = 0.08  # Lowered for better matching

# Initialize the similarity matcher
matcher = SimilarityMatcher()


def load_faqs(filepath):
    """
    Load FAQ dataset from JSON file
    
    Args:
        filepath (str): Path to FAQ JSON file
        
    Returns:
        tuple: (list of FAQs, list of topics)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            faqs = data.get('faqs', [])
            topics = data.get('topics', [])
            return faqs, topics
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        return [], []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        return [], []


# Global variables for topics
FAQ_TOPICS = []


def initialize_app():
    """Initialize the FAQ matcher with FAQ data"""
    global FAQ_TOPICS
    
    faqs, topics = load_faqs(FAQ_FILE)
    FAQ_TOPICS = topics
    
    if faqs:
        matcher.fit_faq_data(faqs)
        print(f"FAQ Chatbot initialized with {len(faqs)} FAQs across {len(topics)} topics")
    else:
        print("Warning: No FAQs loaded!")
    
    # Check API configuration
    if API_AVAILABLE:
        print("✓ Google API is configured for enhanced answers")
    else:
        print("⚠️  Google API not configured - chatbot works without enhanced features")


# ================== API ENDPOINTS ==================

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/query', methods=['POST'])
def query_faq():
    """
    Main FAQ query endpoint with optional API enhancement
    
    Request JSON:
        {
            "query": "user question"
        }
    
    Returns:
        {
            "success": true/false,
            "question": "matched FAQ question",
            "answer": "FAQ answer (optionally enhanced with additional info)",
            "confidence": 0.856,
            "faq_id": 1,
            "enhanced": true/false
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Invalid request. Please provide a "query" field.'
            }), 400
        
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                'error': 'Query cannot be empty.'
            }), 400
        
        # Get the answer from similarity matcher (use lower threshold for better matches)
        response = matcher.get_answer(user_query, threshold=SIMILARITY_THRESHOLD_OVERRIDE)
        
        # Enhance answer with Google API if available
        if response.get('success') and API_AVAILABLE:
            try:
                enhanced_answer = get_enhanced_answer(
                    response['answer'],
                    response['question']
                )
                response['answer'] = enhanced_answer
                response['enhanced'] = True
            except Exception as e:
                print(f"Error enhancing answer: {str(e)}")
                response['enhanced'] = False
        else:
            response['enhanced'] = False
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': f'An unexpected error occurred: {str(e)}'
        }), 500


@app.route('/api/faqs', methods=['GET'])
def get_all_faqs():
    """
    Get all FAQs in the database
    
    Returns:
        {
            "total": 25,
            "faqs": [...]
        }
    """
    faqs, _ = load_faqs(FAQ_FILE)
    return jsonify({
        'total': len(faqs),
        'faqs': faqs
    }), 200


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """
    Get all available topics/categories
    
    Returns:
        {
            "total_topics": 4,
            "topics": [
                {
                    "id": "ai-ml-dl",
                    "name": "💡 AI / Machine Learning / Deep Learning",
                    "count": 7
                },
                ...
            ]
        }
    """
    return jsonify({
        'total_topics': len(FAQ_TOPICS),
        'topics': FAQ_TOPICS
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        {
            "status": "ok",
            "total_faqs": 25,
            "total_topics": 4,
            "api_available": true/false
        }
    """
    faqs, topics = load_faqs(FAQ_FILE)
    return jsonify({
        'status': 'ok',
        'total_faqs': len(faqs),
        'total_topics': len(topics),
        'api_available': API_AVAILABLE
    }), 200


@app.route('/api/config/check', methods=['GET'])
def check_config():
    """
    Check if API is properly configured (for debugging)
    Only accessible in debug mode for security
    
    Returns:
        {
            "api_configured": true/false,
            "has_api_key": true/false
        }
    """
    if not DEBUG:
        return jsonify({'error': 'Not available in production'}), 403
    
    return jsonify({
        'api_configured': API_AVAILABLE,
        'has_api_key': bool(GOOGLE_API_KEY),
        'similarity_threshold': SIMILARITY_THRESHOLD
    }), 200

@app.route('/api/debug/similarity', methods=['POST'])
def debug_similarity():
    """
    Debug endpoint to check similarity scores for a query
    Only in debug mode
    
    Request: {"query": "What is AI?"}
    Response: Shows top 5 matching FAQs with scores
    """
    if not DEBUG:
        return jsonify({'error': 'Not available in production'}), 403
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Please provide a query'}), 400
    
    user_query = data.get('query', '').strip()
    
    # Get best match
    best_idx, score = matcher.find_best_match(user_query)
    
    if best_idx is None:
        return jsonify({'error': 'No matches found'}), 400
    
    # Get FAQ
    faqs, _ = load_faqs(FAQ_FILE)
    faq = faqs[best_idx]
    
    return jsonify({
        'query': user_query,
        'best_match': {
            'faq_id': faq.get('id'),
            'question': faq.get('question'),
            'similarity_score': round(score, 4),
            'meets_threshold': score >= SIMILARITY_THRESHOLD_OVERRIDE,
            'threshold': SIMILARITY_THRESHOLD_OVERRIDE
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ================== MAIN ==================

if __name__ == '__main__':
    # Check if FAQ dataset exists
    if not os.path.exists(FAQ_FILE):
        print(f"Error: {FAQ_FILE} not found in project root!")
        print("Please ensure faq_dataset.json exists in the same directory as app.py")
    else:
        # Initialize the app
        initialize_app()
        
        # Start Flask development server
        print(f"\nStarting FAQ Chatbot on http://localhost:5000")
        print(f"Similarity threshold: {SIMILARITY_THRESHOLD}")
        print(f"Press CTRL+C to stop\n")
        
        app.run(
            debug=DEBUG,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
