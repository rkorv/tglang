-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: parcial
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `minerales`
--

DROP TABLE IF EXISTS `minerales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `minerales` (
  `nomCientifico` varchar(55) NOT NULL,
  `tipo` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`nomCientifico`),
  CONSTRAINT `minerales_ibfk_1` FOREIGN KEY (`nomCientifico`) REFERENCES `especies` (`nomCientifico`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `minerales`
--

LOCK TABLES `minerales` WRITE;
/*!40000 ALTER TABLE `minerales` DISABLE KEYS */;
INSERT INTO `minerales` VALUES ('Acrantophis madagascariensis','cobre'),('Amphibolurus barbatus','plutonio'),('Anastomus oscitans','torio'),('Anitibyx armatus','plomo'),('Antechinus flavipes','estaño'),('Anthropoides paradisea','torio'),('Antidorcas marsupialis','oro'),('Bos frontalis','cobre'),('Bubalus arnee','cromo'),('Butorides striatus','titanio'),('Capra ibex','cobalto'),('Ceratotherium simum','plomo'),('Certotrichas paena','uranio'),('Choloepus hoffmani','tungsteno'),('Crocodylus niloticus','titanio'),('Crocuta crocuta','tungsteno'),('Cyrtodactylus louisiadensis','hierro'),('Dacelo novaeguineae','cobalto'),('Dasypus septemcincus','estaño'),('Dasyurus viverrinus','titanio'),('Falco mexicanus','plomo'),('Falco peregrinus','cromo'),('Felis chaus','torio'),('Geochelone elegans','cobre'),('Geochelone elephantopus','tungsteno'),('Herpestes javanicus','cobalto'),('Isoodon obesulus','torio'),('Kobus defassa','platino'),('Limosa haemastica','oro'),('Mellivora capensis','cobalto'),('Merops nubicus','manganeso'),('Nasua nasua','titanio'),('Nyctanassa violacea','radio'),('Ovis canadensis','cromo'),('Pelecanus occidentalis','platino'),('Phasianus colchicus','plutonio'),('Physignathus cocincinus','torio'),('Rangifer tarandus','manganeso'),('Sarkidornis melachotos','oro'),('Sarkidornis melanotos','radio'),('Speothos vanaticus','plutonio'),('Spermophilus armatus','plomo'),('Spizaetus coronatus','cobre'),('Stenella coeruleoalba','cobalto'),('Tachyglossus aculeatus','cromo'),('Taurotagus oryx','titanio'),('Trachyphonus vaillantii','manganeso'),('Varanus albigularis','uranio'),('Vulpes vulpes','cobre'),('Zalophus californicus','uranio');
/*!40000 ALTER TABLE `minerales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-26  0:25:17
