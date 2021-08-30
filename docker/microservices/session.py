from flask import request, jsonify
from models import app, db, Session, Participation, StudentSessionScore
import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv()

SESSION_PORT = os.getenv("SESSION_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


##<!-------------- SESSION --------------!>##

# Add new session
@app.route("/addSession", methods=['POST'])
def addSession():
    if request.is_json:
        sessionDetails = request.get_json()

        session = Session(
            acadYear = sessionDetails['acadYear'], 
            termNo = sessionDetails['termNo'], 
            courseCode = sessionDetails['courseCode'],
            sectionNo = sessionDetails['sectionNo'],
            sessNo = sessionDetails['sessNo'],
            date = sessionDetails['date']
        )

        try:
            db.session.add(session)
            db.session.commit()
            print("Session created")

            return jsonify(
                {
                    "code": 200,
                    "data": session.json()
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
                    "data": session.json(),
                    "message": "An error occurred when creating the new session."
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

# Create 13 Sessions for a Section
@app.route("/createAllSessions", methods=['POST'])
def createAllSessions():
    if request.is_json:
        createDetails = request.get_json()

        sessionList = []

        startDate = dt.datetime.strptime(createDetails["startDate"], "%Y-%m-%d")
        for i in range(13):
            date = (startDate + dt.timedelta(days=i*7)).strftime('%Y-%m-%d')
            session = Session(
                acadYear = createDetails['acadYear'], 
                termNo = createDetails['termNo'], 
                courseCode = createDetails['courseCode'],
                sectionNo = createDetails['sectionNo'],
                sessNo = (i+1),
                date = date
            )
            db.session.add(session)
            sessionList.append(session)

        try:
            db.session.commit()
            print("Sessions created")

            return jsonify(
                {
                    "code": 200,
                    "data": [session.json() for session in sessionList]
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
                    "data": [session.json() for session in sessionList],
                    "message": "An error occurred when creating the new sessions."
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

# Get a session
@app.route("/getSession/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>")
def getSession(acadYear, termNo, courseCode, sectionNo, sessNo):
    session = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo, 
        Session.sessNo == sessNo
    ).first()

    if session:
        print("Retrieved session")
        return jsonify(
            {
                "code": 200,
                "data": session.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "Session not found"
        }
    ), 404

# Get all sessions for a section
@app.route("/getSessionsBySection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getSessionsBySection(acadYear, termNo, courseCode, sectionNo):
    sessionList = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo
    ).all()

    if len(sessionList):
        print('Retrieved all sessions')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "sessions": [session.json() for session in sessionList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No sessions found"
        }
    ), 404

# Get number of sessions for a section
@app.route("/getSessionCount/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getSessionCount(acadYear, termNo, courseCode, sectionNo):
    sessionCount = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo
    ).count()

    if isinstance(sessionCount, int):
        return jsonify(
            {
                "code": 200,
                "data": sessionCount
            }
        ), 200
    return jsonify(
        {
            "code": 500, 
            "message": "Error occurred in getting session count."
        }
    ), 500

# Get available session for a section
@app.route("/getAvailableSession/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getAvailableSession(acadYear, termNo, courseCode, sectionNo):
    session = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo,
        Session.available == 1)\
    .first()

    if session:
        print("Retrieved session")
        print(session)
        return jsonify(
            {
                "code": 200,
                "data": session.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No available session"
        }
    ), 404

# Update Session information
@app.route("/updateSessionInfo/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>", methods=['PUT'])
def updateSessionInfo(acadYear, termNo, courseCode, sectionNo, sessNo):
    session = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo, 
        Session.sessNo == sessNo
    ).first()

    if session:
        try:
            Session.query.filter(
                Session.acadYear == acadYear, 
                Session.termNo == termNo, 
                Session.courseCode == courseCode, 
                Session.sectionNo == sectionNo, 
                Session.sessNo == sessNo
            ).update(request.args.to_dict())
            db.session.commit()
            print("Session information updated")

            return jsonify(
                {
                    "code": 200,
                    "data": session.json()
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
                    "data": session.json(),
                    "message": "An error occurred when updating the session."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Session not found."
            }
        ), 404

# Update Session's availability
@app.route("/updateSessionAvailability/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<int:available>", methods=['PUT'])
def updateSessionAvailability(acadYear, termNo, courseCode, sectionNo, sessNo, available):
    currSession = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo, 
        Session.sessNo == sessNo
    ).first()

    if currSession:
        try:
            if available == 1:
                prevSession = session = Session.query.filter(
                    Session.acadYear == acadYear, 
                    Session.termNo == termNo, 
                    Session.courseCode == courseCode, 
                    Session.sectionNo == sectionNo, 
                    Session.available == 1
                ).first()

                if prevSession:
                    prevSession.available = 0
                    
            currSession.available = available
            db.session.commit()
            print("Session's availability updated")

            return jsonify(
                {
                    "code": 200,
                    "data": currSession.json()
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
                    "data": session.json(),
                    "message": "An error occurred when updating the session's availability."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Session not found."
            }
        ), 404

# Delete session
@app.route("/deleteSession/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>", methods=['DELETE'])
def deleteSession(acadYear, termNo, courseCode, sectionNo, sessNo):
    session = Session.query.filter(
        Session.acadYear == acadYear, 
        Session.termNo == termNo, 
        Session.courseCode == courseCode, 
        Session.sectionNo == sectionNo, 
        Session.sessNo == sessNo
    ).first()

    if session:
        try:
            db.session.delete(session)
            db.session.commit()
            print("Session deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": session.json()
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
                    "data": session.json(),
                    "message": "An error occurred when deleting the session."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Session not found."
            }
        ), 404


