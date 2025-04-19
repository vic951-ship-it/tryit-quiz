from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

USERS = []
GROUPS = {}
QUIZ_BANK = {
    "quiz1": [
        {"question": "Capital of Kenya?", "options": ["Nairobi", "Mombasa", "Kisumu", "Eldoret"], "answer": "Nairobi"},
        {"question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"}
    ]
}
GROUP_SIZE = 10

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    user_id = str(uuid.uuid4())
    new_user = {"id": user_id, "username": username, "paid": True, "contribution": 0, "group": None, "score": 0}
    USERS.append(new_user)

    ungrouped = [u for u in USERS if u["group"] is None]
    if len(ungrouped) >= GROUP_SIZE:
        group_id = str(uuid.uuid4())
        for i in range(GROUP_SIZE):
            ungrouped[i]["group"] = group_id
        GROUPS[group_id] = {"members": [u["id"] for u in ungrouped[:GROUP_SIZE]], "quiz_id": "quiz1", "completed": False}
    
    return jsonify({"message": "Registered"})

@app.route("/pay", methods=["POST"])
def pay():
    username = request.json.get("username")
    for u in USERS:
        if u["username"] == username:
            u["contribution"] += 2
            return jsonify({"message": "Payment OK"})
    return jsonify({"error": "User not found"}), 404

@app.route("/quiz", methods=["GET"])
def quiz():
    # Just return the quiz for anyone who has registered
    quiz_id = "quiz1"
    return jsonify(QUIZ_BANK[quiz_id])

@app.route("/submit", methods=["POST"])
def submit():
    username = request.json["username"]
    score = request.json["score"]

    user = next((u for u in USERS if u["username"] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["score"] = score
    group_id = user["group"]
    group_users = [u for u in USERS if u["group"] == group_id]

    if all(u["score"] > 0 for u in group_users):
        group_users.sort(key=lambda x: x["score"], reverse=True)
        for winner in group_users[:2]:
            winner["prize"] = 8.5
        GROUPS[group_id]["completed"] = True

    return jsonify({"message": "Score submitted"})

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