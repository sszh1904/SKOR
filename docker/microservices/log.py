from flask import request, jsonify
from models import app, db, ParticipationScoreLog
import os
from dotenv import load_dotenv
load_dotenv()

LOG_PORT = os.getenv("LOG_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


# Add new ParticipationScoreLog from raisehand list
@app.route("/addParticipationLog", methods=['POST'])
def addParticipationLog():
    if request.is_json:
        participationLogDetails = request.get_json()

        participationLog = ParticipationScoreLog(
            acadYear = participationLogDetails['acadYear'], 
            termNo = participationLogDetails['termNo'], 
            courseCode = participationLogDetails['courseCode'],
            sectionNo = participationLogDetails['sectionNo'],
            sessNo = participationLogDetails['sessNo'],
            studentEmail = participationLogDetails['studentEmail'],
            logDatetime = participationLogDetails['logDatetime'],
            participationRecordDatetime = participationLogDetails['participationRecordDatetime'],
            action = participationLogDetails['action'],
            actionBy = participationLogDetails['identityEmail'],
            role = participationLogDetails['identity']
        )

        try:
            db.session.add(participationLog)
            db.session.commit()
            print("Participation log created")

            return jsonify(
                {
                    "code": 200,
                    "data": participationLog.json()
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
                    "data": participationLog.json(),
                    "message": "An error occurred when creating the new participation log."
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

# Add new StudentSessionScore log
@app.route("/addStudentSessionScoreLog", methods=['POST'])
def addStudentSessionScoreLog():
    if request.is_json:
        studentSessionScoreLogDetails = request.get_json()

        studentSessionScoreLog = ParticipationScoreLog(
            acadYear = studentSessionScoreLogDetails['acadYear'], 
            termNo = studentSessionScoreLogDetails['termNo'], 
            courseCode = studentSessionScoreLogDetails['courseCode'],
            sectionNo = studentSessionScoreLogDetails['sectionNo'],
            sessNo = studentSessionScoreLogDetails['sessNo'],
            studentEmail = studentSessionScoreLogDetails['studentEmail'],
            logDatetime = studentSessionScoreLogDetails['logDatetime'],
            action = studentSessionScoreLogDetails['action'],
            actionBy = studentSessionScoreLogDetails['identityEmail'],
            role = studentSessionScoreLogDetails['identity']
        )

        try:
            db.session.add(studentSessionScoreLog)
            db.session.commit()
            print("StudentSessionScore log created")

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScoreLog.json()
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
                    "data": studentSessionScoreLog.json(),
                    "message": "An error occurred when creating the new StudentSessionScore log."
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

# Add StudentSessionScore Log in bulk
@app.route("/bulkAddStudentSessionScoreLog", methods=["POST"])
def bulkAddStudentSessionScoreLog():
    if request.is_json:
        studentSessionScoreLogDetails = request.get_json()
        studentSessionScoreLogObjects = studentSessionScoreLogDetails['objects']

        try:
            db.session.bulk_insert_mappings(ParticipationScoreLog, studentSessionScoreLogObjects)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScoreLogObjects,
                    "message": "All student session score logs created."
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
                    "data": studentSessionScoreLogObjects,
                    "message": "An error occurred when creating the new student session score logs."
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

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=LOG_PORT)
    else:
        app.run(host='0.0.0.0', port=LOG_PORT)