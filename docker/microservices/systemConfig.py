from flask import request, jsonify
from models import app, db, SkorEmail, Configuration
import os
from dotenv import load_dotenv
load_dotenv()

SYSTEM_CONFIG_PORT = os.getenv("SYSTEM_CONFIG_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


##<!-------------- SKOR EMAIL --------------!>##

# Add a SkorEmail
@app.route("/addSkorEmail", methods=['POST'])
def addSkorEmail():
    if request.is_json:
        emailDetails = request.get_json()

        skorEmail = SkorEmail(
            email = emailDetails['email'],
            password = emailDetails['password'],
            domain = emailDetails['domain']
        )

        try:
            db.session.add(skorEmail)
            db.session.commit()
            print("SkorEmail created")

            return jsonify(
                {
                    "code": 200,
                    "data": skorEmail.json()
                }                
            ), 200
                
        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": skorEmail.json(),
                    "message": "An error occurred when creating the new skorEmail."
                }
            ), 500
        
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

# Get a SkorEmail
@app.route("/getSkorEmail/<string:email>")
def getSkorEmail(email):
    skorEmail = SkorEmail.query.get(email)
    
    if skorEmail:
        return jsonify(
            {
                "code": 200,
                "data": skorEmail.json(),
                "message": "SkorEmail retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "SkorEmail not found."
        }
    ), 404

# Get selected SkorEmail
@app.route("/getSelectedSkorEmail")
def getSelectedSkorEmail():
    selectedEmail = SkorEmail.query.filter(SkorEmail.selected == 1).first()
    
    if selectedEmail:
        return jsonify(
            {
                "code": 200,
                "data": selectedEmail.json(),
                "message": "Selected skorEmail retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "SkorEmail not found."
        }
    ), 404

# Get all SkorEmail
@app.route("/getAllSkorEmail")
def getAllSkorEmail():
    skorEmailList = SkorEmail.query.all()

    if len(skorEmailList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skorEmailList": [email.json() for email in skorEmailList]
                },
                "message": "All skorEmails retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No skorEmail found."
        }
    ), 404

# Update selected SkorEmail
@app.route("/updateSkorEmailSelected/<string:email>", methods=['PUT'])
def updateSkorEmailSelected(email):
    selectedEmail = SkorEmail.query.get(email)

    if selectedEmail:
        previousSelected = SkorEmail.query.filter(SkorEmail.selected == 1).first()
        if previousSelected:
            previousSelected.selected = 0
        
        try:
            selectedEmail.selected = 1
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": selectedEmail.json(),
                    "message": "Skor selected email updated."
                }
            ), 200
                
        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": selectedEmail.json(),
                    "message": "An error occurred when updating the skor email selection."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "SkorEmail not found."
            }
        ), 404

# Delete SkorEmail
@app.route("/deleteSkorEmail/<string:email>", methods=['DELETE'])
def deleteSkorEmail(email):
    skorEmail = SkorEmail.query.get(email)

    if skorEmail:
        try:
            db.session.delete(skorEmail)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": skorEmail.json(),
                    "message": "SkorEmail deleted."
                }
            ), 200

        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": skorEmail.json(),
                    "message": "An error occurred when deleting the skorEmail."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "SkorEmail not found."
            }
        ), 404


##<!-------------- Configuration --------------!>##

# Get configuration
@app.route("/getConfiguration")
def getConfiguration():
    config = Configuration.query.get(1)
    
    if config:
        return jsonify(
            {
                "code": 200,
                "data": config.json(),
                "message": "Configuration retrieved."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Configuration not found."
        }
    ), 404

# Update test mode
@app.route("/updateTestMode/<int:testMode>", methods=["PUT"])
def updateTestMode(testMode):
    config = Configuration.query.get(1)

    if config:
        try:
            config.testMode = testMode
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": config.json(),
                    "message": "Configuration updated."
                }
            ), 200
                
        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": config.json(),
                    "message": "An error occurred when updating the configuration."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Configuration not found."
            }
        ), 404

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=SYSTEM_CONFIG_PORT)
    else:
        app.run(host='0.0.0.0', port=SYSTEM_CONFIG_PORT)