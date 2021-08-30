// ***********************  GENERAL  ***********************
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

var toDeleteUrl;

async function confirmDelete() {
    const responseData = await sendDelRequest(toDeleteUrl);
	if (responseData.code == 200) {
        location.reload();
	}
}

function reload() {
    window.location.reload();
}

function showAlert(status) {
    const alerts = document.getElementsByTagName("alert");
    for (let alert of alerts) {
        let alertName = alert.id.split("-")[0];
        if (alertName == status) {
            alert.style.display="inline-block";
        }
        else {
            alert.style.display="none";
        }
    }
}

function showModalAlert(status) {
    const alerts = document.getElementsByTagName("alert");
    for (let alert of alerts) {
        let alertName = alert.id.split("-")[0];
        if (alertName == status) {
            alert.style.display="block";
        }
        else {
            alert.style.display="none";
        }
    }
}

// ---------- GET HTML PAGE ---------- 
// Redirect to login page if user directly access in-app pages without logging in
const path = window.location.pathname;
const page = path.split("/").pop();
if (page != "about.html" && page != "index.html" && page != "contact.html") {
    const sessionIdentity = sessionStorage.getItem('identity');
    if (sessionIdentity == null) {
        window.location.replace("index.html");
    }
}

// ---------- LOGIN PAGE ---------- 
function resetResetPassword() {
    document.getElementById("reset-password-after").style.display = "none";
    document.getElementById("reset-password-before").style.display = "block";
}

async function chooseUserType(userType) {
    let userDetails = JSON.parse(sessionStorage.getItem("mixed"));
    sessionStorage.setItem("identity", userType)
    sessionStorage.setItem(userType, JSON.stringify(userDetails));
    window.location.replace(userType + "_home.html");
}

function goToHome() {
    const accountIdentity = sessionStorage.getItem("identity");
    if (accountIdentity == "mixed") {
        window.location.replace("choose_user.html");
    }
    else if (accountIdentity == "student") {
        window.location.replace("student_home.html");
    }
    else if (accountIdentity == "admin") {
        window.location.replace("admin_home.html");
    }
    else {
        window.location.replace("ta_home.html");
    }
}

// ---------- MANUAL/AUTO LOGOUT ---------- 
var timeout = 1800000; // 30min idle timeout
var timeoutTimerID;

function startTimer() {
    timeoutTimerID = window.setTimeout(idleTimeout, timeout);
}

function resetTimer() {
    window.clearTimeout(timeoutTimerID);
    startTimer();
}

function idleTimeout() {
    logout();
}

function setupTimers() {
    document.addEventListener("mousemove", resetTimer, false);
    document.addEventListener("mousedown", resetTimer, false);
    document.addEventListener("keypress", resetTimer, false);
    document.addEventListener("touchmove", resetTimer, false);
    document.addEventListener("onscroll", resetTimer, false);
    startTimer();
}

async function logout() {
    let identity = sessionStorage.getItem("identity");
    let user = JSON.parse(sessionStorage.getItem(identity));
    let loginTime = sessionStorage.getItem("loginTime");
    if (identity == "ta" || identity == "mixed") {
        identity = "student"
    }
    updateLoginStatusUrl = dns + userPort + "/update" + identity.charAt(0).toUpperCase() + identity.substring(1) + "Info/" + user.email + "?isLogin=0&lastLogin=" + loginTime;
    try {
        const updateLoginStatusData = await sendPutRequest(updateLoginStatusUrl);
        if (updateLoginStatusData.code == 200) {
            sessionStorage.clear();
            window.location.replace("index.html");
        }
    } catch (error) {
        console.log(error);
    }
}

// ---------- POINTER ---------- 
function loadingPointer() {
    document.body.style.cursor='wait';
}

function defaultPointer() {
    document.body.style.cursor='default';
}

