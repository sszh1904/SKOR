from flask import request, jsonify
from models import app, db, Admin, TATerm, Faculty, Instructor, Student, Enrolment
from password import *
import os
from dotenv import load_dotenv
load_dotenv()

USER_PORT = os.getenv("USER_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


##<!-------------- ADMIN --------------!>##

# Add new admin
@app.route("/addAdmin", methods=['POST'])
def addAdmin():
    if request.is_json:
        adminDetails = request.get_json()

        hashed_password = hashPassword(adminDetails['password'])

        admin = Admin(
            email = adminDetails['email'].strip(),
            name = adminDetails['name'],
            password = hashed_password
            # actualPassword = adminDetails['password']
        )
        
        try:
            db.session.add(admin)
            db.session.commit()

            return jsonify(
                {
                    "code":200,
                    "data": admin.json(),
                    "message": "Admin created."
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
                    "data": {
                        "admin": admin.json(),
                    },
                    "message": "An error occurred when creating the new admin."
                }
            ), 500
        
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not in JSON format.'
            }
        ), 500

# Get admin by email
@app.route("/getAdmin/<string:email>")
def getAdmin(email):
    
    admin = Admin.query.get(email)
    
    if admin:
        return jsonify(
            {
                "code": 200,
                "data": admin.json(),
                "message": "Admin retrieved."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Admin not found."
        }
    ), 404

# Update admin information
@app.route("/updateAdminInfo/<string:email>", methods=['PUT'])
def updateAdminInfo(email):
    admin = Admin.query.get(email)

    if admin:
        try:
            Admin.query.filter(
                Admin.email == email
            ).update(request.args.to_dict())
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": admin.json(),
                    "message": "Admin information updated."
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
                    "data": admin.json(),
                    "message": "An error occurred when updating admin information."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Admin not found."
            }
        ), 404

# Update admin password
@app.route("/updateAdminPassword/<string:email>/<string:password>", methods=['PUT'])
def updateAdminPassword(email, password):
    admin = Admin.query.get(email)
    
    hashed_password = hashPassword(password)

    if admin:
        try:
            admin.password = hashed_password
            # admin.actualPassword = password
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": admin.json(),
                    "message": "Admin password updated."
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
                    "data": admin.json(),
                    "message": "An error occurred when updating admin password."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Admin not found."
            }
        ), 404

# Delete admin
@app.route("/deleteAdmin/<string:email>", methods=['DELETE'])
def deleteAdmin(email):
    admin = Admin.query.get(email)
    if admin:
        try:
            db.session.delete(admin)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": admin.json(),
                    "message": "Admin deleted."
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
                    "data": admin.json(),
                    "message": "An error occurred when deleting the admin."
                }
            ), 500
            
        finally:
            db.session.close()
            
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Admin not found."
            }
        ), 404


##<!-------------- FACULTY --------------!>##

# Add new Faculty
@app.route("/addFaculty", methods=['POST'])
def addFaculty():
    if request.is_json:
        facultyDetails = request.get_json()

        faculty = Faculty(
            email = facultyDetails['email'],
            name = facultyDetails['name'],
            password = facultyDetails['password']
            # actualPassword = facultyDetails['actualPassword'] 
        )

        try:
            db.session.add(faculty)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": faculty.json(),
                    "message": "Faculty created."
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
                    "data": faculty.json(),
                    "message": "An error occurred when creating the new faculty."
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

# Get an faculty
@app.route("/getFaculty/<string:email>")
def getFaculty(email):
    faculty = Faculty.query.get(email)
    
    if faculty:
        return jsonify(
            {
                "code": 200,
                "data": faculty.json(),
                "message": "Faculty retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Faculty not found."
        }
    ), 404

# Get all facultys
@app.route("/getAllFaculty")
def getAllFaculty():
    facultyList = Faculty.query.order_by(Faculty.name).all()
    
    if len(facultyList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "facultyList": [faculty.json() for faculty in facultyList]
                },
                "message": "All faculty retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No faculty found."
        }
    ), 404

# Update faculty information
@app.route("/updateFacultyInfo/<string:email>", methods=['PUT'])
def updateFacultyInfo(email):
    faculty = Faculty.query.get(email)

    if faculty:
        try:
            Faculty.query.filter(
                Faculty.email == email
            ).update(request.args.to_dict())
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": faculty.json(),
                    "message": "Faculty information updated."
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
                    "data": faculty.json(),
                    "message": "An error occurred when updating the faculty information."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Faculty not found."
            }
        ), 404
        
