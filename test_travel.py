# Import necessary libraries for the Flask application and other functionalities
from flask import Flask, request, jsonify,session, render_template  # Flask for web framework
from amadeus_api import AmadeusAPI  # Amadeus API for flight data
import requests  # For making HTTP requests
import random  # For generating random flight IDs
import json  # For handling JSON data
import os  # For file operations
import re  # For regular expressions
from datetime import datetime  # For date handling
import traceback  # For detailed error logging
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import phonenumbers



# Initialize the Flask application
app = Flask(__name__)  # Create an instance of the Flask class
app.secret_key = "your_secret_key"  # Required for session handling

#app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # For Gmail
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'niharikatiwari6307@gmail.com'
# app.config['MAIL_PASSWORD'] = 'iurr zfxb txjx hjrh'
# app.config['MAIL_DEFAULT_SENDER'] = 'niharikatiwari6307@gmail.com'

# mail = Mail(app)

# def send_email(to_email, subject, body):
#     """
#     Sends an email to the specified address with the given subject and body.
#     """
#     try:
#         msg = Message(subject, recipients=[to_email])
#         msg.body = body
#         mail.send(msg)
#         print(f"Email sent successfully to {to_email}")
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {str(e)}")
#         return False

CITY_IMAGES = {
    "paris": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=2560",  # Eiffel Tower
    "london": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=2560",  # Big Ben
    "new york": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=2560",  # Times Square
    "tokyo": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?auto=format&fit=crop&w=2560",  # Tokyo Tower
    "rome": "https://images.unsplash.com/photo-1525874684015-58379d421a52?auto=format&fit=crop&w=2560",  # Colosseum
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=2560",  # Burj Khalifa
    "singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=2560",  # Marina Bay Sands
    "sydney": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=2560",  # Opera House
    "mumbai": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?auto=format&fit=crop&w=2560",  # Gateway of India
    "delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=2560",  # India Gate
    "barcelona": "https://images.unsplash.com/photo-1543349689-9dd27f3d5420?auto=format&fit=crop&w=2560",  # Sagrada Familia
    "amsterdam": "https://images.unsplash.com/photo-1512608851468-95f527ab3a2e?auto=format&fit=crop&w=2560",  # Canals of Amsterdam
    "venice": "https://images.unsplash.com/photo-1512314889357-e157c22f938d?auto=format&fit=crop&w=2560",  # Grand Canal
    "hong kong": "https://images.unsplash.com/photo-1569949386996-7b11fbb1b2e0?auto=format&fit=crop&w=2560",  # Hong Kong Skyline
    "los angeles": "https://images.unsplash.com/photo-1536532184021-da5392f30967?auto=format&fit=crop&w=2560",  # Hollywood
    "istanbul": "https://images.unsplash.com/photo-1546412414-e19569947c87?auto=format&fit=crop&w=2560",  # Hagia Sophia
    "bali": "https://images.unsplash.com/photo-1520642417671-ae7c03741aa2?auto=format&fit=crop&w=2560",  # Bali Rice Terraces
    "cairo": "https://images.unsplash.com/photo-1551269901-5c5a38d2a2d1?auto=format&fit=crop&w=2560",  # Pyramids of Giza
    "athens": "https://images.unsplash.com/photo-1555157939-0209d260aed2?auto=format&fit=crop&w=2560",  # Parthenon
    "rio de janeiro": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=2560",  # Christ the Redeemer
    "moscow": "https://images.unsplash.com/photo-1510070112810-d4e9a46d9e91?auto=format&fit=crop&w=2560",  # Red Square
    "seoul": "https://images.unsplash.com/photo-1609871962568-bd27f93e24d1?auto=format&fit=crop&w=2560",  # Seoul Tower
    "bangalore": "https://images.unsplash.com/photo-1578732429472-1cb1ef0ff2a8?auto=format&fit=crop&w=2560",  # Bangalore Skyline
    "chennai": "https://images.unsplash.com/photo-1611465575803-d091e98a37f8?auto=format&fit=crop&w=2560",  # Marina Beach
    "kolkata": "https://images.unsplash.com/photo-1579171804200-1e00a1b50b6a?auto=format&fit=crop&w=2560",  # Howrah Bridge
    "hyderabad": "https://images.unsplash.com/photo-1599485560363-201a1a17327b?auto=format&fit=crop&w=2560",  # Charminar
    "pune": "https://images.unsplash.com/photo-1574323347401-1b53dbb17d61?auto=format&fit=crop&w=2560",  # Shaniwar Wada
    "jaipur": "https://images.unsplash.com/photo-1564507592333-7b47d82c6a6b?auto=format&fit=crop&w=2560",  # Hawa Mahal
    "udaipur": "https://images.unsplash.com/photo-1600266611634-7b3ccff5245b?auto=format&fit=crop&w=2560",  # City Palace
    "varanasi": "https://images.unsplash.com/photo-1566563715101-9946f61e4d87?auto=format&fit=crop&w=2560",  # Ganga Ghats
    "goa": "https://images.unsplash.com/photo-1559373443-1559b874f695?auto=format&fit=crop&w=2560",  # Goa Beach
    "agra": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=2560",  # Taj Mahal
    "amritsar": "https://images.unsplash.com/photo-1572802419224-c501f6c5358c?auto=format&fit=crop&w=2560",  # Golden Temple
    "mysore": "https://images.unsplash.com/photo-1624784224473-04d9b33c1162?auto=format&fit=crop&w=2560",  # Mysore Palace
    "coimbatore": "https://images.unsplash.com/photo-1599156631818-121ba51377b8?auto=format&fit=crop&w=2560",  # Adiyogi Shiva Statue
    "shimla": "https://images.unsplash.com/photo-1610096191688-2c01d0d5a74f?auto=format&fit=crop&w=2560",  # Snowy Shimla Hills
    "manali": "https://images.unsplash.com/photo-1590476561703-1298f3a62a1e?auto=format&fit=crop&w=2560",  # Mountains of Manali
    "darjeeling": "https://images.unsplash.com/photo-1622109015507-cbe26f8e95d7?auto=format&fit=crop&w=2560",  # Tea Gardens
    "leh": "https://images.unsplash.com/photo-1536400328828-08d2f62b62c4?auto=format&fit=crop&w=2560",  # Pangong Lake
    "raipur": "https://images.unsplash.com/photo-1616062915156-b87e7b80efcc?auto=format&fit=crop&w=2560",  # Nandan Van Zoo
 
 
 }


# Add more cities as needed

def generate_itinerary(destination_city):
    """
    Generates a travel itinerary for the specified destination city using LLM.
    """
    prompt = f"""
    Create a  travel itinerary for {destination_city} in a structured, clear, and visually appealing format. Each day should be broken down as follows:

1. **Day Title** (e.g., Day 1: Explore the City)
   - Use bold for the day title and make sure the sections are clearly separated.
   
2. **Morning, Afternoon, and Evening sections**:
   - Clearly divide the day into morning, afternoon, and evening activities.
   - Each section should include:
     - **Tourist Attractions**: List popular tourist spots, including the name and a brief description.
     - **Local Cuisine**: Recommend at least one restaurant or dish to try, with details such as what to order and the restaurant’s name.
     - **Cultural Activities**: Suggest an activity that offers insight into the local culture (e.g., museum, gallery, local performance).
     - **Best Time to Visit**: Provide ideal times to visit each place to avoid crowds or experience it at its best.
     - **Estimated Time Needed**: Include how long each activity or visit should take.
     - **Transportation Tips**: Give practical advice on how to get there, including metro lines, buses, or walking directions.
   
3. **Formatting Requirements**:
   - Use **bold** for headings (e.g., Day Title, Activity titles).
   - Use bullet points for each place or restaurant, with sub-points for additional details.
   - Include spaces between each activity to ensure clarity.
   - Use a clean, readable font (such as Arial or Helvetica), and keep the design simple and easy to follow.
   - Ensure each day is practical, well-paced, and contains no more than 4 activities to avoid overwhelming the reader.
   - The final output should have clear headers for each day, as well as for the morning, afternoon, and evening sections.

The response should be easy to read and structured so that it's both informative and aesthetically pleasing.
"""

    try:
        # Generate itinerary using SambaNova LLM
        itinerary = generate_response(prompt)
        if not itinerary:
            return "Unable to generate itinerary at this time."
        
        return itinerary
    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        return "Error generating itinerary. Please try again."