##<!-------------- PARTICIPATION --------------!>##

# Add new raise hand record
@app.route("/addParticipation", methods=['POST'])
def addParticipation():
    if request.is_json:
        participationDetails = request.get_json()

        participation = Participation(
                acadYear = participationDetails['acadYear'], 
                termNo = participationDetails['termNo'], 
                courseCode = participationDetails['courseCode'],
                sectionNo = participationDetails['sectionNo'],
                sessNo = participationDetails['sessNo'],
                studentEmail = participationDetails['studentEmail'],
                datetime = participationDetails['dateTime']
            )

        try:
            db.session.add(participation)
            db.session.commit()
            print("Participation created")

            return jsonify(
                {
                    "code": 200,
                    "data": participation.json()
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
                    "data": participation.json(),
                    "message": "An error occurred when creating the new participation."
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

# Get a Participation
@app.route("/getParticipation/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:datetime>/<string:studentEmail>")
def getParticipation(acadYear, termNo, courseCode, sectionNo, sessNo, datetime, studentEmail):
    participation = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo,
        Participation.datetime == datetime,
        Participation.studentEmail == studentEmail
    ).first()

    if participation:
        print('Retrieved participation.')
        return jsonify(
            {
                "code": 200,
                "data": participation.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participation found."
        }
    ), 404

# Get all participation in a session
@app.route("/getParticipationBySession/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>")
def getParticipationBySession(acadYear, termNo, courseCode, sectionNo, sessNo):
    participationList = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo,
        Participation.isAccepted == 1
    ).all()

    if len(participationList):
        print('Retrieved all participations')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "participation": [participation.json() for participation in participationList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participations found."
        }
    ), 404

# Get all participation in a session by a student
@app.route("/getParticipationBySessionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>")
def getParticipationBySessionByStudent(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail):
    participationList = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo, 
        Participation.studentEmail == studentEmail,
        Participation.isAccepted == 1
    ).all()

    if len(participationList):
        print('Retrieved all participations for student')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "participation": [participation.json() for participation in participationList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participations found."
        }
    ), 404

# Get all raise hand in a session
@app.route("/getRaiseHandBySession/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>")
def getRaiseHandBySession(acadYear, termNo, courseCode, sectionNo, sessNo):
    participationList = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo
    ).all()

    if len(participationList):
        print('Retrieved all participations for student')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "participation": [participation.json() for participation in participationList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participations found."
        }
    ), 404

