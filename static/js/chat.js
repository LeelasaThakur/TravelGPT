window.ChatController = {
    inputEl: document.getElementById('chat-input'),
    sendBtn: document.getElementById('send-btn'),
    messagesContainer: document.getElementById('chat-messages'),
    
    init() {
        this.sendBtn.addEventListener('click', () => this.handleSend());
        this.inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSend();
        });
    },
    
    handleSend() {
        const text = this.inputEl.value.trim();
        if (!text || AppState.isProcessing) return;
        
        this.sendMessage(text);
        this.inputEl.value = '';
    },
    
    sendMessage(text) {
        // Remove welcome card if it exists
        const welcome = document.querySelector('.welcome-card');
        if (welcome) welcome.remove();
        
        this.appendUserMessage(text);
        this.showTypingIndicator();
        AppState.isProcessing = true;
        
        fetch('/api/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                conversation_id: AppState.conversationId
            })
        })
        .then(res => res.json())
        .then(data => {
            AppState.isProcessing = false;
            this.hideTypingIndicator();
            if (data.status === 'success') {
                AppState.conversationId = data.conversation_id;
                this.appendAssistantMessage(data.data.reply, data.data.options);
                this.updateContextPanel(data.data);
                
                // If voice mode is on, speak it
                if (window.VoiceController && window.VoiceController.isVoiceMode) {
                    window.VoiceController.speak(data.data.reply);
                }
            } else {
                this.appendAssistantMessage("I'm sorry, I encountered an error processing that request.");
            }
        })
        .catch(err => {
            console.error(err);
            AppState.isProcessing = false;
            this.hideTypingIndicator();
            this.appendAssistantMessage("Network error occurred. Please try again.");
        });
    },
    
    appendUserMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'message user-message';
        msg.textContent = text;
        this.messagesContainer.appendChild(msg);
        this.scrollToBottom();
    },
    
    appendAssistantMessage(markdownText, options = []) {
        const msg = document.createElement('div');
        msg.className = 'message assistant-message';
        
        const content = document.createElement('div');
        content.innerHTML = marked.parse(markdownText);
        msg.appendChild(content);
        
        if (options && options.length > 0) {
            const optsContainer = document.createElement('div');
            optsContainer.className = 'options-container';
            
            options.forEach((opt, idx) => {
                const card = document.createElement('div');
                card.className = 'option-card';
                card.innerHTML = `
                    <div class="option-title">${opt.airline || opt.hotel_name}</div>
                    <div class="option-detail">${opt.departure_time || opt.address}</div>
                    <div class="option-price">$${opt.price} ${opt.currency}</div>
                `;
                card.addEventListener('click', () => {
                    this.sendMessage(`I select option ${idx + 1}`);
                });
                optsContainer.appendChild(card);
            });
            msg.appendChild(optsContainer);
        }
        
        this.messagesContainer.appendChild(msg);
        this.scrollToBottom();
    },
    
    showTypingIndicator() {
        const div = document.createElement('div');
        div.className = 'typing-indicator';
        div.id = 'typing-indicator';
        div.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        this.messagesContainer.appendChild(div);
        this.scrollToBottom();
    },
    
    hideTypingIndicator() {
        const el = document.getElementById('typing-indicator');
        if (el) el.remove();
    },
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    },
    
    updateContextPanel(data) {
        const contextPanel = document.getElementById('context-content');
        if (data.details && Object.keys(data.details).length > 0) {
            let html = '<ul style="list-style:none; padding:0; display:flex; flex-direction:column; gap:12px;">';
            for (const [key, value] of Object.entries(data.details)) {
                if (value) {
                    const formattedKey = key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                    html += `<li style="font-size:13px"><strong style="color:var(--text-secondary)">${formattedKey}:</strong><br/><span style="color:var(--accent-gold)">${value}</span></li>`;
                }
            }
            html += '</ul>';
            contextPanel.innerHTML = html;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.ChatController.init();
});
