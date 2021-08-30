// Variables
const student = JSON.parse(sessionStorage.getItem("student"));
const studentEmail = student.email;
const studentName = student.name;
const session = JSON.parse(sessionStorage.getItem("session"));
const acadYear = session.acadYear;
const termNo = session.termNo;
const courseCode = session.courseCode;
const courseName = JSON.parse(sessionStorage.getItem("section")).courseName;
const sectionNo = session.sectionNo;
const sessNo = session.sessNo;
const sectionID = courseCode + sectionNo;

// Web Socket
const socket = io.connect(dns + sessionSocketPort, { withCredentials: true });

socket.on("connect", () => {
    console.log("You have successfully connected");
    socket.emit("join", {"name": studentName, "session": session});
    var raisehandBtn = document.getElementById("hand");
    raisehandBtn.addEventListener("click", async function(event) {
        event.preventDefault();
        const dateTime = new Date();
        const addParticipationUrl = dns + sessionPort + "/addParticipation";
        const body = {
            "acadYear": acadYear,
            "termNo": termNo,
            "courseCode": courseCode,
            "sectionNo": sectionNo,
            "sessNo": sessNo,
            "studentEmail": studentEmail,
            "dateTime": dateTime,
        }
        try {
            var responseData = await sendPostRequest(addParticipationUrl, JSON.stringify(body));
            if (responseData.code == 200) {
                sessionStorage.setItem("participateState", "waiting");
                sessionStorage.setItem("handState", "disabled");
                document.getElementById("hand").disabled = true;
                showAlert("waiting");
                socket.emit("raiseHand", {"student": student, "session": session, "dateTime": dateTime});
            }
        } catch (error) {
            console.log(error);
        }
    });
});

socket.on("connect_error", (e) => {
    console.log(e.message);
});

socket.on("disconnect", () => {
    console.log("You have disconnected");
});

socket.on("message", (message) => {
    console.log(message);
});

socket.on("clearHands", () => {
    sessionStorage.setItem("participateState", "available");
    sessionStorage.setItem("handState", "enabled");
    showAlert("");
    document.getElementById("hand").disabled = false;
});

socket.on("selectHand", (data) => {
    if (studentEmail == data.studentEmail) {
        sessionStorage.setItem("participateState", "accepted");
        sessionStorage.setItem("handState", "disabled");
        showAlert("accepted");
    }
})

socket.on("invalid", (data) => {
    if (studentEmail == data.studentEmail) {
        sessionStorage.setItem("participateState", "invalidated");
        showAlert("invalidated");
    }
})

socket.on("bonus", (data) => {
    if (studentEmail == data.studentEmail) {
        sessionStorage.setItem("participateState", "bonus");
        showAlert("bonus");
    }
})

socket.on("enableRaisehand", (data) => {
    if (studentEmail == data) {
        sessionStorage.setItem("handState", "enabled");
        document.getElementById("hand").disabled = false;
    }
})

socket.on("updateChart", (data) => {
    if (studentEmail == data) {
        displayChart();
    }
})

socket.on("closeRoom", () => {
    console.log("Room has been closed");
    window.location.replace("student_class.html");
})

// Functions
async function displayChart() {
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