# Update faculty password
@app.route("/updateFacultyPassword/<string:email>/<string:password>", methods=['PUT'])
def updateFacultyPassword(email, password):
    faculty = Faculty.query.get(email)

    hashed_password = hashPassword(password)

    if faculty:
        try:
            faculty.password = hashed_password
            # faculty.actualPassword = password
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": faculty.json(),
                    "message": "Faculty password updated."
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
                    "data": faculty.json(),
                    "message": "An error occurred when updating the faculty password."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Faculty not found."
            }
        ), 404

# Delete faculty
@app.route("/deleteFaculty/<string:email>", methods=['DELETE'])
def deleteFaculty(email):
    faculty = Faculty.query.get(email)
    if faculty:
        try:
            db.session.delete(faculty)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": faculty.json(),
                    "message": "Faculty deleted."
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
                    "data": faculty.json(),
                    "message": "An error occurred when deleting the faculty."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Faculty not found."
            }
        ), 404


##<!-------------- INSTRUCTOR --------------!>##

# Add new Instructor
@app.route("/addInstructor", methods=['POST'])
def addInstructor():
    if request.is_json:
        instructorDetails = request.get_json()

        instructor = Instructor(
            email = instructorDetails['email'],
            name = instructorDetails['name'],
            password = instructorDetails['password']
            # actualPassword = instructorDetails['actualPassword']
        )

        try:
            db.session.add(instructor)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": instructor.json(),
                    "message": "Instructor created."
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
                    "data": instructor.json(),
                    "message": "An error occurred when creating the new instructor."
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

# Get an instructor
@app.route("/getInstructor/<string:email>")
def getInstructor(email):
    instructor = Instructor.query.get(email)
    
    if instructor:
        return jsonify(
            {
                "code": 200,
                "data": instructor.json(),
                "message": "Instructor retrieved."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Instructor not found."
        }
    ), 404

# Get all instructors
@app.route("/getAllInstructors")
def getAllInstructors():
    instructorList = Instructor.query.order_by(Instructor.name).all()
    
    if len(instructorList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "instructorList": [instructor.json() for instructor in instructorList]
                },
                "message": "All instructors retrieved."
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No instructor found."
        }
    ), 404

# Update instructor information
@app.route("/updateInstructorInfo/<string:email>", methods=['PUT'])
def updateInstructorInfo(email):
    instructor = Instructor.query.get(email)

    if instructor:
        try:
            Instructor.query.filter(
                Instructor.email == email
            ).update(request.args.to_dict())
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": instructor.json(),
                    "message": "Instructor information updated."
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
                    "data": instructor.json(),
                    "message": "An error occurred when updating the instructor information."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Instructor not found."
            }
        ), 404

# Update instructor password
@app.route("/updateInstructorPassword/<string:email>/<string:password>", methods=['PUT'])
def updateInstructorPassword(email, password):
    instructor = Instructor.query.get(email)

    hashed_password = hashPassword(password)

    if instructor:
        try:
            instructor.password = hashed_password
            # instructor.actualPassword = password
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": instructor.json(),
                    "message": "Instructor password updated."
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
                    "data": instructor.json(),
                    "message": "An error occurred when updating the instructor password."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Instructor not found."
            }
        ), 404

# Delete instructor
@app.route("/deleteInstructor/<string:email>", methods=['DELETE'])
def deleteInstructor(email):
    instructor = Instructor.query.get(email)
    if instructor:
        try:
            db.session.delete(instructor)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": instructor.json(),
                    "message": "Instructor deleted."
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
                    "data": instructor.json(),
                    "message": "An error occurred when deleting the instructor."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Instructor not found."
            }
        ), 404


##<!-------------- STUDENT --------------!>##

# Add new Student
@app.route("/addStudent", methods=['POST'])
def addStudent():
    if request.is_json:
        studentDetails = request.get_json()

        student = Student(
            email = studentDetails['email'],
            name = studentDetails['name'],
            password = studentDetails['password']
            # actualPassword = studentDetails['actualPassword'] 
        )

        try:
            db.session.add(student)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": student.json(),
                    "message": "Student created."
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
                    "data": student.json(),
                    "message": "An error occurred when creating the new student."
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

# Get all students
@app.route("/getAllStudents")
def getAllStudents():
    studentList = Student.query.order_by(Student.name).all()
    
    if len(studentList):
        print('Retrieved all students')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "studentList": [student.json() for student in studentList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No students found."
        }
    ), 404

# Get a student
@app.route("/getStudent/<string:email>")
def getStudent(email):
    student = Student.query.get(email)
    
    if student:
        print('Retrieved student')
        return jsonify(
            {
                "code": 200,
                "data": student.json(),
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Student not found."
        }
    ), 404

