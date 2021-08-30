// API Request Variables
const dns = "https://skor.smu.edu.sg:";
const userPort = "8081";
const termPort = "8082";
const coursePort = "8083";
const sectionPort = "8084";
const sessionPort = "8085";
const logPort = "8086";
const systemConfigPort = "8087";
const sectionSocketPort = "8090";
const sessionSocketPort = "8091";
const accountPort = "8092";
const importPort = "8093";
const displayInfoPort = "8094";
const updateCpPort = "8095"
const contactSkorPort = "8096";

// API Request Functions
async function sendPostRequest(url, body) {
	const response = await fetch(url, {
        method: "POST",
        mode: "cors", 
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: body,
    });
    
	return response.json();
}

async function sendGetRequest(url) {
    const response = await fetch(url, {
        method: "GET",
        mode: "cors", 
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });
    
    return response.json();
}

async function sendPutRequest(url) {
    const response = await fetch(url, {
        method: "PUT",
        mode: "cors", 
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });
    
    return response.json();
}

async function sendDelRequest(url) {
    const response = await fetch(url, {
        method: "DELETE",
        mode: "cors", 
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });
    
    return response.json();
}