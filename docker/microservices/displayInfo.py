from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

DISPLAY_INFO_PORT = os.getenv("DISPLAY_INFO_PORT")
USER_PORT = os.getenv("USER_PORT")
COURSE_PORT = os.getenv("COURSE_PORT")
SECTION_PORT = os.getenv("SECTION_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


getSectionUrl = os.environ.get('getSectionUrl') or f"http://localhost:{SECTION_PORT}/getSection"
getSectionsByCourseUrl = os.environ.get('getSectionsByCourseUrl') or f"http://localhost:{SECTION_PORT}/getSectionsByCourse"
getSectionsByTermByTAUrl = os.environ.get('getSectionsByTermByTAUrl') or f"http://localhost:{SECTION_PORT}/getSectionsByTermByTA"
getSectionsByTermByFacultyUrl = os.environ.get('getSectionsByTermByFacultyUrl') or f"http://localhost:{SECTION_PORT}/getSectionsByTermByFaculty"
getSectionsByTermByInstructorUrl = os.environ.get('getSectionsByTermByInstructorUrl') or f"http://localhost:{SECTION_PORT}/getSectionsByTermByInstructor"
getPriorityCallBySectionUrl = os.environ.get('getPriorityCallBySectionUrl') or f"http://localhost:{SECTION_PORT}/getPriorityCallBySection"
getStudentUrl = os.environ.get('getStudentUrl') or f"http://localhost:{USER_PORT}/getStudent"
getFacultyUrl = os.environ.get('getFacultyUrl') or f"http://localhost:{USER_PORT}/getFaculty"
getInstructorUrl = os.environ.get('getInstructorUrl') or f"http://localhost:{USER_PORT}/getInstructor"
getCourseUrl = os.environ.get('getCourseUrl') or f"http://localhost:{COURSE_PORT}/getCourse"


# Get Section Information
@app.route("/getSectionInfo/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>", methods=["GET"])
def getSectionInfo(acadYear, termNo, courseCode, sectionNo):
    section = invoke_http(f"{getSectionUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}", method='GET')

    if section["code"] == 200:
        
        dataOutput = section['data']
        dataOutput['facultyName'] = invoke_http(f"{getFacultyUrl}/{section['data']['facultyEmail']}", method='GET')['data']['name']
        if dataOutput['taEmail']:
            dataOutput['taName'] = invoke_http(f"{getStudentUrl}/{section['data']['taEmail']}", method='GET')['data']['name']
        if dataOutput['instructorEmail']:
            dataOutput['instructorName'] = invoke_http(f"{getInstructorUrl}/{section['data']['instructorEmail']}", method='GET')['data']['name']
        dataOutput['courseName'] = invoke_http(f"{getCourseUrl}/{section['data']['courseCode']}", method='GET')['data']['courseName']

        print(f'Retrieved information for {courseCode} section {sectionNo} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No section {sectionNo} found for course {courseCode} in {acadYear} term {termNo}."
        }
    ), 404

# Get Sections information by course in a term
@app.route("/getSectionsInfoByCourse/<string:acadYear>/<int:termNo>/<string:courseCode>", methods=["GET"])
def getSectionsInfoByCourse(acadYear, termNo, courseCode):
    sectionList = invoke_http(f"{getSectionsByCourseUrl}/{acadYear}/{termNo}/{courseCode}", method='GET')

    if sectionList["code"] == 200:

        dataOutput = []
        for section in sectionList['data']:
            section['facultyName'] = invoke_http(f"{getFacultyUrl}/{section['facultyEmail']}", method='GET')['data']['name']
            if section['taEmail']:
                section['taName'] = invoke_http(f"{getStudentUrl}/{section['taEmail']}", method='GET')['data']['name']
            if section['instructorEmail']:
                section['instructorName'] = invoke_http(f"{getInstructorUrl}/{section['instructorEmail']}", method='GET')['data']['name']
            dataOutput.append(section)

        print(f'Retrieved sections for course {courseCode} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for course {courseCode} in {acadYear} term{termNo}."
        }
    ), 404

# Get Sections information by term and by TA
@app.route("/getSectionsInfoByTermByTA/<string:acadYear>/<int:termNo>/<string:taEmail>", methods=["GET"])
def getSectionsInfoByTermByTA(acadYear, termNo, taEmail):
    sectionList = invoke_http(f"{getSectionsByTermByTAUrl}/{acadYear}/{termNo}/{taEmail}", method='GET')

    if sectionList["code"] == 200:

        dataOutput = []
        for section in sectionList['data']:
            section['courseName'] = invoke_http(f"{getCourseUrl}/{section['courseCode']}", method='GET')['data']['courseName']
            dataOutput.append(section)
        
        print(f'Retrieved sections for {taEmail} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {taEmail} in {acadYear} term {termNo}."
        }
    ), 404

# Get Sections information by term and by Faculty
@app.route("/getSectionsInfoByTermByFaculty/<string:acadYear>/<int:termNo>/<string:facultyEmail>", methods=["GET"])
def getSectionsInfoByTermByFaculty(acadYear, termNo, facultyEmail):
    sectionList = invoke_http(f"{getSectionsByTermByFacultyUrl}/{acadYear}/{termNo}/{facultyEmail}", method='GET')

    if sectionList["code"] == 200:

        dataOutput = []
        for section in sectionList['data']:
            section['courseName'] = invoke_http(f"{getCourseUrl}/{section['courseCode']}", method='GET')['data']['courseName']
            dataOutput.append(section)
        
        print(f'Retrieved sections for {facultyEmail} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {facultyEmail} in {acadYear} term {termNo}."
        }
    ), 404

# Get Sections information by term and by Instructor
@app.route("/getSectionsInfoByTermByInstructor/<string:acadYear>/<int:termNo>/<string:instructorEmail>", methods=["GET"])
def getSectionsInfoByTermByInstructor(acadYear, termNo, instructorEmail):
    sectionList = invoke_http(f"{getSectionsByTermByInstructorUrl}/{acadYear}/{termNo}/{instructorEmail}", method='GET')

    if sectionList["code"] == 200:

        dataOutput = []
        for section in sectionList['data']:
            section['courseName'] = invoke_http(f"{getCourseUrl}/{section['courseCode']}", method='GET')['data']['courseName']
            dataOutput.append(section)
        
        print(f'Retrieved sections for {instructorEmail} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {instructorEmail} in {acadYear} term {termNo}."
        }
    ), 404

# Get PriorityCall Information in a Section
@app.route("/getPriorityCallInfoBySection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>", methods=["GET"])
def getPriorityCallInfoBySection(acadYear, termNo, courseCode, sectionNo):
    priorityCallList = invoke_http(f"{getPriorityCallBySectionUrl}/{acadYear}/{termNo}/{courseCode}/{sectionNo}", method='GET')

    if priorityCallList["code"] == 200:
        
        dataOutput = []
        for priorityCall in priorityCallList['data']:
            priorityCall['studentName'] = invoke_http(f"{getStudentUrl}/{priorityCall['studentEmail']}", method='GET')['data']['name']
            dataOutput.append(priorityCall)

        print(f'Retrieved priorityCalls for {courseCode} section {sectionNo} in {acadYear} term {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No priorityCalls found for course {courseCode} section {sectionNo}  in {acadYear} term {termNo}."
        }
    ), 404



if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=DISPLAY_INFO_PORT)
    else:
        app.run(host='0.0.0.0', port=DISPLAY_INFO_PORT)