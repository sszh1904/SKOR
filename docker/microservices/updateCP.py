from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

UPDATE_CP_PORT = os.getenv("UPDATE_CP_PORT")
SECTION_PORT = os.getenv("SECTION_PORT")
SESSION_PORT = os.getenv("SESSION_PORT")
LOG_PORT = os.getenv("LOG_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


getSectionUrl = os.environ.get('getSectionUrl') or f"http://localhost:{SECTION_PORT}/getSection"
getScoreBySessionByStudentUrl = os.environ.get('getScoreBySessionByStudentUrl') or f"http://localhost:{SESSION_PORT}/getScoreBySessionByStudent"
awardParticipationUrl = os.environ.get('awardParticipationUrl') or f"http://localhost:{SESSION_PORT}/awardParticipation"
invalidateParticipationUrl = os.environ.get('invalidateParticipationUrl') or f"http://localhost:{SESSION_PORT}/invalidateParticipation"
awardBonusParticipationUrl = os.environ.get('awardBonusParticipationUrl') or f"http://localhost:{SESSION_PORT}/awardBonusParticipation"
plusStudentSessionScoreUrl = os.environ.get('plusStudentSessionScoreUrl') or f"http://localhost:{SESSION_PORT}/plusStudentSessionScore"
minusStudentSessionScoreUrl = os.environ.get('minusStudentSessionScoreUrl') or f"http://localhost:{SESSION_PORT}/minusStudentSessionScore"
updateStudentSessionScoreUrl = os.environ.get('updateStudentSessionScoreUrl') or f"http://localhost:{SESSION_PORT}/updateStudentSessionScore"
addParticipationLogUrl = os.environ.get('addParticipationLogUrl') or f"http://localhost:{LOG_PORT}/addParticipationLog"
addStudentSessionScoreLogUrl = os.environ.get('addStudentSessionScoreLogUrl') or f"http://localhost:{LOG_PORT}/addStudentSessionScoreLog"


# Accept raisehand
@app.route("/acceptRaisehand/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:logDatetime>/<string:participationRecordDatetime>/<string:identity>/<string:identityEmail>", methods=["PUT"])
def acceptRaisehand(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, logDatetime, participationRecordDatetime, identity, identityEmail):
    participationScoreLimit = invoke_http(f"{getSectionUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}", method='GET')['data']['participationScoreLimit']

    studentSessionScore = invoke_http(f"{getScoreBySessionByStudentUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}", method='GET')['data']['score']

    participation = invoke_http(f"{awardParticipationUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}/{participationRecordDatetime}", method='PUT')

    if participationScoreLimit == None or studentSessionScore < participationScoreLimit:
        plusStudentSessionScore = invoke_http(f"{plusStudentSessionScoreUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}", method='PUT')

        action = 'Accepted raisehand and awarded participation score on raisehand list, participation score changed to 1'
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participation['code'] == 200) and (plusStudentSessionScore['code'] == 200) and (participationLog['code'] == 200):
            print("Updated Participation, StudentSessionScore and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participation": participation["data"],
                        "studentSessionScore": plusStudentSessionScore["data"],
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200
        elif (participation["code"] == 500) or (plusStudentSessionScore['code'] == 500) or (participationLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": plusStudentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating Participation/ StudentSessionScore/ParticipationLog."
                }
            ), 500
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": plusStudentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Participation/StudentSessionScore/ParticipationLog not found."
                }
            ), 404
    else:
        action = "Accepted raisehand but no participation score added to student's participation score for this session as student's participation score for this session exceed the participation score limit"
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participation['code'] == 200) and (participationLog['code'] == 200):
            print("Updated Participation and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participation": participation["data"],
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200
        elif (participation["code"] == 500) or (participationLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participation": participation,
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating Participation/ParticipationLog."
                }
            ), 500
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "participation": participation,
                        "participationLog": participationLog
                    },
                    "message": "Participation/ParticipationLog not found."
                }
            ), 404

# Invalidate Participation
@app.route("/invalidateCP/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:logDatetime>/<string:participationRecordDatetime>/<string:identity>/<string:identityEmail>/<int:reachedLimit>", methods=["PUT"])
def invalidateCP(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, logDatetime, participationRecordDatetime, identity, identityEmail, reachedLimit):
    if reachedLimit == 0:
        participation = invoke_http(f"{invalidateParticipationUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}/{participationRecordDatetime}", method='PUT')

        studentSessionScore = invoke_http(f"{minusStudentSessionScoreUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}", method='PUT')

        action = 'Invalidated participation on raisehand list, participation score is changed to 0'
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participation['code'] == 200) and (studentSessionScore['code'] == 200) and (participationLog['code'] == 200):
            print("Updated Participation, StudentSessionScore and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participation": participation["data"],
                        "studentSessionScore": studentSessionScore["data"],
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200

        elif (participation["code"] == 500) or (studentSessionScore['code'] == 500) or (participationLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": studentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating Participation/ StudentSessionScore/ParticipationLog."
                }
            ), 500

        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": studentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Participation/StudentSessionScore/ParticipationLog not found."
                }
            ), 404
    else:
        action = 'Invalidated participation on raisehand list, participation score is not changed since student reached the class participation prior to invalidation.'
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participationLog['code'] == 200):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating ParticipationLog."
                }
            ), 500

