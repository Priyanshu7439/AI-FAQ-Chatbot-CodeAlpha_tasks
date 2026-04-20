/**
 * FAQ ChatBot Frontend
 * Handles user interactions, API calls, and message display
 */

const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const topicsContainer = document.getElementById('topicsContainer');
const navbarTopics = document.getElementById('navbarTopics');

// API endpoint
const API_ENDPOINT = '/api/query';
const TOPICS_ENDPOINT = '/api/topics';

// Current selected topic filter
let selectedTopic = null;

/**
 * Load and display available topics
 */
async function loadTopics() {
    try {
        const response = await fetch(TOPICS_ENDPOINT);
        if (response.ok) {
            const data = await response.json();
            displayTopics(data.topics);
            displayNavbarTopics(data.topics);
        }
    } catch (error) {
        console.error('Error loading topics:', error);
        topicsContainer.innerHTML = '<p class="error">Failed to load topics</p>';
        navbarTopics.innerHTML = '<p class="error">Failed to load topics</p>';
    }
}

/**
 * Display topics as badges in the navbar
 */
function displayNavbarTopics(topics) {
    navbarTopics.innerHTML = '';
    
    topics.forEach(topic => {
        const btn = document.createElement('button');
        btn.className = 'navbar-topic-btn';
        btn.textContent = topic.name;
        btn.title = `${topic.count} questions`;
        btn.addEventListener('click', () => selectTopicFromNavbar(topic.id, btn));
        navbarTopics.appendChild(btn);
    });
}

/**
 * Handle topic selection from navbar
 */
function selectTopicFromNavbar(topicId, btnElement) {
    // Update navbar button states
    document.querySelectorAll('.navbar-topic-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Toggle selected topic
    if (selectedTopic === topicId) {
        selectedTopic = null;
    } else {
        selectedTopic = topicId;
        btnElement.classList.add('active');
    }
    
    // Update regular topics section
    document.querySelectorAll('.topic-badge').forEach(badge => {
        if (selectedTopic && badge.dataset.topicId === topicId) {
            badge.classList.add('active');
        } else {
            badge.classList.remove('active');
        }
    });
    
    // Add filter hint to chat
    if (selectedTopic) {
        addMessage(`📌 Filtered by topic: ${topicId}`, 'bot');
    }
}

/**
 * Display topics as badges in the main section
 */
function displayTopics(topics) {
    topicsContainer.innerHTML = '';
    
    topics.forEach(topic => {
        const badge = document.createElement('div');
        badge.className = 'topic-badge';
        badge.dataset.topicId = topic.id;
        badge.innerHTML = `${topic.name} <span class="count">(${topic.count})</span>`;
        badge.addEventListener('click', () => selectTopic(topic.id, badge));
        topicsContainer.appendChild(badge);
    });
}

/**
 * Handle topic selection from regular badges
 */
function selectTopic(topicId, badgeElement) {
    // Remove active class from all badges
    document.querySelectorAll('.topic-badge').forEach(badge => {
        badge.classList.remove('active');
    });
    
    // Remove active from navbar buttons
    document.querySelectorAll('.navbar-topic-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Toggle selected topic
    if (selectedTopic === topicId) {
        selectedTopic = null;
    } else {
        selectedTopic = topicId;
        badgeElement.classList.add('active');
        
        // Activate corresponding navbar button
        document.querySelectorAll('.navbar-topic-btn').forEach(btn => {
            if (btn.textContent.includes(topicId)) {
                btn.classList.add('active');
            }
        });
    }
    
    // Add filter hint to UI
    if (selectedTopic) {
        addMessage(`📌 Filters active: Showing ${selectedTopic} questions`, 'bot');
    }
}

/**
 * Add a message to the chat display
 */
function addMessage(text, sender = 'user', metadata = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    let content = `<div class="message-content"><p>${escapeHtml(text)}</p>`;

    if (metadata) {
        if (metadata.confidence !== undefined) {
            const confidenceClass = metadata.confidence < 0.5 ? 'confidence low-confidence' : 'confidence';
            content += `<div class="${confidenceClass}">Confidence: ${(metadata.confidence * 100).toFixed(1)}%</div>`;
        }
        if (metadata.faq_id !== undefined) {
            content += `<div class="faq-label">FAQ #${metadata.faq_id}</div>`;
        }
    }

    content += '</div>';

    if (metadata && metadata.original_question) {
        content += `<div class="message-meta">Matched with: "${escapeHtml(metadata.original_question)}"</div>`;
    }

    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Add a loading indicator
 */
function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'typingIndicator';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Remove the typing indicator
 */
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 0);
}

/**
 * Escape HTML special characters to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Send query to the API
 */
async function sendQuery() {
    const query = userInput.value.trim();

    if (!query) {
        alert('Please enter a question');
        return;
    }

    // Disable input and button
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message to chat
    addMessage(query, 'user');
    userInput.value = '';

    // Show typing indicator
    addTypingIndicator();

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        removeTypingIndicator();

        if (response.ok) {
            const data = await response.json();

            if (data.success) {
                // Display the FAQ answer
                addMessage(data.answer, 'bot', {
                    confidence: data.confidence,
                    faq_id: data.faq_id,
                    original_question: data.question
                });
            } else {
                // Display the confidence message (not confident)
                addMessage(data.message, 'bot', {
                    confidence: data.confidence
                });
            }
        } else {
            const error = await response.json();
            addMessage('Sorry, an error occurred: ' + (error.error || 'Unknown error'), 'bot');
        }
    } catch (error) {
        removeTypingIndicator();
        console.error('Error:', error);
        addMessage('Sorry, I cannot reach the server. Please try again later.', 'bot');
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

/**
 * Event listeners
 */
sendBtn.addEventListener('click', sendQuery);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
    }
});

// Focus input on load
window.addEventListener('load', () => {
    loadTopics();  // Load topics on page load
    userInput.focus();
});
