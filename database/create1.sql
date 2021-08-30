-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: skor
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.17-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `name` varchar(80) NOT NULL,
  `password` varchar(100) NOT NULL,
  `lastLogin` varchar(30) DEFAULT NULL,
  `isLogin` int(11) NOT NULL DEFAULT 0,
  `email` varchar(80) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('SKOR Admin','$5$rounds=535000$lAtcCyCFrU5iTPKI$cpXI0DB4rdOXRm8jV5XgnDR12HG.Wb.01w0DDWR0P60','10 Aug 2021 16:27',1,'admin@smu.edu.sg');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configuration`
--

DROP TABLE IF EXISTS `configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testMode` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration`
--

LOCK TABLES `configuration` WRITE;
/*!40000 ALTER TABLE `configuration` DISABLE KEYS */;
INSERT INTO `configuration` VALUES (1,1);
/*!40000 ALTER TABLE `configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `courseCode` varchar(10) NOT NULL,
  `courseName` varchar(80) NOT NULL,
  PRIMARY KEY (`courseCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('IS211','Interaction Design and Prototyping');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseOffering`
--

DROP TABLE IF EXISTS `courseOffering`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courseOffering` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`),
  KEY `courseCode` (`courseCode`),
  CONSTRAINT `courseOffering_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`) REFERENCES `term` (`acadYear`, `termNo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `courseOffering_ibfk_2` FOREIGN KEY (`courseCode`) REFERENCES `course` (`courseCode`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseOffering`
--

LOCK TABLES `courseOffering` WRITE;
/*!40000 ALTER TABLE `courseOffering` DISABLE KEYS */;
INSERT INTO `courseOffering` VALUES ('AY2021-22',1,'IS211');
/*!40000 ALTER TABLE `courseOffering` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolment`
--

DROP TABLE IF EXISTS `enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrolment` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `studentEmail` varchar(80) NOT NULL,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`,`sectionNo`,`studentEmail`),
  KEY `studentEmail` (`studentEmail`),
  CONSTRAINT `enrolment_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`, `courseCode`, `sectionNo`) REFERENCES `section` (`acadYear`, `termNo`, `courseCode`, `sectionNo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `enrolment_ibfk_2` FOREIGN KEY (`studentEmail`) REFERENCES `student` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolment`
--

LOCK TABLES `enrolment` WRITE;
/*!40000 ALTER TABLE `enrolment` DISABLE KEYS */;
/*!40000 ALTER TABLE `enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `name` varchar(80) NOT NULL,
  `password` varchar(100) NOT NULL,
  `lastLogin` varchar(30) DEFAULT NULL,
  `isLogin` int(11) NOT NULL DEFAULT 0,
  `email` varchar(80) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES ('Benjamin Gan','$5$rounds=535000$VJezRatDlC6LWEdC$0xL8XY4IZ2rUL7jJLvOfOG4prsR7pfPUbEmptD.qJMD','6 Aug 2021 09:18',0,'benjamingan@smu.edu.sg'),('OUH Eng Lieh','$5$rounds=535000$v6o6/dzrPh5cwF1n$yKlkNcRF4tOc07LhAiar2Dp3jqzBGArbMO2IvSGscd4','10 Aug 2021 15:12',0,'elouh@smu.edu.sg'),('Gabriyel WONG','$5$rounds=535000$mYZcut1Km87tESOu$yKIxJPELnF4gE/kbkG6byUw8vCM1p0FZW1FjZx6Nmk9',NULL,0,'gabriyelwong@smu.edu.sg'),('Kotaro HARA','$5$rounds=535000$94S2KU2cQZVnE1O/$03ENEmf4lT8MsumZ6A5HFX3VIHTKPBwY7kwCyxF6MC8',NULL,0,'kotarohara@smu.edu.sg');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `name` varchar(80) NOT NULL,
  `password` varchar(100) NOT NULL,
  `lastLogin` varchar(30) DEFAULT NULL,
  `isLogin` int(11) NOT NULL DEFAULT 0,
  `email` varchar(80) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES ('Coen CHUA','$5$rounds=535000$C9veFtvlsTctkRpc$LjyLAT3r6RVkK8HGzBAgKyX3pg.E./4ZatjKa6UEZ58','30 Jul 2021 04:55',0,'coenchua@smu.edu.sg'),('Joseph SUNG','$5$rounds=535000$I0aWh4VvORPaekyx$OXGPZeR9s9SUKLRDdIgddncKNc2eZAw42sG7OtWO/q3','29 Jul 2021 14:27',0,'josephsung@smu.edu.sg'),('LEE Kok Khing','$5$rounds=535000$1rURcgMfqMB1pwoX$FeJmDCI.YlpOcsPGD5Zqr5trj8mvzDkQLEOjrnluJtA',NULL,0,'kklee@smu.edu.sg'),('Michelle KAN','$5$rounds=535000$ETAn17Ozjs4kG1hs$lHlFPXtPRi5.ChSo2eVvcFcq.dkg9AC0RFHUlhgG/f0',NULL,0,'michellekan@smu.edu.sg');
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participation`
--

DROP TABLE IF EXISTS `participation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participation` (
  `datetime` varchar(30) NOT NULL,
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `sessNo` int(11) NOT NULL,
  `studentEmail` varchar(80) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `isAccepted` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`datetime`,`acadYear`,`termNo`,`courseCode`,`sectionNo`,`sessNo`,`studentEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participation`
--

LOCK TABLES `participation` WRITE;
/*!40000 ALTER TABLE `participation` DISABLE KEYS */;
/*!40000 ALTER TABLE `participation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participationScoreLog`
--

DROP TABLE IF EXISTS `participationScoreLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participationScoreLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `sessNo` int(11) NOT NULL,
  `studentEmail` varchar(80) NOT NULL,
  `logDatetime` varchar(30) NOT NULL,
  `participationRecordDatetime` varchar(30) DEFAULT NULL,
  `action` text NOT NULL,
  `actionBy` varchar(80) NOT NULL,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9750 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participationScoreLog`
--

LOCK TABLES `participationScoreLog` WRITE;
/*!40000 ALTER TABLE `participationScoreLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `participationScoreLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priorityCall`
--

DROP TABLE IF EXISTS `priorityCall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `priorityCall` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `studentEmail` varchar(80) NOT NULL,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`,`sectionNo`,`studentEmail`),
  KEY `studentEmail` (`studentEmail`),
  CONSTRAINT `priorityCall_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`, `courseCode`, `sectionNo`) REFERENCES `section` (`acadYear`, `termNo`, `courseCode`, `sectionNo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `priorityCall_ibfk_2` FOREIGN KEY (`studentEmail`) REFERENCES `enrolment` (`studentEmail`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priorityCall`
--

LOCK TABLES `priorityCall` WRITE;
/*!40000 ALTER TABLE `priorityCall` DISABLE KEYS */;
/*!40000 ALTER TABLE `priorityCall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `section` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `facultyEmail` varchar(80) NOT NULL,
  `instructorEmail` varchar(80) DEFAULT NULL,
  `taEmail` varchar(80) DEFAULT NULL,
  `day` varchar(10) NOT NULL,
  `startDate` varchar(10) NOT NULL,
  `startTime` varchar(10) NOT NULL,
  `endTime` varchar(10) NOT NULL,
  `participationScoreLimit` int(11) DEFAULT NULL,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`,`sectionNo`),
  KEY `facultyEmail` (`facultyEmail`),
  KEY `instructorEmail` (`instructorEmail`),
  KEY `taEmail` (`taEmail`),
  CONSTRAINT `section_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`, `courseCode`) REFERENCES `courseOffering` (`acadYear`, `termNo`, `courseCode`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `section_ibfk_2` FOREIGN KEY (`facultyEmail`) REFERENCES `faculty` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `section_ibfk_3` FOREIGN KEY (`instructorEmail`) REFERENCES `instructor` (`email`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `section_ibfk_4` FOREIGN KEY (`taEmail`) REFERENCES `taTerm` (`email`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `section`
--

LOCK TABLES `section` WRITE;
/*!40000 ALTER TABLE `section` DISABLE KEYS */;
INSERT INTO `section` VALUES ('AY2021-22',1,'IS211',1,'benjamingan@smu.edu.sg','josephsung@smu.edu.sg',NULL,'Mon','2021-08-16','1200','1515',2),('AY2021-22',1,'IS211',2,'benjamingan@smu.edu.sg','coenchua@smu.edu.sg',NULL,'Mon','2021-08-16','1530','1845',2),('AY2021-22',1,'IS211',3,'benjamingan@smu.edu.sg','kklee@smu.edu.sg',NULL,'Tue','2021-08-17','1200','1515',2),('AY2021-22',1,'IS211',4,'benjamingan@smu.edu.sg','michellekan@smu.edu.sg',NULL,'Wed','2021-08-18','1200','1515',NULL),('AY2021-22',1,'IS211',5,'benjamingan@smu.edu.sg','michellekan@smu.edu.sg',NULL,'Wed','2021-08-18','1530','1845',NULL),('AY2021-22',1,'IS211',6,'kotarohara@smu.edu.sg','kklee@smu.edu.sg',NULL,'Mon','2021-08-16','0815','1130',NULL),('AY2021-22',1,'IS211',7,'kotarohara@smu.edu.sg','kklee@smu.edu.sg',NULL,'Mon','2021-08-16','1530','1845',NULL),('AY2021-22',1,'IS211',8,'kotarohara@smu.edu.sg','michellekan@smu.edu.sg',NULL,'Thu','2021-08-19','1200','1515',NULL),('AY2021-22',1,'IS211',9,'elouh@smu.edu.sg','coenchua@smu.edu.sg',NULL,'Thu','2021-08-19','0815','1130',2),('AY2021-22',1,'IS211',10,'elouh@smu.edu.sg','coenchua@smu.edu.sg',NULL,'Thu','2021-08-19','1530','1845',2),('AY2021-22',1,'IS211',11,'gabriyelwong@smu.edu.sg','kklee@smu.edu.sg',NULL,'Tue','2021-08-17','1900','2215',NULL),('AY2021-22',1,'IS211',12,'gabriyelwong@smu.edu.sg','josephsung@smu.edu.sg',NULL,'Wed','2021-08-18','1900','2215',2);
/*!40000 ALTER TABLE `section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `sessNo` int(11) NOT NULL,
  `date` varchar(10) NOT NULL,
  `available` int(11) DEFAULT 0,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`,`sectionNo`,`sessNo`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`, `courseCode`, `sectionNo`) REFERENCES `section` (`acadYear`, `termNo`, `courseCode`, `sectionNo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
INSERT INTO `session` VALUES ('AY2021-22',1,'IS211',1,1,'2021-08-16',0),('AY2021-22',1,'IS211',1,2,'2021-08-23',0),('AY2021-22',1,'IS211',1,3,'2021-08-30',0),('AY2021-22',1,'IS211',1,4,'2021-09-06',0),('AY2021-22',1,'IS211',1,5,'2021-09-13',0),('AY2021-22',1,'IS211',1,6,'2021-09-20',0),('AY2021-22',1,'IS211',1,7,'2021-09-27',0),('AY2021-22',1,'IS211',1,8,'2021-10-04',0),('AY2021-22',1,'IS211',1,9,'2021-10-11',0),('AY2021-22',1,'IS211',1,10,'2021-10-18',0),('AY2021-22',1,'IS211',1,11,'2021-10-25',0),('AY2021-22',1,'IS211',1,12,'2021-11-01',0),('AY2021-22',1,'IS211',1,13,'2021-11-08',0),('AY2021-22',1,'IS211',2,1,'2021-08-16',1),('AY2021-22',1,'IS211',2,2,'2021-08-23',0),('AY2021-22',1,'IS211',2,3,'2021-08-30',0),('AY2021-22',1,'IS211',2,4,'2021-09-06',0),('AY2021-22',1,'IS211',2,5,'2021-09-13',0),('AY2021-22',1,'IS211',2,6,'2021-09-20',0),('AY2021-22',1,'IS211',2,7,'2021-09-27',0),('AY2021-22',1,'IS211',2,8,'2021-10-04',0),('AY2021-22',1,'IS211',2,9,'2021-10-11',0),('AY2021-22',1,'IS211',2,10,'2021-10-18',0),('AY2021-22',1,'IS211',2,11,'2021-10-25',0),('AY2021-22',1,'IS211',2,12,'2021-11-01',0),('AY2021-22',1,'IS211',2,13,'2021-11-08',0),('AY2021-22',1,'IS211',3,1,'2021-08-17',0),('AY2021-22',1,'IS211',3,2,'2021-08-24',0),('AY2021-22',1,'IS211',3,3,'2021-08-31',0),('AY2021-22',1,'IS211',3,4,'2021-09-07',0),('AY2021-22',1,'IS211',3,5,'2021-09-14',0),('AY2021-22',1,'IS211',3,6,'2021-09-21',0),('AY2021-22',1,'IS211',3,7,'2021-09-28',0),('AY2021-22',1,'IS211',3,8,'2021-10-05',0),('AY2021-22',1,'IS211',3,9,'2021-10-12',0),('AY2021-22',1,'IS211',3,10,'2021-10-19',0),('AY2021-22',1,'IS211',3,11,'2021-10-26',0),('AY2021-22',1,'IS211',3,12,'2021-11-02',0),('AY2021-22',1,'IS211',3,13,'2021-11-09',0),('AY2021-22',1,'IS211',4,1,'2021-08-18',0),('AY2021-22',1,'IS211',4,2,'2021-08-25',0),('AY2021-22',1,'IS211',4,3,'2021-09-01',0),('AY2021-22',1,'IS211',4,4,'2021-09-08',0),('AY2021-22',1,'IS211',4,5,'2021-09-15',0),('AY2021-22',1,'IS211',4,6,'2021-09-22',0),('AY2021-22',1,'IS211',4,7,'2021-09-29',0),('AY2021-22',1,'IS211',4,8,'2021-10-06',0),('AY2021-22',1,'IS211',4,9,'2021-10-13',0),('AY2021-22',1,'IS211',4,10,'2021-10-20',0),('AY2021-22',1,'IS211',4,11,'2021-10-27',0),('AY2021-22',1,'IS211',4,12,'2021-11-03',0),('AY2021-22',1,'IS211',4,13,'2021-11-10',0),('AY2021-22',1,'IS211',5,1,'2021-08-18',1),('AY2021-22',1,'IS211',5,2,'2021-08-25',0),('AY2021-22',1,'IS211',5,3,'2021-09-01',0),('AY2021-22',1,'IS211',5,4,'2021-09-08',0),('AY2021-22',1,'IS211',5,5,'2021-09-15',0),('AY2021-22',1,'IS211',5,6,'2021-09-22',0),('AY2021-22',1,'IS211',5,7,'2021-09-29',0),('AY2021-22',1,'IS211',5,8,'2021-10-06',0),('AY2021-22',1,'IS211',5,9,'2021-10-13',0),('AY2021-22',1,'IS211',5,10,'2021-10-20',0),('AY2021-22',1,'IS211',5,11,'2021-10-27',0),('AY2021-22',1,'IS211',5,12,'2021-11-03',0),('AY2021-22',1,'IS211',5,13,'2021-11-10',0),('AY2021-22',1,'IS211',6,1,'2021-08-16',0),('AY2021-22',1,'IS211',6,2,'2021-08-23',0),('AY2021-22',1,'IS211',6,3,'2021-08-30',0),('AY2021-22',1,'IS211',6,4,'2021-09-06',0),('AY2021-22',1,'IS211',6,5,'2021-09-13',0),('AY2021-22',1,'IS211',6,6,'2021-09-20',0),('AY2021-22',1,'IS211',6,7,'2021-09-27',0),('AY2021-22',1,'IS211',6,8,'2021-10-04',0),('AY2021-22',1,'IS211',6,9,'2021-10-11',0),('AY2021-22',1,'IS211',6,10,'2021-10-18',0),('AY2021-22',1,'IS211',6,11,'2021-10-25',0),('AY2021-22',1,'IS211',6,12,'2021-11-01',0),('AY2021-22',1,'IS211',6,13,'2021-11-08',0),('AY2021-22',1,'IS211',7,1,'2021-08-16',0),('AY2021-22',1,'IS211',7,2,'2021-08-23',0),('AY2021-22',1,'IS211',7,3,'2021-08-30',0),('AY2021-22',1,'IS211',7,4,'2021-09-06',0),('AY2021-22',1,'IS211',7,5,'2021-09-13',0),('AY2021-22',1,'IS211',7,6,'2021-09-20',0),('AY2021-22',1,'IS211',7,7,'2021-09-27',0),('AY2021-22',1,'IS211',7,8,'2021-10-04',0),('AY2021-22',1,'IS211',7,9,'2021-10-11',0),('AY2021-22',1,'IS211',7,10,'2021-10-18',0),('AY2021-22',1,'IS211',7,11,'2021-10-25',0),('AY2021-22',1,'IS211',7,12,'2021-11-01',0),('AY2021-22',1,'IS211',7,13,'2021-11-08',0),('AY2021-22',1,'IS211',8,1,'2021-08-19',1),('AY2021-22',1,'IS211',8,2,'2021-08-26',0),('AY2021-22',1,'IS211',8,3,'2021-09-02',0),('AY2021-22',1,'IS211',8,4,'2021-09-09',0),('AY2021-22',1,'IS211',8,5,'2021-09-16',0),('AY2021-22',1,'IS211',8,6,'2021-09-23',0),('AY2021-22',1,'IS211',8,7,'2021-09-30',0),('AY2021-22',1,'IS211',8,8,'2021-10-07',0),('AY2021-22',1,'IS211',8,9,'2021-10-14',0),('AY2021-22',1,'IS211',8,10,'2021-10-21',0),('AY2021-22',1,'IS211',8,11,'2021-10-28',0),('AY2021-22',1,'IS211',8,12,'2021-11-04',0),('AY2021-22',1,'IS211',8,13,'2021-11-11',0),('AY2021-22',1,'IS211',9,1,'2021-08-19',1),('AY2021-22',1,'IS211',9,2,'2021-08-26',0),('AY2021-22',1,'IS211',9,3,'2021-09-02',0),('AY2021-22',1,'IS211',9,4,'2021-09-09',0),('AY2021-22',1,'IS211',9,5,'2021-09-16',0),('AY2021-22',1,'IS211',9,6,'2021-09-23',0),('AY2021-22',1,'IS211',9,7,'2021-09-30',0),('AY2021-22',1,'IS211',9,8,'2021-10-07',0),('AY2021-22',1,'IS211',9,9,'2021-10-14',0),('AY2021-22',1,'IS211',9,10,'2021-10-21',0),('AY2021-22',1,'IS211',9,11,'2021-10-28',0),('AY2021-22',1,'IS211',9,12,'2021-11-04',0),('AY2021-22',1,'IS211',9,13,'2021-11-11',0),('AY2021-22',1,'IS211',10,1,'2021-08-19',0),('AY2021-22',1,'IS211',10,2,'2021-08-26',0),('AY2021-22',1,'IS211',10,3,'2021-09-02',0),('AY2021-22',1,'IS211',10,4,'2021-09-09',0),('AY2021-22',1,'IS211',10,5,'2021-09-16',0),('AY2021-22',1,'IS211',10,6,'2021-09-23',0),('AY2021-22',1,'IS211',10,7,'2021-09-30',0),('AY2021-22',1,'IS211',10,8,'2021-10-07',0),('AY2021-22',1,'IS211',10,9,'2021-10-14',0),('AY2021-22',1,'IS211',10,10,'2021-10-21',0),('AY2021-22',1,'IS211',10,11,'2021-10-28',0),('AY2021-22',1,'IS211',10,12,'2021-11-04',0),('AY2021-22',1,'IS211',10,13,'2021-11-11',0),('AY2021-22',1,'IS211',11,1,'2021-08-17',0),('AY2021-22',1,'IS211',11,2,'2021-08-24',0),('AY2021-22',1,'IS211',11,3,'2021-08-31',0),('AY2021-22',1,'IS211',11,4,'2021-09-07',0),('AY2021-22',1,'IS211',11,5,'2021-09-14',0),('AY2021-22',1,'IS211',11,6,'2021-09-21',0),('AY2021-22',1,'IS211',11,7,'2021-09-28',0),('AY2021-22',1,'IS211',11,8,'2021-10-05',0),('AY2021-22',1,'IS211',11,9,'2021-10-12',0),('AY2021-22',1,'IS211',11,10,'2021-10-19',0),('AY2021-22',1,'IS211',11,11,'2021-10-26',0),('AY2021-22',1,'IS211',11,12,'2021-11-02',0),('AY2021-22',1,'IS211',11,13,'2021-11-09',0),('AY2021-22',1,'IS211',12,1,'2021-08-18',0),('AY2021-22',1,'IS211',12,2,'2021-08-25',0),('AY2021-22',1,'IS211',12,3,'2021-09-01',0),('AY2021-22',1,'IS211',12,4,'2021-09-08',0),('AY2021-22',1,'IS211',12,5,'2021-09-15',0),('AY2021-22',1,'IS211',12,6,'2021-09-22',0),('AY2021-22',1,'IS211',12,7,'2021-09-29',0),('AY2021-22',1,'IS211',12,8,'2021-10-06',0),('AY2021-22',1,'IS211',12,9,'2021-10-13',0),('AY2021-22',1,'IS211',12,10,'2021-10-20',0),('AY2021-22',1,'IS211',12,11,'2021-10-27',0),('AY2021-22',1,'IS211',12,12,'2021-11-03',0),('AY2021-22',1,'IS211',12,13,'2021-11-10',0);
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skorEmail`
--

DROP TABLE IF EXISTS `skorEmail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skorEmail` (
  `email` varchar(80) NOT NULL,
  `password` varchar(100) NOT NULL,
  `domain` varchar(10) NOT NULL,
  `selected` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skorEmail`
--

LOCK TABLES `skorEmail` WRITE;
/*!40000 ALTER TABLE `skorEmail` DISABLE KEYS */;
INSERT INTO `skorEmail` VALUES ('skorsmu1@gmail.com','seCre+12','google',0),('skorsmu@gmail.com','seCre+12','google',1);
/*!40000 ALTER TABLE `skorEmail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `name` varchar(80) NOT NULL,
  `password` varchar(100) NOT NULL,
  `lastLogin` varchar(30) DEFAULT NULL,
  `isLogin` int(11) NOT NULL DEFAULT 0,
  `email` varchar(80) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentSessionScore`
--

DROP TABLE IF EXISTS `studentSessionScore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentSessionScore` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `sectionNo` int(11) NOT NULL,
  `sessNo` int(11) NOT NULL,
  `studentEmail` varchar(80) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`acadYear`,`termNo`,`courseCode`,`sectionNo`,`sessNo`,`studentEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentSessionScore`
--

LOCK TABLES `studentSessionScore` WRITE;
/*!40000 ALTER TABLE `studentSessionScore` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentSessionScore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taTerm`
--

DROP TABLE IF EXISTS `taTerm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taTerm` (
  `email` varchar(80) NOT NULL,
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  PRIMARY KEY (`email`,`acadYear`,`termNo`),
  KEY `acadYear` (`acadYear`,`termNo`),
  CONSTRAINT `taTerm_ibfk_1` FOREIGN KEY (`acadYear`, `termNo`) REFERENCES `term` (`acadYear`, `termNo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `taTerm_ibfk_2` FOREIGN KEY (`email`) REFERENCES `student` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taTerm`
--

LOCK TABLES `taTerm` WRITE;
/*!40000 ALTER TABLE `taTerm` DISABLE KEYS */;
/*!40000 ALTER TABLE `taTerm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term` (
  `acadYear` varchar(10) NOT NULL,
  `termNo` int(11) NOT NULL,
  `startDate` varchar(10) NOT NULL,
  `endDate` varchar(10) NOT NULL,
  `isCurrent` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`acadYear`,`termNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
INSERT INTO `term` VALUES ('AY2021-22',1,'2021-08-16','2021-12-12',1);
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-10  8:54:45
