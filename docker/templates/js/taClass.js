// Variables
const identity = sessionStorage.getItem("identity");
const user = JSON.parse(sessionStorage.getItem(identity));
const userName = user.name;
const userEmail = user.email;
const section = JSON.parse(sessionStorage.getItem("section"));
const acadYear = section.acadYear;
const termNo = section.termNo;
const courseCode = section.courseCode;
const courseName = section.courseName;
const sectionNo = section.sectionNo;
let scoreLimit = section.participationScoreLimit;
let priorityList = section.priorityList;
const sectionID = courseCode + sectionNo;

// Web Socket
const socket = io.connect(dns + sectionSocketPort, { withCredentials: true });

socket.on("connect", () => {
    console.log("You have successfully connected");
    socket.emit("join", {"name": userName, "sectionID": sectionID})
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

// Functions
function refreshSocket() {
    socket.emit("refresh", {"email": userEmail, "sectionID": sectionID});
}