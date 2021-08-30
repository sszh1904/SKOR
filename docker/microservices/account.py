from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
from passlib.hash import sha256_crypt
import os
from datetime import timedelta, datetime
from password import *
from emailHandling import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app) 

ACCOUNT_PORT = os.getenv("ACCOUNT_PORT")
USER_PORT = os.getenv("USER_PORT")
SYSTEM_CONFIG_PORT = os.getenv("SYSTEM_CONFIG_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


adminDetailsUrl = os.environ.get('adminDetailsUrl') or f"http://localhost:{USER_PORT}/getAdmin"
updateAdminPasswordUrl = os.environ.get('updateAdminPasswordUrl') or f"http://localhost:{USER_PORT}/updateAdminPassword"
addStudentUrl = os.environ.get('addStudentUrl') or f"http://localhost:{USER_PORT}/addStudent"
studentDetailsUrl = os.environ.get('studentDetailsUrl') or f"http://localhost:{USER_PORT}/getStudent"
updateStudentPasswordUrl = os.environ.get('updateStudentPasswordUrl') or f"http://localhost:{USER_PORT}/updateStudentPassword"
taDetailsUrl = os.environ.get('taDetailsUrl') or f"http://localhost:{USER_PORT}/getTA"
addFacultyUrl = os.environ.get('addFacultyUrl') or f"http://localhost:{USER_PORT}/addFaculty"
facultyDetailsUrl = os.environ.get('facultyDetailsUrl') or f"http://localhost:{USER_PORT}/getFaculty"
updateFacultyPasswordUrl = os.environ.get('updateFacultyPasswordUrl') or f"http://localhost:{USER_PORT}/updateFacultyPassword"
addInstructorUrl = os.environ.get('addInstructorUrl') or f"http://localhost:{USER_PORT}/addInstructorUrl"
instructorDetailsUrl = os.environ.get('instructorDetailsUrl') or f"http://localhost:{USER_PORT}/getInstructor"
updateInstructorPasswordUrl = os.environ.get('updateInstructorPasswordUrl') or f"http://localhost:{USER_PORT}/updateInstructorPassword"


def getTestMode():
    getConfigurationUrl = os.environ.get('getConfigurationUrl') or f"http://localhost:{SYSTEM_CONFIG_PORT}/getConfiguration"
    config = invoke_http(getConfigurationUrl, method='GET')

    if config:
        testMode = config['data']['testMode']
    
    return testMode


# Login Authentication
@app.route("/loginAuthentication", methods=["POST"])
def loginAuthentication():
    if request.is_json:
        loginInput = request.get_json()
        inputEmail = loginInput['email']
        inputPassword = loginInput['password']
        acadYear = loginInput['acadYear']
        termNo = loginInput['termNo']

        studentDetails = invoke_http(f"{studentDetailsUrl}/{inputEmail}", method='GET')
        taDetails = invoke_http(f"{taDetailsUrl}/{inputEmail}/{acadYear}/{termNo}", method='GET')
        adminDetails = invoke_http(f"{adminDetailsUrl}/{inputEmail}", method='GET')
        facultyDetails = invoke_http(f"{facultyDetailsUrl}/{inputEmail}", method='GET')
        instructorDetails = invoke_http(f"{instructorDetailsUrl}/{inputEmail}", method='GET')

        if studentDetails["code"] == 200:
            if studentDetails['data']['lastLogin']:
                lastLogin = datetime.strptime(studentDetails['data']['lastLogin'], "%d %b %Y %H:%M")
                if (studentDetails['data']['isLogin'] != 0) and (datetime.now() - lastLogin) < timedelta(hours = 12):
                    return jsonify(
                        {
                            "code": 409,
                            "message": "You have already logged in."
                        }
                    ), 409
            
            hashedPassword = studentDetails["data"]["password"]
            if sha256_crypt.verify(inputPassword, hashedPassword):
                
                if taDetails["code"] == 200:
                    identity = "mixed"
                else:
                    identity = "student"

                output = {
                    "code": 200,
                    "identity": identity,
                    "details": studentDetails["data"]
                }

                return jsonify(
                    {
                        "code": 200,
                        "data": output
                    }
                ), 200
            else:
                return jsonify(
                    {
                        "code": 403,
                        "message": "Wrong password."
                    }
                ), 403
        
        elif facultyDetails["code"] == 200:
            if facultyDetails['data']['lastLogin']:
                lastLogin = datetime.strptime(facultyDetails['data']['lastLogin'], "%d %b %Y %H:%M")
                if (facultyDetails['data']['isLogin'] != 0) and (datetime.now() - lastLogin) < timedelta(hours = 12):
                    return jsonify(
                        {
                            "code": 409,
                            "message": "You have already logged in."
                        }
                    ), 409
            
            hashedPassword = facultyDetails["data"]["password"]
            if sha256_crypt.verify(inputPassword, hashedPassword):
                
                output = {
                    "code": 200,
                    "identity": "faculty",
                    "details": facultyDetails["data"]
                }

                return jsonify(
                    {
                        "code": 200,
                        "data": output
                    }
                ), 200
            else:
                return jsonify(
                    {
                        "code": 403,
                        "message": "Wrong password."
                    }
                ), 403

        elif instructorDetails["code"] == 200:
            if instructorDetails['data']['lastLogin']:
                lastLogin = datetime.strptime(instructorDetails['data']['lastLogin'], "%d %b %Y %H:%M")
                if (instructorDetails['data']['isLogin'] != 0) and (datetime.now() - lastLogin) < timedelta(hours = 12):
                    return jsonify(
                        {
                            "code": 409,
                            "message": "You have already logged in."
                        }
                    ), 409

            hashedPassword = instructorDetails["data"]["password"]
            if sha256_crypt.verify(inputPassword, hashedPassword):
                
                output = {
                    "code": 200,
                    "identity": "instructor",
                    "details": instructorDetails["data"]
                }

                return jsonify(
                    {
                        "code": 200,
                        "data": output
                    }
                ), 200
            else:
                return jsonify(
                    {
                        "code": 403,
                        "message": "Wrong password."
                    }
                ), 403
        
        elif adminDetails["code"] == 200:
            if adminDetails['data']['lastLogin']:
                lastLogin = datetime.strptime(adminDetails['data']['lastLogin'], "%d %b %Y %H:%M")
                if (adminDetails['data']['isLogin'] != 0) and (datetime.now() - lastLogin) < timedelta(hours = 12):
                    return jsonify(
                        {
                            "code": 409,
                            "message": "You have already logged in."
                        }
                    ), 409

            hashedPassword = adminDetails["data"]["password"]
            if sha256_crypt.verify(inputPassword, hashedPassword):
                
                output = {
                    "code": 200,
                    "identity": "admin",
                    "details": adminDetails["data"]
                }

                return jsonify(
                    {
                        "code": 200,
                        "data": output
                    }
                ), 200
            else:
                return jsonify(
                    {
                        "code": 403,
                        "message": "Wrong password."
                    }
                ), 403

        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404

    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

@app.route("/resetPassword/<string:email>", methods=['PUT'])
def resetPassword(email):
    studentDetails = invoke_http(f"{studentDetailsUrl}/{email}", method='GET')
    adminDetails = invoke_http(f"{adminDetailsUrl}/{email}", method='GET')
    facultyDetails = invoke_http(f"{facultyDetailsUrl}/{email}", method='GET')
    instructorDetails = invoke_http(f"{instructorDetailsUrl}/{email}", method='GET')
    
    rand_password = generateRandomPassword()

    dataOutput = None

    if studentDetails["code"] == 200:
        invoke_http(f"{updateStudentPasswordUrl}/{email}/{rand_password}", method='PUT')
        dataOutput = studentDetails
    elif facultyDetails["code"] == 200:
        invoke_http(f"{updateFacultyPasswordUrl}/{email}/{rand_password}", method='PUT')
        dataOutput = facultyDetails
    elif instructorDetails["code"] == 200:
        invoke_http(f"{updateInstructorPasswordUrl}/{email}/{rand_password}", method='PUT')
        dataOutput = instructorDetails
    elif adminDetails["code"] == 200:
        invoke_http(f"{updateAdminPasswordUrl}/{email}/{rand_password}", method='PUT')
        dataOutput = adminDetails

    if dataOutput == None:
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404
    
    testMode = getTestMode()
    sendResetPasswordEmail(email, PASSWORD_RESET_EMAIL_SUBJECT, rand_password, testMode)

    return jsonify(
        {
            "code": 200,
            "data": dataOutput,
            "message": "Password reset and email sent to user."
        }
    ), 200

@app.route("/createStudentAccount", methods=["POST"])
def createStudentAccount():
    if request.is_json:
        accountDetails = request.get_json()

        testMode = getTestMode()
        if testMode == 0:
            rand_password = generateRandomPassword()
        else:
            rand_password = "password"

        hashed_password = hashPassword(rand_password)
        accountInfo = {
            "email": accountDetails['email'].strip(),
            "name": accountDetails['name'],
            "password": hashed_password
            # "actualPassword": rand_password
        }

        studentDetails = invoke_http(addStudentUrl, method="POST", json=accountInfo)

        if studentDetails["code"] == 200:
            sendPasswordEmail(accountDetails['email'].strip(), NEW_ACCOUNT_EMAIL_SUBJECT, rand_password, testMode)

        return studentDetails
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

@app.route("/createFacultyAccount", methods=["POST"])
def createFacultyAccount():
    if request.is_json:
        accountDetails = request.get_json()

        testMode = getTestMode()
        if testMode == 0:
            rand_password = generateRandomPassword()
        else:
            rand_password = "password"

        hashed_password = hashPassword(rand_password)
        accountInfo = {
            "email": accountDetails['email'].strip(),
            "name": accountDetails['name'],
            "password": hashed_password
            # "actualPassword": rand_password
        }

        facultyDetails = invoke_http(addFacultyUrl, method="POST", json=accountInfo)

        if facultyDetails["code"] == 200:
            sendPasswordEmail(accountDetails['email'].strip(), NEW_ACCOUNT_EMAIL_SUBJECT, rand_password, testMode)

        return facultyDetails
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

@app.route("/createInstructorAccount", methods=["POST"])
def createInstructorAccount():
    if request.is_json:
        accountDetails = request.get_json()

        testMode = getTestMode()
        if testMode == 0:
            rand_password = generateRandomPassword()
        else:
            rand_password = "password"

        hashed_password = hashPassword(rand_password)
        accountInfo = {
            "email": accountDetails['email'].strip(),
            "name": accountDetails['name'],
            "password": hashed_password
            # "actualPassword": rand_password
        }

        instructorDetails = invoke_http(addInstructorUrl, method="POST", json=accountInfo)

        if instructorDetails["code"] == 200:
            sendPasswordEmail(accountDetails['email'].strip(), NEW_ACCOUNT_EMAIL_SUBJECT, rand_password, testMode)

        return instructorDetails
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=ACCOUNT_PORT)
    else:
        app.run(host='0.0.0.0', port=ACCOUNT_PORT)