# Get all raise hand by a student in a session
@app.route("/getRaiseHandBySessionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>")
def getRaiseHandBySessionByStudent(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail):
    participationList = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo,
        Participation.studentEmail == studentEmail
    ).all()

    if len(participationList):
        print('Retrieved all participations for student')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "participation": [participation.json() for participation in participationList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participations found."
        }
    ), 404

# Get all raise hand by a student in a section
@app.route("/getRaiseHandBySectionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>")
def getRaiseHandBySectionByStudent(acadYear, termNo, courseCode, sectionNo, studentEmail):
    participationList = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.studentEmail == studentEmail
    ).all()

    if len(participationList):
        print('Retrieved all participations for student')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "participation": [participation.json() for participation in participationList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No participations found."
        }
    ), 404

# Accept Raisehand and award Participation
@app.route("/awardParticipation/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:datetime>", methods=['POST', 'PUT'])
def awardParticipation(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, datetime):
    participation = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo, 
        Participation.studentEmail == studentEmail,
        Participation.datetime == datetime
    ).first()

    if participation:
        try:
            participation.isAccepted = 1
            participation.score = 1
            db.session.commit()
            print("Participation score updated")

            return jsonify(
                {
                    "code": 200,
                    "data": participation.json()
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
                    "data": participation.json(),
                    "message": "An error occurred when updating the participation."
                }
            ), 500
        
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Participation not found."
            }
        ), 404

# Invalidate Participation
@app.route("/invalidateParticipation/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:datetime>", methods=['POST', 'PUT'])
def invalidateParticipation(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, datetime):
    participation = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo, 
        Participation.studentEmail == studentEmail,
        Participation.datetime == datetime
    ).first()

    if participation:
        try:
            participation.score = 0
            db.session.commit()
            print("Participation score updated")

            return jsonify(
                {
                    "code": 200,
                    "data": participation.json()
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
                    "data": participation.json(),
                    "message": "An error occurred when updating the participation."
                }
            ), 500
        
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Participation not found."
            }
        ), 404

# Award bonus Participation Score
@app.route("/awardBonusParticipation/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:datetime>", methods=['POST', 'PUT'])
def awardBonusParticipation(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, datetime):
    participation = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo, 
        Participation.studentEmail == studentEmail,
        Participation.datetime == datetime
    ).first()

    if participation:
        try:
            participation.score = 2
            db.session.commit()
            print("Participation score updated")

            return jsonify(
                {
                    "code": 200,
                    "data": participation.json()
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
                    "data": participation.json(),
                    "message": "An error occurred when updating the participation."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Participation not found."
            }
        ), 404

# Delete participation
@app.route("/deleteParticipation/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<string:datetime>", methods=['DELETE'])
def deleteParticipation(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, datetime):
    participation = Participation.query.filter(
        Participation.acadYear == acadYear, 
        Participation.termNo == termNo, 
        Participation.courseCode == courseCode, 
        Participation.sectionNo == sectionNo, 
        Participation.sessNo == sessNo, 
        Participation.studentEmail == studentEmail,
        Participation.datetime == datetime
    ).first()

    if participation:
        try:
            db.session.delete(participation)
            db.session.commit()
            print("Participation deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": participation.json()
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
                    "data": participation.json(),
                    "message": "An error occurred when deleting the participation."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Participation not found."
            }
        ), 404


##<!-------------- STUDENTSESSIONSCORE --------------!>##

# Add new raise hand record
@app.route("/addStudentSessionScore", methods=['POST'])
def addStudentSessionScore():
    if request.is_json:
        studentSessionScoreDetails = request.get_json()

        studentSessionScore = StudentSessionScore(
                acadYear = studentSessionScoreDetails['acadYear'], 
                termNo = studentSessionScoreDetails['termNo'], 
                courseCode = studentSessionScoreDetails['courseCode'],
                sectionNo = studentSessionScoreDetails['sectionNo'],
                sessNo = studentSessionScoreDetails['sessNo'],
                studentEmail = studentSessionScoreDetails['studentEmail']
            )

        try:
            db.session.add(studentSessionScore)
            db.session.commit()
            print("StudentSessionScore created")

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScore.json()
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
                    "data": studentSessionScore.json(),
                    "message": "An error occurred when creating the new studentSessionScore."
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

