from flask import request, jsonify
from models import app, db, Course, CourseOffering
import os
from dotenv import load_dotenv
load_dotenv()

COURSE_PORT = os.getenv("COURSE_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


###<!-------------- COURSE --------------!>###

# Add new course
@app.route("/addCourse", methods=['POST']) 
def addCourse():
    if request.is_json:
        courseDetails = request.get_json()

        course = Course(
            courseCode = courseDetails['courseCode'],
            courseName = courseDetails['courseName'],
        )

        try:
            db.session.add(course)
            db.session.commit()
            print('Course created')

            return jsonify(
                {
                    "code":200,
                    "data":course.json()
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
                    "data": course.json(),
                    "message": "An error occurred when creating the new course."
                }
            ), 500
            
        finally:
            db.session.close()

    return jsonify(
        {
            "code": 500,
            "message": 'Input is not JSON.'
        }
    ), 500

# Get course by PK
@app.route("/getCourse/<string:courseCode>")
def getCourse(courseCode):
    course = Course.query.get(courseCode)
    
    if course:
        print('Retrieved course')
        return jsonify(
            {
                "code": 200,
                "data": course.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Course not found."
        }
    ), 404

# Get all courses
@app.route("/getAllCourses")
def getAllCourses():
    courseList = Course.query.all()

    if len(courseList):
        print('Retrieved all courses.')
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in courseList]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No courses found."
        }
    ), 404

# Update Course information
@app.route("/updateCourseInfo/<string:courseCode>", methods=['PUT'])
def updateCourseInfo(courseCode):
    course = Course.query.get(courseCode)

    if course:
        try:
            Course.query.filter(
                Course.courseCode == courseCode
            ).update(request.args.to_dict())
            db.session.commit()
            print("Course information updated")

            return jsonify(
                {
                    "code": 200,
                    "data": course.json()
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
                    "data": course.json(),
                    "message": "An error occurred when updating the course."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Course not found."
            }
        ), 404

# Delete course
@app.route("/deleteCourse/<string:courseCode>", methods=['DELETE'])
def deleteCourse(courseCode):
    course = Course.query.get(courseCode)
    
    if course:
        try:
            db.session.delete(course)
            db.session.commit()
            print("Course deleted")

        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code":500,
                    "data": course.json(),
                    "message": "An error occurred when deleting the course."
                }
            ), 500
            
        finally:
            db.session.close()

        return jsonify(
            {
                "code":200,
                "data":course.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Course not found."
        }
    ), 404


###<!-------------- COURSE OFFERING--------------!>###

# Add course offering
@app.route("/addCourseOffering", methods=['POST'])
def addCourseOffering():
    if request.is_json:
        courseOfferingDetails = request.get_json()

        courseOffering = CourseOffering(
            acadYear = courseOfferingDetails['acadYear'], 
            termNo = courseOfferingDetails['termNo'],
            courseCode=courseOfferingDetails['courseCode']
        )
        try: 
            db.session.add(courseOffering)
            db.session.commit()
            print('Course offering created')

            return jsonify(
                {
                    "code":200,
                    "data":courseOffering.json()
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
                    "data": courseOffering.json(),
                    "message": "An error occurred when creating the new course offering."
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

# Get course offering by PK
@app.route("/getCourseOffering/<string:acadYear>/<int:termNo>/<string:courseCode>")
def getCourseOffering(acadYear, termNo, courseCode):
    courseOffering = CourseOffering.query.filter(
        CourseOffering.acadYear == acadYear,
        CourseOffering.termNo == termNo,
        CourseOffering.courseCode == courseCode
    ).first()
    
    if courseOffering:
        print('Retrieved course offering')
        return jsonify(
            {
                "code": 200,
                "data": courseOffering.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Course Offering not found."
        }
    ), 404

# Get course offerings by term
@app.route("/getCourseOfferingsByTerm/<string:acadYear>/<int:termNo>")
def getCourseOfferingsByTerm(acadYear, termNo):
    courseOfferingList = db.session.query(CourseOffering, Course.courseName)\
        .join(Course, CourseOffering.courseCode == Course.courseCode)\
        .filter(
            CourseOffering.acadYear == acadYear, 
            CourseOffering.termNo == termNo
        ).all()
    
    if len(courseOfferingList):
        print('Retrieved course offerings for term')

        dataOutput = []
        for courseOfferingInfo in courseOfferingList:
            infoJson = courseOfferingInfo[0].json()
            infoJson['courseName'] = courseOfferingInfo[1]
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
            "message": "No course offerings found in this term."
        }
    ), 404

# Update Course Offering information
@app.route("/updateCourseOfferingInfo/<string:acadYear>/<int:termNo>/<string:courseCode>", methods=['PUT'])
def updateCourseOfferingInfo(acadYear, termNo, courseCode):
    courseOffering = CourseOffering.query.filter(
        CourseOffering.acadYear == acadYear,
        CourseOffering.termNo == termNo,
        CourseOffering.courseCode == courseCode
    ).first()

    if courseOffering:
        try:
            CourseOffering.query.filter(
                CourseOffering.acadYear == acadYear,
                CourseOffering.termNo == termNo,
                CourseOffering.courseCode == courseCode
            ).update(request.args.to_dict())
            db.session.commit()
            print("Course Offering information updated")

            return jsonify(
                {
                    "code": 200,
                    "data": courseOffering.json()
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
                    "data": courseOffering.json(),
                    "message": "An error occurred when updating the course offering."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Course Offering not found."
            }
        ), 404

# Delete Course Offering
@app.route("/deleteCourseOffering/<string:acadYear>/<int:termNo>/<string:courseCode>", methods=['DELETE'])
def deleteCourseOffering(acadYear, termNo, courseCode):
    courseOffering = CourseOffering.query.filter(
        CourseOffering.acadYear == acadYear,
        CourseOffering.termNo == termNo,
        CourseOffering.courseCode == courseCode
    ).first()
    
    if courseOffering:
        try:
            db.session.delete(courseOffering)
            db.session.commit()
            print("Course offering deleted")

        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code":500,
                    "data": courseOffering.json(),
                    "message": "An error occurred when deleting the course offering."
                }
            ), 500
            
        finally:
            db.session.close()

        return jsonify(
            {
                "code":200,
                "data":courseOffering.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Course offering not found."
        }
    ), 404

if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=COURSE_PORT)
    else:
        app.run(host='0.0.0.0', port=COURSE_PORT)