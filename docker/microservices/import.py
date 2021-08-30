from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app) 

IMPORT_PORT = os.getenv("IMPORT_PORT")
USER_PORT = os.getenv("USER_PORT")
SESSION_PORT = os.getenv("SESSION_PORT")
LOG_PORT = os.getenv("LOG_PORT")
ACCOUNT_PORT = os.getenv("ACCOUNT_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


getStudentUrl = os.environ.get('getStudentUrl') or f"http://localhost:{USER_PORT}/getStudent"
getFacultyUrl = os.environ.get('getFacultyUrl') or f"http://localhost:{USER_PORT}/getFaculty"
getInstructorUrl = os.environ.get('getInstructorUrl') or f"http://localhost:{USER_PORT}/getInstructor"
bulkAddEnrolmentUrl = os.environ.get('bulkAddEnrolmentUrl') or f"http://localhost:{USER_PORT}/bulkAddEnrolment"
deleteAllEnrolmentBySectionUrl = os.environ.get('deleteAllEnrolmentBySectionUrl') or f"http://localhost:{USER_PORT}/deleteAllEnrolmentBySection"
bulkAddStudentSessionScoreUrl = os.environ.get('bulkAddStudentSessionScoreUrl') or f"http://localhost:{SESSION_PORT}/bulkAddStudentSessionScore"
getScoreBySectionByStudentUrl = os.environ.get('getScoreBySectionByStudentUrl') or f"http://localhost:{SESSION_PORT}/getScoreBySectionByStudent"
bulkUpdateStudentSessionScoreUrl = os.environ.get('bulkUpdateStudentSessionScoreUrl') or f"http://localhost:{SESSION_PORT}/bulkUpdateStudentSessionScore"
bulkAddStudentSessionScoreLogUrl = os.environ.get('bulkAddStudentSessionScoreLogUrl') or f"http://localhost:{LOG_PORT}/bulkAddStudentSessionScoreLog"
createStudentAccountUrl = os.environ.get('createStudentAccountUrl') or f"http://localhost:{ACCOUNT_PORT}/createStudentAccount"
createFacultyAccountUrl = os.environ.get('createFacultyAccountUrl') or f"http://localhost:{ACCOUNT_PORT}/createFacultyAccount"
createInstructorAccountUrl = os.environ.get('createInstructorAccountUrl') or f"http://localhost:{ACCOUNT_PORT}/createInstructorAccount"


# Import classlist
@app.route("/importClasslist", methods=['POST'])
def importClasslist():
    if request.is_json:
        classlistDetails = request.get_json()
        print(classlistDetails)
        classlist = classlistDetails['classlist']

        invoke_http(f"{deleteAllEnrolmentBySectionUrl}/{classlistDetails['acadYear']}/{classlistDetails['termNo']}/{classlistDetails['courseCode']}/{classlistDetails['sectionNo']}", method='DELETE')

        enrolmentObjects = []
        studentSessScoreObjects = []
        newStudentSessScoreObjects = []
        studentSessScoreLogObjects = []

        for student in classlist:
            getStudent = invoke_http(f"{getStudentUrl}/{student['Email']}", method='GET')
            if getStudent["code"] == 404:
                studentInfo = {
                    "email": student["Email"],
                    "name": student["Name"]
                }
                studentDetails = invoke_http(createStudentAccountUrl, method='POST', json=studentInfo)

                if studentDetails["code"] == 500:
                    return jsonify(
                        {
                            "code": 500,
                            "data": studentInfo,
                            "message": studentDetails["message"]
                        }
                    )

            enrolment = {
                "acadYear": classlistDetails['acadYear'],
                "termNo": classlistDetails['termNo'],
                "courseCode": classlistDetails['courseCode'],
                "sectionNo": classlistDetails['sectionNo'],
                "studentEmail": student["Email"]
            }
            enrolmentObjects.append(enrolment)

            getStudentSessionScores = invoke_http(f"{getScoreBySectionByStudentUrl}/{classlistDetails['acadYear']}/{classlistDetails['termNo']}/{classlistDetails['courseCode']}/{classlistDetails['sectionNo']}/{student['Email']}", method='GET')
            if getStudentSessionScores["code"] == 404:
                for i in range(13):
                    studentSessScore = {
                        "acadYear": classlistDetails['acadYear'],
                        "termNo": classlistDetails['termNo'],
                        "courseCode": classlistDetails['courseCode'],
                        "sectionNo": classlistDetails['sectionNo'],
                        "sessNo": i+1,
                        "studentEmail": student["Email"]
                    }
                    studentSessScoreObjects.append(studentSessScore)
            
            for week, score in student['weeks'].items():
                newStudentSessScore = {
                    "acadYear": classlistDetails['acadYear'],
                    "termNo": classlistDetails['termNo'],
                    "courseCode": classlistDetails['courseCode'],
                    "sectionNo": classlistDetails['sectionNo'],
                    "sessNo": int(week[1:]),
                    "studentEmail": student["Email"],
                    "score": int(score)
                }
                newStudentSessScoreObjects.append(newStudentSessScore)

                currTime = str(datetime.now()).replace(' ', 'T')
                action = f'Imported and updated score for student. Score for this week is {int(score)}'
                studentSessionScoreLog = {
                    "acadYear": classlistDetails['acadYear'],
                    "termNo": classlistDetails['termNo'],
                    "courseCode": classlistDetails['courseCode'],
                    "sectionNo": classlistDetails['sectionNo'],
                    "sessNo": int(week[1:]),
                    "studentEmail": student["Email"],
                    "logDatetime": currTime,
                    "action": action,
                    "actionBy": classlistDetails['identityEmail'],
                    "role": classlistDetails['identity']
                }
                studentSessScoreLogObjects.append(studentSessionScoreLog)

        bulkAddEnrolment = invoke_http(bulkAddEnrolmentUrl, method='POST', json={"objects": enrolmentObjects})
        if bulkAddEnrolment['code'] == 500:
            return bulkAddEnrolment
        
        bulkAddStudentSessionScore = invoke_http(bulkAddStudentSessionScoreUrl, method='POST', json={"objects": studentSessScoreObjects})
        if bulkAddStudentSessionScore['code'] == 500:
            return bulkAddStudentSessionScore
        
        bulkUpdateStudentSessionScore = invoke_http(bulkUpdateStudentSessionScoreUrl, method='PUT', json={"objects": newStudentSessScoreObjects})
        if bulkUpdateStudentSessionScore['code'] == 500:
            return bulkUpdateStudentSessionScore

        bulkAddStudentSessionScoreLog = invoke_http(bulkAddStudentSessionScoreLogUrl, method='POST', json={"objects": studentSessScoreLogObjects})
        if bulkAddStudentSessionScoreLog['code'] == 500:
            return bulkAddStudentSessionScoreLog

        return jsonify(
            {
                "code": 200,
                "data": classlistDetails
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

# Import students
@app.route("/importStudent", methods=["POST"])
def importStudent():
    if request.is_json:
        studentDetails = request.get_json()
        studentList = studentDetails["data"]

        for student in studentList:
            getStudent = invoke_http(f"{getStudentUrl}/{student['Email']}", method='GET')
            if getStudent["code"] == 404:
                studentInfo = {
                    "email": student["Email"],
                    "name": student["Name"]
                }

                newStudent = invoke_http(createStudentAccountUrl, method='POST', json=studentInfo)

                if newStudent["code"] == 500:
                    return jsonify(
                        {
                            "code": 500,
                            "data": studentInfo,
                            "message": newStudent["message"]
                        }
                    )
        return jsonify(
            {
                "code": 200,
                "data": studentList
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

# Import faculty
@app.route("/importFaculty", methods=["POST"])
def importFaculty():
    if request.is_json:
        facultyDetails = request.get_json()
        facultyList = facultyDetails["data"]

        for faculty in facultyList:
            getFaculty = invoke_http(f"{getFacultyUrl}/{faculty['Email']}", method='GET')
            if getFaculty["code"] == 404:
                facultyInfo = {
                    "email": faculty["Email"],
                    "name": faculty["Name"]
                }

                newFaculty = invoke_http(createFacultyAccountUrl, method='POST', json=facultyInfo)

                if newFaculty["code"] == 500:
                    return jsonify(
                        {
                            "code": 500,
                            "data": facultyInfo,
                            "message": newFaculty["message"]
                        }
                    )
        return jsonify(
            {
                "code": 200,
                "data": facultyList
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

# Import instructor
@app.route("/importInstructor", methods=["POST"])
def importInstructor():
    if request.is_json:
        instructorDetails = request.get_json()
        instructorList = instructorDetails["data"]

        for instructor in instructorList:
            getInstructor = invoke_http(f"{getInstructorUrl}/{instructor['Email']}", method='GET')
            if getInstructor["code"] == 404:
                instructorInfo = {
                    "email": instructor["Email"],
                    "name": instructor["Name"]
                }

                newInstructor = invoke_http(createInstructorAccountUrl, method='POST', json=instructorInfo)

                if newInstructor["code"] == 500:
                    return jsonify(
                        {
                            "code": 500,
                            "data": instructorInfo,
                            "message": newInstructor["message"]
                        }
                    )
        return jsonify(
            {
                "code": 200,
                "data": instructorList
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500


if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=IMPORT_PORT)
    else:
        app.run(host='0.0.0.0', port=IMPORT_PORT)