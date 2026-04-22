# FAQ Chatbot with NLP-Based Similarity Matching

A professional FAQ chatbot application that uses Natural Language Processing (NLP) and TF-IDF-based similarity matching to provide instant answers from a predefined FAQ dataset.

## Features

✅ **NLP Text Preprocessing** - Tokenization, lowercasing, stopword removal, lemmatization  
✅ **TF-IDF Vectorization** - Converts text to numerical vectors for comparison  
✅ **Cosine Similarity Matching** - Finds the best matching FAQ question  
✅ **Confidence Scoring** - Shows how confident the system is about each answer  
✅ **Modular Architecture** - Clean separation of concerns (preprocessing, similarity, API)  
✅ **REST API** - JSON-based endpoints for query processing  
✅ **Web UI** - Modern, responsive chat interface  
✅ **25 Sample FAQs** - Covering Tech, ML, DL, Java, C, Python topics  

## Project Structure

```
AI faq ChatBot/
├── app.py                    # Flask application (main server)
├── preprocessing.py          # NLP preprocessing module
├── similarity.py             # TF-IDF and similarity matching module
├── faq_dataset.json         # FAQ database
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── static/
    ├── index.html          # Chat UI
    ├── style.css           # UI styling
    └── script.js           # Frontend logic
```

## Technology Stack

- **Backend:** Flask 3.0.0, Python 3.x
- **NLP:** NLTK 3.8.1 (Natural Language Toolkit)
- **Similarity:** TF-IDF vectorization with cosine similarity
- **API Integration:** Google APIs (Knowledge Graph, Custom Search)
- **Security:** python-dotenv for secure credential management
- **Frontend:** HTML5, CSS3, JavaScript
- **API:** REST with JSON

## 🔒 Security & API Integration

### API Key Management (No Credentials in GitHub)

This project includes **secure API integration** without exposing credentials:

✅ **Credentials Stored Locally** - API keys in `.env` file (never committed)  
✅ **Environment Variables** - All secrets loaded from environment  
✅ **Safe for GitHub** - `.env` is in `.gitignore` and never uploaded  
✅ **Easy Setup** - Copy `.env.example` and add your own key  

### Files for Security

- **`.env`** - Local credentials (NOT on GitHub)
  - Contains: `GOOGLE_API_KEY=your_key_here`
  - This file is in `.gitignore` and stays private

- **`.env.example`** - Template for GitHub
  - Shows structure: `GOOGLE_API_KEY=your_google_api_key_here`
  - Others copy this to `.env` and add their key

- **`config.py`** - Reads from environment variables
  - Never hardcodes secrets
  - Loads from `.env` file using `python-dotenv`

- **`api_client.py`** - Secure API client
  - Uses credentials from `config.py`
  - Handles API requests safely

### How to Add Your API Key

1. **Create `.env` file** in project root (copy from `.env.example`):
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

2. **Keep `.env` private** - it will NOT be committed to GitHub

3. **For collaboration:**
   - Share `.env.example` (no secrets)
   - Each developer adds their own `.env` with their API key
   - `.gitignore` prevents accidental commits

## Installation Instructions

### Prerequisites

- Python 3.7 or higher (tested with Python 3.8+)
- pip (Python package manager)

### Step 1: Create Virtual Environment (Recommended)

