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

@
    })

if __name__ == "__main__":
    app.run(debug=True)