# Create all student session score for a student in a section
@app.route("/createAllStudentSessionScore", methods=["POST"])
def createAllStudentSessionScore():
    if request.is_json:
        createDetails = request.get_json()

        studentSessionScoreList = []

        for _ in range(13):
            studentSessionScore = Session(
                acadYear = createDetails['acadYear'], 
                termNo = createDetails['termNo'], 
                courseCode = createDetails['courseCode'],
                sectionNo = createDetails['sectionNo'],
                sessNo = createDetails['sessNo'],
                studentEmail = createDetails['studentEmail'] 
            )
            db.session.add(studentSessionScore)
            studentSessionScoreList.append(studentSessionScore)

        try:
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": [studentSessionScore.json() for studentSessionScore in studentSessionScoreList],
                    "message": "Student session scores created."
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
                    "data": [studentSessionScore.json() for studentSessionScore in studentSessionScoreList],
                    "message": "An error occurred when creating the new student session scores."
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

# Add new student session scores in bulk
@app.route("/bulkAddStudentSessionScore", methods=["POST"])
def bulkAddStudentSessionScore():
    if request.is_json:
        studentSessionScoreDetails = request.get_json()
        studentSessionScoreObjects = studentSessionScoreDetails['objects']

        try:
            db.session.bulk_insert_mappings(StudentSessionScore, studentSessionScoreObjects)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScoreObjects,
                    "message": "All student session scores created."
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
                    "data": studentSessionScoreObjects,
                    "message": "An error occurred when creating the new student session scores."
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

# Get participation score for a student in a session
@app.route("/getScoreBySessionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>")
def getScoreBySessionByStudent(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail):
    studentSessionScore = StudentSessionScore.query.filter(
        StudentSessionScore.acadYear == acadYear, 
        StudentSessionScore.termNo == termNo, 
        StudentSessionScore.courseCode == courseCode, 
        StudentSessionScore.sectionNo == sectionNo, 
        StudentSessionScore.sessNo == sessNo, 
        StudentSessionScore.studentEmail == studentEmail
    ).first()

    if studentSessionScore:
        print('Retrieved studentSessionScore for student')

        return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScore.json()
                }
            ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No studentSessionScore found."
        }
    ), 404

# Get total participation score for a student in a section
@app.route("/getTotalScoreBySectionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>")
def getTotalScoreBySectionByStudent(acadYear, termNo, courseCode, sectionNo, studentEmail):
    studentSessionTotalScore = db.session\
        .query(
            StudentSessionScore.studentEmail,
            db.func.sum(StudentSessionScore.score))\
        .filter(
            StudentSessionScore.acadYear == acadYear, 
            StudentSessionScore.termNo == termNo, 
            StudentSessionScore.courseCode == courseCode, 
            StudentSessionScore.sectionNo == sectionNo, 
            StudentSessionScore.studentEmail == studentEmail
        ).all()

    if studentSessionTotalScore:
        print('Retrieved total participation score for student')

        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "studentEmail": studentSessionTotalScore[0][0],
                        "score": int(studentSessionTotalScore[0][1])
                    }
                }
            ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No studentSessionTotalScore found."
        }
    ), 404

# Get all session scores by a student in a section
@app.route("/getScoreBySectionByStudent/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>")
def getScoreBySectionByStudent(acadYear, termNo, courseCode, sectionNo, studentEmail):
    studentSessionScoreList = StudentSessionScore.query.filter(
        StudentSessionScore.acadYear == acadYear, 
        StudentSessionScore.termNo == termNo, 
        StudentSessionScore.courseCode == courseCode, 
        StudentSessionScore.sectionNo == sectionNo, 
        StudentSessionScore.studentEmail == studentEmail
    ).all()

    if len(studentSessionScoreList):
        print('Retrieved all studentSessionScore for student')

        sessionScores = {}
        for session in studentSessionScoreList:
            sessionScores[session.sessNo] = session.score
            
        return jsonify(
            {
                "code": 200,
                "data": {
                    "sessionScores": sessionScores
                }
            }
        ), 200
        
    return jsonify(
        {
            "code": 404, 
            "message": "No studentSessionScore found."
        }
    ), 404

