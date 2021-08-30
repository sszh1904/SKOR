from flask import Flask, request, jsonify
from flask_cors import CORS 
from emailHandling import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

CONTACT_SKOR_PORT = os.getenv("CONTACT_SKOR_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


# Report Issue/Bug
@app.route("/reportIssue", methods=['POST']) 
def reportIssue():
    if request.is_json:
        issueDetails = request.get_json()

        userName = issueDetails['userName']
        userEmail = issueDetails['userEmail']
        issueMessage = issueDetails['issueMessage']

        host_email = sendIssueReportEmail(REPORT_ISSUE_EMAIL_SUBJECT, userName, userEmail, issueMessage)

        return jsonify(
            {
                "code":200,
                "message": f"Issue has been reported and successfully sent to {host_email}"
            }
        ), 200
    return jsonify(
        {
            "code": 500,
            "message": 'Input is not JSON.'
        }
    ), 500

# Contact Us
@app.route("/contactUs", methods=['POST']) 
def contactUs():
    if request.is_json:
        emailDetails = request.get_json()

        userName = emailDetails['contactName']
        userEmail = emailDetails['contactEmail']
        subject = emailDetails['subject']
        message = emailDetails['message']

        host_email = sendContactUsEmail(subject, userName, userEmail, message)

        return jsonify(
            {
                "code":200,
                "message": f"Contact Us email successfully sent to {host_email}"
            }
        ), 200
    return jsonify(
        {
            "code": 500,
            "message": 'Input is not JSON.'
        }
    ), 500


if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=CONTACT_SKOR_PORT)
    else:
        app.run(host='0.0.0.0', port=CONTACT_SKOR_PORT)