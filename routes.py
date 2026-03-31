import os
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, render_template, request
from werkzeug.utils import secure_filename

from utils.gemini_service import analyze_crop_image, ask_farming_question
from utils.weather_service import fetch_weather_data

main_bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main_bp.route("/detect", methods=["GET"])
def detect_page():
    return render_template("detect.html")


@main_bp.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chat.html")


@main_bp.route("/weather", methods=["GET"])
def weather_page():
    return render_template("weather.html")


@main_bp.route("/voice", methods=["GET"])
def voice_page():
    return render_template("voice.html")


@main_bp.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze uploaded crop image using Gemini."""
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided."}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"success": False, "error": "Please choose an image file."}), 400

    if not is_allowed_file(image.filename):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unsupported file format. Please upload PNG/JPG/JPEG/WEBP.",
                }
            ),
            400,
        )

    try:
        extension = image.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(f"{uuid4().hex}.{extension}")
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        image.save(file_path)

        diagnosis = analyze_crop_image(file_path)

        return jsonify({"success": True, "data": diagnosis}), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unable to analyze image right now. Please try again.",
                    "details": str(exc),
                }
            ),
            500,
        )


@main_bp.route("/api/chat", methods=["POST"])
def chat():
    """Answer farmer text query through Gemini with fallback."""
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"success": False, "error": "Message is required."}), 400

    try:
        answer = ask_farming_question(message)
        return jsonify({"success": True, "data": {"answer": answer}}), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unable to answer right now. Please try again.",
                    "details": str(exc),
                }
            ),
            500,
        )


@main_bp.route("/api/voice", methods=["POST"])
def voice():
    """Voice assistant endpoint (accepts text transcript)."""
    payload = request.get_json(silent=True) or {}
    transcript = (payload.get("transcript") or "").strip()
    if not transcript:
        return jsonify({"success": False, "error": "Transcript is required."}), 400

    try:
        answer = ask_farming_question(transcript)
        return jsonify({"success": True, "data": {"answer": answer}}), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unable to process voice query right now.",
                    "details": str(exc),
                }
            ),
            500,
        )


@main_bp.route("/api/weather", methods=["GET"])
def weather():
    """Get weather data and farming suggestions."""
    city = request.args.get("city", "Delhi").strip()
    if not city:
        return jsonify({"success": False, "error": "City is required."}), 400

    try:
        weather_info = fetch_weather_data(city)
        return jsonify({"success": True, "data": weather_info}), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Unable to fetch weather right now. Please try again.",
                    "details": str(exc),
                }
            ),
            500,
        )
