# app.py
import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from llm_analysis import analyse_prompt
from prompt_analysis import run_prompt_evaluation

app = Flask(__name__)

# -----------------------
# CORS / Allowed origins
# -----------------------
# Example env value:
# ALLOWED_ORIGINS="http://127.0.0.1:5173,https://prompt-optimiser-client.vercel.app"
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5173")
ALLOWED_ORIGINS = [o.strip() for o in allowed_origins_raw.split(",") if o.strip()]

# Print allowed origins into logs so you can verify Render picked them up
print("ALLOWED_ORIGINS =", ALLOWED_ORIGINS)

# Apply flask-cors (standard behavior)
CORS(
    app,
    origins=ALLOWED_ORIGINS,
    supports_credentials=False,  # set True only if you use cookies/auth across origins
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
    expose_headers=["Content-Type"],
    methods=["GET", "POST", "OPTIONS"],
)

# Log incoming origin and request details for debugging (appears in Render logs)
@app.before_request
def _log_request_origin():
    origin = request.headers.get("Origin")
    print(f"Incoming request: path={request.path}, method={request.method}, Origin={origin}")

# Explicitly handle OPTIONS preflight for any path (defensive)
@app.route("/", methods=["OPTIONS"])
@app.route("/<path:any_path>", methods=["OPTIONS"])
def _catch_all_options(any_path=None):
    origin = request.headers.get("Origin", "")
    resp = make_response("", 204)
    if origin and origin in ALLOWED_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin"
        # If you use credentials (cookies/auth), set to "true" and set supports_credentials=True above
        resp.headers["Access-Control-Allow-Credentials"] = "false"
    return resp

# Ensure actual responses include CORS headers when origin is allowed
@app.after_request
def _add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin and origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin"
        response.headers["Access-Control-Allow-Credentials"] = "false"
    return response

# -----------------------
# Routes
# -----------------------
@app.route("/analyse_prompt", methods=["POST"])
def analyse_prompt_route():
    data = request.get_json() or {}
    user_prompt = data.get("prompt", "")

    try:
        analysis = analyse_prompt(user_prompt)
        return jsonify(analysis), 200
    except Exception as e:
        print("Error in /analyse_prompt:", e)
        return jsonify({"error": "Failed to analyze prompt"}), 500


@app.route("/quick_analyse_prompt", methods=["POST"])
def quick_analyse_prompt():
    data = request.get_json() or {}
    user_prompt = data.get("prompt", "")

    try:
        result = run_prompt_evaluation(user_prompt)
        return jsonify(result), 200
    except Exception as e:
        print("Error in /quick_analyse_prompt:", e)
        return jsonify({"error": "Failed to analyze prompt"}), 500


# -----------------------
# Dev entrypoint
# -----------------------
if __name__ == "__main__":
    # For production on Render use:
    #   gunicorn app:app --bind 0.0.0.0:$PORT
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
