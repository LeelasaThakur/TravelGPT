window.VoiceController = {
    isVoiceMode: false,
    recognition: null,
    synthesis: window.speechSynthesis,
    toggleBtn: document.getElementById('voiceToggle'),
    inputBtn: document.getElementById('voiceInputBtn'),

    init() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.inputBtn.classList.remove('recording');
                window.ChatController.inputEl.value = transcript;
                window.ChatController.handleSend();
            };

            this.recognition.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                this.inputBtn.classList.remove('recording');
            };

            this.recognition.onend = () => {
                this.inputBtn.classList.remove('recording');
            };
        } else {
            console.warn("Speech Recognition API not supported in this browser.");
            if (this.inputBtn) this.inputBtn.style.display = 'none';
        }

        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggleVoiceMode());
        }

        if (this.inputBtn) {
            this.inputBtn.addEventListener('click', () => this.startListening());
        }
    },

    toggleVoiceMode() {
        this.isVoiceMode = !this.isVoiceMode;
        if (this.isVoiceMode) {
            this.toggleBtn.classList.add('recording');
            this.toggleBtn.innerHTML = '<i class="fa-solid fa-microphone-slash"></i> Disable Voice';
            this.speak("Voice mode activated. How can I help you?");
        } else {
            this.toggleBtn.classList.remove('recording');
            this.toggleBtn.innerHTML = '<i class="fa-solid fa-microphone"></i> Voice Mode';
            this.synthesis.cancel(); // stop talking
        }
    },

    startListening() {
        if (!this.recognition) return;
        this.inputBtn.classList.add('recording');
        this.synthesis.cancel(); // Stop talking if we start listening
        this.recognition.start();
    },

    speak(text) {
        if (!this.synthesis || !this.isVoiceMode) return;
        
        // Strip markdown before speaking
        const cleanText = text.replace(/[*#_`~>]/g, '');
        
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'en-US';
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        
        this.synthesis.speak(utterance);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.VoiceController.init();
});
