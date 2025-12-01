from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_analysis import analyse_prompt
from prompt_analysis import run_prompt_evaluation;
import os

app = Flask(__name__)
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [o.strip() for o in allowed_origins_raw.split(",") if o.strip()]

CORS(
    app,
    origins=allowed_origins,
    supports_credentials=False,                     # set False if you don't use cookies/auth
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
    expose_headers=["Content-Type"],
    methods=["GET", "POST", "OPTIONS"]
)

@app.route("/analyse_prompt", methods=["POST"])
def analyse_prompt_route():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    try:
        analysis = analyse_prompt(user_prompt)
        return jsonify(analysis), 200
    except Exception as e:
        print("Error in /analyse_prompt:", e)
        return jsonify({"error": "Failed to analyze prompt"}), 500


@app.route("/quick_analyse_prompt", methods=["POST"])
def quick_analyse_prompt():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    try:
        result = run_prompt_evaluation(user_prompt)
        return jsonify(result), 200
    except Exception as e:
        print("Error in /analyse_prompt:", e)
        return jsonify({"error": "Failed to analyze prompt"}), 500



if __name__ == "__main__":
    app.run(debug=True)
