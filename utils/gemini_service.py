import json
import mimetypes
import os

import google.generativeai as genai


def _fallback_response() -> dict:
    """Safe fallback response when API key is missing or API fails."""
    return {
        "disease_name": "Likely Fungal Leaf Spot (Preliminary)",
        "causes": [
            "High moisture and poor air circulation around leaves.",
            "Contaminated soil or infected plant residue in the field.",
        ],
        "treatment": [
            "Remove and destroy heavily infected leaves.",
            "Use a suitable fungicide recommended by local agriculture experts.",
            "Avoid overhead irrigation during late evening.",
        ],
        "preventive_measures": [
            "Maintain proper spacing between plants.",
            "Rotate crops and keep field hygiene strong.",
            "Inspect crops early in the morning for first signs of infection.",
        ],
        "note": "This is a fallback advisory. Add GEMINI_API_KEY in .env for real AI image diagnosis.",
    }


def _get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def analyze_crop_image(image_path: str) -> dict:
    """
    Analyze crop image using Gemini and return structured, farmer-friendly output.
    Falls back to a static structured result if key/config is unavailable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback_response()

    model = _get_model(api_key)

    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    prompt = (
        "You are an expert agricultural diagnostician helping farmers. "
        "Analyze this crop image and return JSON only with keys: "
        "disease_name (string), causes (array of strings), treatment (array of strings), "
        "preventive_measures (array of strings). "
        "Keep language simple and practical for Indian farmers."
    )

    try:
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": mime_type,
                    "data": image_data,
                },
            ]
        )
        text = (response.text or "").strip()

        cleaned = text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)
        required = {"disease_name", "causes", "treatment", "preventive_measures"}
        if not required.issubset(parsed.keys()):
            raise ValueError("Gemini response missing expected keys.")
        return parsed
    except Exception as e:
        print(f"[DEBUG] Image Analysis Error: {str(e)}")
        return _fallback_response()


def ask_farming_question(message: str) -> str:
    """
    Chat helper for farmer Q&A.
    Falls back to safe static text when API key is unavailable or API fails.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "I am in demo mode. For healthy crops, monitor leaves daily, irrigate early "
            "morning, and remove infected parts quickly. Add GEMINI_API_KEY for live AI answers."
        )

    try:
        model = _get_model(api_key)
        prompt = (
            "You are KrishiRakshak AI, a practical farming assistant. "
            "Respond in simple, short, actionable language for farmers in India. "
            f"User question: {message}"
        )
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        return text or "I could not generate a response. Please try again."
    except Exception as e:
        print(f"[DEBUG] Gemini API Error: {str(e)}")
        return (
            "Unable to connect to AI right now. Please try again in a moment. "
            "Meanwhile, inspect crop leaves and soil moisture before applying treatment."
        )
