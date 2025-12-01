from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_analysis import analyse_prompt
from prompt_analysis import run_prompt_evaluation;
import os

app = Flask(__name__)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

CORS(app, origins=allowed_origins)

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