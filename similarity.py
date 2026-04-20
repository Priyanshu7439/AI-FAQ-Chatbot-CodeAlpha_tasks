"""
Similarity Matching Module
Implements TF-IDF vectorization and cosine similarity for FAQ matching
"""

import math
from collections import Counter
from preprocessing import TextPreprocessor


class TFIDFVectorizer:
    """
    Simple TF-IDF vectorizer implementation
    Converts text to vectors and computes similarity
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vocabulary = set()
        self.document_vectors = []
        self.documents = []
        self.idf_scores = {}
    
    def fit(self, documents):
        """
        Fit TF-IDF vectorizer on a list of documents
        
        Args:
            documents (list): List of text documents
        """
        self.documents = documents
        
        # Build vocabulary and calculate IDF
        doc_count = len(documents)
        word_doc_freq = Counter()
        
        # Preprocess all documents and build vocabulary
        preprocessed_docs = []
        for doc in documents:
            tokens = self.preprocessor.preprocess(doc)
            preprocessed_docs.append(tokens)
            self.vocabulary.update(tokens)
            word_doc_freq.update(set(tokens))
        
        # Calculate IDF scores
        for word in self.vocabulary:
            doc_freq = word_doc_freq.get(word, 1)
            # IDF = log(total_docs / docs_containing_word)
            self.idf_scores[word] = math.log(doc_count / doc_freq)
        
        # Create TF-IDF vectors for all documents
        for tokens in preprocessed_docs:
            vector = self._create_tfidf_vector(tokens)
            self.document_vectors.append(vector)
    
    def _create_tfidf_vector(self, tokens):
        """
        Create TF-IDF vector for a list of tokens
        
        Args:
            tokens (list): Preprocessed tokens
            
        Returns:
            dict: Word -> TF-IDF score mapping
        """
        vector = {}
        word_freq = Counter(tokens)
        
        for word in self.vocabulary:
            # TF = (word_count_in_doc) / (total_words_in_doc)
            tf = word_freq.get(word, 0) / len(tokens) if tokens else 0
            # IDF score (precomputed)
            idf = self.idf_scores.get(word, 0)
            # TF-IDF = TF * IDF
            vector[word] = tf * idf
        
        return vector
    
    def transform(self, query_text):
        """
        Transform a single query to TF-IDF vector
        
        Args:
            query_text (str): Query text to transform
            
        Returns:
            dict: TF-IDF vector for the query
        """
        tokens = self.preprocessor.preprocess(query_text)
        return self._create_tfidf_vector(tokens)


class SimilarityMatcher:
    """
    Matches queries to FAQ using TF-IDF vectors and cosine similarity
    """
    
    def __init__(self):
        self.vectorizer = TFIDFVectorizer()
        self.faq_data = []
    
    def fit_faq_data(self, faq_list):
        """
        Fit the matcher with FAQ questions
        
        Args:
            faq_list (list): List of FAQ dictionaries with 'question' and 'answer'
        """
        self.faq_data = faq_list
        questions = [faq['question'] for faq in faq_list]
        self.vectorizer.fit(questions)
    
    @staticmethod
    def cosine_similarity(vector1, vector2):
        """
        Calculate cosine similarity between two TF-IDF vectors
        
        Args:
            vector1 (dict): First TF-IDF vector
            vector2 (dict): Second TF-IDF vector
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        # Get all words from both vectors
        all_words = set(vector1.keys()) | set(vector2.keys())
        
        # Calculate dot product
        dot_product = sum(
            vector1.get(word, 0) * vector2.get(word, 0)
            for word in all_words
        )
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(score ** 2 for score in vector1.values()))
        magnitude2 = math.sqrt(sum(score ** 2 for score in vector2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_best_match(self, query):
        """
        Find the best matching FAQ for a query
        
        Args:
            query (str): User query
            
        Returns:
            tuple: (best_match_index, similarity_score)
        """
        query_vector = self.vectorizer.transform(query)
        
        similarities = [
            self.cosine_similarity(query_vector, doc_vector)
            for doc_vector in self.vectorizer.document_vectors
        ]
        
        if not similarities:
            return None, 0.0
        
        best_idx = max(range(len(similarities)), key=lambda i: similarities[i])
        best_score = similarities[best_idx]
        
        return best_idx, best_score
    
    def get_answer(self, query, threshold=0.08):
        """
        Get FAQ answer for a query with similarity thresholding
        
        Args:
            query (str): User query
            threshold (float): Minimum similarity score required (0.0-1.0)
            
        Returns:
            dict: Response with answer or fallback message
        """
        best_idx, similarity_score = self.find_best_match(query)
        
        if best_idx is None:
            return {
                'success': False,
                'message': "I'm not confident about the answer. Please rephrase your question.",
                'confidence': 0.0
            }
        
        if similarity_score >= threshold:
            faq = self.faq_data[best_idx]
            return {
                'success': True,
                'question': faq['question'],
                'answer': faq['answer'],
                'confidence': round(similarity_score, 3),
                'faq_id': faq.get('id', best_idx + 1)
            }
        else:
            return {
                'success': False,
                'message': "I'm not confident about the answer. Please rephrase your question.",
                'confidence': round(similarity_score, 3)
            }
