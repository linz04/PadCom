-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: padcom
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.20.04.1

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
-- Table structure for table `codes`
--

DROP TABLE IF EXISTS `codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `codes` (
  `codes_id` int NOT NULL AUTO_INCREMENT,
  `user_id` json DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `content` text,
  PRIMARY KEY (`codes_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codes`
--

LOCK TABLES `codes` WRITE;
/*!40000 ALTER TABLE `codes` DISABLE KEYS */;
/*!40000 ALTER TABLE `codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `notes_id` char(32) NOT NULL,
  `user_id` json DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`notes_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES ('1d957ebda8324338995ac86b00f1c55b','[3, 1]','123','123'),('26976aa1a76f49eabea794cb05e0fe85','[3]',NULL,NULL),('53a303a461f94802bda34c0096a3e13e','[3, 1, 1]','Ini punya Testing','<p>asdasd</p>\r\n'),('78c78d0d68424d4b8b36ecbd97c4b205','[1]','1233','<p><img alt=\"sad\" src=\"http://127.0.0.1:5000/static/ckeditor/plugins/smiley/images/sad_smile.png\" style=\"height:23px; width:23px\" title=\"sad\" /></p>\r\n'),('9a83a254f6354558a07cacbe20e232b7','[1]',NULL,NULL),('9fbf1ff869ad4ec8b892f04eec5a9657','[3]','123','<p>123</p>\r\n'),('a4dab16c84144ab79f36f4eb8e7bce16','[4]','123','123'),('abf7258b08f94254b0f1ce0129e52bb0','[4]','Testing','<h1>HEHEHE</h1>asdasd'),('b9967198ed574de1b1a7a17fd17675b4','[3]','Ini Punya Saya','<p>Gk boleh lihat</p>\r\n'),('f9ea7c9bb61a43379d66d9f303fece6c','[1]','haha','testing<strong>Testing</testing>'),('fd92090e6cbc4a45a00b463037751d7a','[1]','213','<h1>Linz</h1>\r\n<img src=\"//www.jquery-az.com/html/images/banana.jpg\" title=\"Title of image\" alt=\"alt text here\"/>\r\n');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` char(50) NOT NULL,
  `password` char(60) DEFAULT NULL,
  `fullname` char(50) NOT NULL,
  `isLecturer` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'testing@gmail.com','$2b$12$XTPNXeSKDozI.3BR8OTUDO7Yt/rS616c5QYjiX6nYcSfc1FT1.lWG','Testing',0),(2,'linuz@gmail.com','$2b$12$q2.9PZBpOvtH1FiMEVu9ueW0Viz4XR3CvidiEBfvNI8d1hoaIKlHu','Linuz',0),(3,'123@gmail.com','$2b$12$.6fYNYTVp8aXh2yqPhpwKOZq.ZTzbfNznrNphOxw5mwANbRYb5cKy','123',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-30 21:55:57