# plus participation score for a Student in a Session
@app.route("/plusStudentSessionScore/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>", methods=['POST', 'PUT'])
def plusStudentSessionScore(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail):
    studentSessionScore = StudentSessionScore.query.filter(
        StudentSessionScore.acadYear == acadYear, 
        StudentSessionScore.termNo == termNo, 
        StudentSessionScore.courseCode == courseCode, 
        StudentSessionScore.sectionNo == sectionNo, 
        StudentSessionScore.sessNo == sessNo, 
        StudentSessionScore.studentEmail == studentEmail
    ).first()

    if studentSessionScore:
        try:
            studentSessionScore.score += 1
            db.session.commit()
            print("StudentSessionScore updated")

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScore.json()
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
                    "data": studentSessionScore.json(),
                    "message": "An error occurred when updating the StudentSessionScore."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "StudentSessionScore not found."
            }
        ), 404

# Minus participation score for a Student in a Session
@app.route("/minusStudentSessionScore/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>", methods=['POST', 'PUT'])
def minusStudentSessionScore(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail):
    studentSessionScore = StudentSessionScore.query.filter(
        StudentSessionScore.acadYear == acadYear, 
        StudentSessionScore.termNo == termNo, 
        StudentSessionScore.courseCode == courseCode, 
        StudentSessionScore.sectionNo == sectionNo, 
        StudentSessionScore.sessNo == sessNo, 
        StudentSessionScore.studentEmail == studentEmail
    ).first()

    if studentSessionScore:
        try:
            studentSessionScore.score -= 1
            db.session.commit()
            print("StudentSessionScore updated")

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScore.json()
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
                    "data": studentSessionScore.json(),
                    "message": "An error occurred when updating the StudentSessionScore."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "StudentSessionScore not found."
            }
        ), 404

# Update participation score for a Student in a Session from StudentSessionScore table
@app.route("/updateStudentSessionScore/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<int:sessNo>/<string:studentEmail>/<int:score>", methods=['POST', 'PUT'])
def updateStudentSessionScore(acadYear, termNo, courseCode, sectionNo, sessNo, studentEmail, score):
    studentSessionScore = StudentSessionScore.query.filter(
        StudentSessionScore.acadYear == acadYear, 
        StudentSessionScore.termNo == termNo, 
        StudentSessionScore.courseCode == courseCode, 
        StudentSessionScore.sectionNo == sectionNo, 
        StudentSessionScore.sessNo == sessNo, 
        StudentSessionScore.studentEmail == studentEmail
    ).first()

    if studentSessionScore:
        try:
            studentSessionScore.score = score
            db.session.commit()
            print("StudentSessionScore updated")

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScore.json()
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
                    "data": studentSessionScore.json(),
                    "message": "An error occurred when updating the StudentSessionScore."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "StudentSessionScore not found."
            }
        ), 404

# Update student session scores in bulk
@app.route("/bulkUpdateStudentSessionScore", methods=["PUT"])
def bulkUpdateStudentSessionScore():
    if request.is_json:
        studentSessionScoreDetails = request.get_json()
        studentSessionScoreObjects = studentSessionScoreDetails['objects']

        try:
            db.session.bulk_update_mappings(StudentSessionScore, studentSessionScoreObjects)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": studentSessionScoreObjects,
                    "message": "All student session scores updated."
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
                    "data": studentSessionScoreObjects,
                    "message": "An error occurred when updating the new student session scores."
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

if __name__== '__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=SESSION_PORT)
    else:
        app.run(host='0.0.0.0', port=SESSION_PORT)