# Award bonus Participation
@app.route("/awardBonusCP/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:logDatetime>/<string:participationRecordDatetime>/<string:identity>/<string:identityEmail>", methods=["PUT"])
def awardBonusCP(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, logDatetime, participationRecordDatetime, identity, identityEmail):
    participationScoreLimit = invoke_http(f"{getSectionUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}", method='GET')['data']['participationScoreLimit']
    studentSessionScore = invoke_http(f"{getScoreBySessionByStudentUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}", method='GET')['data']['score']

    participation = invoke_http(f"{awardBonusParticipationUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}/{participationRecordDatetime}", method='PUT')

    if participationScoreLimit == None or studentSessionScore < participationScoreLimit:
        plusStudentSessionScore = invoke_http(f"{plusStudentSessionScoreUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}", method='PUT')

        action = 'Awarded bonus participation score on raisehand list, participation score changed to 2.'
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participation['code'] == 200) and (plusStudentSessionScore['code'] == 200) and (participationLog['code'] == 200):
            print("Updated Participation, StudentSessionScore and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participation": participation["data"],
                        "studentSessionScore": plusStudentSessionScore["data"],
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200
        elif (participation["code"] == 500) or (plusStudentSessionScore['code'] == 500) or (participationLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": plusStudentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating Participation/ StudentSessionScore/ParticipationLog."
                }
            ), 500
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "participation": participation,
                        "studentSessionScore": plusStudentSessionScore,
                        "participationLog": participationLog
                    },
                    "message": "Participation/StudentSessionScore/ParticipationLog not found."
                }
            ), 404
    else:
        action = "Awarded bonus score for this participation but no bonus participation score added to student's participation score for this session as student's participation score for this session exceed the participation score limit"
        participationLogInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "participationRecordDatetime": participationRecordDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        participationLog = invoke_http(addParticipationLogUrl, method='POST', json=participationLogInfo)

        if (participation['code'] == 200) and (participationLog['code'] == 200):
            print("Updated Participation and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "participation": participation["data"],
                        "participationLog" : participationLog["data"]
                    }
                }
            ), 200
        elif (participation["code"] == 500) or (participationLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "participation": participation,
                        "participationLog": participationLog
                    },
                    "message": "Error occurred when updating Participation/ParticipationLog."
                }
            ), 500
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "participation": participation,
                        "participationLog": participationLog
                    },
                    "message": "Participation/ParticipationLog not found."
                }
            ), 404

# Update cp score from StudentSessionScore table
@app.route("/updateStudentSessionCPScore/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<int:score>/<string:logDatetime>/<string:identity>/<string:identityEmail>", methods=["PUT"])
def updateStudentSessionCPScore(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, score, logDatetime, identity, identityEmail):
        studentSessionScore = invoke_http(f"{updateStudentSessionScoreUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}/{sessNo}/{studentEmail}/{score}", method='PUT')

        action = f'Updated class participation score to {score} on StudentSessionScore table.'
        studentSessionScoreInfo = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "logDatetime": logDatetime,
            "action": action,
            "identity": identity,
            "identityEmail": identityEmail
        }
        studentSessionScoreLog = invoke_http(addStudentSessionScoreLogUrl, method='POST', json=studentSessionScoreInfo)

        if (studentSessionScore['code'] == 200) and (studentSessionScoreLog['code'] == 200):
            print("Updated StudentSessionScore and ParticipationLog.")

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "studentSessionScore": studentSessionScore["data"],
                        "studentSessionScoreLog" : studentSessionScoreLog["data"]
                    }
                }
            ), 200

        elif (studentSessionScore['code'] == 500) or (studentSessionScoreLog['code'] == 500):
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "studentSessionScore": studentSessionScore,
                        "studentSessionScoreLog": studentSessionScoreLog
                    },
                    "message": "Error occurred when updating StudentSessionScore/ParticipationLog."
                }
            ), 500

        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "studentSessionScore": studentSessionScore,
                        "studentSessionScoreLog": studentSessionScoreLog
                    },
                    "message": "StudentSessionScore/ParticipationLog not found."
                }
            ), 404


if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=UPDATE_CP_PORT)
    else:
        app.run(host='0.0.0.0', port=UPDATE_CP_PORT)