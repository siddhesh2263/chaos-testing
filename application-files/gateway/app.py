from flask import Flask, request, jsonify
import requests
import logging
import sys

app = Flask(__name__)

# Set up logging
logger = logging.getLogger("gateway")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Internal address of the database writer service
DB_WRITER_URL = "http://db-writer-service:5000/write"

@app.route('/ingest', methods=['POST'])
def ingest():
    logger.info("Received /ingest request")
    data = request.get_json()

    if not data:
        logger.warning("No JSON received in /ingest")
        return jsonify({"error": "No JSON received"}), 400

    try:
        logger.info(f"Forwarding data to DB Writer: {data}")
        response = requests.post(DB_WRITER_URL, json=data)
        logger.info(f"DB Writer responded with {response.status_code}")

        return jsonify({"status": "forwarded", "response": response.json()}), response.status_code
    
    except Exception as e:
        logger.error(f"Error forwarding to DB Writer: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ui')
def ui_proxy():
    logger.info("Received /ui proxy request")

    try:
        ui_response = requests.get("http://ui-service:5002/")
        logger.info("UI Service responded successfully")
        return ui_response.content, ui_response.status_code
    
    except Exception as e:
        logger.error(f"UI Service unavailable: {e}")
        return f"UI Service unavailable: {e}", 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)