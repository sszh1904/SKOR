from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)

TEST_PORT = os.getenv("TEST_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route('/<path:path>')
def send_path(path):
    return send_from_directory("templates", path)

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=TEST_PORT)
    else:
        app.run(host='0.0.0.0', port=TEST_PORT)
    