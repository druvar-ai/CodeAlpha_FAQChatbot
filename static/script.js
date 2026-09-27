document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBox = document.getElementById('chat-box');
    const errorMessage = document.getElementById('error-message');

    // Utility to scroll to the bottom of the chat
    const scrollToBottom = () => {
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Add a message to the UI
    const addMessage = (text, sender = 'bot') => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    };

    // Add loading indicator
    const addLoading = () => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot', 'loading-msg');
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = `
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        
        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    };

    // Remove loading indicator
    const removeLoading = () => {
        const loadingMsg = document.querySelector('.loading-msg');
        if (loadingMsg) {
            loadingMsg.remove();
        }
    };

    const showError = (msg) => {
        errorMessage.textContent = msg;
        errorMessage.classList.remove('hidden');
    };

    const hideError = () => {
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden');
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = userInput.value.trim();
        if (!text) {
            showError('Please enter a question.');
            return;
        }

        if (text.length > 500) {
            showError('Question is too long. Please keep it under 500 characters.');
            return;
        }

        // Add user message
        addMessage(text, 'user');
        
        // Reset UI
        userInput.value = '';
        hideError();
        sendBtn.disabled = true;
        
        // Show loading
        addLoading();

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: text })
            });

            const data = await response.json();
            
            removeLoading();
            
            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred.');
            }

            // Display bot answer
            addMessage(data.answer, 'bot');
            
        } catch (error) {
            removeLoading();
            addMessage('Sorry, an error occurred while processing your request.', 'bot');
            console.error('Chat error:', error);
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    });
});
