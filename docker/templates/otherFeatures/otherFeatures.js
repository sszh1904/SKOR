// *************************  REVERSE PROXY  *************************
const dns = "https://skor.smu.edu.sg/";
const userPort = "user";
const termPort = "term";
const coursePort = "course";
const sectionPort = "section";
const sessionPort = "session";
const logPort = "log";
const skorEmailPort = "skorEmail";
const sectionSocketPort = "sectionSocket";
const sessionSocketPort = "sessionSocket";
const loginPort = "login";
const importPort = "import";
const displayInfoPort = "displayInfo";
const updateCpPort = "updateCP"
const reportIssuePort = "reportIssue";

// *************************  GENERAL  *************************

// *************************  ADMIN  *************************
const createTAForm = document.getElementById("create-ta-form");
createTAForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const plainFormData = Object.fromEntries(formData.entries());
    const getTAUrl = dns + userPort + "/getTA" + "/" + plainFormData.email;
    try {
        const getTAData = await sendGetRequest(getTAUrl);
        if (getTAData.code == 200) {
            document.getElementById("ta-error-msg").innerHTML = "TA already exists."
        }
        else if ((getTAData.code == 404)){
            const addTAUrl = dns + userPort + "/addTA";
            const jsonFormData = JSON.stringify(plainFormData);
            try {
                const addTAData = await sendPostRequest(addTAUrl, jsonFormData);
                location.reload();
            } catch (error) {
                console.log(error);
            }
        }
    } catch (error) {
        console.log(error);
        document.getElementById("ta-error-msg").innerHTML = "An error occurred when adding new TA."
    }
});

const updateTAForm = document.getElementById("update-ta-form");
updateTAForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const plainFormData = Object.fromEntries(formData.entries());
    const updateTAUrl = dns + userPort + "/updateTAInfo" + "/" + plainFormData.email + "?name=" + plainFormData.name;
    try {
        const updateTAData = await sendPutRequest(updateTAUrl);
        location.reload();
    } catch (error) {
        console.log(error);
        document.getElementById("update-error-msg").innerHTML = "An error occurred when updating TA."
    }
});
// *************************  STUDENT/TA  *************************

// *************************  TA  *************************
const uploadClasslistForm = document.getElementById('upload-classlist-form')
uploadClasslistForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const url = dns + importPort + "/importClasslist";
    const file = document.getElementById("classlist-file").files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(event) {
            var data = event.target.result;
            var workbook = XLSX.read(data, {
                type: "binary"
            });

            workbook.SheetNames.forEach(async function(sheetName) {
                var XLRowObject = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                console.log(XLRowObject);
                const section = JSON.parse(sessionStorage.getItem("section"));
                section.classlist = XLRowObject;
                const response = await fetch(url, {
                    method: "POST",
                    mode: "cors", 
                    headers: {
                        "Content-Type": "application/json",
                        Accept: "application/json",
                    },
                    body: JSON.stringify(section)
                });

                if (!response.ok) {
                    const errorMessage = await response.text();
                    throw new Error(errorMessage);
                }
                location.reload();
            })
        };
        reader.onerror = function(event) {
            console.log("error");
        };
        reader.readAsBinaryString(file);
    }
});

const importChatForm = document.getElementById('import-chat-form')
importChatForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const url = dns + sessionPort + "/updateCpText";
    const form = event.currentTarget;
    const formData = new FormData(form);
    const plainFormData = Object.fromEntries(formData.entries());
    const sessNo = plainFormData.week;
    const section = JSON.parse(sessionStorage.getItem("section"));
    section.sessNo = sessNo;
    const file = document.getElementById("chat-file").files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = async function(event) {
            var data = event.target.result;
            section.text = data

            const response = await fetch(url, {
                method: "POST",
                mode: "cors", 
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: JSON.stringify(section)
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                throw new Error(errorMessage);
            }

            fillWeekOptions(section.acadYear, section.termNo, section.courseCode, section.sectionNo, "import-week");
            $("#upload-chat").load(window.location.href + " #upload-chat");
            if (response.status == 200) {
                document.getElementById("success-text").innerHTML = "Chat successfully imported!";
                $("#success").modal("show");
            }
        };
        reader.onerror = function(event) {
            console.log("error");
        };
        reader.readAsText(file);
    }
});

