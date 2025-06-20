from flask import Flask, request, jsonify
import psycopg2
import os
import logging
import sys

app = Flask(__name__)

logger = logging.getLogger("db-writer")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# PostgreSQL connection config — hardcoded for simplicity
DB_CONFIG = {
    "host": "10.0.0.220",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_connection():
    logger.info("Connecting to database...")
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

@app.route('/write', methods=['POST'])
def write_data():
    data = request.get_json()
    if not data or 'value' not in data:
        logger.error("JSON with key - value - required")
        return jsonify({"error": "JSON with key 'value' required"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO sensor_data (value) VALUES (%s);", (data['value'],))
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Data written to database")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error writing to database - {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)