#### On Windows (Command Prompt or PowerShell):
```
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-Origin Resource Sharing
- NLTK 3.8.1 - Natural Language Processing

### Step 3: Verify Installation

```
python -c "import flask; import nltk; print('All dependencies installed!')"
```

## Running the Application

### Start the Server

```
python app.py
```

You should see output like:
```
FAQ Chatbot initialized with 25 FAQs
Similarity threshold: 0.2
Starting FAQ Chatbot on http://localhost:5000
Press CTRL+C to stop
```

### Access the Chatbot

Open your web browser and navigate to:
```
http://localhost:5000
```

### Stop the Server

Press `CTRL+C` in the terminal

## Usage

### Web Interface

1. Open http://localhost:5000 in your browser
2. Type a question in the input field
3. Click "Send" or press Enter
4. View the chatbot's response with confidence score

### Example Queries

- "What is deep learning?"
- "Difference between lists and tuples in Python"
- "Explain polymorphism in Java"
- "What are pointers in C?"
- "What is machine learning?"
- "How does a CNN work?"


## How It Works

### Processing Pipeline

1. **User Input** → User types a question in the chat interface
2. **Text Preprocessing** (preprocessing.py):
   - Lowercasing
   - Tokenization (word splitting)
   - Stopword removal (remove common words like "the", "is")
   - Lemmatization (convert to base form: "running" → "run")
3. **TF-IDF Vectorization** (similarity.py):
   - Term Frequency (TF) = importance of word in document
   - Inverse Document Frequency (IDF) = how rare the word is across all documents
   - TF-IDF = TF × IDF (higher score for important words)
4. **Similarity Matching** (similarity.py):
   - Calculate cosine similarity between query vector and all FAQ vectors
   - Find FAQ with highest similarity
5. **Threshold Check**:
   - If similarity ≥ 0.2 (20%) → Return FAQ answer
   - If similarity < 0.2 → Return "not confident" message
6. **Display Response** (frontend):
   - Show matched FAQ question
   - Show answer
   - Show confidence score (0.0 to 1.0)

### Example Processing

```
Input: "Can I change my password?"
↓
Preprocessed: [can, change, password]
↓
TF-IDF Vector: {can: 0.15, change: 0.25, password: 0.42, ...}
↓
Compare with FAQ: "How do I reset my account password?"
Preprocessed: [reset, account, password]
TF-IDF Vector: {reset: 0.18, account: 0.20, password: 0.42, ...}
↓
Cosine Similarity: 0.78 (78%)
↓
0.78 > 0.2 threshold ✓
↓
Return: "To reset your password, go to the login page..."
```

## Configuration

### Similarity Threshold

Edit `app.py` to adjust the confidence threshold:

```python
SIMILARITY_THRESHOLD = 0.2  # Range: 0.0 to 1.0
```

- **Lower threshold** (0.1): More responses but less accurate
- **Higher threshold** (0.5): Fewer responses but more confident
- **Default** (0.2): Balanced approach

## Code Modules

### preprocessing.py

Handles all NLP text preprocessing:

- `TextPreprocessor.clean_text()` - Remove special characters
- `TextPreprocessor.tokenize()` - Split into words
- `TextPreprocessor.remove_stopwords()` - Remove common words
- `TextPreprocessor.lemmatize()` - Convert to base forms
- `TextPreprocessor.preprocess()` - Complete pipeline

### similarity.py

Implements TF-IDF and similarity matching:

- `TFIDFVectorizer.fit()` - Learn from FAQ questions
- `TFIDFVectorizer.transform()` - Convert query to vector
- `SimilarityMatcher.find_best_match()` - Find best FAQ
- `SimilarityMatcher.get_answer()` - Return answer with confidence

### config.py (Secure Configuration)

Manages API keys and settings securely:

- Loads environment variables from `.env` file using `python-dotenv`
- Never exposes credentials in code
- `validate_config()` - Checks if all required variables are set
- Provides centralized config access for entire app

### api_client.py (Google API Integration)

Integrates with Google APIs to enhance FAQ answers:

- `GoogleAPIClient` - Secure client for Google Knowledge Graph API
- `search_knowledge_graph(query)` - Query Google Knowledge Graph
- `extract_knowledge_info(query)` - Extract additional information  
- `validate_api_key()` - Test if API key is valid
- `get_enhanced_answer(answer, question)` - Enhance FAQ with additional info

### app.py

Flask server with REST API and API integration:

- Loads configuration securely via `config.py`
- Uses `SimilarityMatcher` for core FAQ matching
- Optionally enhances answers using `api_client.py`
- `POST /api/query` - Query endpoint (with optional enhancement)
- `GET /api/faqs` - Get all FAQs
- `GET /api/health` - Health check with API status
- `GET /api/config/check` - Configuration check (debug only)
- `GET /` - Serve web UI

## Troubleshooting

### ModuleNotFoundError: No module named 'python-dotenv'

Install dependencies again:
```
pip install -r requirements.txt
```

### ModuleNotFoundError: No module named 'nltk'

Install dependencies again:
```
pip install -r requirements.txt
```

### Port 5000 Already in Use

Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### FAQ Dataset Not Found

Ensure `faq_dataset.json` is in the same directory as `app.py`

### Browser Shows "Cannot GET /"

Make sure the Flask server is running with `python app.py`

### API Key Not Working

1. Check `.env` file exists in project root
2. Verify `GOOGLE_API_KEY` is set in `.env`
3. Make sure `.env` is NOT in `.gitignore` (should be there to keep it private)
4. Restart Flask app: `python app.py`
5. Test with: `curl http://localhost:5000/api/health` (in debug mode)

### NLTK Data Download Error

The app will auto-download NLTK data on first run. If it fails:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Sample FAQ Topics

The chatbot includes 25 sample FAQs covering:

**AI/ML Topics:**
- AI vs Machine Learning
- Supervised vs Unsupervised Learning
- Overfitting in ML
- Neural Networks
- Deep Learning vs ML
- CNNs and RNNs

**Python:**
- Python basics
- Lists vs Tuples
- Lambda functions
- List comprehension
- == vs is operators

**Java:**
- Garbage Collection
- String/StringBuilder/StringBuffer
- Access Modifiers
- Polymorphism
- Exception Handling
- Abstract Classes vs Interfaces

**C:**
- Pointers
- Dynamic Memory Allocation
- Structures vs Unions
- Function Pointers
- Stack vs Heap
- Linked Lists vs Arrays
- Binary Search Trees

## Performance

- Query processing: ~100-500ms (depends on query length)
- Suitable for: up to 1000+ FAQs without significant slowdown
- Concurrent users: Limited by server resources

## Future Enhancements

- [ ] Database support (PostgreSQL/MongoDB)
- [ ] User feedback loop to improve matching
- [ ] Advanced NLP (Word2Vec, BERT embeddings)
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Authentication and rate limiting
- [ ] Admin dashboard for FAQ management
- [ ] Live chat escalation

## License and Usage

This project is provided as an educational resource for building FAQ chatbots.

## Support and Documentation

For detailed information:
- Read the inline code comments in `app.py`, `preprocessing.py`, `similarity.py`
- Check API endpoint examples in this README
- Review the FAQ dataset format in `faq_dataset.json`

---
```
Author - Priyanshu Kumar
github - @Priyanshu7439
Linkdin - https://www.linkedin.com/in/priyanshu-kumar-8a51382b4/?skipRedirect=true

**Version:** 1.0  
**Last Updated:** April 2026  
**Technology:** Flask + NLTK + TF-IDF + Cosine Similarity
