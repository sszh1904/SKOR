// Variables
const identity = sessionStorage.getItem("identity");
const user = JSON.parse(sessionStorage.getItem(identity));
const userName = user.name;
const userEmail = user.email;
const session = JSON.parse(sessionStorage.getItem("session"));
const acadYear = session.acadYear;
const termNo = session.termNo;
const courseCode = session.courseCode;
const sectionNo = session.sectionNo;
const sessNo = session.sessNo;
const courseName = JSON.parse(sessionStorage.getItem("section")).courseName;
let scoreLimit = JSON.parse(sessionStorage.getItem("section")).participationScoreLimit;
const sectionID = courseCode + sectionNo;

// Web Socket
const socket = io.connect(dns + sessionSocketPort, { withCredentials: true });
let raisehandList = [];

socket.on("connect", () => {
    console.log("You have successfully connected");
    socket.emit("join", {"name": userName, "session": session})

    var clearRaisehandBtn = document.getElementById("clearHands");
    clearRaisehandBtn.addEventListener("click", function(event) {
        event.preventDefault();
        socket.emit("clearHands", {"sectionID": sectionID});
    });
});

socket.on("connect_error", (e) => {
    console.log(e.message);
});

socket.on("disconnect", () => {
    console.log('You have disconnected');
});

socket.on("message", (message) => {
    console.log(message);
})

socket.on("addRaisehand", async (data) => {
    const raisehandContainer = document.getElementById("raisehand-list");
    const studentScorebySessionUrl = dns + sessionPort + "/getScoreBySessionByStudent/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/" + data.student.email;
    const studentScorebySectionUrl = dns + sessionPort + "/getTotalScoreBySectionByStudent/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + data.student.email;
    try {
        let studentScore = await sendGetRequest(studentScorebySessionUrl);
        let score = 0;
        if (studentScore.data.score) {
            score = studentScore.data.score;
        }
        let studentTotalScore = await sendGetRequest(studentScorebySectionUrl);
        let totalScore = 0;
        if (studentTotalScore.data.score) {
            totalScore = studentTotalScore.data.score;
        }
        let priorityList = JSON.parse(sessionStorage.getItem("section")).priorityList;
        let priority = "";
        if (data.student.email in priorityList) {
            priority = "Yes";
        }
        raisehandList.push({"score": score,
                            "totalScore": totalScore,
                            "priority": priority, 
                            "email": data.student.email,
                            "data": data
                            });
        raisehandList = raisehandList.sort(function(a, b) { return b.priority.localeCompare(a.priority) || a.score - b.score || a.totalScore - b.totalScore ; });
        document.getElementById("raisehand-list").innerHTML = "";
        raisehandList.forEach(function(hand) {
            let student = hand.data.student;
            let studentEmail = student.email;
            let studentName = student.name;
            let dateTime = data.dateTime;
            let cpScore = hand.score;
            let totalCpScore = hand.totalScore;
            let priority = hand.priority;
            let reachedLimit = 0;
            if (cpScore == scoreLimit) {
                reachedLimit = 1;
            }
            raisehandContainer.innerHTML += `
                <tr id="${studentEmail}-${dateTime}"><td class="col">${studentName}</td><td class="col-2 text-center">${priority}</td><td class="col-1 text-center">${cpScore}</td><td class="col-1 text-center">${totalCpScore}</td><td class="col-2 text-center"><button class="btn btn-primary select-raisehand-btn" onclick="selectHand('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sectionID}', '${sessNo}', '${studentEmail}', '${dateTime}', '${reachedLimit}')">SELECT</button></td>
                </tr>
            `;
        })
    } catch (error) {
        console.log(error);
    }
})

socket.on("selectHand", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    const reachedLimit = data.reachedLimit;
    displaySelectHand(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit);
})

socket.on("invalid", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    const reachedLimit = data.reachedLimit;
    displayInvalidateParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit);
})

socket.on("bonus", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    displayBonusParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime);
})

socket.on("clearHands", () => {
    document.getElementById("raisehand-list").innerHTML = "";
    document.getElementById("answered-list").innerHTML = "";
    raisehandList = [];
})

socket.on("refresh", async (email) => {
    if (userEmail != email) {
        const getSectionUrl = dns + sectionPort + "/getSection" + "/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
        try {
            getSectionData = await sendGetRequest(getSectionUrl);
            if (getSectionData.code == 200) {
                const newSection = getSectionData.data;
                newSection.courseName = courseName;
                sessionStorage.setItem("section", JSON.stringify(newSection));
                location.reload();
            }
        } catch (error) {
            console.log(error);
        }
    }
})

socket.on("closeRoom", () => {
    console.log("Room has been closed");
    window.location.replace("ta_class.html");
})

// Functions
async function selectHand(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit) {
    socket.emit("selectHand", {
        "sectionID": sectionID, 
        "studentEmail": studentEmail,
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
        "dateTime": dateTime,
        "reachedLimit": reachedLimit,
    });
    let logDateTime = new Date();
    logDateTime.setTime(logDateTime.getTime() + 8*60*60*1000);
    const acceptRaisehandUrl = dns + updateCpPort + "/acceptRaisehand/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/" + studentEmail + "/" + logDateTime.toISOString().slice(0,-1) + "/" + dateTime + "/" + identity + "/" + userEmail;
    try {
        const acceptRaisehandData = await sendPutRequest(acceptRaisehandUrl);
    } catch (error) {
        console.log(error);
    }
}

