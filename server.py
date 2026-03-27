import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from database import get_contacts, init_db, save_contact


app = Flask(__name__)
CORS(app)
ROOT_DIR = Path(__file__).resolve().parent.parent
init_db()


@app.get("/")
def serve_home():
    return send_from_directory(ROOT_DIR, "index.html.html")


@app.get("/admin")
@app.get("/admin.html")
def serve_admin():
    return send_from_directory(ROOT_DIR, "admin.html")


@app.get("/script.js")
def serve_script():
    return send_from_directory(ROOT_DIR, "script.js")


@app.get("/style.css")
def serve_style():
    return send_from_directory(ROOT_DIR, "style.css")


@app.get("/public/<path:filename>")
def serve_public_file(filename: str):
    return send_from_directory(ROOT_DIR / "public", filename)


@app.get("/health")
def health_check():
    return jsonify({"message": "Backend is running"})


@app.post("/contact")
@app.post("/api/contact")
def handle_contact():
    payload = request.get_json(silent=True) or {}

    required_fields = ["name", "email", "message"]
    missing = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing:
        return (
            jsonify({"message": f"Missing required fields: {', '.join(missing)}"}),
            400,
        )

    contact_id = save_contact(
        {
            "name": payload["name"].strip(),
            "email": payload["email"].strip(),
            "message": payload["message"].strip(),
        }
    )
    return jsonify({"message": "Message sent successfully!", "id": contact_id}), 201


@app.get("/admin/messages")
@app.get("/api/admin/messages")
def list_messages():
    return jsonify({"messages": get_contacts()})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
