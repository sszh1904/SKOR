from flask import request, jsonify
from models import app, db, Section, PriorityCall
import os
from dotenv import load_dotenv
load_dotenv()

SECTION_PORT = os.getenv("SECTION_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")


##<!-------------- SECTION --------------!>##

# Add new section
@app.route("/addSection", methods=['POST'])
def addSection():
    if request.is_json:
        sectionDetails = request.get_json()

        section = Section(
            acadYear = sectionDetails['acadYear'],
            termNo = sectionDetails['termNo'],
            courseCode = sectionDetails['courseCode'],
            sectionNo = sectionDetails['sectionNo'],
            facultyEmail = sectionDetails['facultyEmail'],
            instructorEmail = sectionDetails['instructorEmail'],
            taEmail = sectionDetails['taEmail'],
            day = sectionDetails['day'],
            startDate = sectionDetails['startDate'],
            startTime = sectionDetails['startTime'],
            endTime = sectionDetails['endTime'],
        )

        try:
            db.session.add(section)
            db.session.commit()
            print('Section created')

            return jsonify(
                {
                    "code": 200,
                    "data": section.json()
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
                    "data": section.json(),
                    "message": "An error occurred when creating the new section."
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

# Get section by PK
@app.route("/getSection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getSection(acadYear, termNo, courseCode, sectionNo):
    section = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.courseCode == courseCode, 
        Section.sectionNo == sectionNo
    ).first()
    
    if section:
        print('Retrieved section')
        return jsonify(
            {
                "code": 200,
                "data": section.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Section not found."
        }
    ), 404

# Get sections by course in a term
@app.route("/getSectionsByCourse/<string:acadYear>/<int:termNo>/<string:courseCode>")
def getSectionsByCourse(acadYear, termNo, courseCode):
    sectionList = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.courseCode == courseCode
    ).all()
    
    if len(sectionList):
        print(f'Retrieved sections for course {courseCode} in {acadYear} {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": [section.json() for section in sectionList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for course {courseCode} in {acadYear} {termNo}."
        }
    ), 404

# Get sections by term and by TA
@app.route("/getSectionsByTermByTA/<string:acadYear>/<int:termNo>/<string:taEmail>")
def getSectionsByTermByTA(acadYear, termNo, taEmail):
    sectionList = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.taEmail == taEmail
    ).all()

    if len(sectionList):
        print(f'Retrieved sections for {taEmail} in {acadYear} {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": [section.json() for section in sectionList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {taEmail} in {acadYear} {termNo}."
        }
    ), 404

# Get sections by term and by Faculty
@app.route("/getSectionsByTermByFaculty/<string:acadYear>/<int:termNo>/<string:facultyEmail>")
def getSectionsByTermByFaculty(acadYear, termNo, facultyEmail):
    sectionList = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.facultyEmail == facultyEmail
    ).all()

    if len(sectionList):
        print(f'Retrieved sections for {facultyEmail} in {acadYear} {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": [section.json() for section in sectionList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {facultyEmail} in {acadYear} {termNo}."
        }
    ), 404

# Get sections by term and by Instructor
@app.route("/getSectionsByTermByInstructor/<string:acadYear>/<int:termNo>/<string:instructorEmail>")
def getSectionsByTermByInstructor(acadYear, termNo, instructorEmail):
    sectionList = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.instructorEmail == instructorEmail
    ).all()

    if len(sectionList):
        print(f'Retrieved sections for {instructorEmail} in {acadYear} {termNo}.')

        return jsonify(
            {
                "code": 200,
                "data": [section.json() for section in sectionList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": f"No sections found for {instructorEmail} in {acadYear} {termNo}."
        }
    ), 404

# Update section configurations/info
@app.route("/updateSectionConfig/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>", methods=['PUT'])
def updateSectionConfig(acadYear, termNo, courseCode, sectionNo):
    section = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.courseCode == courseCode, 
        Section.sectionNo == sectionNo
    ).first()

    if section:
        try:
            Section.query.filter(
                Section.acadYear == acadYear, 
                Section.termNo == termNo,
                Section.courseCode == courseCode,
                Section.sectionNo == sectionNo
            ).update(request.args.to_dict())
            db.session.commit()

            print(f'Configuration updated for {courseCode} section {sectionNo} in {acadYear} {termNo}.')

            return jsonify(
                    {
                        "code": 200,
                        "data": section.json()
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
                    "data": section.json(),
                    "message": "An error occurred when updating the configurations."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": f"No section found for {courseCode} in {acadYear} {termNo}."
            }
        ), 404