function displaySelectHand(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit) {
    var studentRow = document.getElementById(studentEmail + "-" + dateTime);
    // studentRow.classList.add("accepted");
    studentRow.firstChild.innerHTML += `<img id="tick-icon" src="images/tick.svg"></img>`;
    var btn = studentRow.lastElementChild;
    btn.innerHTML = `<button class="btn btn-bonus action-btn" onclick="bonusParticipation('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sectionID}', '${sessNo}', '${studentEmail}', '${dateTime}')"><img id="white-star-icon" src="images/white_star.svg"></button><button class="btn btn-invalid action-btn" onclick="invalidateParticipation('${acadYear}', '${termNo}', '${courseCode}', '${sectionNo}', '${sectionID}', '${sessNo}', '${studentEmail}', '${dateTime}', '${reachedLimit}')"><img id="white-x-icon" src="images/white_x.svg"></button>`;
    // <img id="x-btn" src="images/x.svg"></img>
    var score = studentRow.children[2];
    if (Number(score.innerHTML) < scoreLimit) {
        score.innerHTML = Number(score.innerHTML) + 1;
        var totalScore = studentRow.children[3];
        totalScore.innerHTML = Number(totalScore.innerHTML) + 1;
        var classlistScore = document.getElementById(studentEmail + "-" + sessNo);
        classlistScore.innerHTML = Number(classlistScore.innerHTML) + 1;
        var classlistTotalScore = document.getElementById(studentEmail).lastElementChild;
        classlistTotalScore.innerHTML = Number(classlistTotalScore.innerHTML) + 1;
    }
    studentRow.remove();
    let index = 0;
    for (let hand of raisehandList) {
        if (hand.email == studentEmail) {
            raisehandList.splice(index, 1);
            break;
        }
        index++;
    }
    document.getElementById("answered-list").innerHTML += studentRow.outerHTML;
}

async function invalidateParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit) {
    socket.emit("invalid", {
        "sectionID": sectionID, 
        "studentEmail": studentEmail,
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
        "dateTime": dateTime,
        "reachedLimit": reachedLimit
    });
    let logDateTime = new Date();
    logDateTime.setTime(logDateTime.getTime() + 8*60*60*1000);
    const invalidateCPUrl = dns + updateCpPort + "/invalidateCP/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/" + studentEmail + "/" + logDateTime.toISOString().slice(0,-1) + "/" + dateTime + "/" + identity + "/" + userEmail + "/" + reachedLimit;
    try {
        const invalidateCPData = await sendPutRequest(invalidateCPUrl);
    } catch (error) {
        console.log(error);
    }
}

function displayInvalidateParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime, reachedLimit) {
    var studentRow = document.getElementById(studentEmail + "-" + dateTime);
    // studentRow.classList.remove("accepted");
    // studentRow.classList.add("invalidated");
    studentRow.firstChild.lastChild.remove();
    studentRow.firstChild.innerHTML += `<img id="x-icon" src="images/x.svg"></img>`;
    var btn = studentRow.lastElementChild;
    btn.innerHTML = "-";
    if (reachedLimit == 0) {
        var score = studentRow.children[2];
        score.innerHTML = Number(score.innerHTML) - 1;
        var totalScore = studentRow.children[3];
        totalScore.innerHTML = Number(totalScore.innerHTML) - 1;
        var classlistScore = document.getElementById(studentEmail + "-" + sessNo);
        classlistScore.innerHTML = Number(classlistScore.innerHTML) - 1;
        var classlistTotalScore = document.getElementById(studentEmail).lastElementChild;
        classlistTotalScore.innerHTML = Number(classlistTotalScore.innerHTML) - 1;
    }
}

async function bonusParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime) {
    socket.emit("bonus", {
        "sectionID": sectionID, 
        "studentEmail": studentEmail,
        "acadYear": acadYear,
        "termNo": termNo,
        "courseCode": courseCode,
        "sectionNo": sectionNo,
        "sessNo": sessNo,
        "dateTime": dateTime,
    });
    let logDateTime = new Date();
    logDateTime.setTime(logDateTime.getTime() + 8*60*60*1000);
    const awardBonusCPUrl = dns + updateCpPort + "/awardBonusCP/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo + "/" + sessNo + "/" + studentEmail + "/" + logDateTime.toISOString().slice(0,-1) + "/" + dateTime + "/" + identity + "/" + userEmail;
    try {
        const awardBonusCPData = await sendPutRequest(awardBonusCPUrl);
    } catch (error) {
        console.log(error);
    }
}

function displayBonusParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime) {
    var studentRow = document.getElementById(studentEmail + "-" + dateTime);
    // studentRow.classList.remove("accepted");
    // studentRow.classList.add("bonus");
    studentRow.firstChild.lastChild.remove();
    studentRow.firstChild.innerHTML += `<img id="star-icon" src="images/star.svg"></img>`;
    var btn = studentRow.lastElementChild;
    btn.innerHTML = "-";
    var score = studentRow.children[2];
    if (Number(score.innerHTML) < scoreLimit) {
        score.innerHTML = Number(score.innerHTML) + 1;
        var totalScore = studentRow.children[3];
        totalScore.innerHTML = Number(totalScore.innerHTML) + 1;
        var classlistScore = document.getElementById(studentEmail + "-" + sessNo);
        classlistScore.innerHTML = Number(classlistScore.innerHTML) + 1;
        var classlistTotalScore = document.getElementById(studentEmail).lastElementChild;
        classlistTotalScore.innerHTML = Number(classlistTotalScore.innerHTML) + 1;
    }
}

function refreshSocket() {
    socket.emit("refresh", {"email": userEmail, "sectionID": sectionID});
}

function closeRoom() {
    socket.emit("close", {"sectionID": sectionID});
}