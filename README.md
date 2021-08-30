# SKOR Application

## Table of contents
1. [Introduction](#introduction)
2. [Technologies Required](#technologies_required)
    1. [Installation](#installation)
        1. [SSH and Security](#setup_ssh_security)
        2. [Python](#install_python)
        3. [Xampp](#install_xampp)
        4. [Docker](#install_docker)
        5. [Git](#install_git)
    2. [Version Check](#version_check)
        1. [Python](#version_check_python)
        2. [Xampp](#version_check_xampp)
        3. [Docker](#version_check_docker)
        4. [Git](#version_check_git)
3. [Configuration & Setting Up](#setup)
    1. [Server](#server)
        1. [Xampp Security](#xampp_security)
        2. [Cloning Repository](#cloning_repository)
        3. [HTTPS Deployment](#https_deployment)
        4. [Environment File](#environment_file)
        5. [Database Setup](#database_setup)
    2. [Client](#client)
        1. [Client Request](#client_request)
    3. [Localhost](#localhost)
4. [Running the Application](#run_app)
    1. [Create Admin Account](#create_admin)
    2. [Add Data](#add_data)
    3. [Run Docker Application](#run_docker)
5. [Database Schema](#database_schema)
    1. [Admin](#db_admin)
    2. [Faculty](#db_faculty)
    3. [Instructor](#db_instructor)
    4. [Student](#db_student)
    5. [Term](#db_term)
    6. [TATerm](#db_taTerm)
    7. [Course](#db_course)
    8. [CourseOffering](#db_courseOffering)
    9. [Section](#db_section)
    10. [Enrolment](#db_enrolment)
    11. [PriorityCall](#db_priorityCall)
    12. [Session](#db_session)
    13. [Participation](#db_participation)
    14. [StudentSessionScore](#db_studentSessionScore)
    15. [ParticipationScoreLog](#db_participationScoreLog)
    16. [SkorEmail](#db_skorEmail)
    17. [Configuration](#db_configuration)

---
## Introduction <a name="introduction"></a>
SKOR is a class participation system that allows student to raise hands and educators to select raised hands. It addresses "consolidation of responsibility" [Karp 1976], wherein a few students assume the responsibility for the majority of participation in discussion, by presenting a dashboard that feedbacks frequency of student participation. SKOR is designed to work in traditional lectures, active learning, group project-based learning as well as blended learning.

This repository contains instructions of setting up and running the SKOR project. The example codes below are based on **Linux Ubuntu** OS, which is used for development. The commands may differ slightly if you are working on **Windows** or **Mac** OS. We used HTTPS protocol in our development but you can visit [Localhost](#localhost) segment for instructions to use HTTP protocol and run this project on your local machine. 

Do ensure that you have all the [required technologies](#technologies_required) installed on your machine before proceeding with the [setup](#setup).

[Back To The Top](#SKOR-Application)

---
## Technologies Required <a name="technologies_required"></a>
This project is created with the following technologies and versions.
- [Python] : >= 3.8
- [Xampp] : >= 8.0.0-2
- [Docker] : >= 20.10.7
- [Git] : >= 2.25.1

If these technologies are installed in the server, follow the steps in the [Version Check](#version_check) segment to check the version installed in the server. If you have yet to install any, please refer to the [Installation](#installation) segment.

<br>

[Back To The Top](#SKOR-Application)

---
## Installation <a name="installation"></a>
The following are command lines to install the required technologies.

<br>

Before we start installing the various technologies, let's update our Advanced Package Tool in our Ubuntu server. Run the following command to update apt package index:
```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt update && sudo apt upgrade
```

<br>

### - Server and Security Setup <a name="setup_ssh_security"></a>

Setup ssh:
```
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

<br>

Configure firewall to open ports: ssh (22), http (80), http (8080-8100), MySQL (3306), Github (9418):
```
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 8080:8100/tcp
sudo ufw allow 3306/tcp
sudo ufw allow 9418/tcp
sudo ufw enable
sudo ufw status
```

<br>

Open https (443)
```
sudo ufw allow https
```

<br>

### - Python <a name="install_python"></a>
After setting up the ssh, firewall and certificates, you may install these technologies in the root directory of the server. Run the following command to change to the root directory:
```
cd /
```

<br>

Run the following command to install Python:
```
sudo apt-get install python3.8
```

<br>

### - Xampp <a name="install_xampp"></a>
Download Xampp package:
```
wget https://www.apachefriends.org/xampp-files/8.0.0/xampp-linux-x64-8.0.0-2-installer.run
```
Change Xampp package permission to executable:
```
sudo chmod 755 xampp-linux-x64-8.0.0-2-installer.run
```
Run the following command to install Xampp package:
```
sudo ./xampp-linux-x64-8.0.0-2-installer.run
```

Alternatively, you can refer to this [link](https://trendoceans.com/how-to-install-xampp-on-ubuntu-20-04-lts/) for installation instructions for Xampp.

<br>

### - Docker <a name="install_docker"></a>
Run the following command to install Docker Engine:
```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

<br>

### - Git <a name="install_git"></a>
Run the following command to install Git:
```
sudo apt install git
```

[Back To The Top](#SKOR-Application)

---
## Version Check <a name="version_check"></a>
The following are methods you can use to check the version of your current technologies.

<br>

### - Python <a name="version_check_python"></a>
Run the following command to check the version for Python:
```
python3 --version
```
If your current version of Python is older than **3.8.10**, [install](#install_python) the latest version.  

<br>

### - Xampp <a name="version_check_xampp"></a>
To check for Xampp version, you have to be in the Xampp directory. To do so, you can type the following command:
```
cd /opt/lampp
```
Run the following command to check the version for Xampp:
```
./xampp status
```
If your current version of Xampp is older than **8.0.0-2**, [install](#install_xampp) the latest version.

<br>

### - Docker <a name="version_check_docker"></a>
Run the following command to check the version for Docker:
```
docker version
```
If your current version of Docker is older than **20.10.7**, [install](#install_docker) the latest version.

<br>

### - Git <a name="version_check_git"></a>
Run the following command to check the version for Git:
```
git --version
```
If your current version of Docker is older than **2.25.1**, [install](#install_git) the latest version.

[Back To The Top](#SKOR-Application)

---
## Configuration & Setup <a name="setup"></a>
After you have installed the required technologies, you can proceed to setup the project. If you have yet to install/update the required technologies, please proceed the [Technologies Required](#technologies_required) segment to do so.

<br>

## Server <a name="server"></a>
The following instructions are for setting up and configuring the backend development of the project.

<br>

### - Xampp Security <a name="xampp_security"></a>
The following instructions checks Xampp's security and you can set new passwords for **MySQL/phpMyAdmin user pma** and **MySQL root user**. You can skip password setting for **FTP password for user 'daemon'** and leave it as default.

First, change directory into Xampp. If you installed Xampp in the root directory, run the following command:
```
cd /opt/lampp
```
<br>

To update Xampp's security, run the following command:
```
sudo ./xampp security
```
Follow the steps accordingly and update the password when necessary.

<br>

### - Cloning Repository <a name="cloning_repository"></a>
Since we run our application using Xampp, we have to clone the project into Xampp's htdocs folder.
If you installed Xampp in the root directory, run the following command to change directory into Xampp's htdocs:
```
cd /opt/lampp/htdocs
```

<br>

After creating and getting into Xampp's htdocs folder directory, you can start cloning the SKOR's git repository. Run the following command to clone SKOR's repository:
```
sudo git clone https://github.com/SkorSMU/SKOR.git
```
You will be prompted to log in to a Github account. You may use SKOR's github account and any other Github account which has access to clone the repository.

<br>

### - HTTPS Deployment<a name="https_deployment"></a>
We'll be using certbot to generate SSL certificates for our application.

#### Generate SSL Certificates

Run the following commands to install certbot and generate the cert files needed: <br>
```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot certonly --webroot -v -w /opt/lampp/htdocs/SKOR/docker -d skor.smu.edu.sg
sudo certbot renew --dry-run
```
You should now see 2 Privacy Enhanced Mail (PEM) files in /opt/lampp/htdocs/SKOR/docker folder. These 2 files will be referenced in the .env file (mentioned in the next section).

<br>

#### Free Up Port 443 

Run the following command to edit XAMPP HTTPS configuration file:
```
sudo nano /opt/lampp/etc/extra/httpd-ssl.conf
```

<br>

Then, look for the following lines within the file and change "443" to another available port (e.g. 8443), which changes the listening port for XAMPP HTTPS, so that port 443 will be available for the application:
```
1. Listen 443
2. <VirtualHost _default_:443>
3. ServerName ...:443
```
Save and exit the file.

<br>

#### Redirect Port 80 to 443 (Optional)

Run the following command to edit XAMPP HTTP configuration file:
```
sudo nano /opt/lampp/etc/httpd.conf
```

<br>

Then, below the line "Listen 80", add the following lines:
```
<VirtualHost *:80>
  ServerName app_dns
  Redirect permanent / https://app_dns/
</VirtualHost>
```
**Note: app_dns refers to the Domain Name System(DNS) of the application**

Save and exit the file.

<br>

### - Environment File <a name="environment_file"></a>
Below are the instructions to create a environment variables file for our application. More details on the variables are written after the command line examples.

<br>

Change directory into SKOR repository __docker__ folder:
```
cd /opt/lampp/htdocs/SKOR/docker
```

<br>

Create a `.env` file with the following fields in the __docker__ folder:
```
APP_PORT = ''
USER_PORT = ''
TERM_PORT = ''
COURSE_PORT = ''
SECTION_PORT = ''
SESSION_PORT = ''
LOG_PORT = ''
SYSTEM_CONFIG_PORT = ''
SECTION_SOCKET_PORT = ''
SESSION_SOCKET_PORT = ''
ACCOUNT_PORT = ''
IMPORT_PORT = ''
DISPLAY_INFO_PORT = ''
UPDATE_CP_PORT = ''
CONTACT_SKOR_PORT = ''

DNS = ''

CERT_FILE = ''
KEY_FILE = ''
LOCAL = ''

SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_POOL_RECYCLE = ''
SQLALCHEMY_TRACK_MODIFICATIONS = ''
```

<br>

You may run the following command to write a new `.env` file in the __docker__ folder:
```
nano .env
```

<br>

If you face "permission denied" when writing the new `.env` file, you may run the following command to change and and allow writing permission in __htdocs__ folder:
```
sudo chmod -R 777 /opt/lampp/htdocs
```

<br>

As SKOR application is built using microservices architecture, each microservice will run on its own port. Thus, you may assign any unused port for each **port** variable in `.env` file.

Enter the Domain Name System (DNS) for the application. The DNS used in our development is `'skor.smu.edu.sg'`.

Enter the certificate and key files for HTTPS protocol. If you have not obtain the certificate and key files, refer to [SSL_Certificates](#ssl_certificates) segment for intructions. Enter `LOCAL = False` to run on HTTPS protocol.

Enter the database URI that should be used for the MySQL connection. An example could be `"mysql+mysqlconnector://root:root@localhost:3306/skor"` where a database named `'skor'` is created. Enter the configuration values for other MYSQL configurations. Configurartions used in our development will be `SQLALCHEMY_POOL_RECYCLE = 280` and `SQLALCHEMY_TRACK_MODIFICATIONS = False`.

<br>

### - Database Setup <a name="database_setup"></a>
To setup the database, we will create our database/schema using Xampp's MySQL.
If you installed Xampp in the root directory, run the following command to run Xampp's MySQL.
```
sudo /opt/lampp/bin/mysql -u root -p
```
You may be prompted to type your root password. Enter your password to run the MySQL.

<br>

Run the following the command to create a SKOR database/schema:
```
CREATE SCHEMA skor;
```
<br>

To exit MySQL, run the following command:
```
exit
```

<br>

## Client <a name="client"></a>
The following instructions are for setting up and configuring the frontend development of the project.

<br>

### - Client Request <a name="client_request"></a>
You may need to change the client side DNS and ports to match with the server side. Open the js file in the following directory:
```
/opt/lampp/htdocs/SKOR/docker/templates/js/request,js
```

<br>

You may need to edit the **const** variables in this `request.js` file:
```
const dns = "";
const userPort = "";
const termPort = "";
const coursePort = "";
const sectionPort = "";
const sessionPort = "";
const logPort = "";
const systemConfigPort = "";
const sectionSocketPort = "";
const sessionSocketPort = "";
const accountPort = "";
const importPort = "";
const displayInfoPort = "";
const updateCpPort = ""
const contactSkorPort = "";
```

<br>

Example of the variable `dns` is `const dns = "https://skor.smu.edu.sg"`.

All other ports variables should match the ports in the `.env` created in the [Environment File](#environment_file) section.

<br>

## Localhost <a name="localhost"></a>
This segment is only for setting up and running the application on localhost. If you are not doing so, you may skip this segment.

<br>

### - Change Environment File Variables
The following variables in `.env` file needs to be changed:
```
DNS = ''

CERT_FILE = None
KEY_FILE = None
LOCAL = True

SQLALCHEMY_TRACK_MODIFICATIONS = ''
``` 

<br>

### - Docker-compose yml file
In the __docker-compose.yml__ file located at `~/SKOR/docker` folder, environment endpoint URLs under each microservice need to change from `https` to `http`.

<br>

### - Client Side DNS
In the __request.js__ file located at `~SKOR/docker/templates/js` folder, `const dns` value needs to be updated.

[Back To The Top](#SKOR-Application)

---
## Running the Application <a name="run_app"></a>
Your setup is now configured and ready to run. 

<br>

### - Create Admin Account <a name="create_admin"></a>
To use this SKOR class participation application, we need to first create an Admin account so that this Admin user account can log into the application and create new users and modules.

<br>

Run the following command to run Xampp's MySQL;
```
sudo /opt/lampp/bin/mysql -u root -p
```
You may be prompted to type your root password. Enter your password to run the MySQL.

<br>

Run the following commands to create an Admin user account:
```
USE skor;

INSERT INTO admin('email', 'name', 'password') VALUES ('admin@smu.edu.sg', 'Admin', 'password123');
```
You may enter your own values when creating Admin account.

<br>

To exit Xampp's MYSQL, run the following command:
```
exit
```

<br>

### - Add Data [OPTIONAL] <a name="add_data"></a>
You may copy the SQl statements in the __test.sql__ file located at `~/SKOR/database` into Xampp's MYSql if you wish to preload some data. An Admin account will also be created in the process.

If not, you may use the web interface to create users/modules after starting the application.

<br>

### - Run Docker Application <a name="run_docker"></a>
To run our SKOR Docker application, you will first need to change directory to the docker folder in our SKOR repository. Run the following command from the root directory:
```
cd /opt/lampp/htdocs/SKOR/docker
```

<br>

Run the following command to build our Docker containers:
```
sudo docker-compose build
```

<br>

Run the following command to start our Docker containers:
```
sudo docker-compose up
```

<br>

To **stop** the Docker containers, press ```Ctrl``` or ```Cmd``` + ```C```. 

To stop and remove containers, networks, images, and volumes: you may run the following command:
```
sudo docker-compose down -v
```

<br>

The application has now been successfully setup and ready to be used. You can visit the web application at this URL: [https://skor.smu.edu.sg](https://skor.smu.edu.sg) 

[Back To The Top](#SKOR-Application)

---
## Database Schema <a name="database_schema"></a>
The Entity Relationship diagram below shows the interactions between the database tables utilised in this project. Click on the image to view a clearer version of it!

![SKOR ER Diagram](https://i.postimg.cc/jj5GJzCX/Screenshot-2021-08-01-at-4-41-00-AM.png)

The remainder of this section will detail the tables and fields used.

<br>

### - Admin <a name="db_admin"></a>
The Admin table stores the details of admin users that will use the application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - Admin user's email|
|name|Varchar(80)|False|- Admin user's name|
|password|Varchar(100)|False|- Admin user's hashed password|
|lastLogin|Varchar(30)|True|- Admin user's last login datetime|
|isLogin|Integer|False|- Admin user's login status <ul><li>0 - logged out</li><li>1 - logged in</li></ul>|

<br>

### - Faculty <a name="db_faculty"></a>
The Faculty table stores the details of faculty users that will use the application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - Faculty user's email|
|name|Varchar(80)|False|- Faculty user's name|
|password|Varchar(100)|False|- Faculty user's hashed password|
|lastLogin|Varchar(30)|True|- Faculty user's last login datetime|
|isLogin|Integer|False|- Faculty user's login status <ul><li>0 - logged out</li><li>1 - logged in</li></ul>|

<br>

### - Instructor <a name="db_instructor"></a>
The Instructor table stores the details of instructor users that will use the application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - Instructor user's email|
|name|Varchar(80)|False|- Instructor user's name|
|password|Varchar(100)|False|- Instructor user's hashed password|
|lastLogin|Varchar(30)|True|- Instructor user's last login datetime|
|isLogin|Integer|False|- Instructor user's login status <ul><li>0 - logged out</li><li>1 - logged in</li></ul>|

<br>

### - Student <a name="db_student"></a>
The Student table stores the details of student users that will use the application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - Student user's email|
|name|Varchar(80)|False|- Student user's name|
|password|Varchar(100)|False|- Student user's hashed password|
|lastLogin|Varchar(30)|True|- Student user's last login datetime|
|isLogin|Integer|False|- Student user's login status <ul><li>0 - logged out</li><li>1 - logged in</li></ul>|

<br>

### - Term <a name="db_term"></a>
The Term table stores the details of an academic school term.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - Academic year|
|termNo|Integer|False|- PK <br> - Academic term number|
|startDate|Varchar(10)|False|- Start date of an academic term|
|endDate|Varchar(10)|False|- End date of an academic term|
|isCurrent|Integer|False|- Indicates if this academic term is the currently ongoing <ul><li>0 - not currently ongoing</li><li>1 - is currently ongoing</li><li>Default: 0</li></ul>|

<br>

### - TATerm <a name="db_taTerm"></a>
The TATerm table stores the students who are teaching assistants in an academic term.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - FK to [student](#db_student).email <br> - Student user's email|
|acadYear|Varchar(10)|False|- PK <br> - FK to [term](#db_term).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [term](#db_term).termNo <br> - Academic term number|

<br>

### - Course <a name="db_course"></a>
The Course table stores the details of the courses in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|courseCode|Varchar(10)|False|- PK <br> - Course code (Eg. IS111)|
|courseName|Varchar(10)|False|- Course name (Eg. Introduction to Progamming)|

<br>

### - CourseOffering <a name="db_courseOffering"></a>
The CourseOffering table stores the courses offered in an acedmic term in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - FK to [term](#db_term).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [term](#db_term).termNo <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - FK to [course](#db_course).courseCode <br> - Course code (Eg. IS111)|

<br>

### - Section <a name="db_section"></a>
The Section table stores the details of a section for a course offered in an academic term in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - FK to [courseOffering](#db_courseOffering).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [courseOffering](#db_courseOffering).termNo <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - FK to [courseOffering](#db_courseOffering).courseCode <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - Section number|
|facultyEmail|Varchar(80)|False|- FK to [faculty](#db_faculty).email <br> - Faculty user's email|
|instructorEmail|Varchar(80)|True|- FK to [instructor](#db_instructor).email <br> - Instructor user's email|
|taEmail|Varchar(80)|True|- FK to [taTerm](#db_taTerm).email <br> - Teaching assistant's email|
|day|Varchar(10)|False|- Day of Week (Eg. Monday)|
|startDate|Varchar(10)|False|- Date for the first lesson in the academic term|
|startTime|Varchar(10)|False|- Lesson start time|
|endTime|Varchar(10)|False|- Lesson end time|   
|participationScoreLimit|Integer|True|- Student's participation score limit in a lesson|   

<br>

### - Enrolment <a name="db_enrolment"></a>
The Enrolment table stores which students are enrolled into a section for a course offered in an academic term in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - FK to [section](#db_section).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [section](#db_section).termNo <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - FK to [section](#db_section).courseCode <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - FK to [section](#db_section).sectioNo <br> - Section number|
|studentEmail|Varchar(80)|False|- FK to [student](#db_student).email <br> - Student user's email|

<br>

### - PriorityCall <a name="db_priorityCall"></a>
The PriorityCall table stores which students are on the priority call list for class participation in a section for a course offered in an academic term in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - FK to [section](#db_section).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [section](#db_section).termNo <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - FK to [section](#db_section).courseCode <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - FK to [section](#db_section).sectioNo <br> - Section number|
|studentEmail|Varchar(80)|False|- PK <br> - FK to [enrolment](#db_enrolment).email <br> - Student user's email|

<br>

### - Session <a name="db_session"></a>
The Session table stores the details of a session for a section of a course offered in an academic term in SMU.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - FK to [section](#db_section).acadYear <br> - Academic year|
|termNo|Integer|False|- PK <br> - FK to [section](#db_section).termNo <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - FK to [section](#db_section).courseCode <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - FK to [section](#db_section).sectioNo <br> - Section number|
|sessNo|Integer|False|- PK <br> - Session number|
|date|Varchar(10)|False|- Date of the session|
|available|Integer|False|- Whether the class is available for students to join <ul><li>0 - not available</li><li>1 - available</li><li>Default: 0</li></ul>|

<br>

### - Participation <a name="db_participation"></a>
The Participation table stores the details of all participation attempts by students.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|datetime|Varchar(30)|False|- PK <br> - Datetime of student's participation attempt|
|acadYear|Varchar(10)|False|- PK <br> - Academic year|
|termNo|Integer|False|- PK <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - Section number|
|sessNo|Integer|False|- PK <br> - Session number|
|studentEmail|Varchar(80)|False|- PK <br> - Student user's email|
|score|Integer|False|- Score awarded to this participation attempt <ul><li>Default: 0</li></ul>|
|isAccepted|Integer|False|- Whether student's participation attempt is accepted (Raise hand attempt accepted and student gets to answer) <ul><li>0 - not accepted</li><li>1 - accepted</li><li>Default: 0</li></ul>|

<br>

### - StudentSessionScore <a name="db_studentSessionScore"></a>
The StudentSessionScore table stores the total participation score for each session by a student.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|acadYear|Varchar(10)|False|- PK <br> - Academic year|
|termNo|Integer|False|- PK <br> - Academic term number|
|courseCode|Varchar(10)|False|- PK <br> - Course code (Eg. IS111)|
|sectionNo|Integer|False|- PK <br> - Section number|
|sessNo|Integer|False|- PK <br> - Session number|
|studentEmail|Varchar(80)|False|- PK <br> - Student user's email|
|score|Integer|False|- Total participation score earned in this session <ul><li>Default: 0</li></ul>|

<br>

### - ParticipationScoreLog <a name="db_participationScoreLog"></a>
The ParticipationScoreLog table stores all score changes for student's participation attempts and session's total participation score.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|id|Integer|False|- PK|
|acadYear|Varchar(10)|False|- Academic year|
|termNo|Integer|False|- Academic term number|
|courseCode|Varchar(10)|False|- Course code (Eg. IS111)|
|sectionNo|Integer|False|- Section number|
|sessNo|Integer|False|- Session number|
|studentEmail|Varchar(80)|False|- Student user's email|
|logDatetime|Varchar(30)|False|- Log time when the change is made|
|participationRecordDatetime|Varchar(30)|True|- Datetime of student's participation attempt in a session <br> - This value will be null if the score change is not made on student's in class participation score|
|action|Text|False|- Description to the change made to the score|
|actionBy|Varchar(80)|False|- Email of the user who changed/edited the score|
|role|Varchar(10)|False|- Role/type of user <ul><li>Admin</li><li>Faculty</li><li>Instructor</li><li>Teaching Assistant</li></ul>|

<br>

### - SkorEmail <a name="db_skorEmail"></a>
The SkorEmail table stores the details of different emails used by SKOR application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|email|Varchar(80)|False|- PK <br> - Email address|
|password|Varchar(100)|False|- Email account password|
|domain|Varchar(10)|False|- Email domain <ul><li>Google</li><li>Yahoo</li><li>Outlook</li></ul>|
|selected|Integer|False|- Selected email to be in use <ul><li>0 - not selected</li><li>1 - selected</li><li>Default: 0</li></ul>|

<br>

### - Configuration <a name="db_configuration"></a>
The Configuration table stores the details of different configurations for SKOR application.

|Column Name|Data Type|Nullable|Description|
|-|-|-|-|
|id|Integer|False|- PK|
|testMode|Varchar(100)|False|- Whether test mode is activated <ul><li>0 - not activated</li><li>1 - activated</li><li>Default: 0</li></ul>|

[Back To The Top](#SKOR-Application)