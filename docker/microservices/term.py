from flask import request, jsonify
from models import app, db, Term
import os
from dotenv import load_dotenv
load_dotenv()

TERM_PORT = os.getenv("TERM_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


# Add new term
@app.route("/addTerm", methods=['POST'])
def addTerm():
    if request.is_json:
        termDetails = request.get_json()

        term = Term(
            acadYear = termDetails['acadYear'],
            termNo = termDetails['termNo'],
            startDate = termDetails['startDate'],
            endDate = termDetails['endDate']
        )

        try:
            db.session.add(term)
            db.session.commit()
            print('Term created.')

            return jsonify(
                {
                    "code":200,
                    "data":term.json()
                }
            ), 200

        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database.")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": term.json(),
                    "message": "An error occurred when creating the new term."
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

# Get a list of all the terms
@app.route("/getAllTerms")
def getAllTerms():
    termList = Term.query.all()
    if termList:
        print('Retrieved list of all terms')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "terms": [term.json() for term in termList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": "",
            "message": "Please create a term."
        }
    )

# Get a term
@app.route("/getTerm/<string:acadYear>/<int:termNo>")
def getTerm(acadYear, termNo):
    term = Term.query.filter(
        Term.acadYear == acadYear, 
        Term.termNo == termNo
    ).first()
    
    if term:
        print('Retrieved term')
        return jsonify(
            {
                "code": 200,
                "data": term.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Term not found."
        }
    ), 404

# Get current term
@app.route("/getCurrentTerm")
def getCurrentTerm():
    term = Term.query.filter(Term.isCurrent == 1).first()
    
    if term:
        print('Retrieved current term')
        return jsonify(
            {
                "code": 200,
                "data": term.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Current term not set."
        }
    ), 404

# Update current term
@app.route("/updateTerm/<string:acadYear>/<int:termNo>", methods=['PUT'])
def updateTerm(acadYear, termNo):
    currentTerm = Term.query.filter(
        Term.acadYear == acadYear, 
        Term.termNo == termNo
    ).first()
    prevTerm = Term.query.filter(Term.isCurrent == 1).first()

    if currentTerm:
        try:
            if prevTerm:
                prevTerm.isCurrent = 0
            currentTerm.isCurrent = 1
            db.session.commit()
            print('Current term updated')

            return jsonify(
                {
                    "code": 200,
                    "data": currentTerm.json()
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
                    "data": currentTerm.json(),
                    "message": "An error occurred when updating current term."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Term not found."
            }
        ), 404

# Update term info
@app.route("/updateTermInfo/<string:acadYear>/<int:termNo>/", methods=['PUT'])
def updateTermInfo(acadYear, termNo):
    term = Term.query.filter(
        Term.acadYear == acadYear, 
        Term.termNo == termNo
    ).first()

    if term:
        try:
            Term.query.filter(
                Term.acadYear == acadYear, 
                Term.termNo == termNo
            ).update(request.args.to_dict())
            db.session.commit()
            print('Current term updated')

            return jsonify(
                {
                    "code": 200,
                    "data": term.json()
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
                    "data": term.json(),
                    "message": "An error occurred when updating current term."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Term not found."
            }
        ), 404

# Delete term
@app.route("/deleteTerm/<string:acadYear>/<int:termNo>", methods=['DELETE'])
def deleteTerm(acadYear, termNo):
    term = Term.query.filter(Term.acadYear == acadYear, Term.termNo == termNo).first()
    if term:
        try:
            db.session.delete(term)
            db.session.commit()
            print("Term deleted")

            return jsonify(
            {
                "code":200,
                "data":term.json()
            }
            ), 200
        
        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code":500,
                    "data": term.json(),
                    "message": "An error occurred when deleting the term."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Term not found."
            }
        ), 404



if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=TERM_PORT)
    else:
        app.run(host='0.0.0.0', port=TERM_PORT)