# Update student information
@app.route("/updateStudentInfo/<string:email>", methods=['PUT'])
def updateStudentInfo(email):
    student = Student.query.get(email)

    if student:
        try:
            Student.query.filter(
                Student.email == email
            ).update(request.args.to_dict())
            db.session.commit()
            print("Student information updated")

            return jsonify(
                {
                    "code": 200,
                    "data": student.json()
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
                    "data": student.json(),
                    "message": "An error occurred when updating the student."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Student not found."
            }
        ), 404
        
# Update student password
@app.route("/updateStudentPassword/<string:email>/<string:password>", methods=['PUT'])
def updateStudentPassword(email, password):
    student = Student.query.get(email)

    hashed_password = hashPassword(password)

    if student:
        try:
            student.password = hashed_password
            # student.actualPassword = password
            db.session.commit()
            print("Student password updated")

            return jsonify(
                {
                    "code": 200,
                    "data": student.json()
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
                    "data": student.json(),
                    "message": "An error occurred when updating the student."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Student not found."
            }
        ), 404

# Delete student
@app.route("/deleteStudent/<string:email>", methods=['DELETE'])
def deleteStudent(email):
    student = Student.query.get(email)
    if student:
        try:
            db.session.delete(student)
            db.session.commit()
            print("Student deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": student.json()
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
                    "data": student.json(),
                    "message": "An error occurred when deleting the student."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Student not found."
            }
        ), 404


##<!-------------- TATerm --------------!>##

# Add new TATerm
@app.route("/addTA", methods=['POST'])
def addTA():
    if request.is_json:
        taDetails = request.get_json()

        ta = TATerm(
            email = taDetails['email'],
            acadYear = taDetails['acadYear'],
            termNo = taDetails['termNo']
        )

        try:
            db.session.add(ta)
            db.session.commit()
            print("TATerm created")
            
            return jsonify(
                {
                    "code": 200,
                    "data": ta.json()
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
                    "data": ta.json(),
                    "message": "An error occurred when creating the new TATerm."
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

# Get a TA
@app.route("/getTA/<string:email>/<string:acadYear>/<int:termNo>")
def getTA(email, acadYear, termNo):
    ta = TATerm.query.filter(
        TATerm.email == email,
        TATerm.acadYear == acadYear,
        TATerm.termNo == termNo
    ).first()
    
    if ta:
        print('Retrieved TA')
        return jsonify(
            {
                "code": 200,
                "data": ta.json(),
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "TA not found."
        }
    ), 404

# Get all TAs in a Term
@app.route('/getAllTAByTerm/<string:acadYear>/<int:termNo>')
def getAllTAByTerm(acadYear, termNo):
    taList = db.session.query(TATerm, Student.name)\
        .join(Student, TATerm.email == Student.email)\
        .filter(
            TATerm.acadYear == acadYear,
            TATerm.termNo == termNo
        )\
        .order_by(
            Student.name
        ).all()
    
    if len(taList):
        print('Retrieved TAs in the term.')

        dataOutput = []
        for taInfo in taList:
            infoJson = taInfo[0].json()
            infoJson['name'] = taInfo[1]
            dataOutput.append(infoJson)

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No TAs found."
        }
    ), 404

# Delete TA
@app.route("/deleteTA/<string:email>/<string:acadYear>/<int:termNo>", methods=['DELETE'])
def deleteTA(email, acadYear, termNo):
    ta = TATerm.query.filter(
        TATerm.email == email,
        TATerm.acadYear == acadYear,
        TATerm.termNo == termNo
    ).first()

    if ta:
        try:
            db.session.delete(ta)
            db.session.commit()
            print("TA deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": ta.json()
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
                    "data": ta.json(),
                    "message": "An error occurred when deleting the ta."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "TA not found."
            }
        ), 404


##<!-------------- ENROLMENT --------------!>##