# Define the route for the home page
@app.route('/')  # Route decorator for the home page
def index():
    # Return the HTML structure for the chat interface
    session.clear()
    global active_task, expected_key, user_details
    active_task = None
    expected_key = None
    user_details = {}
    print("Session cleared!")
    
    #return render_template('index.html')  # Uncomment to use a separate HTML file
 
    #return to the initial chatbot interface
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Travel Assistant</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        .glass {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }

        .chat-container {
            height: calc(100vh - 2rem);
        }

        .message {
            max-width: 85%;
            margin: 0.75rem;
            padding: 1rem 1.25rem;
            border-radius: 1rem;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .user-message {
            background: #3182ce;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 0.25rem;
        }

        .bot-message {
            background: white;
            color: #1a202c;
            margin-right: auto;
            border-bottom-left-radius: 0.25rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .quick-action {
            transition: all 0.3s ease;
        }

        .quick-action:hover {
            transform: translateY(-2px);
        }

        .typing-indicator {
            display: flex;
            padding: 1rem;
            gap: 0.25rem;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: #3182ce;
            border-radius: 50%;
            animation: bounce 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }

        .sidebar-card {
            transition: all 0.3s ease;
        }

        .sidebar-card:hover {
            transform: scale(1.02);
        }
        /* Add these right after your existing styles */
.itinerary-container {
    scrollbar-width: thin;  /* For Firefox */
    scrollbar-color: rgba(203, 213, 225, 0.8) transparent;  /* For Firefox */
}

/* For Chrome, Safari, and newer Edge */
.itinerary-container::-webkit-scrollbar {
    width: 6px;
}

.itinerary-container::-webkit-scrollbar-track {
    background: transparent;
}

.itinerary-container::-webkit-scrollbar-thumb {
    background-color: rgba(203, 213, 225, 0.8);
    border-radius: 20px;
}

.itinerary-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(148, 163, 184, 0.8);
}
    </style>
</head>
<body class="min-h-screen p-4">
    <div class="max-w-7xl mx-auto chat-container">
        <div class="flex h-full gap-4">
            <!-- Left Sidebar -->
            <div class="hidden lg:flex flex-col w-1/4 gap-4">
                <!-- Update the Trip Summary HTML part -->
                <div class="glass rounded-2xl p-4 flex-1">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-xl font-bold text-gray-800">Trip Summary</h3>
                        <button class="text-blue-600 hover:text-blue-800">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                    <div id="tripSummary" class="space-y-4">
                        <!-- Trip details will be inserted here -->
                    </div>
                </div>
                <!-- Weather Widget -->
                <div class="glass rounded-2xl p-4">
                    <h3 class="text-xl font-bold text-gray-800 mb-3">Weather Forecast</h3>
                    <div id="weatherWidget" class="text-center">
                        <!-- Weather info will be inserted here -->
                    </div>
                </div>
            </div>

            <!-- Main Chat Area -->
            <div class="flex-1 flex flex-col glass rounded-2xl overflow-hidden">
                <!-- Header -->
                <div class="p-4 bg-white bg-opacity-90 border-b border-gray-200">
                    <div class="flex items-center justify-between">
                        <div>
                            <h2 class="text-2xl font-bold text-gray-800">Travel Assistant</h2>
                            <p class="text-sm text-gray-600">Available 24/7 to help plan your perfect trip</p>
                        </div>
                        <div class="flex gap-2">
                            <button class="p-2 rounded-full hover:bg-gray-100" title="Clear Chat">
                                <i class="fas fa-trash-alt text-gray-600"></i>
                            </button>
                            <button class="p-2 rounded-full hover:bg-gray-100" title="Settings">
                                <i class="fas fa-cog text-gray-600"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="flex gap-4 p-4 overflow-x-auto">
                    <button class="quick-action flex-none px-4 py-2 bg-blue-100 text-blue-800 rounded-lg hover:bg-blue-200">
                        <i class="fas fa-plane-departure mr-2"></i>Book a Flight 
                    </button>
                    <button class="quick-action flex-none px-4 py-2 bg-green-100 text-green-800 rounded-lg hover:bg-green-200">
                        <i class="fas fa-hotel mr-2"></i>Hotels
                    </button>
                    <button class="quick-action flex-none px-4 py-2 bg-purple-100 text-purple-800 rounded-lg hover:bg-purple-200">
                        <i class="fas fa-car mr-2"></i>Car Rental
                    </button>
                    <button class="quick-action flex-none px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg hover:bg-yellow-200">
                        <i class="fas fa-map-marked-alt mr-2"></i>Activities
                    </button>
                </div>

                <!-- Chat Messages -->
                <div id="chatbox" class="flex-1 overflow-y-auto p-4 space-y-4">
                    <div id="typing-indicator" class="typing-indicator hidden">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>

                <!-- Input Area -->
                <div class="p-4 bg-white bg-opacity-90">
                    <div class="flex gap-3">
                        <button class="p-2 text-gray-600 hover:text-blue-600" title="Attach Files">
                            <i class="fas fa-paperclip"></i>
                        </button>
                        <input type="text" id="userInput" 
                               class="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                               placeholder="Ask me anything about your travel plans...">
                        <button id="sendButton"
                                class="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-2">
                            <span>Send</span>
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right Sidebar -->
            <div class="hidden lg:flex flex-col w-1/4 gap-4">
                <!-- Upcoming Trips -->
                <div class="glass rounded-2xl p-4 flex-1">
                    <h3 class="text-xl font-bold text-gray-800 mb-4">Upcoming Trips</h3>
                    <div id="upcomingTrips" class="space-y-4">
                        <!-- Trip cards will be inserted here -->
                    </div>
                </div>

                <!-- Travel Tips -->
                <div class="glass rounded-2xl p-4">
                    <h3 class="text-xl font-bold text-gray-800 mb-3">Travel Tips</h3>
                    <div id="travelTips" class="text-sm text-gray-700">
                        <!-- Tips will be inserted here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const typingIndicator = document.getElementById("typing-indicator");

    let passengerDetails = {};

    // Initialize demo content 
    initializeDemoContent();

    function appendMessage(message, type) {
        const msgClass = type === "user" ? "user-message" : "bot-message";
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${msgClass}`;
        messageDiv.innerHTML = type === "user" ? 
            `<div class="flex items-center gap-2">
                <i class="fas fa-user-circle"></i>
                <span>${message}</span>
            </div>` :
            `<div class="flex items-center gap-2">
                <i class="fas fa-robot"></i>
                <span>${message}</span>
            </div>`;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function initializeDemoContent() {
        // Initialize Trip Summary
        document.getElementById("tripSummary").innerHTML = `
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Destination</span>
                    <span class="font-semibold">Not Selected</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Dates</span>
                    <span class="font-semibold">Not Selected</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Budget</span>
                    <span class="font-semibold">Not Set</span>
                </div>
                <div class="mt-4">
                    <span class="text-gray-600">No itinerary generated yet</span>
                </div>
            </div>
        `;

        // Initialize Weather Widget
        document.getElementById("weatherWidget").innerHTML = `
            <div class="text-center">
                <i class="fas fa-sun text-4xl text-yellow-500 mb-2"></i>
                <div class="font-bold text-2xl">24°C</div>
                <div class="text-gray-600">Sunny</div>
            </div>
        `;

        // Initialize Upcoming Trips
        document.getElementById("upcomingTrips").innerHTML = `
            <div class="sidebar-card p-3 bg-blue-50 rounded-xl">
                <div class="font-semibold">No trips planned</div>
                <div class="text-sm text-gray-600">Start planning your next adventure!</div>
            </div>
        `;

        // Initialize Travel Tips
        document.getElementById("travelTips").innerHTML = `
            <div class="space-y-3">
                <div class="flex items-center gap-2">
                    <i class="fas fa-lightbulb text-yellow-500"></i>
                    <span>Remember to check visa requirements</span>
                </div>
                <div class="flex items-center gap-2">
                    <i class="fas fa-shield-alt text-blue-500"></i>
                    <span>Get travel insurance for peace of mind</span>
                </div>
            </div>
        `;

        // Initial welcome message
        appendMessage(
            `👋 Welcome to your Smart Travel Assistant! I'm here to help you plan your perfect trip. 
            What would you like to do?
            
            You can:
            • Search for flights and hotels
            • Plan activities and excursions
            • Get local weather updates
            • Manage your bookings
            • Get travel tips and recommendations`,
            "bot"
        );
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, "user");
        userInput.value = "";
        
        typingIndicator.classList.remove("hidden");
        
        try {
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message, passengerDetails }),
            });

            if (!response.ok) throw new Error("Network response was not ok.");

            const data = await response.json();
            typingIndicator.classList.add("hidden");

            appendMessage(data.response || "Sorry, something went wrong.", "bot");

            // Update background if provided
            if (data.background_url) {
                document.body.style.backgroundImage = `url('${data.background_url}')`;
                document.body.style.backgroundSize = 'cover';
                document.body.style.backgroundPosition = 'center';
                document.body.style.backgroundRepeat = 'no-repeat';
            }

            // Update trip summary if itinerary is provided
            // First, add this style to your existing <style> section in the HTML head
// Add right after your existing styles
if (data.itinerary) {
    const destination_city = message.match(/to\s+([^?.,]+)/i)?.[1] || "Selected Destination";
    
    // New regex patterns for date extraction
    const datePatterns = {
        // Matches dates like "June 15 - June 22" or "Jun 15 - Jun 22"
        fullMonth: /(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|[Mm]ay|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ep(?:tember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\s+\d{1,2}(?:\s*-\s*(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|[Mm]ay|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ep(?:tember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\s+\d{1,2})?/,
        
        // Matches dates like "15/06 - 22/06" or "15-06 to 22-06"
        numerical: /\d{1,2}[-/]\d{1,2}(?:\s*(?:to|-)\s*\d{1,2}[-/]\d{1,2})?/,
        
        // Matches dates like "June 15" or "Jun 15"
        singleDate: /(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|[Mm]ay|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ep(?:tember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\s+\d{1,2}/
    };

    // Try to extract dates using different patterns
    let tripDates = message.match(datePatterns.fullMonth) || 
                    message.match(datePatterns.numerical) || 
                    message.match(datePatterns.singleDate) || 
                    "To be decided";

    // If we found a date, use it; otherwise use default
    tripDates = tripDates ? tripDates[0] : "To be decided";

    document.getElementById("tripSummary").innerHTML = `
        <div class="space-y-4">
            <div class="space-y-2 border-b border-gray-200 pb-3">
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Destination</span>
                    <span class="font-semibold">${destination_city}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Dates</span>
                    <span class="font-semibold">${tripDates}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-gray-600">Budget</span>
                    <span class="font-semibold">To be decided</span>
                </div>
            </div>
            <div class="mt-4">
                <h4 class="font-semibold text-gray-800 mb-2">Generated Itinerary</h4>
                <div class="itinerary-container max-h-64 overflow-y-auto pr-2 text-sm text-gray-700 whitespace-pre-wrap">
                    ${data.itinerary}
                </div>
            </div>
        </div>
    `;

                // Also update the Upcoming Trips section
                document.getElementById("upcomingTrips").innerHTML = `
                    <div class="sidebar-card p-3 bg-blue-50 rounded-xl">
                        <div class="font-semibold">${destination_city} Trip</div>
                        <div class="text-sm text-gray-600">Planning in progress</div>
                        <div class="mt-2 text-xs text-blue-600">View Details →</div>
                    </div>
                `;
            }

        } catch (error) {
            typingIndicator.classList.add("hidden");
            appendMessage(`Error: ${error.message}`, "bot");
        }
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessage();
    });

    // Add click handlers for quick action buttons
    document.querySelectorAll('.quick-action').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.textContent.trim();
            userInput.value = `I want to ${action}`;
            sendMessage();
        });
    });
});
    </script>
</body>
</html>"""


     # End of HTML structure
HOTEL_BOOKINGS_FILE = "hotel_bookings.json"
 # Define the path for passenger details file
PASSENGER_FILE = "user_details.json"  # JSON file to store passenger details
SAMBANOVA_BASE_URL = "https://api.sambanova.ai/v1/chat/completions"  # Base URL for SambaNova API
SAMBANOVA_API_KEY = "7a3ea02e-28b0-43e5-8179-8df9132981eb"  # API key for SambaNova

# Initialize the Amadeus API
amadeus = AmadeusAPI()  # Create an instance of AmadeusAPI

@app.route('/send_message', methods=['POST'])  # Route for sending messages
def send_message():
    global active_task, expected_key, user_details

    # Reset active_task if new session
    if not active_task:
        active_task = None
        user_details = {}

    user_message = request.json.get("message")  # Get user message from request
    if not user_message:  # Check if message is provided
        return jsonify({"error": "No message provided."}), 400  # Return error response

    # Process the message using your chatbot logic
    response = chatbot_response(user_message)

    #generate itinerary if destination city 
    itinerary = None
    #background_url = None
    destination_city = None
    
    # Check user_details for destination city
    if user_details.get("destination_city"):
        destination_city = user_details["destination_city"]
    
    # If not found in user_details, try to extract from the current message
    if not destination_city:
        extracted_details = extract_flight_details_llm(user_message)
        if extracted_details.get("destination_city"):
            destination_city = extracted_details["destination_city"]
    
    # Get the background URL if we have a destination city
    if destination_city:
        itinerary = generate_itinerary(destination_city)
        
        
    background_url = CITY_IMAGES.get(destination_city.lower()if destination_city else None)
  # Get response from chatbot
    # if isinstance(response, dict):  # If response is a dictionary
    #     return jsonify(response)  # Return as JSON
    # elif isinstance(response, str):  # If response is a string
    return jsonify({"response": response,
                    "background_url":background_url,
                    "itinerary":itinerary})  # Wrap in JSON
    # else:
    #     return jsonify({"error": "Invalid response format."}), 500  # Return error for invalid format

# Function to generate a response using SambaNova API
def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {SAMBANOVA_API_KEY}",  # Set authorization header
        "Content-Type": "application/json"  # Set content type
    }

    payload = {
        "model": "Meta-Llama-3.1-8B-Instruct",  # Model to use for response generation
        "messages": [  # Messages to send to the model
            {"role": "system", "content": "You are a highly intelligent and efficient flight booking assistant. Your role is to help users with tasks such as booking flights, updating travel details, retrieving flight information, and canceling bookings. Provide clear, concise, and accurate responses while guiding the user through the process step-by-step."},  # System message
            {"role": "user", "content": prompt}  # User message
        ],
        "temperature": 0.1,  # Temperature for randomness
        "top_p": 0.1  # Top-p sampling
    }

    try:
        response = requests.post(SAMBANOVA_BASE_URL, headers=headers, json=payload, timeout=5)  # API call
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_data = response.json()  # Parse JSON response
        #print("SambaNova API Response:", response_data)  # Log the response data
        return response_data["choices"][0]["message"]["content"]  # Return the content of the response

    except requests.exceptions.RequestException as e:  # Handle request exceptions
        print("API call failed:", e)  # Log the error
        return None  # Return None on failure

    except (json.JSONDecodeError, KeyError) as e:  # Handle JSON parsing errors
        print("Parsing Error:", e)  # Log the error
        return None  # Return None on failure

# Function to detect entities in user input and intent
def extract_flight_details_llm(user_message):
    # Prepare a structured prompt for the LLM
    prompt = f"""
    Extract the following flight booking details from the user's input. Ensure that you replace any incorrect or misspelled city names with valid city names. Handle different formats where applicable.
1. Intent: Identify the user's intent by looking for phrases like:"book a flight", "fetch flight details", "update my flight", "cancel my flight", "book a room", "book a hotel", "update hotel".
   - Extract one of the following intents: `book_flight`, `update_flight`, `fetch_flight`, `cancel_flight`, `book_hotel`, `update_hotel`.
2. Boarding City: Extract the boarding city from phrases such as:"from <city>", "departing from <city>", "leaving from <city>".
3. Destination City: Extract the destination city from phrases like:"to <city>", "destination is <city>", "destination city is <city>".
4. Date of Flight: Extract the flight date from:Formats like *"on <YYYY-MM-DD>"*, *"on <DD-MM-YYYY>"*, *"for <MM/DD/YYYY>"*.Relative terms such as *"tomorrow"*, *"next week"*, *"in two days"*,*"tomm"*.
5. Name of the Passenger: Extract the passenger’s name from:*"I am <name>"*, *"My name is <name>"*, *"I would like to book under the name <name>"*.
6. Contact Number: Extract the phone number from:"my number is <phone_number>", "contact number is <phone_number>", "you can reach me at <phone_number>".
7. Flight ID: Extract the flight ID from:*"the flight ID is <flight_id>"*, *"my flight ID is <flight_id>"*, *"ID is <flight_id>"*.
8. Update Request: Identify update requests from:*"change flight date"*, *"update travel date"*, *"change destination city"*, *"change date"*, *"update boarding city"*.
9. Update Travel Date: Extract the new travel date from:*"change my date to <YYYY-MM-DD>"*, *"reschedule to <DD-MM-YYYY>"*, *"move my flight to <MM/DD/YYYY>"*.
10. Update Destination City: Extract the new destination city from:*"change my destination city to <city>"*, *"update my destination city to <city>"*, *"I want to fly to <city>"*.
11. Update Boarding City: Extract the new boarding city from:*"change my boarding city to <city>"*, *"update my departure city to <city>"*, *"I want to leave from <city>"*.
12. Email: Extract email addresses from:*"<email@example.com>"*.
13. City Name: Extract the city name for hotel bookings from:
    - *"I want to stay in <city>"*, *"book a hotel in <city>"*, *"find hotels in <city>"*.
14. Check-in Date: Extract the check-in date from:Formats like *"check-in on <YYYY-MM-DD>"*, *"arrival date is <YYYY-MM-DD>"*.
    - Relative terms such as *"tomorrow"*, *"next week"*, *"in two days"*.
15. Check-out Date: Extract the check-out date from:*"check-out on <YYYY-MM-DD>"*, *"departure date is <YYYY-MM-DD>"*, *"I will leave on <YYYY-MM-DD>"*.
16. Number of Adults: Extract the number of adults from:*"for <number> adults"*, *"number of guests <number>"*, *"booking for <number> people"*.
17. Update Choice: Identify requests to update hotel details from:*"change city"*, *"update check-in date"*, *"update check-out date"*, *"update adults"*.
18. New City: Extract the new city for hotel bookings from:*"change my hotel city to <city>"*, *"change my city to <city>"*.
19. New Check-in Date: Extract the new check-in date from:*"change my check-in date to <YYYY-MM-DD>"*, *"update my check-in date to <YYYY-MM-DD>"*.
20. New Check-out Date: Extract the new check-out date from:*"change my checkout date to <YYYY-MM-DD>"*.
21. Booking ID: Extract the hotel booking ID from:*"the booking ID is <booking_id>"*, *"my booking ID is <booking_id>"*, *"ID is <booking_id>"*.
    User input: "{user_message}"

    Provide the response ONLY in this JSON format without any extra text:
    {{
        "intent": "<intent>",
        "name": "<name>",
        "contact": "<contact>",
        "email": "<email>",
        "boarding_city": "<boarding_city>",
        "destination_city": "<destination_city>",
        "travel_date": "<travel_date>",
        "flight_id": "<flight_id>",
        "update_request": "<update_request>",
        "new_travel_date": "<new_travel_date>",
        "new_destination_city": "<new_destination_city>",
        "new_boarding_city": "<new_boarding_city>",
        "city_name": "<city_name>",
        "check_in_date": "<check_in_date>",
        "check_out_date": "<check_out_date>",
        "adults": "<adults>",
        "update_choice":<"update_choice">,
        "booking_id":<"booking_id">,
        "new_city":<"new_city">,
        "new_check_in_date":<"new_check_in_date">,
        "new_check_out_date":<"new_check_out_date">

    }}
    """  # End of prompt

    # Generate response using SambaNova LLM
    response = generate_response(prompt)  # Call the generate_response function

    # Debug: Print the raw response
    print("Raw LLM Response:", response)  # Log the raw response for debugging

    # Initialize passenger details dictionary
    passenger_details = {
        "intent": None,  # Initialize intent
        "name": None,  # Initialize name
        "contact": None,
        "email":None, # Initialize contact number
        "boarding_city": None,  # Initialize boarding city
        "destination_city": None,  # Initialize destination city
        "travel_date": None,  # Initialize travel date
        "flight_id": None,  # Initialize flight ID
        "update_request": None,  # Initialize update request
        "new_travel_date": None,  # Initialize new travel date
        "new_destination_city": None,  # Initialize new destination city
        "new_boarding_city": None,  # Initialize new boarding city
        "city_name": None,  # Initialize city name for hotel booking
        "check_in_date": None,  # Initialize check-in date
        "check_out_date": None,  # Initialize check-out date
        "adults": None,
        "update_choice":None,
        "booking_id":None,
        "new_city":None,
        "new_check_in_date":None,
        "new_check_out_date":None,  # Initialize number of adults for booking
        "missing_info": []  # Initialize list for missing information
    }

    # Attempt to extract the JSON part from the response
    try:
        # Locate the start and end of the JSON object
        json_start = response.find("{")  # Find the start of JSON
        json_end = response.rfind("}") + 1  # Find the end of JSON
        json_str = response[json_start:json_end]  # Extract JSON string

        # Parse the extracted JSON string
        response_data = json.loads(json_str)  # Convert JSON string to dictionary

        # Extract details from the parsed JSON
        passenger_details["intent"] = response_data.get("intent")  # Get intent
        passenger_details["name"] = response_data.get("name")  # Get name
        passenger_details["contact"] = response_data.get("contact")  # Get contact number
        passenger_details["email"] = response_data.get("email")  # Get contact number
        passenger_details["boarding_city"] = response_data.get("boarding_city")  # Get boarding city
        passenger_details["destination_city"] = response_data.get("destination_city")  # Get destination city
        passenger_details["travel_date"] = response_data.get("travel_date")  # Get travel date
        passenger_details["flight_id"] = response_data.get("flight_id")  # Get flight ID
        passenger_details["update_request"] = response_data.get("update_request")  # Get update request
        passenger_details["new_travel_date"] = response_data.get("new_travel_date")  # Get new travel date
        passenger_details["new_destination_city"] = response_data.get("new_destination_city")  # Get new destination city
        passenger_details["new_boarding_city"] = response_data.get("new_boarding_city")  # Get new boarding city
        passenger_details["city_name"] = response_data.get("city_name")  # Get city name for hotel booking
        passenger_details["check_in_date"] = response_data.get("check_in_date")  # Get check-in date
        passenger_details["check_out_date"] = response_data.get("check_out_date")  # Get check-out date
        passenger_details["adults"] = response_data.get("adults")  # Get number of adults
        passenger_details["update_choice"] = response_data.get("update_choice")  # Get number of adults
        passenger_details["booking_id"] = response_data.get("booking_id")  # Get number of adults
        passenger_details["new_city"] = response_data.get("new_city")  # Get number of adults
        passenger_details["new_check_in_date"] = response_data.get("new_check_in_date")  # Get number of adults
        passenger_details["new_check_out_date"] = response_data.get("new_check_out_date")  # Get number of adults
        
    except (json.JSONDecodeError, KeyError) as e:  # Handle JSON parsing errors
        print("Error: Failed to parse LLM response as JSON.", e)  # Log error
        return passenger_details  # Return passenger details

    # Check for missing information
    required_fields = ["boarding_city", "destination_city", "travel_date", "name", "contact","email", "flight_id", "update_request", "new_travel_date", "new_boarding_city", "new_destination_city", "city_name", "check_in_date", "check_out_date", "adults", "update_choice","booking_id","new_city","new_check_in_date","new_check_out_date"]  # List of required fields
    for key in required_fields:  # Iterate through required fields
        if not passenger_details[key]:  # Check if field is missing
            passenger_details["missing_info"].append(key)  # Add to missing info list

    return passenger_details  # Return passenger details


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return email if re.match(email_regex, email) else None
# Function to get IATA code for a city
def get_iata_code(city_name):
    try:
        return amadeus.get_airport_city(city_name)  # Call Amadeus API to get IATA code
    except Exception as e:  # Handle exceptions
        print(f"Error: {str(e)}")  # Log error
        return None  # Return None on error

def get_city_code(city_name):
    """
    Retrieves city details (latitude and longitude) using the Amadeus API.
    """
    try:
        city_data = amadeus.get_city_code(city_name)
        if not city_data:
            raise ValueError(f"City code not found for {city_name}.")

        return {
            "latitude": city_data.get("latitude"),
            "longitude": city_data.get("longitude")
        }
    except Exception as e:
        print(f"Error retrieving city code: {e}")
        return None

# # Function to validate input date format
# from datetime import datetime, timedelta
# import re

from datetime import datetime, timedelta
import re

def validate_input_date(date_str):
    """
    Parses various date formats and converts them into YYYY-MM-DD.
    Accepts:
    - Standard formats (YYYY-MM-DD, DD-MM-YYYY, MM/DD/YYYY)
    - Relative dates ("tomorrow", "next week", "in 3 days")
    - Natural language dates ("25th Feb", "5th March 2025")
    """

    if not date_str:
        return None

    date_str = date_str.lower().strip()
    today = datetime.today()

    # ✅ Handle relative dates
    if date_str in ["tomorrow", "tomm"]:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str == "next week":
        return (today + timedelta(days=7)).strftime("%Y-%m-%d")
    elif re.match(r"in (\d+) days", date_str):  # Example: "in 3 days"
        days = int(re.findall(r"\d+", date_str)[0])
        return (today + timedelta(days=days)).strftime("%Y-%m-%d")

    #  Handle standard date formats
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue  # Try the next format

    # Handle natural language dates like "25th Feb", "5th March 2025"
    try:
        date_str = re.sub(r"(st|nd|rd|th)", "", date_str)  # Remove ordinal suffixes
        return datetime.strptime(date_str, "%d %b").replace(year=today.year).strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")  # Full month name with year
    except ValueError:
        pass

    return None  # Invalid date format

def convert_to_inr(usd_price):
    """
    Converts USD price to INR using a fixed conversion rate.
    """
    conversion_rate = 82  # Example conversion rate (1 USD = 82 INR)
    return round(usd_price * conversion_rate, 2)

# Function to validate contact number
def validate_contact(contact):
    try:
        parsed_number = phonenumbers.parse(contact, None)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        pass
    return None
# Function to generate a random flight ID
def generate_flight_id():
    return str(random.randint(10000, 99999))  # Return a random flight ID as string

# Function to save passenger details to a JSON file
def save_passenger_details(passenger_details):
    try:
        if os.path.exists(PASSENGER_FILE):  # Check if file exists
            with open(PASSENGER_FILE, 'r') as file:  # Open file for reading
                data = json.load(file)  # Load existing data
        else:
            data = []  # Initialize empty list if file does not exist

        data.append(passenger_details)  # Append new passenger details

        with open(PASSENGER_FILE, 'w') as file:  # Open file for writing
            json.dump(data, file, indent=4)  # Save data to file

        print("\nPassenger details saved successfully!")  # Log success message
    except Exception as e:  # Handle exceptions
        print(f"Error saving details: {str(e)}")  # Log error
def generate_booking_id():
    """Generates a unique booking ID for hotel reservations."""
    return f"HB{random.randint(100000, 999999)}"

def save_hotel_booking(booking_details):
    """Saves hotel booking details to a JSON file."""
    HOTEL_BOOKINGS_FILE = "hotel_bookings.json"
    try:
        if os.path.exists(HOTEL_BOOKINGS_FILE):
            with open(HOTEL_BOOKINGS_FILE, 'r') as file:
                bookings = json.load(file)
        else:
            bookings = []

        bookings.append(booking_details)

        with open(HOTEL_BOOKINGS_FILE, 'w') as file:
            json.dump(bookings, file, indent=4)

        print("\nHotel booking details saved successfully!")
    except Exception as e:
        print(f"Error saving booking details: {str(e)}") 



def book_flight(name, contact,email, boarding_city, destination_city, travel_date):
    # Validate contact number
    if not validate_contact(contact):  # Validate contact
        return "Invalid contact number. Please enter at least 10 digits."  # Return error message
    
    email= validate_email(user_details["email"])
    if not email:
        return prompt_user("Invalid email address. Please enter a valid email:", "email")

    # Validate travel date
    while not validate_input_date(travel_date):  # Check if travel date is valid
        travel_date ="Invalid date format. Please use YYYY-MM-DD. Enter travel date again: " # Prompt for new date

    # Fetch IATA code for boarding city
    boarding_city_code = get_iata_code(boarding_city)  # Get IATA code
    while not boarding_city_code:  # Check if IATA code is valid
        return prompt_user( "Unable to retrieve the IATA code for the boarding city. Please provide a valid city name: ",boarding_city)  # Prompt for new city
    boarding_city_code = get_iata_code(boarding_city)  # Get IATA code

    # Fetch IATA code for destination city
    destination_city_code = get_iata_code(destination_city)  # Get IATA code
    while not destination_city_code:  # Check if IATA code is valid
        return ("Unable to retrieve the IATA code for the destination city. Please provide a valid city name: ")  # Prompt for new city
    destination_city_code = get_iata_code(destination_city)  # Get IATA code

    # Search for flights
    available_flights = amadeus.search_flights(boarding_city_code, destination_city_code, travel_date)  # Search for flights
    while not available_flights:  # Check if flights are available
        return f"No flights available for {travel_date}. Please enter a new date (YYYY-MM-DD): "  # Prompt for new date
    while not validate_input_date(travel_date):  # Validate new date
        travel_date = input("Invalid date format. Please use YYYY-MM-DD. Enter travel date again: ")  # Prompt for new date
    available_flights = amadeus.search_flights(boarding_city_code, destination_city_code, travel_date)  # Search for flights
    #return prompt_user = f"Flights found for {travel_date}. Displaying the results..."  # Message for available flights
    
    response = display_flight(available_flights,boarding_city_code, destination_city_code)  # Call function to display flights
    return str(response)  # Return response as string

def display_flight(available_flights, boarding_city_code, destination_city_code):
    """
    Handles displaying available flights, prompting user for a selection,
    validating their input, and saving the selected flight details.
    """
    if not available_flights:  # Check if flights are available
        return "No flights available. Please try searching with different criteria."  # Return message

    # Step 1: Prepare the list of available flights
    user_details = []  # Initialize list for flight details
    for idx, flight in enumerate(available_flights, 1):  # Iterate through available flights
        offer = flight['itineraries'][0]  # Get itinerary
        segments = offer['segments']  # Get flight segments
        carrier_code = segments[0]['carrierCode']  # Get airline code
        airline_name = amadeus.get_airline_name(carrier_code)
        departure_time = segments[0]['departure']['at']  # Get departure time
        arrival_time = segments[-1]['arrival']['at']
        usd_price = float(flight['price']['total'])  # Get price in USD
        inr_price = convert_to_inr(usd_price)  # Get arrival time
        price = f"₹{inr_price}"  # Get flight price
        user_details.append(f"{idx}. Airline: {airline_name}, Departure: {departure_time}, Arrival: {arrival_time}, Price:{price}")  # Append flight detail

        
    # Prepare and send the message with available flights
    flights_message = "\n\n".join(user_details)  # Join flight details into a string
    response = f"Available flights for {boarding_city_code} to {destination_city_code}:\n\n{flights_message}\n\nPlease select a flight by entering the number."  # Response message
    return response  # Return response

def handle_flight_selection(flight_choice, available_flights, name, contact,email, boarding_city_code, destination_city_code, travel_date):
    """
    Handles the user's flight selection, validates the choice, and saves booking details.
    """
    if not str(flight_choice).isdigit():  # Check if flight choice is a number
        return "Invalid selection. Please enter a valid number."  # Return error message

    selected_flight_index = int(flight_choice) - 1  # Convert choice to index
    if selected_flight_index < 0 or selected_flight_index >= len(available_flights):  # Check if index is valid
        return "Invalid flight selection. Please select a number within the available options."  # Return error message

    # Extract flight details
    selected_flight = available_flights[selected_flight_index]  # Get selected flight
    segments = selected_flight['itineraries'][0]['segments']  # Get flight segments
    carrier_code = segments[0]['carrierCode']  # Get airline code
    airline_name = amadeus.get_airline_name(carrier_code)
    departure_time = segments[0]['departure']['at']  # Get departure time
    arrival_time = segments[-1]['arrival']['at']  # Get arrival time
    usd_price = float(selected_flight['price']['total'])  # Get price in USD
    inr_price = convert_to_inr(usd_price)  # Get arrival time
    price = f"₹{inr_price}"
    # Generate flight ID and save passenger details
    flight_id = generate_flight_id()  # Generate flight ID
    passenger_details = {  # Create passenger details dictionary
        "name": name,  # Get name
        "contact": contact,  # Get contact
        "email":email,
        "flight_id": flight_id,  # Set flight ID
        "airline": airline_name,  # Set airline
        "boarding_city": boarding_city_code,  # Set boarding city
        "destination_city": destination_city_code,  # Set destination city
        "travel_date": travel_date,  # Set travel date
        "departure_time": departure_time,  # Set departure time
        "arrival_time": arrival_time,  # Set arrival time
        "price":price  # Set price
    }

    save_passenger_details(passenger_details)  # Save passenger details

    # Confirmation message
    return (f"Flight booked successfully! Flight ID: {flight_id}, Airline: {airline_name},"
            f"Departure: {departure_time}, Arrival: {arrival_time}, Price:{price}.")  # Return confirmation message

def fetch_flight(flight_id):
    try:
        # Read the passenger details from the JSON file
        if not os.path.exists(PASSENGER_FILE):  # Check if file exists
            return {"error": "No passenger details file found."}  # Return error response

        with open(PASSENGER_FILE, "r") as file:  # Open file for reading
            passengers = json.load(file)  # Load passenger data

        # Find the matching passenger details based on flight_id
        passenger_info = next((p for p in passengers if p['flight_id'] == flight_id), None)  # Find passenger info

        if passenger_info:  # Check if passenger info is found
            return passenger_info  # Return plain dictionary
        else:
            return {"error": "No passenger information found for this flight ID."}  # Return error response

    except Exception as e:  # Handle exceptions
        return {"error": f"An error occurred: {str(e)}"}  # Return error response
    
def update_flight():
    """
    Validates and updates the flight details in the data store.
    """
    flight_id = user_details["flight_id"]
    try:
        # Load flight data from the JSON file
        if not os.path.exists(PASSENGER_FILE):
            return "No flight booking data found."

        with open(PASSENGER_FILE, "r") as file:
            passengers = json.load(file)

        # Find and update the flight details
        for passenger in passengers:
            if passenger["flight_id"] == flight_id:
                if user_details.get("new_travel_date"):
                    if not validate_input_date(user_details["new_travel_date"]):
                        return "Invalid travel date format. Please use YYYY-MM-DD."
                    passenger["travel_date"] = user_details["new_travel_date"]

                if user_details.get("new_destination_city"):
                    iata_code = get_iata_code(user_details["new_destination_city"])
                    if not iata_code:
                        return f"Invalid destination city: {user_details['new_destination_city']}"
                    passenger["destination_city"] = iata_code

                if user_details.get("new_boarding_city"):
                    iata_code = get_iata_code(user_details["new_boarding_city"])
                    if not iata_code:
                        return f"Invalid boarding city: {user_details['new_boarding_city']}"
                    passenger["boarding_city"] = iata_code

                # Save updated details back to the JSON file
                with open(PASSENGER_FILE, "w") as file:
                    json.dump(passengers, file, indent=4)

                return passenger  # Return updated passenger details

        return f"No booking found for Flight ID {flight_id}."

    except Exception as e:
        print(f"Error updating flight data: {str(e)}")
        return "An error occurred while updating the flight data."
def search_flights_after_update(updated_details):
    """
    Searches for flights based on the updated details.
    """
    try:
        boarding_city_code = updated_details["boarding_city"]
        destination_city_code = updated_details["destination_city"]
        travel_date = updated_details["travel_date"]

        available_flights = amadeus.search_flights(boarding_city_code, destination_city_code, travel_date)
        return available_flights

    except Exception as e:
        print(f"Error searching for flights: {str(e)}")
        return None


def finalize_flight_selection(updated_details, flight_choice):
    """
    Confirms the user's selected flight and saves the updated booking details.
    """
    available_flights = user_details.get("available_flights", [])
    if not available_flights:
        reset_task()
        return "No flights available to finalize the update."

    # Validate flight selection
    if not flight_choice.isdigit():
        return "Invalid selection. Please enter a valid number."
    flight_choice_index = int(flight_choice) - 1
    if flight_choice_index < 0 or flight_choice_index >= len(available_flights):
        return "Invalid selection. Please select a number within the available options."

    # Extract selected flight details
    selected_flight = available_flights[flight_choice_index]
    segments = selected_flight["itineraries"][0]["segments"]
    carrier_code = segments[0]["carrierCode"]
    airline_name = amadeus.get_airline_name(carrier_code)
    departure_time = segments[0]["departure"]["at"]
    arrival_time = segments[-1]["arrival"]["at"]
    usd_price = float(selected_flight['price']['total'])  # Get price in USD
    inr_price = convert_to_inr(usd_price)  # Get arrival time
    price = f"₹{inr_price}"
    
    # Update the booking details with the selected flight
    updated_details["airline"] = airline_name
    updated_details["departure_time"] = departure_time
    updated_details["arrival_time"] = arrival_time
    updated_details["price"] = price

    # Save updated booking details
    save_passenger_details(updated_details)

    # Reset task
    reset_task()
    return (
        f"Flight updated successfully!\n"
        f"Name: {updated_details['name']}\n"
        f"Contact: {updated_details['contact']}\n"
        f"Airline: {updated_details['airline_name']}\n"
        f"Boarding City: {updated_details['boarding_city']}\n"
        f"Destination City: {updated_details['destination_city']}\n"
        f"Travel Date: {updated_details['travel_date']}\n"
        f"Departure Time: {updated_details['departure_time']}\n"
        f"Arrival Time: {updated_details['arrival_time']}\n"
        f"Price: {updated_details['price']}"
    )

def cancel_flight(flight_id):
    """
    Cancels a flight by its flight ID from the JSON file.
    """
    try:
        # Check if the JSON file exists and load its content
        with open(PASSENGER_FILE, 'r') as file:
            flights = json.load(file)

        # Find the flight entry by flight ID
        flight_entry = next((flight for flight in flights if flight['flight_id'] == flight_id), None)
        if not flight_entry:
            return f"Flight ID {flight_id} not found."

        # Remove the flight entry from the data
        updated_flights = [flight for flight in flights if flight['flight_id'] != flight_id]

        # Write the updated data back to the JSON file
        with open(PASSENGER_FILE, 'w') as file:
            json.dump(updated_flights, file, indent=4)

        return f"Flight {flight_id} canceled successfully!"

    except FileNotFoundError:
        return "Passenger data file not found."
    except Exception as e:
        print(f"Error in cancel_flight: {str(e)}")
        return f"An error occurred while canceling the flight: {str(e)}"

def suggest_alternative_dates(check_in_date, check_out_date):
    check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out = datetime.strptime(check_out_date, "%Y-%m-%d")

    alternative_dates = []
    for delta in range(1, 4):  # Suggest up to 3 days forward
        new_check_in = check_in + timedelta(days=delta)
        new_check_out = check_out + timedelta(days=delta)
        alternative_dates.append((new_check_in.strftime("%Y-%m-%d"), new_check_out.strftime("%Y-%m-%d")))

    return alternative_dates

def handle_no_rooms_error(hotel_ids, check_in_date, check_out_date):
    return (
        f"Unfortunately, no rooms are available at the selected hotels for the dates "
        f"{check_in_date} to {check_out_date}. Please try different dates or locations."
    )

def handle_hotel_search(city_name, check_in_date, check_out_date, adults=1):
    city_data = amadeus.get_city_code(city_name)
    if not city_data or not city_data.get("iataCode"):
        return []

    city_code = city_data["iataCode"]
    hotel_list = amadeus.fetch_hotel_list_by_city(city_code)
    if not hotel_list:
        return []

    hotel_ids = [hotel["hotelId"] for hotel in hotel_list]
    offers = amadeus.fetch_hotel_offers(hotel_ids, check_in_date, check_out_date, adults)
    if not offers:
        return []

    sorted_offers = []
    for offer in offers:
        hotel = offer.get('hotel', {})
        name = hotel.get('name', 'Unknown Hotel')
        address_lines = hotel.get('address', {}).get('lines', None)
        address = ", ".join(address_lines) if address_lines else "Address not available"
        offer_details = offer.get('offers', [{}])[0]
        price = offer_details.get('price', {}).get('total', None)
        currency = offer_details.get('price', {}).get('currency', 'USD')
        check_in = offer_details.get('checkInDate', 'Unknown')
        check_out = offer_details.get('checkOutDate', 'Unknown')

        if price is None:
            continue

        sorted_offers.append({
            "name": name,
            "address": address,
            "price": float(price),
            "currency": currency,
            "check_in": check_in,
            "check_out": check_out,
        })

    # Sort offers by price
    sorted_offers.sort(key=lambda x: x["price"])
    return sorted_offers

    # Format the sorted results for display
    results = []
    for idx, offer in enumerate(sorted_offers, 1):
        results.append(
            f"{idx}. Hotel Name: {offer['name']}\n"
            f"   Address: {offer['address']}\n"
            f"   Price: {offer['price']} {offer['currency']}\n"
            f"   Stay Dates: {offer['check_in']} to {offer['check_out']}"
        )

    # Join all results into a single string
    hotel_details = "\n\n".join(results)
    response = (
        f"Available Hotels in {city_name} from {check_in_date} to {check_out_date} are:\n\n"
        f"{hotel_details}\n\n"
        "Please select a hotel by entering the number."
    )
    expected_key = "hotel_choice"
    return response
def update_hotel_booking():
    """
    Validates and updates the hotel booking details in the data store.
    """
    booking_id = user_details["booking_id"]
    try:
        # Load hotel booking data from the JSON file
        if not os.path.exists(HOTEL_BOOKINGS_FILE):
            return "No hotel booking data found."

        with open(HOTEL_BOOKINGS_FILE, "r") as file:
            bookings = json.load(file)

        # Find and update the hotel booking
        for booking in bookings:
            if booking["booking_id"] == booking_id:
                # Update the city if requested
                if user_details.get("new_city_name"):
                    city_name = user_details["new_city_name"].strip()
                    city_data = get_city_code(city_name)
                    if not city_data:
                        return f"Invalid city: {city_name}"
                    booking["city_name"] = city_name

                # Update check-in date if requested
                if user_details.get("new_check_in_date"):
                    check_in_date = user_details["new_check_in_date"].strip()
                    if not validate_input_date(check_in_date):
                        return "Invalid check-in date format. Please use YYYY-MM-DD."
                    booking["check_in_date"] = check_in_date

                # Update check-out date if requested
                if user_details.get("new_check_out_date"):
                    check_out_date = user_details["new_check_out_date"].strip()
                    if not validate_input_date(check_out_date):
                        return "Invalid check-out date format. Please use YYYY-MM-DD."
                    booking["check_out_date"] = check_out_date

                # Update number of adults if requested
                if user_details.get("new_adults"):
                    try:
                        adults = int(user_details["new_adults"])
                        if adults < 1:
                            return "Number of adults must be at least 1."
                        booking["adults"] = adults
                    except ValueError:
                        return "Please enter a valid number for adults."

                # Save updated details back to the JSON file
                with open(HOTEL_BOOKINGS_FILE, "w") as file:
                    json.dump(bookings, file, indent=4)

                return booking  # Return updated booking details

        return f"No booking found for Booking ID {booking_id}."

    except Exception as e:
        print(f"Error updating hotel booking data: {str(e)}")
        return "An error occurred while updating the hotel booking."
def search_hotels_after_update(updated_details):
    """
    Searches for hotels based on the updated booking details.
    """
    try:
        city_name = updated_details["city_name"]
        check_in_date = updated_details["check_in_date"]
        check_out_date = updated_details["check_out_date"]
        adults = updated_details["adults"]

        available_hotels = handle_hotel_search(city_name, check_in_date, check_out_date, adults)
        return available_hotels

    except Exception as e:
        print(f"Error searching for hotels: {str(e)}")
        return None
def display_hotels(hotels, city, check_in_date, check_out_date):
    """
    Formats and displays a list of hotels.
    """
    results = []
    for idx, hotel in enumerate(hotels, 1):
        results.append(
            f"{idx}. Hotel Name: {hotel['name']}\n"
            f"   Address: {hotel['address']}\n"
            f"   Price: {hotel['price']} {hotel['currency']}\n"
            f"   Stay Dates: {hotel['check_in']} to {hotel['check_out']}\n"
            "------------------------------------------------------------"
        )
    return (
        f"Hotels available in {city} from {check_in_date} to {check_out_date}:\n\n"
        + "\n".join(results)+
        "\n\n Please select a hotel by entering the number:"
    )


def finalize_hotel_selection(updated_details, hotel_choice):
    """
    Confirms the user's selected hotel and saves the updated booking details.
    """
    available_hotels = user_details.get("available_hotels", [])
    if not available_hotels:
        reset_task()
        return "No hotels available to finalize the update."

    # Validate the hotel selection
    if not hotel_choice.isdigit():
        return "Invalid selection. Please enter a valid number."
    hotel_choice_index = int(hotel_choice) - 1
    if hotel_choice_index < 0 or hotel_choice_index >= len(available_hotels):
        return "Invalid selection. Please select a number within the available options."

    # Extract selected hotel details
    selected_hotel = available_hotels[hotel_choice_index]

    # Update the booking details with the selected hotel
    updated_details.update({
        "hotel_name": selected_hotel["name"],
        "price": f"{selected_hotel['price']} {selected_hotel['currency']}",
        "address": selected_hotel["address"],
        "check_in_date": selected_hotel["check_in"],
        "check_out_date": selected_hotel["check_out"]
    })

    # Save the updated booking details
    save_hotel_booking(updated_details)

    # Confirm the booking update
    reset_task()
    return (
        f"Hotel updated successfully!\n"
        f"Hotel: {selected_hotel['name']}\n"
        f"Address: {selected_hotel['address']}\n"
        f"Check-in: {selected_hotel['check_in']}\n"
        f"Check-out: {selected_hotel['check_out']}\n"
        f"Price: {selected_hotel['price']} {selected_hotel['currency']}\n"
        "Thank you for updating your booking!"
    )
def fetch_hotel_details(booking_id):
    """
    Fetches hotel booking details based on the provided Booking ID.
    """
    try:
        # Check if the hotel booking file exists
        if not os.path.exists(HOTEL_BOOKINGS_FILE):
            return {"error": "No hotel booking data found."}

        # Read hotel booking data
        with open(HOTEL_BOOKINGS_FILE, "r") as file:
            bookings = json.load(file)

        # Find the matching hotel booking by booking_id
        hotel_booking = next((b for b in bookings if b["booking_id"] == booking_id), None)

        if hotel_booking:
            return hotel_booking  # Return hotel booking details as a dictionary
        else:
            return {"error": "No hotel booking found for this Booking ID."}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# Initialize variables
active_task = None  # Initialize active task
expected_key = None  # Initialize expected key
user_details = {}  # Initialize flight details

def prompt_user(message: str, key:str):
    global expected_key  # Use global variable
    expected_key = key  # Set expected key
    return message  # Return message

def reset_task():
    """Resets the task and related variables."""
    global active_task, expected_key, user_details  # Use global variables
    active_task = None  # Reset active task
    expected_key = None  # Reset expected key
    user_details = {}  # Reset flight details
    

def validate_city(city):
    """Validates if a city has a valid IATA code."""
    return bool(get_iata_code(city))  # Return True if city is valid

# Main response function
def chatbot_response(user_message):
    """
    Processes user input, determines the intent, collects required information, and performs actions such as 
    booking, updating, or canceling flights.
    """
    global active_task, expected_key, user_details  # Use global variables

    try:
        # Handle user input for a pending task
        if active_task and handle_pending_task(user_message):  # Check for active task
            pass  # Continue processing

        # Determine intent if no active task
        if not active_task:  # If no active task
            user_details = extract_flight_details_llm(user_message)  # Extract flight details
            active_task = user_details.get("intent")  # Get intent

        # Handle different tasks
        if active_task == "book_flight":  # Check for booking task
            return handle_book_flight(user_message)  # Call function to handle booking
        elif active_task == "fetch_flight":  # Check for fetching task
            return handle_fetch_flight()  # Call function to handle fetching
        elif active_task == "update_flight ":  # Check for updating task
            return handle_update_flight(user_message)  # Call function to handle updating
        elif active_task == "cancel_flight":  # Check for deleting task
            return handle_cancel_flight()  # Call function to handle deleting
        elif active_task == "book_hotel":  # Check for deleting task
             return handle_book_hotel(user_message) 
        elif active_task == "update_hotel":  # Check for deleting task
             return handle_update_hotel(user_message) 
        else:  # If intent is not recognized
            return "I cannot understand. Please try again."  # Return error message
    
    except Exception as e:  # Handle exceptions
        print(f"Error in chatbot_response: {e}")  # Log error
        return "Oops! Something went wrong while processing your request."  # Return error message

def handle_pending_task(user_message):
    """Handles pending user input for incomplete details."""
    global expected_key, user_details  # Use global variables

    if expected_key:  # Check if there is an expected key
        user_details[expected_key] = user_message  # Store user input
        expected_key = None  # Reset expected key

        # If the pending key is "flight_choice", validate the input
        
        return True  # Indicates the task is being processed  
    
def handle_book_hotel(user_message):
    global expected_key, user_details

    # Step 1: Collect missing details
    required_fields = [
        ("name", "Enter your Name:"),
        ("contact", "Enter your Contact No.:"),
        ("email", "Enter your Mail-Id:"),
        ("city_name", "Enter the city where you'd like to stay:"),
        ("check_in_date", "Enter your Check-in Date (YYYY-MM-DD):"),
        ("check_out_date", "Enter your Check-out Date (YYYY-MM-DD):"),
        ("adults", "Enter the number of adults:")
    ]

    for field, prompt in required_fields:
        if not user_details.get(field):
            return prompt_user(prompt, field)

    # Step 2: Validate inputs
    user_details["email"] = validate_email(user_details["email"]) or prompt_user("Invalid email address. Please enter again:", "email")
    user_details["contact"] = validate_contact(user_details["contact"]) or prompt_user("Invalid contact number. Please enter again:", "contact")
    user_details["check_in_date"] = validate_input_date(user_details["check_in_date"]) or prompt_user("Invalid check-in date. Please use YYYY-MM-DD:", "check_in_date")
    user_details["check_out_date"] = validate_input_date(user_details["check_out_date"]) or prompt_user("Invalid check-out date. Please use YYYY-MM-DD:", "check_out_date")

    # Step 3: Search hotels if `hotel_choice` is not set
    if expected_key == "hotel_choice" or not user_details.get("hotel_choice"):
        hotels_response = handle_hotel_search(
            user_details["city_name"],
            user_details["check_in_date"],
            user_details["check_out_date"],
            user_details["adults"]
        )
        if not hotels_response:
            reset_task()
            return "No hotels found for the given details. Please try again."

        # Save the list of hotels for later reference
        user_details["available_hotels"] = hotels_response

        # Prepare the list of hotels for display
        results = []
        for idx, hotel in enumerate(hotels_response, 1):
            results.append(
                f"{idx}. Hotel Name: {hotel['name']}\n"
                f"   Address: {hotel['address']}\n"
                f"   Price: {hotel['price']} {hotel['currency']}\n"
                f"   Stay Dates: {hotel['check_in']} to {hotel['check_out']}"
            )
        response = (
            f"Available Hotels in {user_details['city_name']} from {user_details['check_in_date']} to {user_details['check_out_date']}:\n\n"
            f"{'\n\n'.join(results)}\n\n"
            "Please select a hotel by entering the number."
        )
        expected_key = "hotel_choice"
        return response

    # Step 4: Handle hotel selection
    hotel_choice = user_message.strip()
    if not hotel_choice.isdigit():
        return "Invalid selection. Please enter a valid number."

    hotel_choice_index = int(hotel_choice) - 1
    available_hotels = user_details.get("available_hotels", [])
    if hotel_choice_index < 0 or hotel_choice_index >= len(available_hotels):
        return "Invalid selection. Please choose a valid option."

    # Step 5: Save selected hotel details
    selected_hotel = available_hotels[hotel_choice_index]
    booking_id = generate_booking_id()
    hotel_details = {
        "booking_id": booking_id,
        "name": user_details["name"],
        "contact": user_details["contact"],
        "email": user_details["email"],
        "city": user_details["city_name"],
        "check_in_date": user_details["check_in_date"],
        "check_out_date": user_details["check_out_date"],
        "adults": user_details["adults"],
        "hotel_name": selected_hotel["name"],
        "price": selected_hotel["price"],
        "currency": selected_hotel["currency"],
        "address": selected_hotel["address"]
    }

    # Save booking
    save_hotel_booking(hotel_details)
    reset_task()
    return (
        f"Hotel booked successfully!\n"
        f"Booking ID: {booking_id}\n"
        f"Hotel: {hotel_details['hotel_name']}\n"
        f"Check-in: {hotel_details['check_in_date']}\n"
        f"Check-out: {hotel_details['check_out_date']}\n"
        f"Price: {hotel_details['price']} {hotel_details['currency']}\n"
        "Thank you for booking with us!"
    )
def handle_update_hotel(user_message):
    """
    Handles the flow for updating a hotel booking.
    Collects Booking ID, Update Type, New Details, and allows selecting updated hotels.
    """
    global expected_key, user_details

    # Step 1: Collect Booking ID
    if not user_details.get("booking_id"):
        return prompt_user("Please provide your Booking ID:", "booking_id")

    # Step 2: Collect Update Type
    if not user_details.get("update_request"):
        return prompt_user(
            "What would you like to update? Options:\n"
            "1. City\n"
            "2. Check-in Date\n"
            "3. Check-out Date\n"
            "4. Number of Adults\n"
            "Enter the number or type your choice:", 
            "update_request"
        )

    # Step 3: Collect New Details based on Update Type
    update_request = user_details.get("update_request").strip().lower()

    if update_request in ["1", "city", "change city", "update city"]:
        if not user_details.get("new_city_name"):
            return prompt_user("Enter the new city for your stay:", "new_city_name")
    elif update_request in ["2", "check-in date", "change check-in date", "update check-in date"]:
        if not user_details.get("new_check_in_date"):
            return prompt_user("Enter the new Check-in Date (YYYY-MM-DD):", "new_check_in_date")
    elif update_request in ["3", "check-out date", "change check-out date", "update check-out date"]:
        if not user_details.get("new_check_out_date"):
            return prompt_user("Enter the new Check-out Date (YYYY-MM-DD):", "new_check_out_date")
    elif update_request in ["4", "adults", "number of adults", "update number of adults"]:
        if not user_details.get("new_adults"):
            return prompt_user("Enter the new number of adults:", "new_adults")
    else:
        return "Invalid choice. Please select a valid option."

    # Step 4: Update Data
    updated_data_response = update_hotel_booking()
    if isinstance(updated_data_response, str):  # Error occurred
        reset_task()
        return updated_data_response

    # Step 5: Search for Hotels
    if not user_details.get("hotel_choice"):
        available_hotels = search_hotels_after_update(updated_data_response)
        if not available_hotels:
            reset_task()
            return "No hotels available for the updated details. Please try again."

        # Store available hotels and prompt for hotel choice
        user_details["available_hotels"] = available_hotels
        expected_key = "hotel_choice"
        return display_hotels(
            available_hotels,
            updated_data_response["city_name"],
            updated_data_response["check_in_date"],
            updated_data_response["check_out_date"]
        )

    # Step 6: Process Hotel Choice
    hotel_choice = user_message.strip()
    return finalize_hotel_selection(updated_data_response, hotel_choice)

def handle_book_flight(user_message):
    """Handles the booking flight intent."""
    global expected_key  # Use global variable
    # Step 1: Collect missing details
    for field, prompt in [  
    # List of fields to collect
        ("name", "Enter your Name:"),  # Name prompt
        ("contact", "Enter your Contact No.:"),  # Contact prompt
        ("email","Enter your Mail-Id:"),
        ("boarding_city", "Enter your Boarding city:"),  # Boarding city prompt
        ("destination_city", "Enter your Destination city:"),  # Destination city prompt
        ("travel_date", "Enter your Travel-Date (YYYY-MM-DD):"),  # Travel date prompt
    ]:
        if not user_details.get(field):  # Check if field is missing
            message= prompt_user(prompt, field)  # Prompt user for input
            return message  # Return prompt message
        
    email = user_details.get("email", "").strip()
    if not email:
        return prompt_user("Email is missing. Please provide your email:", "email")

    email=validate_email(user_details["email"])
    if not email:
        return prompt_user("Invalid Mail-id. Please Enter the correct mail-id again", "email") 
    user_details["email"] = email

    contact= validate_contact(user_details['contact'])
    if not contact:  # Validate contact
        return prompt_user("Invalid contact number. Please enter at least 10 digits:", "contact")
    user_details['contact'] = contact
    # Step 3: Validate travel date
    travel_date=validate_input_date(user_details["travel_date"])
    if not travel_date:  # Validate travel date
        return prompt_user("Invalid date format. Please use YYYY-MM-DD. Enter travel date:", "travel_date")
    user_details["travel_date"]= travel_date

    # Step 2: Display flights if `flight_choice` is not set
    if expected_key == "flight_choice" or not user_details.get("flight_choice"):  # Check if flight choice is expected
        boarding_city_code = get_iata_code(user_details["boarding_city"])  # Get IATA code for boarding city
        while not boarding_city_code:  # Check if IATA code is valid
            return prompt_user("Unable to retrieve the IATA code for the boarding city. Please provide a valid city name:","boarding_city")  # Prompt for new city
        

        destination_city_code = get_iata_code(user_details["destination_city"])  # Get IATA code for destination city
        while not destination_city_code:  # Check if IATA code is valid
            return prompt_user("Unable to retrieve the IATA code for the destination city. Please provide a valid city name:","destination_city")  # Prompt for new city
        

        available_flights = amadeus.search_flights(boarding_city_code, destination_city_code,travel_date)

        while not available_flights:  # Check if flights are available
            return prompt_user("No flights available for {user_details['travel_date']}. Please enter a new travel date (YYYY-MM-DD):","travel_date"),
        available_flights = amadeus.search_flights( boarding_city_code, destination_city_code, travel_date)

        # Save available flights in `flight_details`
        user_details["available_flights"] = available_flights  # Store available flights

        # Prompt user to select a flight
        expected_key = "flight_choice"  # Set expected key for user input
        return display_flight(  # Call function to display flights
            available_flights,
            boarding_city_code,
            destination_city_code
        )

    # Step 3: Process the `flight_choice` if provided
    flight_choice = user_message.strip()  # Get user input
    if not flight_choice.isdigit():  # Check if input is a number
        return "Invalid selection. Please enter a valid number."  # Return error message

    flight_choice_index = int(flight_choice) - 1  # Convert choice to index
    available_flights = user_details.get("available_flights", [])  # Get available flights

    if flight_choice_index < 0 or flight_choice_index >= len(available_flights):  # Check if index is valid
        return "Invalid flight selection. Please choose a valid option from the list."  # Return error message
    
    # Extract selected flight details
    selected_flight = available_flights[flight_choice_index]  # Get selected flight
    segments = selected_flight['itineraries'][0]['segments']  # Get flight segments
    carrier_code = segments[0]['carrierCode']  # Get airline code
    airline_name = amadeus.get_airline_name(carrier_code)
    departure_time = segments[0]['departure']['at']  # Get departure time
    arrival_time = segments[-1]['arrival']['at']  # Get arrival time
    usd_price = float(selected_flight['price']['total'])  # Get price in USD
    inr_price = convert_to_inr(usd_price)  # Get arrival time
    price = f"₹{inr_price}"
    
    # Save passenger details
    flight_id = generate_flight_id()  # Generate flight ID
    passenger_details = {  # Create passenger details dictionary
        "name": user_details["name"],  # Get name
        "contact": user_details["contact"],  # Get contact
        "flight_id": flight_id,  # Set flight ID
        "airline_name": airline_name,  # Set airline
        "boarding_city": get_iata_code(user_details["boarding_city"]),  # Set boarding city
        "destination_city":get_iata_code(user_details["destination_city"]),  # Set destination city
        "travel_date": user_details["travel_date"],  # Set travel date
        "departure_time": departure_time,  # Set departure time
        "arrival_time": arrival_time,  # Set arrival time
        "price": price  # Set price
    }
    save_passenger_details(passenger_details)  # Save passenger details

    # Reset task and confirm booking
    reset_task()  # Reset task

    email_subject ="Flight Booking Confirmation"
    email_body = (
            f"Flight booked successfully!\n"
            f"Flight ID: {flight_id}\n"
            f"Airline: {airline_name}\n"
            f"Departure: {departure_time}\n"
            f"Arrival: {arrival_time}\n"
            f"Price: {price}\n"
            "Thank you for booking with us!"
        )

        # Send SMS
    # if send_email(email, email_subject, email_body):
    #         return (
    #             f"Flight booked successfully! Flight ID: {flight_id}, Airline: {airline_name}, "
    #             f"Departure: {departure_time}, Arrival: {arrival_time}, Price: {price}. "
    #             "A confirmation SMS has been sent to your phone."
    #         )
    # else:
    #         return (
    #             f"Flight booked successfully! Flight ID: {flight_id}, Airline: {airline_name}, "
    #             f"Departure: {departure_time}, Arrival: {arrival_time}, Price: {price}. "
    #             "However, we were unable to send a confirmation SMS."
    #         )
        
    
def handle_fetch_flight():
    """Handles the fetch flight intent."""
    if not user_details.get("flight_id"):  # Check if flight ID is provided
        # Prompt user for flight ID if missing
        message = prompt_user("Enter your flight ID:", "flight_id")  # Prompt for flight ID
        return message  # Return prompt message

    # Get the flight details
    flight_id = user_details.get("flight_id")  # Get flight ID
    flight_info = fetch_flight(flight_id)  # Ensure fetch_flight returns plain data
    
    # Reset task state
    reset_task()  # Reset task state

    # If fetch_flight returns an error in a dictionary
    if isinstance(flight_info, dict) and "error" in flight_info:  # Check for error
        return flight_info["error"]  # Return error message

    # Format flight details for user display
    if isinstance(flight_info, dict):  # Assuming fetch_flight returns a dictionary for valid responses
        return (  # Return formatted flight details
            f"Flight Details:\n"
            f"Name: {flight_info.get('name')}\n"
            f"Contact: {flight_info.get('contact')}\n"
            f"Airline: {flight_info.get('airline_name')}\n"
            f"Boarding City: {flight_info.get('boarding_city')}\n"
            f"Destination City: {flight_info.get('destination_city')}\n"
            f"Travel Date: {flight_info.get('travel_date')}\n"
            f"Departure Time: {flight_info.get('departure_time')}\n"
            f"Arrival Time: {flight_info.get('arrival_time')}\n"
            f"Price: {flight_info.get('price')}"
        )
    
    # Default error handling
    return "Unable to fetch flight details. Please try again."  # Return error message

def handle_update_flight(user_message):
    """
    Handles the flow for updating a flight.
    Collects Flight ID, Update Type, New Details, and allows selecting updated flights.
    """
    global expected_key, user_details

    # Step 1: Collect Flight ID
    if not user_details.get("flight_id"):
        return prompt_user("Please provide your Flight ID:", "flight_id")

    # Step 2: Collect Update Type
    if not user_details.get("update_request"):
        return prompt_user(
            "What would you like to update? Options: travel date, destination city, boarding city.", 
            "update_request"
        )

    # Step 3: Collect New Details based on Update Type
    update_request = user_details.get("update_request").strip().lower()

    # Step 3: Prompt for specific update details
    if update_request in ["1", "change date", "change date of travel", "date"]:
        if not user_details.get("new_travel_date"):
            return prompt_user("Enter the new Travel Date (YYYY-MM-DD):", "new_travel_date")
    elif update_request in ["2", "change destination", "change destination city", "destination","update destination city"]:
        if not user_details.get("new_destination_city"):
            return prompt_user("Enter the new Destination City:", "new_destination_city")
    elif update_request in ["3", "change boarding city", "boarding","update boarding city"]:
        if not user_details.get("new_boarding_city"):
            return prompt_user("Enter the new Boarding City:", "new_boarding_city")


    # Step 4: Update Data
    updated_data_response = update_flight()
    if isinstance(updated_data_response, str):  # Error occurred
        reset_task()
        return updated_data_response

    # Step 5: Search for Flights
    if not user_details.get("flight_choice"):
        available_flights = search_flights_after_update(updated_data_response)
        if not available_flights:
            reset_task()
            return f"No flights available for the updated details. Please try again."

        # Store available flights and prompt for flight choice
        user_details["available_flights"] = available_flights
        expected_key = "flight_choice"
        return display_flight(
            available_flights,
            updated_data_response["boarding_city"],
            updated_data_response["destination_city"]
        )

    # Step 6: Process Flight Choice
    flight_choice = user_message.strip()
    return finalize_flight_selection(updated_data_response, flight_choice)

def handle_cancel_flight():
    """
    Handles the cancel flight intent by prompting for a flight ID
    and calling the cancel_flight function.
    """
    # Check if flight ID is provided
    if not user_details.get("flight_id"):
        return prompt_user("Enter your flight ID:", "flight_id")

    # Call the cancel_flight function
    response = cancel_flight(user_details["flight_id"])

    # Reset task state after handling the cancellation
    reset_task()
    return response
def handle_fetch_hotel_details():
    """Handles the fetch hotel booking intent."""
    
    # Step 1: Check if Booking ID is provided
    if not user_details.get("booking_id"):
        return prompt_user("Enter your hotel Booking ID:", "booking_id")  # Prompt for booking ID

    # Step 2: Fetch hotel booking details
    booking_id = user_details.get("booking_id")  # Get Booking ID
    hotel_info = fetch_hotel_details(booking_id)  # Fetch details

    # Reset task state
    reset_task()

    # Step 3: Handle errors
    if isinstance(hotel_info, dict) and "error" in hotel_info:
        return hotel_info["error"]  # Return error message

    # Step 4: Format and return hotel details
    if isinstance(hotel_info, dict):  # Ensure response is a dictionary
        return (
            f"Hotel Booking Details:\n"
            f"Name: {hotel_info.get('name')}\n"
            f"Contact: {hotel_info.get('contact')}\n"
            f"Email: {hotel_info.get('email')}\n"
            f"City: {hotel_info.get('city_name')}\n"
            f"Hotel Name: {hotel_info.get('hotel_name')}\n"
            f"Address: {hotel_info.get('address')}\n"
            f"Check-in Date: {hotel_info.get('check_in_date')}\n"
            f"Check-out Date: {hotel_info.get('check_out_date')}\n"
            f"Number of Adults: {hotel_info.get('adults')}\n"
            f"Price: {hotel_info.get('price')} {hotel_info.get('currency')}"
        )

    # Default error handling
    return "Unable to fetch hotel booking details. Please try again."


# Initialize the main application window
if __name__ == "__main__":  # Check if the script is run directly
    app.run(debug=True)  # Run the Flask application in debug mode