// ************************  ADMIN  ************************
// ---------- TERM ---------- 
async function displayAllTerms() {
    try {
        const responseData = await sendGetRequest(dns + termPort + "/getAllTerms");
        let termContainer = document.getElementById('term-container');
        termContainer.innerHTML = `
            <button class="btn btn-create-new" data-bs-toggle="modal" data-bs-target="#create-term"><h4><img id="plus-icon" src="images/plus.svg">Add New Term</h4></button>
        `;
        let termsContent = "";
        let termList = responseData.data.terms;
        termList.forEach(term => {
            let termContent = "";
            let acadYear = term.acadYear;
            let termNo = term.termNo;
            let startDate = term.startDate;
            startDate = startDate.replaceAll("-", "/");
            let endDate = term.endDate;
            endDate = endDate.replaceAll("-", "/");
            let isCurrent = term.isCurrent;
            termContent = `
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="module-section">
                            <button class="btn btn-light float-end session-dropdown" data-bs-toggle="dropdown" aria-expanded=False><img id="arrow-down" src="images/arrow_down.svg"></button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="#" onclick="updateTerm('${acadYear}', '${termNo}')">Set Current</a></li>
                                <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#delete-term" onclick="deleteTerm('${acadYear}', '${termNo}')">Delete</a></li>
                            </ul>
                            <div class="module-text-container">
                                <overline>TERM</overline>
                            </div>
                            <div class="module-text-container">
                                <h4 class="mb-2 d-inline">${acadYear} Term ${termNo}</h4>`;
            if (isCurrent) {
                termContent += `
                            <div class="badge current-badge ms-2">
                                <overline>CURRENT</overline>
                            </div>`;
            }
            termContent += `         
                                <br>
                                <overline>${startDate} - ${endDate}</overline>
                                <a href="#"><button class="btn btn-primary float-end" onclick="selectTerm('${acadYear}', '${termNo}')">Select</button></a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            termsContent = termContent + termsContent;
        });
        termContainer.innerHTML += termsContent;
    } catch (error) {
        console.log(error);
    }
}

function setMinEndDate(date) {
    document.getElementById("endDate").min = date;
}

function setMaxStartDate(date) {
    document.getElementById("startDate").max = date;
}

async function updateTerm(acadYear, termNo) {
    const url = dns + termPort + "/updateTerm/" + acadYear + "/" + termNo;
    const response = await fetch(url, {
            method: "PUT",
            mode: "cors", 
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

    if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }
    location.reload();
}

async function selectTerm(acadYear, termNo) {
    const term = await sendGetRequest(dns + termPort + "/getTerm/" + acadYear + "/" + termNo);
    sessionStorage.setItem("term", JSON.stringify(term.data));
    window.location.replace("admin_term.html");
}

function deleteTerm(acadYear, termNo) {
    toDeleteUrl = dns + termPort + "/deleteTerm/" + acadYear + "/" + termNo;
}

// ---------- COURSE  ---------- 
async function displayAllCourses() {
    const url = dns + coursePort + "/getAllCourses";
    try {
        const responseData = await sendGetRequest(url);
        let courseContainer = document.getElementById('course-container');

        let courseList = responseData.data.courses;
        courseList.forEach(course => {
            let courseCode = course.courseCode;
            let courseName = course.courseName;

            courseContainer.innerHTML += `
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${courseCode}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4>${courseName}</h4>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 text-end">
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#update-course" onclick="fillCourseForm('${courseCode}', '${courseName}')"><img class="admin-display-icon" src="images/pencil.svg"></button>
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#delete-course" onclick="deleteCourse('${courseCode}')"><img class="admin-display-icon" src="images/bin.svg"></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.log(error);
    }
}

function fillCourseForm(courseCode, courseName) {
    document.getElementById("updateCourseCode").value = courseCode;
    document.getElementById("displayCourseCode").value = courseCode;
    document.getElementById("updateCourseName").value = courseName;
}

function deleteCourse(courseCode) {
    toDeleteUrl = dns + coursePort + "/deleteCourse/" + courseCode;
}

// ------ COURSE OFFERING ------
async function displayCoursesByTerm() {
    const term = JSON.parse(sessionStorage.getItem('term'));
    const acadYear = term.acadYear;
    const termNo = term.termNo;
    const startDate = term.startDate;
    const endDate = term.endDate;
    displayTermHeader(acadYear, termNo, startDate, endDate);
    fillCourseInput();
    const url = dns + coursePort + "/getCourseOfferingsByTerm/" + acadYear + "/" + termNo;
    try {
        const responseData = await sendGetRequest(url);
        let courseContainer = document.getElementById('course-container');
        courseContainer.innerHTML = `
            <button class="btn btn-create-new" data-bs-toggle="modal" data-bs-target="#add-course-offering"><h4><img id="plus-icon" src="images/plus.svg">Add Course Offering</h4></button>
        `;
        let coursesContent = "";
        let courseList = responseData.data;
        courseList.forEach(course => {
            let courseCode = course.courseCode;
            let courseName = course.courseName;
            
            coursesContent += `
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="module-section">
                            <button class="btn btn-light float-end session-dropdown" data-bs-toggle="dropdown" aria-expanded=False><img id="arrow-down" src="images/arrow_down.svg"></button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#delete-course-offering" onclick="deleteCourseOffering('${acadYear}', '${termNo}', '${courseCode}')">Delete</a></li>
                            </ul>
                            <div class="module-text-container">
                                <overline>${courseCode}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4 class="mb-2 d-inline">${courseName}</h4>
                                <a href="#"><button class="btn btn-primary float-end" onclick="selectCourse('${courseCode}')">Select</button></a>
                            </div>
                        </div>
                    </div>
                </div>`;
        });
        courseContainer.innerHTML += coursesContent;
    } catch (error) {
        console.log(error);
    }
}

function displayTermHeader(acadYear, termNo, startDate, endDate) {
    startDate = startDate.replaceAll("-", "/");
    endDate = endDate.replaceAll("-", "/");
    document.getElementById("term-header").innerHTML = `
        <div class="module-text-container mb-2">
            <h2 class="mb-0">${acadYear} Term ${termNo}</h2>
        </div>
        <div class="module-text-container mb-5">
            <s1 class="tertiary-dark-2 mb-0">${startDate} - ${endDate}</s1>
        </div>`;
}

async function selectCourse(courseCode) {
    const course = await sendGetRequest(dns + coursePort + "/getCourse/" + courseCode);
    sessionStorage.setItem("course", JSON.stringify(course.data));
    window.location.replace("admin_course_offering.html");
}

function deleteCourseOffering(acadYear, termNo, courseCode) {
    toDeleteUrl = dns + coursePort + "/deleteCourseOffering/" + acadYear + "/" + termNo + "/" + courseCode;
}

async function fillCourseInput() {
    const url = dns + coursePort + "/getAllCourses";
    const courseSelect = document.getElementById('courseOffering');
    courseSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        const courses = responseData.data.courses;
        courses.forEach(course => {
            courseSelect.innerHTML += `<option value="${course.courseCode}">${course.courseName}</option>`;
        })
    } catch (error) {
        console.log(error);
    }
}

// ---------- SECTION ---------- 
async function displayAllSections() {
    const term = JSON.parse(sessionStorage.getItem("term"));
    const course = JSON.parse(sessionStorage.getItem("course"));
    const acadYear = term.acadYear;
    const termNo = term.termNo;
    const courseCode = course.courseCode;
    const courseName = course.courseName;
    displayCourseHeader(acadYear, termNo, courseCode, courseName);
    const url = dns + displayInfoPort + "/getSectionsInfoByCourse/" + acadYear + "/" + termNo + "/" + courseCode;
    try {
        const responseData = await sendGetRequest(url);
        let sectionContainer = document.getElementById('section-container');
        sectionContainer.innerHTML = `
            <button class="btn btn-create-new" data-bs-toggle="modal" data-bs-target="#create-section"><h4><img id="plus-icon" src="images/plus.svg">Add New Section</h4></button>
        `;
        let sectionContent = "";
        let sectionList = responseData.data;
        sectionList.forEach(section => {
            let sectionNo = section.sectionNo;
            let facName = section.facultyName;
            let facEmail = section.facultyEmail;
            let instrName = section.instructorName;
            let instrEmail = section.instructorEmail;
            let taName = section.taName;
            let taEmail = section.taEmail;
            let day = section.day;
            let startTime = section.startTime;
            let endTime = section.endTime;
            let startDate = section.startDate;
            let educators = facEmail;
            let educatorsDisplay = facName;
            if (instrEmail != null && taEmail != null) {
                educatorsDisplay = facName + ", " + instrName + ", " + taName;
                educators = facEmail + "/" + instrEmail + "/" + taEmail;
            } else if (instrEmail != null) {
                educatorsDisplay = facName + ", " + instrName;
                educators = facEmail + "/" + instrEmail;
            } else if (taEmail != null) {
                educatorsDisplay = facName + ", " + taName;
                educators = facEmail + "/" + taEmail;
            }
                sectionContent += `
                    <div class="card module admin-display-container">
                        <div class="card-body row">
                            <div class="col-md-9 col-lg-10 module-section">
                                <div class="module-text-container">
                                    <overline>${educatorsDisplay}</overline>
                                </div>
                                <div class="module-text-container">
                                    <h4>G${sectionNo}</h4>
                                </div>
                            </div>
                            <div class="col-md-3 col-lg-2 module-section module-right-section">
                                <button class="btn btn-light float-end session-dropdown" data-bs-toggle="dropdown" aria-expanded=False><img id="arrow-down" src="images/arrow_down.svg"></button>
                                <ul class="dropdown-menu dropdown-menu-end">
                                    <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#update-section" onclick="fillSectionForm('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${educators}', '${day}', '${startTime}', '${endTime}', '${startDate}')">Update</a></li>
                                    <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#delete-section" onclick="deleteSection('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}')">Delete</a></li>
                                </ul>
                                <div class="module-enter-container">
                                    <div class="module-text-container">
                                        <overline>${day}</overline>
                                    </div>
                                    <div class="module-text-container">
                                        ${startTime} - ${endTime}<br>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;
        });
        sectionContainer.innerHTML += sectionContent;
        defaultPointer();
    } catch (error) {
        defaultPointer();
        console.log(error);
    }
    fillTAInput();
    loadAllTA(); 
    loadAllFac(); 
    loadAllInstr(); 
    updateLoadAllTA(); 
    updateLoadAllFac(); 
    updateLoadAllInstr();
}

function setMinEndTime(id, time) {
    let select = document.getElementById(id);
    for (let child of select.children) {
        if (child.value < time) {
            child.disabled = true;
        }
        else {
            child.disabled = false;
        }
    }
}

function setMaxStartTime(id, time) {
    let select = document.getElementById(id);
    for (let child of select.children) {
        if (child.value > time) {
            child.disabled = true;
        }
        else {
            child.disabled = false;
        }
    }
}

function displayCourseHeader(acadYear, termNo, courseCode, courseName) {
    document.getElementById("course-header").innerHTML = `
        <div class="module-text-container mb-2">
            <h3 class="tertiary-dark-2 mb-0">${courseCode}</h3>
        </div>
        <div class="module-text-container mb-2">
            <h2 class="mb-0">${courseName}</h2>
        </div>
        <div class="module-text-container tertiary-dark-2 mb-5">
            <s2 class="mb-0">${acadYear} Term ${termNo}</s2>
        </div>`;
}

async function loadAllTA() {
    const term = JSON.parse(sessionStorage.getItem("term"));
    const url = dns + userPort + "/getAllTAByTerm" + "/" + term.acadYear + "/" + term.termNo;
    let taSelect = document.getElementById('taSelect');
    taSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        let taList = responseData.data;
        taList.forEach(ta => {
            let taEmail = ta.email;
            let taName = ta.name;
            
            taSelect.innerHTML += `<option value="${taEmail}">${taName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

async function loadAllFac() {
    const url = dns + userPort + "/getAllFaculty";
    let facSelect = document.getElementById('facSelect');
    facSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        let facList = responseData.data.facultyList;
        facList.forEach(faculty => {
            let facEmail = faculty.email;
            let facName = faculty.name;
            
            facSelect.innerHTML += `<option value="${facEmail}">${facName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

async function loadAllInstr() {
    const url = dns + userPort + "/getAllInstructors";
    let instrSelect = document.getElementById('instrSelect');
    instrSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        let instrList = responseData.data.instructorList;
        instrList.forEach(instructor => {
            let instrEmail = instructor.email;
            let instrName = instructor.name;
            
            instrSelect.innerHTML += `<option value="${instrEmail}">${instrName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

async function updateLoadAllTA() {
    const term = JSON.parse(sessionStorage.getItem("term"));
    const url = dns + userPort + "/getAllTAByTerm" + "/" + term.acadYear + "/" + term.termNo;
    let taSelect = document.getElementById('updateTASelect');
    taSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        let taList = responseData.data;
        taList.forEach(ta => {
            let taEmail = ta.email;
            let taName = ta.name;
            
            taSelect.innerHTML += `<option id="${taEmail}" value="${taEmail}">${taName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

async function updateLoadAllFac() {
    const url = dns + userPort + "/getAllFaculty";
    let facSelect = document.getElementById('updateFacSelect');
    try {
        const responseData = await sendGetRequest(url);
        let facList = responseData.data.facultyList;
        facList.forEach(faculty => {
            let facEmail = faculty.email;
            let facName = faculty.name;
            
            facSelect.innerHTML += `<option id="${facEmail}" value="${facEmail}">${facName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

async function updateLoadAllInstr() {
    const url = dns + userPort + "/getAllInstructors";
    let instrSelect = document.getElementById('updateInstrSelect');
    instrSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        let instrList = responseData.data.instructorList;
        instrList.forEach(instructor => {
            let instrEmail = instructor.email;
            let instrName = instructor.name;
            
            instrSelect.innerHTML += `<option id="${instrEmail}" value="${instrEmail}">${instrName}</option>`;
        });
    } catch (error) {
        console.log(error);
    }   
}

function fillSectionForm(acadYear, termNo, courseCode, sectionNo, educators, day, startTime, endTime, startDate) {
    document.getElementById("acadYear").value = acadYear;
    document.getElementById("termNo").value = termNo;
    document.getElementById("courseCode").value = courseCode;
    document.getElementById("updateSectionNo").value = sectionNo;
    document.getElementById("displaySectionNo").value = "G" + sectionNo;
    educators = educators.split("/");
    console.log(educators);
    for (let i = 0; i < educators.length; i++) {
        let id = educators[i];
        document.getElementById(id).selected = true;
    }
    document.getElementById(day).selected = true;
    document.getElementById("start-" + startTime).selected = true;
    document.getElementById("end-" + endTime).selected = true;
    document.getElementById("updateStartDate").value = startDate;
}

function deleteSection(acadYear, termNo, courseCode, sectionNo) {
    toDeleteUrl = dns + sectionPort + "/deleteSection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
}

// ---------- TA ---------- 
async function displayAllTA() {
    const term = JSON.parse(sessionStorage.getItem("term"));
    const acadYear = term.acadYear;
    const termNo = term.termNo;
    fillTAInput();
    const url = dns + userPort + "/getAllTAByTerm" + "/" + acadYear + "/" + termNo;
    try {
        const responseData = await sendGetRequest(url);
        let taContainer = document.getElementById('ta-container');
        
        let taList = responseData.data;
        taList.forEach(ta => {
            let taEmail = ta.email;
            let taName = ta.name;
            
            taContainer.innerHTML += ` 
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${taEmail}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4>${taName}</h4>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 text-end">
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#delete-ta" onclick="deleteTA('${taEmail}')"><img class="admin-display-icon" src="images/bin.svg"></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.log(error);
    }
}

async function fillTAInput() {
    const url = dns + userPort + "/getAllStudents";
    const select = document.getElementById('ta');
    select.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const responseData = await sendGetRequest(url);
        const students = responseData.data.studentList;
        students.forEach(student => {
            select.innerHTML += `<option value="${student.email}">${student.name}</option>`;
        })
    } catch (error) {
        console.log(error);
    }
}

function deleteTA(taEmail, acadYear, termNo) {
    toDeleteUrl = dns + userPort + "/deleteTA/" + taEmail + "/" + acadYear + "/" + termNo;
}

// ---------- FACULTY ---------- 
async function displayAllFac() {
    const url = dns + userPort + "/getAllFaculty";
    try {
        const responseData = await sendGetRequest(url);
        let facContainer = document.getElementById('fac-container');
        
        let facList = responseData.data.facultyList;
        facList.forEach(faculty => {
            let facEmail = faculty.email;
            let facName = faculty.name;
            
            facContainer.innerHTML += ` 
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${facEmail}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4>${facName}</h4>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 text-end">
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#update-faculty" onclick="fillFacForm('${facEmail}', '${facName}')"><img class="admin-display-icon" src="images/pencil.svg"></button>
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#delete-faculty" onclick="deleteFac('${facEmail}')"><img class="admin-display-icon" src="images/bin.svg"></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.log(error);
    } 
}

function fillFacForm(facEmail, facName) {
    document.getElementById("updateFacultyEmail").value = facEmail;
    document.getElementById("displayFacultyEmail").value = facEmail;
    document.getElementById("updateFacultyName").value = facName;
}

function deleteFac(facEmail) {
    toDeleteUrl = dns + userPort + "/deleteFaculty/" + facEmail;
}

// ---------- INSTRUCTOR ---------- 
async function displayAllInstr() {
    const url = dns + userPort + "/getAllInstructors";
    try {
        const responseData = await sendGetRequest(url);
        let instrContainer = document.getElementById('instr-container');
        
        let instrList = responseData.data.instructorList;
        instrList.forEach(instructor => {
            let instrEmail = instructor.email;
            let instrName = instructor.name;
            
            instrContainer.innerHTML += ` 
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${instrEmail}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4>${instrName}</h4>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 text-end">
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#update-instructor" onclick="fillInstrForm('${instrEmail}', '${instrName}')"><img class="admin-display-icon" src="images/pencil.svg"></button>
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#delete-instructor" onclick="deleteInstr('${instrEmail}')"><img class="admin-display-icon" src="images/bin.svg"></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.log(error);
    }displayNavInitials('admin');
}

function fillInstrForm(instrEmail, instrName) {
    document.getElementById("updateInstructorEmail").value = instrEmail;
    document.getElementById("displayInstructorEmail").value = instrEmail;
    document.getElementById("updateInstructorName").value = instrName;
}

function deleteInstr(instrEmail) {
    toDeleteUrl = dns + userPort + "/deleteInstructor/" + instrEmail;
}

// ---------- STUDENT ---------- 
async function displayAllStudents() {
    const url = dns + userPort + "/getAllStudents";
    try {
        const responseData = await sendGetRequest(url);
        let studentContainer = document.getElementById('student-container');
        
        let studentList = responseData.data.studentList;
        studentList.forEach(student => {
            let studentEmail = student.email;
            let studentName = student.name;
            
            studentContainer.innerHTML += ` 
                <div class="card module admin-display-container">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${studentEmail}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4>${studentName}</h4>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 text-end">
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#update-student" onclick="fillStudentForm('${studentEmail}', '${studentName}')"><img class="admin-display-icon" src="images/pencil.svg"></button>
                            <button class="btn bg-white admin-display-icon-btn" data-bs-toggle="modal" data-bs-target="#delete-student" onclick="deleteStudent('${studentEmail}')"><img class="admin-display-icon" src="images/bin.svg"></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.log(error);
    }
}

function fillStudentForm(studentEmail, studentName) {
    document.getElementById("updateStudentEmail").value = studentEmail;
    document.getElementById("displayStudentEmail").value = studentEmail;
    document.getElementById("updateStudentName").value = studentName;
}

function deleteStudent(studentEmail) {
    toDeleteUrl = dns + userPort + "/deleteStudent/" + studentEmail;
}  

// ---------- PROFILE/SETTINGS ---------- 
function displayAdminProfile() {
    var admin = JSON.parse(sessionStorage.getItem("admin"));
    document.getElementById("initials").setAttribute("data-initials", admin.initials);
    document.getElementById("email").innerHTML = admin.email;
    document.getElementById("name").innerHTML = admin.name;
    document.getElementById("lastLogin").innerHTML = admin.lastLogin;
    document.getElementById("oldPassword").innerHTML = "*".repeat(10);
    fillSkorEmail();
    fillTestMode();
}

async function fillSkorEmail() {
    const getAllEmailUrl = dns + systemConfigPort + "/getAllSkorEmail";
    const emailSelect = document.getElementById('selectEmail');
    emailSelect.innerHTML = "";
    try {
        const getAllEmailData = await sendGetRequest(getAllEmailUrl);
        if (getAllEmailData.code == 200) {
            const emails = getAllEmailData.data.skorEmailList;
            emails.forEach(email => {
                emailSelect.innerHTML += `<option id="${email.email}" value="${email.email}">${email.email}</option>`;
            })
            const getSelectedEmailUrl = dns + systemConfigPort + "/getSelectedSkorEmail";
            const getSelectedEmailData = await sendGetRequest(getSelectedEmailUrl);
            if (getSelectedEmailData.code == 200) {
                document.getElementById(getSelectedEmailData.data.email).selected = true;
            }
        }
    } catch (error) {
        console.log(error);
    } 
}

async function fillTestMode() {
    const getTestModeUrl = dns + systemConfigPort + "/getConfiguration";
    const testModeCheckbox = document.getElementById('testMode');
    try {
        const getTestModeData = await sendGetRequest(getTestModeUrl);
        if (getTestModeData.code == 200) {
            const testMode = getTestModeData.data.testMode;
            if (testMode == 1) {
                testModeCheckbox.checked = true;
            }
            else {
                testModeCheckbox.checked = false;
            }
        }
    } catch (error) {
        console.log(error);
    } 
}

// *******************  TA & STUDENT  *********************
function displayClassHeader(courseCode, courseName, sectionNo) {
    document.getElementById("class-header").innerHTML = `
    <div class="module-text-container mb-1">
        <h3 class="tertiary-dark-2 mb-0">${courseCode}</h3>
    </div>
    <div class="module-text-container">
        <h2 class="mb-4">${courseName} [G${sectionNo}]</h2>
    </div>
    `;
}

function displaySessionHeader(courseCode, courseName, sectionNo, sessNo) {
    document.getElementById("session-header").innerHTML = `
    <div class="module-text-container mb-1">
        <h3 class="tertiary-dark-2 mb-0">${courseCode}</h3>
    </div>
    <div class="module-text-container mb-1">
        <h2 class="mb-0">${courseName} [G${sectionNo}]</h2>
    </div>
    <div class="module-text-container tertiary-dark-2 mt-3">
        <s2 class="mb-4">WEEK ${sessNo}</s2>
    </div>
    `;
}

// *************************  TA  *************************
// ---------- GENERAL ---------- 
async function displayClasslist(acadYear, termNo, courseCode, sectionNo, priorityList) {
    const classlistUrl = dns + userPort + "/getEnrolmentBySection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    const getSessionsUrl = dns + sessionPort + "/getSessionsBySection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    try {
        const enrolmentData = await sendGetRequest(classlistUrl);
        if (enrolmentData.code == 404) {
            document.getElementById("add-btn").style.display="none";
            document.getElementById("drop-btn").style.display="none";
            document.getElementById("export-btn").style.display="none";
            document.getElementById("edit-score-btn").style.display="none";
            document.getElementById("classlist-container").innerHTML=`<s1>No enrolled students.</s1>`;
        }
        else {
            let classlistContainer = document.getElementById('classlist-container');
            classlistContainer.innerHTML = "";
            let classlist = `
                <table id="classlist" class="table classlist-table text-center">
                    <thead>
                        <tr>
                            <th class="name text-start">Name</th>
                            <th></th>
                            <th>Priority</th>
            `;
            let section = await sendGetRequest(dns + displayInfoPort + "/getSectionInfo/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo);
            try {
                const priorityListData = await sendGetRequest(dns + displayInfoPort + "/getPriorityCallInfoBySection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo);
                let priorityList = {};
                if (priorityListData.code == 200) {
                    for (let priorityData of priorityListData.data) {
                        priorityList[priorityData.studentEmail] = priorityData;
                    }
                }
                section.data.priorityList = priorityList;
                sessionStorage.setItem("section", JSON.stringify(section.data));
                const sessionsData = await sendGetRequest(getSessionsUrl);
                if (sessionsData.code == 200) {
                    for (let session of sessionsData.data.sessions) {
                        classlist += `<th>W${session.sessNo}</th>`;
                    }
                }
                classlist += `<th>Total</th></tr></thead>`;
                let enrolmentList = enrolmentData.data;
                for (let student of enrolmentList) {
                    let studentName = student.studentName;
                    let studentEmail = student.studentEmail;
                    classlist += `
                        <tr id="${studentEmail}">
                            <td class="name-cell"><s2>${studentName}</s2></td><td></td>`;
                    if (studentEmail in priorityList) {
                        classlist += `<td><label for="#${studentEmail}-checkbox"  class="table-checkbox-container"><input id="${studentEmail}-checkbox" type="checkbox" class="table-checkbox" onchange="updatePriorityList('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${studentEmail}')" checked></label></td>`;
                    } else {
                        classlist += `<td><label for="#${studentEmail}-checkbox" class="table-checkbox-container"><input id="${studentEmail}-checkbox" type="checkbox" class="table-checkbox" onchange="updatePriorityList('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${studentEmail}')"></label></td>`;
                    }
                    const studentScorePerSessionUrl = dns + sessionPort + "/getScoreBySectionByStudent/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + studentEmail;
                    let totalScore = 0;
                    try {
                        const studentScores = await sendGetRequest(studentScorePerSessionUrl);
                        if (studentScores.code == 200) {
                            let scores = studentScores.data.sessionScores;
                            for (let session of sessionsData.data.sessions) {
                                if (scores[session.sessNo]) {
                                    classlist += `<td id="${studentEmail}-${session.sessNo}">${scores[session.sessNo]}</td>`;
                                    totalScore += scores[session.sessNo];
                                }
                                else{
                                    classlist += `<td id="${studentEmail}-${session.sessNo}">0</td>`;
                                }
                            }
                        }
                        else {
                            for (let session of sessionsData.data.sessions) {
                                classlist += `<td id="${studentEmail}-${session.sessNo}">0</td>`;
                            }
                        }
                    } catch (error) {
                        console.log(error);
                    }
                    classlist += `<td id="${studentEmail}-total">${totalScore}</td></tr>`;
                };
            } catch (error) {
                console.log(error);
            }
            classlist += `</table>`;
            classlistContainer.innerHTML = classlist;
        }
    } catch (error) {
        console.log(error);
    }
}

async function displayClassConfig(scoreLimit) {
    if (scoreLimit) {
        document.getElementById("score-limit").value = scoreLimit;
    }
}

async function updatePriorityList(acadYear, termNo, courseCode, sectionNo, studentEmail) {
    let updatePriorityUrl, updatePriorityData;
    let section = JSON.parse(sessionStorage.getItem("section"));
    let priorityList = section.priorityList;
    if (document.getElementById(studentEmail + "-checkbox").checked) {
        updatePriorityUrl = dns + sectionPort + "/addPriorityCall";
        const body = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "studentEmail": studentEmail,
        };
        updatePriorityData = await sendPostRequest(updatePriorityUrl, JSON.stringify(body));
        if (updatePriorityData.code == 200) {
            priorityList[studentEmail] = updatePriorityData.data;
            section.priorityList = priorityList;
            sessionStorage.setItem("section", JSON.stringify(section));
            // alert(studentEmail + " has been added to priority list!");
            refreshSocket();
        }
    }
    else {
        updatePriorityUrl = dns + sectionPort + "/deletePriorityCall" + "/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + studentEmail;
        updatePriorityData = await sendDelRequest(updatePriorityUrl);
        if (updatePriorityData.code == 200) {
            delete priorityList[studentEmail];
            section.priorityList = priorityList;
            sessionStorage.setItem("section", JSON.stringify(section));
            // alert(studentEmail + " has been removed from priority list!");
            refreshSocket();
        }
    }
    if (updatePriorityData.code != 200) {
        console.log(updatePriorityData.message);
    }
}

// ---------- HOME PAGE ---------- 
async function displayTAClasses() {
    loadingPointer();
    const term = JSON.parse(sessionStorage.getItem("term"));
    const acadYear = term.acadYear;
    const termNo = term.termNo;
    const identity = sessionStorage.getItem("identity");
    const userEmail = JSON.parse(sessionStorage.getItem(identity)).email;
    let url;
    if (identity == "ta") {
        url = dns + displayInfoPort + "/getSectionsInfoByTermByTA" + "/" + acadYear + "/" + termNo + "/" + userEmail;
    }
    else {
        url = dns + displayInfoPort + "/getSectionsInfoByTermBy" + identity.charAt(0).toUpperCase() + identity.substring(1) + "/" + acadYear + "/" + termNo + "/" + userEmail;
    }
    try {
        const responseData = await sendGetRequest(url);
        let taClassContainer = document.getElementById('ta-class-container');
        if (responseData.code == 404) {
            taClassContainer.innerHTML = `<h4>No classes for this semester yet.</h4>`;
        }
        else if (responseData.code == 200) {
            taClassContainer.innerHTML = "";
            let taClassList = responseData.data;
            taClassList.forEach(section => {
                let courseCode = section.courseCode;
                let courseName = section.courseName;
                let sectionNo = section.sectionNo;
                let day = section.day;
                let startTime = section.startTime;
                let endTime = section.endTime;
                
                taClassContainer.innerHTML += `
                <div class="card module">
                    <div class="card-body row">
                        <div class="col-md-9 col-lg-10 module-section">
                            <div class="module-text-container">
                                <overline>${courseCode}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4 class="mb-4">${courseName} [G${sectionNo}]</h4>
                                <overline>${acadYear} Term ${termNo}</overline>
                            </div>
                        </div>
                        <div class="col-md-3 col-lg-2 module-section module-right-section">
                            <div class="module-enter-container">
                                <div class="module-text-container">
                                    <overline>${day}</overline>
                                </div>
                                <div id="${courseCode}-${sectionNo}" class="module-text-container">
                                    ${startTime} - ${endTime}<br>
                                    <a href="#"><button class="btn btn-primary mt-1" onclick="enterTAClass('${acadYear}','${termNo}','${courseCode}','${sectionNo}')">Enter</button></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            });
        }
        defaultPointer();
    } catch (error) {
        defaultPointer();
        console.log(error);
    }
}

async function enterTAClass(acadYear, termNo, courseCode, sectionNo) {
    loadingPointer();
    try {
        let section = await sendGetRequest(dns + displayInfoPort + "/getSectionInfo/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo);
        sessionStorage.setItem("section", JSON.stringify(section.data));
        window.location.replace("ta_class.html");
    } catch (error) {
        defaultPointer();
        console.log(error);
    }
}

// ---------- CLASS PAGE ---------- 
function displayTAClassPage() {
    const section = JSON.parse(sessionStorage.getItem("section"));
    const acadYear = section.acadYear; 
    const termNo = section.termNo; 
    const courseCode = section.courseCode; 
    const courseName = section.courseName; 
    const sectionNo = section.sectionNo; 
    const scoreLimit = section.participationScoreLimit; 
    const priorityList = section.priorityList; 
    displayClassHeader(courseCode, courseName, sectionNo);
    displayClasslist(acadYear, termNo, courseCode, sectionNo, priorityList);
    displayAllSessions(acadYear, termNo, courseCode, sectionNo);
    displayClassConfig(scoreLimit);
}

function dropEnrolment() {
    document.getElementById("drop-btn").style.display = "none";
    document.getElementById("import-btn").style.display = "none";
    document.getElementById("export-btn").style.display = "none";
    document.getElementById("add-btn").style.display = "none";
    document.getElementById("edit-score-btn").style.display = "none";
    document.getElementById("done-btn").style.display = "inline";
    let classlist = document.getElementById("classlist");
    const section = JSON.parse(sessionStorage.getItem("section"));
    const acadYear = section.acadYear; 
    const termNo = section.termNo; 
    const courseCode = section.courseCode; 
    const sectionNo = section.sectionNo; 
    for (let row of classlist.lastChild.children) {
        let studentEmail = row.id;
        let td = row.children[1];
        td.innerHTML += `<button class="btn bg-white p-0" data-bs-toggle="modal" data-bs-target="#delete-enrolment" onclick="deleteEnrolment('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${studentEmail}')"><img id="bin-icon" src="images/bin.svg"></button>`;
    }
}

function doneEditing() {
    document.getElementById("done-btn").style.display = "none";
    document.getElementById("drop-btn").style.display = "inline";
    document.getElementById("import-btn").style.display = "inline";
    document.getElementById("export-btn").style.display = "inline";
    document.getElementById("add-btn").style.display = "inline";
    document.getElementById("edit-score-btn").style.display = "inline";
    let classlist = document.getElementById("classlist");
    for (let row of classlist.lastChild.children) {
        row.children[1].lastChild.remove();
    }
}

function deleteEnrolment(acadYear, termNo, courseCode, sectionNo, studentEmail) {
    document.getElementById("confirm-delete-enrolment-btn").onclick = function () {confirmDeleteEnrolment(acadYear, termNo,courseCode, sectionNo, studentEmail);}
}

async function confirmDeleteEnrolment(acadYear, termNo, courseCode, sectionNo, studentEmail) {
    const deleteEnrolmentUrl = dns + userPort + "/deleteEnrolment/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + studentEmail;
    const deleteEnrolmentData = await sendDelRequest(deleteEnrolmentUrl);
    if (deleteEnrolmentData.code == 200) {
        document.getElementById(studentEmail).remove();
        refreshSocket();
    }
}

async function fillEditScoreForm() {
    const section = JSON.parse(sessionStorage.getItem("section"));
    const getEnrolmentUrl = dns + userPort + "/getEnrolmentBySection/" + section.acadYear + "/" + section.termNo + "/" + section.courseCode + "/" + section.sectionNo;
    const studentSelect = document.getElementById("editStudentEmail");
    studentSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    const getSessionsUrl = dns + sessionPort + "/getSessionsBySection/" + section.acadYear + "/" + section.termNo + "/" + section.courseCode + "/" + section.sectionNo;
    const sessNoSelect = document.getElementById("editSessNo");
    sessNoSelect.innerHTML = `<option hidden disabled selected>Please Select</option>`;
    try {
        const getEnrolmentData = await sendGetRequest(getEnrolmentUrl);
        if (getEnrolmentData.code == 200) {
            const enrolmentList = getEnrolmentData.data;
            enrolmentList.forEach(enrolment => {
                let studentEmail = enrolment.studentEmail;
                let studentName = enrolment.studentName;
                studentSelect.innerHTML += `<option value="${studentEmail}">${studentName}</option>`;
            } )
        }
        const getSessionsData = await sendGetRequest(getSessionsUrl);
        if (getSessionsData.code == 200) {
            const sessionList = getSessionsData.data.sessions;
            sessionList.forEach(session => {
                let sessNo = session.sessNo;
                sessNoSelect.innerHTML += `<option value="${sessNo}">${sessNo}</option>`;
            } )
        }
    } catch (error) {
        console.log(error);
    }
}

function exportClasslist() {
    const section = JSON.parse(sessionStorage.getItem("section"));
    let cleanTable = [];
    let headers = document.getElementById("classlist").children[0].children[0];
    let rows = document.getElementById("classlist").children[1].children;
    let cleanHeaders = ["Email", "Name"];
    for (let h = 3; h < headers.children.length-1; h++) {
        cleanHeaders.push(headers.children[h].innerHTML);
    }
    cleanTable.push(cleanHeaders);
    for (let row of rows) {
        let cleanRow = [row.id, row.children[0].innerHTML.slice(4, -5)];
        for (let r = 3; r < row.children.length-1; r++) {
            cleanRow.push(row.children[r].innerHTML);
        }
        cleanTable.push(cleanRow);
    }
    let csvContent = "data:text/csv;charset=utf-8,";
    cleanTable.forEach(function(rowArray) {
        let row = rowArray.join(",");
        csvContent += row + "\r\n";
    });
    csvContent = csvContent.slice(0, -2);
    console.log(csvContent);
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", section.courseCode + "_G" + section.sectionNo + "_Class_List.csv");
    document.body.appendChild(link); // Required for FF

    link.click();
}

async function displayAllSessions(acadYear, termNo, courseCode, sectionNo) {
    const getSessionsUrl = dns + sessionPort + "/getSessionsBySection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    let sessionContainer = document.getElementById("session-container");
    let ongoing = false;
    try {
        let lastSessNo = 0;
        let lastDate;
        const sessionsData = await sendGetRequest(getSessionsUrl);
        for (let session of sessionsData.data.sessions) {
            let sessNo = session.sessNo;
            let date = session.date;
            let formattedDate = date.replaceAll("-", "/");
            if (session.available == 0) {
                sessionContainer.innerHTML += 
                `<div class="col-md-6 col-lg-4 col-xl-3 session-case"><div class="col-md-12 session d-flex justify-content-between tertiary-dark-2">
                    <div><btn-text>WEEK ${sessNo}</btn-text><br>${formattedDate}</div>
                    <button class="btn btn-light session-dropdown" data-bs-toggle="dropdown" aria-expanded=False><img id="arrow-down" src="images/arrow_down.svg"></button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="#" onclick="startSession('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sessNo}')">Start</a></li>
                        <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#delete-session" onclick="deleteSession('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sessNo}')">Delete</a></li>
                    </ul>
                </div></div>`;
            }
            else {
                ongoing = true;
                sessionContainer.innerHTML += 
                `<div class="col-md-6 col-lg-4 col-xl-3 session-case"><div class="col-md-12 session d-flex justify-content-between tertiary-dark-2">
                    <div><btn-text>WEEK ${sessNo}<span class="badge ongoing-badge ms-1"><overline>ONLINE</overline></span></btn-text><br>${formattedDate}</div>
                    <button class="btn btn-light session-dropdown" data-bs-toggle="dropdown" aria-expanded=False><img id="arrow-down" src="images/arrow_down.svg"></button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="#" onclick="startSession('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sessNo}')">Enter</a></li>
                    </ul>
                </div></div>`;
            }            
            lastSessNo = sessNo;
            lastDate = date;
        }
        if (ongoing == true) {
            sessions = document.getElementsByClassName("session");
            for (let session of sessions) {
                if (session.children[2].children.length > 1) {
                    session.children[2].children[0].remove();
                }
            }
        }
        if (lastSessNo < 13) {
            document.getElementById(lastSessNo + 1).selected = true;
            lastDate = new Date(lastDate);
            lastDate.setDate(lastDate.getDate() + 7);
            lastDate = lastDate.toISOString().slice(0, 10)
            document.getElementById("date").value = lastDate;
        }
    } catch (error) {
        console.log(error);
    }
}

async function startSession(acadYear, termNo, courseCode, sectionNo, sessNo) {
    const session = {
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "courseName": JSON.parse(sessionStorage.getItem("section")).courseName,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
    }
    sessionStorage.setItem("session", JSON.stringify(session));
    const updateSessionUrl = dns + sessionPort + "/updateSessionAvailability" + "/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/1";
    try {
        const updateSessionData = await sendPutRequest(updateSessionUrl);
        if (updateSessionData.code == 200) {
            refreshSocket();
            window.location.replace("ta_session.html");
        }
    } catch (error) {
        console.log(error);
    }

}

function deleteSession(acadYear, termNo, courseCode, sectionNo, sessNo) {
    toDeleteUrl = dns + sessionPort + "/deleteSession/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo;
}

// ---------- SESSION PAGE ---------- 
function displayTASessionPage() {
    const session = JSON.parse(sessionStorage.getItem("session"));
    const section = JSON.parse(sessionStorage.getItem("section"));
    const acadYear = session.acadYear; 
    const termNo = session.termNo; 
    const courseCode = session.courseCode; 
    const courseName = session.courseName; 
    const sectionNo = session.sectionNo; 
    const scoreLimit = section.participationScoreLimit; 
    const priorityList = section.priorityList; 
    displaySessionHeader(courseCode, courseName, sectionNo, sessNo);
    displayClasslist(acadYear, termNo, courseCode, sectionNo, priorityList);
    displayClassConfig(scoreLimit);
}

async function endSession() {
    const session = JSON.parse(sessionStorage.getItem("session"));
    const updateSessionUrl = dns + sessionPort + "/updateSessionAvailability" + "/" + session.acadYear + "/" + session.termNo + "/" + session.courseCode + "/" + session.sectionNo + "/" + session.sessNo + "/0";
    try {
        const updateSessionData = await sendPutRequest(updateSessionUrl);
        if (updateSessionData.code == 200) {
            closeRoom();    // function in taClient.js
        }
    } catch (error) {
        console.log(error);
    }
}

// ---------- PROFILE PAGE ---------- 
function displayTAProfile() {
    title = {
        "ta": "Teaching Assistant",
        "faculty": "Faculty",
        "instructor": "Instructor"
    }
    let identity = sessionStorage.getItem("identity");
    let user = JSON.parse(sessionStorage.getItem(identity));
    document.getElementById("identity").innerHTML = title[identity];
    document.getElementById("initials").setAttribute("data-initials", user.initials);
    document.getElementById("email").innerHTML = user.email;
    document.getElementById("name").innerHTML = user.name;
    document.getElementById("lastLogin").innerHTML = user.lastLogin;
    document.getElementById("oldPassword").innerHTML = "*".repeat(10);
}

// ***********************  STUDENT ***********************
// ---------- GENERAL ---------- 
async function displayChart(acadYear, termNo, courseCode, sectionNo, studentEmail) {
    const getSessionsUrl = dns + sessionPort + "/getSessionsBySection/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    const sessionsData = await sendGetRequest(getSessionsUrl);
    if (sessionsData.code == 200) {
        var labels = [];
        var values = [];
        var total = 0;
        for (let session of sessionsData.data.sessions) {
            labels.push(session.sessNo);
        }
        const studentScorePerSessionUrl = dns + sessionPort + "/getScoreBySectionByStudent/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + studentEmail;
        const scoresData = await sendGetRequest(studentScorePerSessionUrl);
        if (scoresData.code == 200) {
            document.getElementById("chart-container").innerHTML = `<canvas id="score-chart"></canvas>`;
            let scores = scoresData.data.sessionScores;
            for (let session of sessionsData.data.sessions) {
                if (scores[session.sessNo]) {
                    values.push(scores[session.sessNo]);
                    total += scores[session.sessNo];
                }
                else{
                    values.push(0);
                }
            }
        }
        else {
            for (let i = 1; i <= sessionsData.data.sessions.length; i++) {
                values.push(0);
            }
        }
        document.getElementById("total-score").innerHTML = total;
        
        const data = {
            labels: labels,
            datasets: [{
                type: 'bar',
                label: "Weekly Score",
                backgroundColor: 'rgb(54, 90, 205)',
                borderColor: 'rgb(54, 90, 205)',
                maxBarThickness: 50,
                data: values
            }]
        };
        
        var chart = new Chart(
            document.getElementById("score-chart"),
            {
                data,
                options: {
                    y: {
                        suggestedMin: 0,
                        ticks: {
                            stepSize: 1
                        }
                    },
                }
            }
        );  
    }
}

function restoreState(participateState, handState) {
    if (handState == "disabled") {
        document.getElementById("hand").disabled = true;
    }
    showAlert(participateState);
}

// ---------- HOME PAGE ---------- 
async function displayStudentClasses() {
    loadingPointer();
    const studentEmail = JSON.parse(sessionStorage.getItem("student")).email;
    const term = JSON.parse(sessionStorage.getItem("term"));
    const acadYear = term.acadYear;
    const termNo = term.termNo;
    const enrolmentUrl = dns + userPort + "/getEnrolmentByStudent/" + acadYear + "/" + termNo + "/" + studentEmail;
    try {
        const responseData = await sendGetRequest(enrolmentUrl);
        let studentClassContainer = document.getElementById('student-class-container');
        studentClassContainer.innerHTML = "";
        if (responseData.code == 404) {
            studentClassContainer.innerHTML = `<h4>Not enrolled in any class for this semester yet.</h4>`;
        }
        else if (responseData.code == 200) {
            let studentClassList = responseData.data;
            for (enrolment of studentClassList) {
                const sectionDataUrl = dns + displayInfoPort + "/getSectionInfo/" + enrolment.acadYear + "/" + enrolment.termNo + "/" + enrolment.courseCode + "/" + enrolment.sectionNo;
                sectionData = await sendGetRequest(sectionDataUrl);
                let courseCode = sectionData.data.courseCode;
                let courseName = sectionData.data.courseName;
                let sectionNo = sectionData.data.sectionNo;
                let day = sectionData.data.day;
                let startTime = sectionData.data.startTime;
                let endTime = sectionData.data.endTime;
                
                studentClassContainer.innerHTML += `
                <div class="card module">
                    <div class="card-body row">
                        <div class="col-md-9 col-xl-10 module-section">
                            <div class="module-text-container">
                                <overline>${courseCode}</overline>
                            </div>
                            <div class="module-text-container">
                                <h4 class="mb-4">${courseName} [G${sectionNo}]</h4>
                                <overline>${acadYear} Term ${termNo}</overline>
                            </div>
                        </div>
                        <div class="col-md-3 col-xl-2 module-section module-right-section">
                            <div class="module-enter-container">
                                <div class="module-text-container">
                                    <overline>${day}</overline>
                                </div>
                                <div id="${courseCode}-${sectionNo}" class="module-text-container">
                                    ${startTime} - ${endTime}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                
                const sessionCountUrl = dns + sessionPort + "/getSessionCount/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
                try {
                    const sessionCount = await sendGetRequest(sessionCountUrl);
                    if (sessionCount.code == 200) {
                        if (sessionCount.data > 0) {
                            document.getElementById(courseCode + "-" + sectionNo).innerHTML += `<br><a href="#"><button class="btn btn-primary mt-1" onclick="enterStudentClass('${acadYear}','${termNo}','${courseCode}','${sectionNo}')">Enter</button></a>`;
                        }
                    }
                } catch (error) {
                    console.log(error);
                }
            }
        }
        defaultPointer();
    } catch (error) {
        defaultPointer();
        console.log(error);
    }
}

async function enterStudentClass(acadYear, termNo, courseCode, sectionNo) {
    loadingPointer();
    try {
        const section = await sendGetRequest(dns + displayInfoPort + "/getSectionInfo/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo);
        sessionStorage.setItem("section", JSON.stringify(section.data));
        window.location.replace("student_class.html");
    } catch (error) {
        defaultPointer();
        console.log(error);
    }
}

// ---------- CLASS PAGE ---------- 
function displayStudentClassPage() {
    const section = JSON.parse(sessionStorage.getItem("section"));
    const acadYear = section.acadYear; 
    const termNo = section.termNo; 
    const courseCode = section.courseCode; 
    const courseName = section.courseName; 
    const sectionNo = section.sectionNo; 
    const studentEmail = JSON.parse(sessionStorage.getItem("student")).email;
    displayClassHeader(courseCode, courseName, sectionNo);
    displayChart(acadYear, termNo, courseCode, sectionNo, studentEmail);
    checkSessionAvailbility(acadYear, termNo, courseCode, sectionNo);
}

async function checkSessionAvailbility(acadYear, termNo, courseCode, sectionNo) {
    const getAvailableSessionUrl = dns + sessionPort + "/getAvailableSession/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    try {
        const availableSessionData = await sendGetRequest(getAvailableSessionUrl);
        if (availableSessionData.code == 200) {
            document.getElementById("class-positive-status").style.display = "inline-block";
            document.getElementById("join-class-btn").onclick = function() {
                enterSession(acadYear, termNo, courseCode, sectionNo, availableSessionData.data.sessNo);   
            }
        }
        else {
            document.getElementById("class-negative-status").style.display = "inline-block";
            document.getElementById("join-class-btn").disabled = true;
        }
    } catch (error) {
        console.log(error);
    }
}

async function enterSession(acadYear, termNo, courseCode, sectionNo, sessNo) {
    const studentEmail = JSON.parse(sessionStorage.getItem("student")).email;
    const courseName = JSON.parse(sessionStorage.getItem("section")).courseName;
    const session = {
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "courseName": courseName,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
    }
    sessionStorage.setItem("session", JSON.stringify(session));
    sessionStorage.setItem("participateState", "available");
    sessionStorage.setItem("handState", "enabled");
    const sessionScore = {
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "courseName": courseName,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
        "studentEmail": studentEmail
    }
    const getSessionScoreUrl = dns + sessionPort + "/getScoreBySessionByStudent/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/" + studentEmail;
    try {
        const getSessionScoreData = await sendGetRequest(getSessionScoreUrl);
        if (getSessionScoreData.code == 200) {
            window.location.replace("student_session.html");
        }
        else if ((getSessionScoreData.code == 404)){
            const addSessionScoreUrl = dns + sessionPort + "/addStudentSessionScore"
            try {
                addSessionScoreData = await sendPostRequest(addSessionScoreUrl, JSON.stringify(sessionScore));
                if (addSessionScoreData.code == 200) {
                    window.location.replace("student_session.html");
                }
            } catch (error) {
                console.log(error);
            }
        }
    } catch (error) {
        console.log(error);
    }
}

// ---------- SESSION PAGE ---------- 
function displayStudentSessionPage() {
    const session = JSON.parse(sessionStorage.getItem("session"));
    const acadYear = session.acadYear; 
    const termNo = session.termNo; 
    const courseCode = session.courseCode; 
    const courseName = session.courseName; 
    const sectionNo = session.sectionNo; 
    const sessNo = session.sessNo;
    const studentEmail = JSON.parse(sessionStorage.getItem("student")).email;
    displaySessionHeader(courseCode, courseName, sectionNo, sessNo);
    displayChart(acadYear, termNo, courseCode, sectionNo, studentEmail);
    let participateState = sessionStorage.getItem("participateState");
    if (participateState != "available") {
        let handState = sessionStorage.getItem("handState");
        restoreState(participateState, handState);
    }
}

// ---------- PROFILE PAGE ---------- 
function displayStudentProfile() {
    let student = JSON.parse(sessionStorage.getItem("student"));
    document.getElementById("initials").setAttribute("data-initials", student.initials);
    document.getElementById("email").innerHTML = student.email;
    document.getElementById("name").innerHTML = student.name;
    document.getElementById("lastLogin").innerHTML = student.lastLogin;
    document.getElementById("oldPassword").innerHTML = "*".repeat(10);
}