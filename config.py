"""
Configuration Module
Loads environment variables and API keys securely from .env file
Never hardcodes secrets - all credentials come from environment
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# API Configuration
# ============================================
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# ============================================
# Application Configuration
# ============================================
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.2'))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ============================================
# Validation
# ============================================
def validate_config():
    """Validate that required configuration is set"""
    errors = []
    
    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY not set in .env file")
    
    if errors:
        print("⚠️  Configuration Warnings:")
        for error in errors:
            print(f"   - {error}")
        print("\nThe application will run incomplete without these values.")
        print("See .env.example for required variables.")
    else:
        print("✓ All configuration loaded successfully")
    
    return len(errors) == 0


if __name__ == '__main__':
    validate_config()
