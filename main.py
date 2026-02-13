from flask import Flask, request, jsonify, send_from_directory
import os

from handlers.candidates_handler import Finder


app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")



def classify_job(job_description: str) -> dict:
    """
    Stub: replace the body of this function with your actual service call.
    It should return a dict with 'top_job_codes' and 'reasoning'.
    """
    finder = Finder(job_description)

    return finder.get_top_5_candidates()



@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    job_description = data.get("job_description", "")
    if not job_description:
        return jsonify({"error": "job_description is required"}), 400

    result = classify_job(job_description)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)