const createSessionForm = document.getElementById("create-session-form");
createSessionForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const section = JSON.parse(sessionStorage.getItem('section'));
    const select = document.getElementById("sessNo");
    let getSessionUrl;
    let getSessionData;
    let selected = [];
    let alreadyExist = [];
    for (let option of select.options) {
        if (option.selected) {
            selected.push(option.innerHTML);
            getSessionUrl = dns + sessionPort + "/getSession" + "/" + section.acadYear + "/" + section.termNo + "/" + section.courseCode + "/" + section.sectionNo + "/" + option.innerHTML;
            try {
                getSessionData = await sendGetRequest(getSessionUrl);
                if (getSessionData.code == 200) {
                    alreadyExist.push(option.innerHTML);
                }
            } catch (error) {
                console.log(error);
                document.getElementById("error-msg").innerHTML = "An error occurred when creating new session(s)."
            }
        }
    }
    console.log(alreadyExist);
    if (alreadyExist.length) {
        errorMsg = "Session(s)";
        for (let exist of alreadyExist) {
            errorMsg += " " + exist + ",";
        }
        errorMsg = errorMsg.slice(0, -1) + " already exists.";
        document.getElementById("error-msg").innerHTML = errorMsg;
    }
    else{
        let addSessionUrl;
        let addSessionData;
        let jsonData;
        for (let selectedOpt of selected) {
            addSessionUrl = dns + sessionPort + "/addSession";
            jsonData = JSON.stringify({
                "acadYear": section.acadYear,
                "termNo": section.termNo,
                "courseCode": section.courseCode,
                "sectionNo": section.sectionNo,
                "sessNo": selectedOpt
            });
            try {
                const addSessionData = await sendPostRequest(addSessionUrl, jsonData);
            } catch (error) {
                console.log(error);
                document.getElementById("error-msg").innerHTML = "An error occurred when creating new session(s)."
            }
        }
        location.reload();
    }
});

async function displayWordCloud(sessNo) {
    const section = JSON.parse(sessionStorage.getItem("section"));
    const url = dns + textProcessPort + "/processParticipationTextBySession/" + section.acadYear + "/" + section.termNo + "/" + section.courseCode + "/" + section.sectionNo + "/" + sessNo;
    const responseData = await sendGetRequest(url);
    if (responseData.code == 200) {
        document.getElementById("word-cloud").innerHTML = "";
        const wordCount = responseData.data;
        var chart = anychart.tagCloud(wordCount);
        chart.title("Participation Word Cloud - Week " + sessNo);
        chart.angles([0]);
        chart.height(450);
        chart.container("word-cloud");
        chart.draw();
    }
}

async function fillWeekOptions(acadYear, termNo, courseCode, sectionNo, container) {
    var weeks = document.getElementById(container);
    weeks.innerHTML = `<option hidden disabled selected value>Select</option>`;
    const url = dns + sessionPort + "/getSessionCount/" + acadYear + "/" + termNo + "/" + courseCode + "/" + sectionNo;
    const responseData = await sendGetRequest(url);
    if (responseData.code == 200) {
        for (var i = 1; i <= responseData.data; i++) {
            weeks.innerHTML += `<option value="${i}">${i}</option>`;
        }
    }
}

socket.on("hideAlert", (data) => {
    if (studentEmail == data) {
        document.getElementById("selected").style.visibility = "hidden";
        document.getElementById("hand").disabled = false;
        document.getElementById("banner").innerHTML = "Click to raise hand!";
    }
})

socket.on("alreadyStarted", (data) => {
    if (data.email == studentEmail) {
        var raisehandBtn = document.getElementById("hand");
        raisehandBtn.addEventListener("click", async function(event) {
            event.preventDefault();
            sessionStorage.setItem("participateState", "waiting");
            sessionStorage.setItem("handState", "disabled");
            document.getElementById("selected").style.visibility = "hidden";
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
                    console.log("raised hand");
                    document.getElementById("hand").disabled = true;
                    document.getElementById("banner").innerHTML = "Waiting to be accepted...";
                    socket.emit("raiseHand", {"student": student, "session": session, "dateTime": dateTime});
                }
            } catch (error) {
                console.log(error);
            }
        });
    }
})

socket.on("notStarted", (data) => {
    if (data.email == studentEmail) {
        document.getElementById("home").innerHTML = "<h3 class='text-center my-5'>Class has not started.</h3>";
    }
})

socket.on("start", () => {
    // sessionStorage.setItem("session", JSON.stringify(data));
    // sessionStorage.setItem("participateState", "available");
    location.reload();
})

var workbook = XLSX.read(data, {
    type: "binary"
});
workbook.SheetNames.forEach(async function(sheetName) {
    var XLRowObject = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
    console.log(XLRowObject);
    const section = JSON.parse(sessionStorage.getItem("section"));
    section.classlist = XLRowObject;
    const response = await fetch(url, {
        method: "POST",
        mode: "cors", 
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(section)
    });

    if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }
    // location.reload();
})

socket.on("selectHand", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    displaySelectHand(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime);
})

socket.on("invalid", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    displayInvalidateParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime);
})

socket.on("bonus", async (data) => {
    console.log(data);
    const studentEmail = data.studentEmail;
    const dateTime = data.dateTime;
    displayBonusParticipation(acadYear, termNo, courseCode, sectionNo, sectionID, sessNo, studentEmail, dateTime);
})