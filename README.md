# 🌾 KrishiRakshak AI

**An intelligent farming assistant that brings AI-powered crop disease diagnosis, weather forecasting, and voice-enabled agricultural guidance to your fingertips.**

---

## 🎯 Overview

**KrishiRakshak AI** is a full-stack web application designed to assist farmers with:
- Real-time crop disease and deficiency detection using image analysis
- AI-powered farming advice through chat and voice interfaces
- Live weather forecasts for informed agricultural planning
- Intuitive, farmer-friendly UI with minimal technical overhead

This project was built to bridge the gap between modern AI technology and rural farming communities, making agricultural expertise accessible and actionable.

---

## ✨ Features

### 🖼️ Crop Disease Detection
- Upload crop images for instant AI-powered diagnosis
- Identifies diseases, nutrient deficiencies, and pest damage
- Provides remediation recommendations

### 💬 Chat Assistant
- Natural language queries about farming practices
- Answers on crop selection, fertilization, irrigation, and pest management
- Context-aware responses from Gemini AI

### 🎤 Voice Assistant
- Speak farming questions directly into the app
- Browser-based speech recognition (Chrome, Edge, etc.)
- Results read aloud for hands-free operation

### 🌦️ Weather Integration
- Real-time weather data by city
- Helps farmers plan planting and harvesting activities
- Supports multiple locations

### 📱 Responsive UI
- Mobile-first design
- Works on desktops, tablets, and smartphones
- Clean, accessible interface

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python, Flask |
| **AI/LLM** | Google Gemini API |
| **Weather API** | OpenWeatherMap|
| **Upload Storage** | Local filesystem |

---

## 📁 Project Structure

```
KrishiRakshakAI/
├── app.py                 # Flask main application
├── routes.py              # API and route definitions
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── utils/
│   ├── __init__.py
│   ├── gemini_service.py  # AI service integration
│   └── weather_service.py # Weather API client
├── templates/             # HTML templates
│   ├── index.html         # Homepage
│   ├── chat.html          # Chat interface
│   ├── voice.html         # Voice assistant
│   ├── detect.html        # Image upload for crop analysis
│   └── weather.html       # Weather lookup
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   ├── js/
│   │   └── script.js      # Frontend logic & AJAX
│   └── uploads/           # User-uploaded images
└── uploads/               # Persistent storage for uploads
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda
- API keys are optional for initial deploy:
  - Google Gemini API (optional; app runs in demo fallback mode without it)
  - OpenWeatherMap API (optional; weather uses demo data without it)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<shradhaa-singh>/KrishiRakshakAI.git
   cd KrishiRakshakAI
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy `.env.example` to `.env` and update values as needed:
   ```bash
   cp .env.example .env
   ```

   `.env` example:
   ```
   FLASK_APP=app.py
   FLASK_ENV=production
   GEMINI_API_KEY=<your-gemini-api-key>
   WEATHER_API_KEY=<your-weather-api-key>
   FLASK_SECRET_KEY=<your-secret-key>
   UPLOAD_FOLDER=uploads
   MAX_CONTENT_LENGTH=8388608
   ```
   If `GEMINI_API_KEY` or `WEATHER_API_KEY` is empty, the app still works in demo mode.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---


## 📖 Usage Guide

### Chat Interface
1. Navigate to **Chat** from the homepage
2. Type your farming question
3. Get instant AI-powered advice
4. Continue the conversation as needed

### Voice Assistant
1. Navigate to **Voice** from the homepage
2. Grant microphone permission when prompted
3. Click **Start Voice** and speak your question
4. Wait for the transcript and AI response
5. Listen to the answer (if audio is enabled)

**Note:** Voice features require:
- HTTPS connection (localhost works for development)
- Supported browser (Chrome)
- Microphone access

### Crop Detection
1. Navigate to **Detect** from the homepage
2. Upload a clear image of affected crop
3. Receive diagnosis with:
   - Disease/deficiency identification
   - Severity assessment
   - Recommended treatments

### Weather Check
1. Navigate to **Weather** from the homepage
2. Enter city name
3. View current conditions and forecast
4. Plan farming activities accordingly

---

## 🐛 Troubleshooting

### Voice Not Working
**Problem:** "Voice input is not supported in this browser"

**Solutions:**
- Use Chrome, Edge, or Safari (14.1+) on desktop
- Ensure HTTPS (production) or localhost (development)
- Check browser console for errors
- Verify microphone permissions granted


### Chat API Not Responding
**Problem:** 500 error from `/api/chat`

**Solutions:**
- If no key is configured, response should still work in demo mode
- If key is configured, verify quota and connectivity
- Review Flask logs for detailed error


### Image Upload Failing
**Problem:** 400 error or image not saved

**Solutions:**
- Ensure `uploads/` directory exists and is writable
- Check file size doesn't exceed `MAX_CONTENT_LENGTH` (default 16MB)
- Verify image format is JPG or PNG

---

### Weather API Issues
**Problem:** City not found or 500 error

**Solutions:**
- If no key is configured, app returns demo weather safely
- If key is configured, verify key, city spelling, and quota
- Fall back to popular city names (Delhi, Mumbai, Bangalore)

---

## 🌟 Future Enhancements

- [ ] **User Authentication** – Save chat history and preferences
- [ ] **Multi-language Support** – Hindi, Tamil, Telugu, etc.
- [ ] **Mobile App** – Native iOS/Android version
- [ ] **Real-time Notifications** – Weather alerts, pest warnings
- [ ] **Community Forum** – Farmer-to-farmer knowledge sharing
- [ ] **Advanced Analytics** – Crop yield predictions
- [ ] **Offline Mode** – Limited functionality without internet
- [ ] **Integration with IoT Sensors** – Real-time field data
- [ ] **Video Tutorial Library** – How-to guides for common issues

---

## 🙏 Acknowledgments

- Built with ❤️ for farmers
- Powered by Google Gemini AI
- Weather data from OpenWeatherMap
- Inspired by agricultural innovation

---

**Last Updated:** April 9, 2026  
**Version:** 1.0.0
