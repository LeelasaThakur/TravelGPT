/* =========================================================
   HORIZON — Chat Engine
   Fully connected to Flask /send_message endpoint
   ========================================================= */

   (function () {
    "use strict";
  
    // ── DOM refs ──────────────────────────────────────────────
    const viewport    = document.getElementById("messagesViewport");
    const input       = document.getElementById("userInput");
    const sendBtn     = document.getElementById("sendBtn");
    const typingRow   = document.getElementById("typingRow");
    const clearBtn    = document.getElementById("clearBtn");
    const bgImage     = document.getElementById("bgImage");
    const statusDot   = document.getElementById("statusDot");
  
    // Left panel
    const tripDest    = document.getElementById("tripDestination");
    const tripDates   = document.getElementById("tripDates");
    const tripGuests  = document.getElementById("tripGuests");
    const progressFill= document.getElementById("progressFill");
    const progressPct = document.getElementById("progressPct");
    const itinCard    = document.getElementById("itineraryCard");
    const itinText    = document.getElementById("itineraryText");
  
    // Right panel
    const statFlights  = document.getElementById("statFlights");
    const statHotels   = document.getElementById("statHotels");
    const spotlightImg = document.getElementById("spotlightImg");
    const spotlightCity= document.getElementById("spotlightCity");
    const spotlightDesc= document.getElementById("spotlightDesc");
  
    // ── Session state ─────────────────────────────────────────
    let flightCount  = 0;
    let hotelCount   = 0;
    let planProgress = 0;
  
    // City spotlight info
    const CITY_INFO = {
      paris:      { desc: "City of Light · Culture · Cuisine",      img: "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=800" },
      london:     { desc: "Royal Heritage · Pubs · Thames",          img: "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800" },
      "new york": { desc: "The City That Never Sleeps",              img: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800" },
      tokyo:      { desc: "Neon · Tradition · Street Food",         img: "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?auto=format&fit=crop&w=800" },
      rome:       { desc: "Eternal City · History · Gelato",         img: "https://images.unsplash.com/photo-1525874684015-58379d421a52?auto=format&fit=crop&w=800" },
      dubai:      { desc: "Luxury · Desert · Architecture",          img: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800" },
      singapore:  { desc: "Garden City · Food · Modernity",          img: "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=800" },
      sydney:     { desc: "Harbour · Beaches · Sun",                 img: "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800" },
      mumbai:     { desc: "City of Dreams · Bollywood · Monsoons",   img: "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?auto=format&fit=crop&w=800" },
      delhi:      { desc: "Capital · History · Street Food",         img: "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800" },
      bali:       { desc: "Temples · Rice Fields · Ocean",           img: "https://images.unsplash.com/photo-1520642417671-ae7c03741aa2?auto=format&fit=crop&w=800" },
      goa:        { desc: "Beaches · Shacks · Sunsets",              img: "https://images.unsplash.com/photo-1559373443-1559b874f695?auto=format&fit=crop&w=800" },
      barcelona:  { desc: "Gaudí · Tapas · Sea · Nightlife",         img: "https://images.unsplash.com/photo-1543349689-9dd27f3d5420?auto=format&fit=crop&w=800" },
      amsterdam:  { desc: "Canals · Tulips · Culture",               img: "https://images.unsplash.com/photo-1512608851468-95f527ab3a2e?auto=format&fit=crop&w=800" },
      istanbul:   { desc: "East Meets West · Spice · History",       img: "https://images.unsplash.com/photo-1546412414-e19569947c87?auto=format&fit=crop&w=800" },
      agra:       { desc: "Taj Mahal · Mughal Heritage",             img: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800" },
      jaipur:     { desc: "Pink City · Palaces · Desert",            img: "https://images.unsplash.com/photo-1564507592333-7b47d82c6a6b?auto=format&fit=crop&w=800" },
      udaipur:    { desc: "City of Lakes · Royal Elegance",          img: "https://images.unsplash.com/photo-1600266611634-7b3ccff5245b?auto=format&fit=crop&w=800" },
    };
  
    // ── Utilities ─────────────────────────────────────────────
  
    function escapeHtml(str) {
      const d = document.createElement("div");
      d.appendChild(document.createTextNode(str));
      return d.innerHTML;
    }
  
    function now() {
      return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }
  
    function scrollToBottom(smooth = true) {
      viewport.scrollTo({ top: viewport.scrollHeight, behavior: smooth ? "smooth" : "instant" });
    }
  
    // ── Message rendering ─────────────────────────────────────
  
    function appendMessage(text, role) {
      const isUser  = role === "user";
      const row     = document.createElement("div");
      row.className = `msg-row ${isUser ? "user" : "bot"}`;
  
      const avatarIcon = isUser ? "fa-user" : "fa-wand-magic-sparkles";
      const bubbleCls  = isUser ? "bubble-user" : "bubble-bot";
  
      row.innerHTML = `
        <div class="avatar avatar-${isUser ? "user" : "bot"}">
          <i class="fa-solid ${avatarIcon}"></i>
        </div>
        <div>
          <div class="bubble ${bubbleCls}">${escapeHtml(text)}</div>
          <div class="bubble-time">${now()}</div>
        </div>`;
  
      viewport.appendChild(row);
      scrollToBottom();
      return row;
    }
  
    function showWelcome() {
      const card = document.createElement("div");
      card.className = "welcome-card";
      card.innerHTML = `
        <div class="welcome-title">Where to next?</div>
        <div class="welcome-sub">
          I'm your AI travel concierge — ready to book flights, find hotels,
          plan itineraries, and manage your bookings.
        </div>
        <div class="welcome-tags">
          <span class="welcome-tag">✦ Flights</span>
          <span class="welcome-tag">✦ Hotels</span>
          <span class="welcome-tag">✦ Itineraries</span>
          <span class="welcome-tag">✦ Bookings</span>
        </div>`;
      viewport.appendChild(card);
    }
  
    // ── Typing indicator ──────────────────────────────────────
  
    function showTyping() {
      typingRow.style.display = "flex";
      // Append typing row at end of viewport (not inside viewport, it's outside)
      scrollToBottom();
    }
    function hideTyping() { typingRow.style.display = "none"; }
  
    // ── Background & spotlight update ─────────────────────────
  
    function updateDestinationUI(city, backgroundUrl) {
      if (!city) return;
      const key  = city.toLowerCase().trim();
      const info = CITY_INFO[key] || { desc: "A wonderful destination", img: null };
  
      // Left panel trip card
      tripDest.textContent = city.charAt(0).toUpperCase() + city.slice(1);
      spotlightCity.textContent = city.charAt(0).toUpperCase() + city.slice(1);
      spotlightDesc.textContent = info.desc;
  
      // Spotlight image
      const imgUrl = info.img || backgroundUrl;
      if (imgUrl) {
        spotlightImg.style.backgroundImage = `url('${imgUrl}')`;
      }
  
      // Full background
      if (backgroundUrl) {
        bgImage.style.backgroundImage = `url('${backgroundUrl}')`;
        bgImage.classList.add("visible");
      }
  
      // Advance progress
      updateProgress(Math.min(planProgress + 25, 75));
    }
  
    function updateProgress(pct) {
      planProgress = pct;
      progressFill.style.width = pct + "%";
      progressPct.textContent  = pct + "%";
    }
  
    // ── Itinerary ─────────────────────────────────────────────
  
    function showItinerary(text) {
      if (!text) return;
      itinCard.style.display = "block";
      itinText.textContent   = text;
      updateProgress(Math.min(planProgress + 25, 100));
    }
  
    // ── Detect city from messages ─────────────────────────────
  
    function extractDestinationFromMsg(msg) {
      // Look for "to <City>" or "in <City>" or "for <City>"
      const m = msg.match(/(?:to|in|for|visit|going to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)/);
      return m ? m[1] : null;
    }
  
    function extractDatesFromMsg(msg) {
      // YYYY-MM-DD
      const iso = msg.match(/\d{4}-\d{2}-\d{2}/g);
      if (iso) return iso.join(" → ");
      // "June 15" style
      const nat = msg.match(/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}/gi);
      if (nat) return nat.join(" → ");
      return null;
    }
  
    // ── Detect booking confirmations ──────────────────────────
  
    function detectBookingType(responseText) {
      const t = responseText.toLowerCase();
      if (t.includes("flight booked successfully") || t.includes("flight id :")) return "flight";
      if (t.includes("hotel booked successfully") || t.includes("booking id :")) return "hotel";
      return null;
    }
  
    function detectGuestsFromMsg(msg) {
      const m = msg.match(/(\d+)\s*(?:adults?|guests?|people|persons?)/i);
      return m ? `${m[1]} adult${m[1] > 1 ? "s" : ""}` : null;
    }
  
    // ── Core send ─────────────────────────────────────────────
  
    async function sendMessage(messageOverride) {
      const text = (messageOverride || input.value).trim();
      if (!text) return;
  
      input.value = "";
      sendBtn.disabled = true;
  
      appendMessage(text, "user");
      showTyping();
  
      // Update dates from user message
      const dates = extractDatesFromMsg(text);
      if (dates) tripDates.textContent = dates;
  
      const guests = detectGuestsFromMsg(text);
      if (guests) tripGuests.textContent = guests;
  
      try {
        const res = await fetch("/send_message", {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          body:    JSON.stringify({ message: text }),
        });
  
        hideTyping();
        sendBtn.disabled = false;
  
        if (!res.ok) {
          appendMessage(`Server error (${res.status}). Please try again.`, "bot");
          return;
        }
  
        const data = await res.json();
  
        if (data.error) {
          appendMessage(`⚠️ ${data.error}`, "bot");
          return;
        }
  
        // Append bot reply
        appendMessage(data.response || "I'm not sure how to respond to that.", "bot");
  
        // Update UI from response
        if (data.background_url || data.itinerary) {
          // Try to detect destination from bot response or user message
          const dest = extractDestinationFromMsg(text) ||
                       extractDestinationFromMsg(data.response || "");
          updateDestinationUI(dest, data.background_url);
        }
  
        if (data.itinerary) {
          showItinerary(data.itinerary);
        }
  
        // Count bookings
        const bookingType = detectBookingType(data.response || "");
        if (bookingType === "flight") {
          flightCount++;
          statFlights.textContent = flightCount;
          updateProgress(100);
        } else if (bookingType === "hotel") {
          hotelCount++;
          statHotels.textContent = hotelCount;
          updateProgress(100);
        }
  
      } catch (err) {
        hideTyping();
        sendBtn.disabled = false;
        appendMessage(`Network error: ${err.message}`, "bot");
      }
    }
  
    // ── Clear ─────────────────────────────────────────────────
  
    function clearConversation() {
      viewport.innerHTML = "";
      showWelcome();
  
      // Reset state
      flightCount  = 0;
      hotelCount   = 0;
      planProgress = 0;
      statFlights.textContent  = "0";
      statHotels.textContent   = "0";
      tripDest.textContent     = "Undecided";
      tripDates.textContent    = "Dates TBD";
      tripGuests.textContent   = "—";
      progressFill.style.width = "0%";
      progressPct.textContent  = "0%";
      itinCard.style.display   = "none";
      itinText.textContent     = "";
      bgImage.classList.remove("visible");
  
      // Notify backend to reset session
      fetch("/send_message", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ message: "__reset__" }),
      }).catch(() => {});
    }
  
    // ── Destination chip click ────────────────────────────────
  
    function handleDestChip(city) {
      // Update spotlight immediately for visual feedback
      const key  = city.toLowerCase();
      const info = CITY_INFO[key];
      spotlightCity.textContent = city;
      if (info) {
        spotlightDesc.textContent = info.desc;
        spotlightImg.style.backgroundImage = `url('${info.img}')`;
      }
      // Then send as a message
      sendMessage(`Tell me about ${city} as a travel destination`);
    }
  
    // ── Event wiring ──────────────────────────────────────────
  
    sendBtn.addEventListener("click", () => sendMessage());
  
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  
    clearBtn.addEventListener("click", clearConversation);
  
    // Quick chip buttons
    document.querySelectorAll(".chip[data-msg]").forEach((btn) => {
      btn.addEventListener("click", () => sendMessage(btn.dataset.msg));
    });
  
    // Destination chips (right panel)
    document.querySelectorAll(".dest-chip[data-city]").forEach((btn) => {
      btn.addEventListener("click", () => handleDestChip(btn.dataset.city));
    });
  
    // ── Init ──────────────────────────────────────────────────
  
    showWelcome();
    input.focus();
  
  })();