# Delete section
@app.route("/deleteSection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>", methods=['DELETE'])
def deleteSection(acadYear, termNo, courseCode, sectionNo):
    section = Section.query.filter(
        Section.acadYear == acadYear, 
        Section.termNo == termNo, 
        Section.courseCode == courseCode, 
        Section.sectionNo == sectionNo
    ).first()
    
    if section:
        try:
            db.session.delete(section)
            db.session.commit()
            print(f"{courseCode} section {sectionNo} in {acadYear} {termNo} deleted.")
        
        except Exception as e:
            db.session.rollback()
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code": 500,
                    "data": section.json(),
                    "message": "An error occurred when deleting the section."
                }
            ), 500

        finally:
            db.session.close()

        return jsonify(
            {
                "code": 200,
                "data": section.json()
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 404,
                "message": f"No section found for {courseCode} in {acadYear} {termNo}."
            }
        ), 404


##<!-------------- PRIORITYCALL --------------!>##

# Add new priority call
@app.route("/addPriorityCall", methods=['POST'])
def addPriorityCall():
    if request.is_json:
        priorityCallDetails = request.get_json()

        priorityCall = PriorityCall(
            acadYear = priorityCallDetails['acadYear'], 
            termNo = priorityCallDetails['termNo'], 
            courseCode = priorityCallDetails['courseCode'],
            sectionNo = priorityCallDetails['sectionNo'],
            studentEmail = priorityCallDetails['studentEmail']
        )

        try:
            db.session.add(priorityCall)
            db.session.commit()
            print("PriorityCall created")

            return jsonify(
                {
                    "code": 200,
                    "data": priorityCall.json()
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
                    "data": priorityCall.json(),
                    "message": "An error occurred when creating the new PriorityCall."
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

# Get all priorityCall in a Section
@app.route("/getPriorityCallBySection/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>")
def getPriorityCallBySection(acadYear, termNo, courseCode, sectionNo):
    priorityCallList = PriorityCall.query.filter(
            PriorityCall.acadYear == acadYear, 
            PriorityCall.termNo == termNo, 
            PriorityCall.courseCode == courseCode, 
            PriorityCall.sectionNo == sectionNo,
        ).all()

    if len(priorityCallList):
        print('Retrieved all priorityCalls')

        return jsonify(
            {
                "code": 200,
                "data": [priorityCall.json() for priorityCall in priorityCallList]
            }
        ), 200
    return jsonify(
        {
            "code": 404, 
            "message": "No priorityCalls found"
        }
    ), 404

# Delete priorityCall
@app.route("/deletePriorityCall/<string:acadYear>/<int:termNo>/<string:courseCode>/<int:sectionNo>/<string:studentEmail>", methods=['DELETE'])
def deletePriorityCall(acadYear, termNo, courseCode, sectionNo, studentEmail):
    priorityCall = PriorityCall.query.filter(
        PriorityCall.acadYear == acadYear, 
        PriorityCall.termNo == termNo, 
        PriorityCall.courseCode == courseCode, 
        PriorityCall.sectionNo == sectionNo, 
        PriorityCall.studentEmail == studentEmail
    ).first()

    if priorityCall:
        try:
            db.session.delete(priorityCall)
            db.session.commit()
            print("PriorityCall deleted")

            return jsonify(
                {
                    "code": 200,
                    "data": priorityCall.json()
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
                    "data": priorityCall.json(),
                    "message": "An error occurred when deleting the PriorityCall."
                }
            ), 500
            
        finally:
            db.session.close()

    else:
        return jsonify(
            {
                "code": 404,
                "message": "PriorityCall not found."
            }
        ), 404


if __name__=='__main__':
    if os.getenv("LOCAL") == 'False':
        app.run(ssl_context=(CERTFILE, KEYFILE), host='0.0.0.0', port=SECTION_PORT)
    else:
        app.run(host='0.0.0.0', port=SECTION_PORT)