# Add new enrolment
@app.route("/addEnrolment", methods=['POST'])
def addEnrolment():
    if request.is_json:
        enrolmentDetails = request.get_json()

        enrolment = Enrolment(
            acadYear = enrolmentDetails['acadYear'], 
            termNo = enrolmentDetails['termNo'], 
            courseCode = enrolmentDetails['courseCode'],
            sectionNo = enrolmentDetails['sectionNo'],
            studentEmail = enrolmentDetails['studentEmail']
        )

        try:
            db.session.add(enrolment)
            db.session.commit()
            print("Enrolment created")

            return jsonify(
                {
                    "code": 200,
                    "data": enrolment.json()
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
                    "data": enrolment.json(),
                    "message": "An error occurred when creating the new enrolment."
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

# Add new enrolments in bulk
@app.route("/bulkAddEnrolment", methods=["POST"])
def bulkAddEnrolment():
    if request.is_json:
        enrolmentDetails = request.get_json()
        enrolmentObjects = enrolmentDetails['objects']

        try:
            db.session.bulk_insert_mappings(Enrolment, enrolmentObjects)
            db.session.commit()

            return jsonify(
                {
                    "code": 200,
                    "data": enrolmentObjects,
                    "message": "All enrolments created."
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
                    "data": enrolmentObjects,
                    "message": "An error occurred when creating the new enrolments."
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

# Get an enrolment
@app.route("/getEnrolment/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>")
def getEnrolment(acadYear, termNo, courseCode, sectionNo, studentEmail):
    enrolment = Enrolment.query.filter(
        Enrolment.acadYear == acadYear, 
        Enrolment.termNo == termNo, 
        Enrolment.courseCode == courseCode, 
        Enrolment.sectionNo == sectionNo, 
        Enrolment.studentEmail == studentEmail
    ).first()

    if enrolment:
        print('Retrieved enrolment')
        return jsonify(
            {
                "code": 200,
                "data": enrolment.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No enrolment found."
        }
    ), 404

# Get enrolment by section (class list)
@app.route("/getEnrolmentBySection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getEnrolmentBySection(acadYear, termNo, courseCode, sectionNo):
    enrolmentList = db.session.query(Enrolment, Student.name)\
        .join(Student, Enrolment.studentEmail == Student.email)\
        .filter(
            Enrolment.acadYear == acadYear, 
            Enrolment.termNo == termNo, 
            Enrolment.courseCode == courseCode, 
            Enrolment.sectionNo == sectionNo,
        )\
        .order_by(
            Student.name
        ).all()

    if len(enrolmentList):
        print('Retrieved all enrolment for student')

        dataOutput = []
        for enrolmentInfo in enrolmentList:
            infoJson = enrolmentInfo[0].json()
            infoJson['studentName'] = enrolmentInfo[1]
            dataOutput.append(infoJson)

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No enrolment found."
        }
    ), 404

# Get all enrolment by student in a term
@app.route("/getEnrolmentByStudent/<string:acadYear>/<int:termNo>/<string:studentEmail>")
def getEnrolmentByStudent(acadYear, termNo, studentEmail):
    enrolmentList = db.session.query(Enrolment, Student.email)\
        .join(Student, Enrolment.studentEmail == Student.email)\
        .filter(
            Enrolment.acadYear == acadYear, 
            Enrolment.termNo == termNo, 
            Enrolment.studentEmail == studentEmail,
        ).all()

    if len(enrolmentList):
        print('Retrieved all enrolment for student')

        dataOutput = []
        for enrolmentInfo in enrolmentList:
            infoJson = enrolmentInfo[0].json()
            infoJson['studentName'] = enrolmentInfo[1]
            dataOutput.append(infoJson)

        return jsonify(
            {
                "code": 200,
                "data": dataOutput
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No enrolment found."
        }
    ), 404

# Delete enrolment
@app.route("/deleteEnrolment/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>", methods=['DELETE'])
def deleteEnrolment(acadYear, termNo, courseCode, sectionNo, studentEmail):
    enrolment = Enrolment.query.filter(
        Enrolment.acadYear == acadYear, 
        Enrolment.termNo == termNo, 
        Enrolment.courseCode == courseCode, 
        Enrolment.sectionNo == sectionNo, 
        Enrolment.studentEmail == studentEmail
    ).first()

    if enrolment:
        try:
            db.session.delete(enrolment)
            db.session.commit()
            print("Enrolment deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": enrolment.json()
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
                    "data": enrolment.json(),
                    "message": "An error occurred when deleting the enrolment."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "No enrolment found."
            }
        ), 404

# Delete all enrolment in a Section
@app.route("/deleteAllEnrolmentBySection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>", methods=['DELETE'])
def deleteAllEnrolmentBySection(acadYear, termNo, courseCode, sectionNo):
    enrolmentList = Enrolment.query.filter(
        Enrolment.acadYear == acadYear, 
        Enrolment.termNo == termNo, 
        Enrolment.courseCode == courseCode, 
        Enrolment.sectionNo == sectionNo
    ).all()

    if len(enrolmentList):
        try:
            Enrolment.query.filter(
                Enrolment.acadYear == acadYear, 
                Enrolment.termNo == termNo, 
                Enrolment.courseCode == courseCode, 
                Enrolment.sectionNo == sectionNo
            ).delete()
            db.session.commit()
            print("Enrolments deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": [enrolment.json() for enrolment in enrolmentList]
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
                    "data": [enrolment.json() for enrolment in enrolmentList],
                    "message": "An error occurred when deleting the enrolments."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "No enrolment found."
            }
        ), 404

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=USER_PORT)
    else:
        app.run(host='0.0.0.0', port=USER_PORT)