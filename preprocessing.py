"""
Text Preprocessing Module
Handles NLP preprocessing: tokenization, lowercasing, stopword removal, lemmatization
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (runs once on first import)
# Handle gracefully if downloads fail (important for Vercel)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords', quiet=True)
    except:
        pass

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    try:
        nltk.download('wordnet', quiet=True)
    except:
        pass

try:
    nltk.data.find('corpora/wordnet_ic')
except LookupError:
    try:
        nltk.download('wordnet_ic', quiet=True)
    except:
        pass


class TextPreprocessor:
    """
    Preprocesses text using NLP techniques:
    - Lowercasing
    - Tokenization
    - Selective stopword removal (keep important words for short queries)
    - Lemmatization
    """
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
            # Remove common stop_words that are important for understanding
            self.stop_words.discard('what')
            self.stop_words.discard('is')
            self.stop_words.discard('are')
            self.stop_words.discard('can')
            self.stop_words.discard('how')
        except:
            # Fallback stopwords if NLTK data unavailable (important for Vercel)
            self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                              'of', 'with', 'by', 'from', 'be', 'been', 'being', 'have', 'has', 'had',
                              'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                              'must', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
                              'we', 'they'}
    
    def clean_text(self, text):
        """
        Clean text by removing special characters and extra whitespace
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove special characters but keep spaces and alphanumeric
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def tokenize(self, text):
        """
        Tokenize text into words
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            list: List of tokens
        """
        try:
            tokens = word_tokenize(text)
            return tokens
        except:
            # Fallback to simple split if word_tokenize fails
            return text.split()
    
    def remove_stopwords(self, tokens):
        """
        Remove stopwords from token list
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Tokens with stopwords removed
        """
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        return filtered_tokens
    
    def lemmatize(self, tokens):
        """
        Lemmatize tokens to their base form
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Lemmatized tokens
        """
        try:
            lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            return lemmatized_tokens
        except:
            # If lemmatization fails, return tokens as-is
            return tokens
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline:
        1. Clean text
        2. Tokenize
        3. Remove stopwords
        4. Lemmatize
        
        Args:
            text (str): Raw text to preprocess
            
        Returns:
            list: Preprocessed tokens
        """
        # Step 1: Clean text
        cleaned_text = self.clean_text(text)
        
        # Step 2: Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Step 3: Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Step 4: Lemmatize
        tokens = self.lemmatize(tokens)
        
        return tokens
    
    def get_preprocessed_text(self, text):
        """
        Get preprocessed text as a string (for TF-IDF or display)
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Space-separated preprocessed tokens
        """
        tokens = self.preprocess(text)
        return ' '.join(tokens)
