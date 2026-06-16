// Global State
const AppState = {
    conversationId: null,
    isProcessing: false,
    currentContext: null
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log("Horizon Travel AI Initialized");
    
    // Set up quick actions
    const quickBtns = document.querySelectorAll('.quick-action-btn');
    quickBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const intent = btn.getAttribute('data-intent');
            let msg = "";
            if (intent === "book_flight") msg = "I want to book a flight.";
            if (intent === "book_hotel") msg = "I need to find a hotel.";
            if (intent === "plan_itinerary") msg = "Can you help me plan an itinerary?";
            
            if (msg) {
                window.ChatController.sendMessage(msg);
            }
        });
    });
});
