from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

USERS = []
GROUPS = {}
QUIZ_BANK = {
    "quiz1": [
        {"question": "Capital of Kenya?", "options": ["Nairobi", "Mombasa", "Kisumu", "Eldoret"], "e submitted"})

@app.route("/results", methods=["GET"])
def results():
    username = request.args.get("username")
    user = next((u for u in USERS if u["username"] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "username": user["username"],
        "group": user["group"],
        "score": user["score"],
        "prize": user.get("prize", 0)
    })

if __name__ == "__main__":
    app.run(debug=True)
