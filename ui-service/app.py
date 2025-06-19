from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "10.0.0.220",
    "port": "5432",
    "dbname": "postgres",
    "user": "postgres",
    "password": "root"
}

def get_total_sum():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cur = conn.cursor()
        cur.execute("SELECT SUM(value) FROM sensor_data;")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result if result is not None else 0
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def index():
    total = get_total_sum()
    return render_template("index.html", total=total)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)