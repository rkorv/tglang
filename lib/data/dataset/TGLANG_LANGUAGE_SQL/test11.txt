-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generato il: Giu 12, 2017 alle 00:07
-- Versione del server: 5.5.54-0ubuntu0.14.04.1
-- Versione PHP: 5.5.9-1ubuntu4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `aireemdb`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `Abuses`
--

CREATE TABLE IF NOT EXISTS `Abuses` (
  `abuID` tinyint(4) NOT NULL AUTO_INCREMENT,
  `abuName` varchar(100) NOT NULL,
  `abuInfo` text,
  `abuTypID` tinyint(4) NOT NULL,
  PRIMARY KEY (`abuID`),
  UNIQUE KEY `abuName` (`abuName`),
  KEY `abuTypID` (`abuTypID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=11 ;

--
-- Dump dei dati per la tabella `Abuses`
--

INSERT INTO `Abuses` (`abuID`, `abuName`, `abuInfo`, `abuTypID`) VALUES
(1, 'Fake service offered', 'One of the services/performances this user offer is fake and does not correspond to what is said in the title or in the description.', 1),
(2, 'Not-fair price', 'One of the services/performances this user offer is too expensive compared to the service quality provided.', 1),
(3, 'Identity theft', 'This user is impersonating me or my company.', 2),
(4, 'Unauthorized use of personal information or photos', 'This user is using some of my personal data or my personal photos without my authorization. (Valid also for companies).', 2),
(5, 'Personal intimidation', 'This user is threatening me either verbally or by using emails.', 3),
(6, 'Annoying user', 'This user is annoying me in some ways.', 3),
(8, 'Offensive images', 'This user uploads and spreads offensive images to incite ethnic or gender hatred.', 4),
(9, 'Offensive language', 'This user is verbally inciting to ethnic or gender hatred.', 4),
(10, 'Spam', 'This user is spamming content.', 5);

-- --------------------------------------------------------

--
-- Struttura della tabella `Appointments`
--

CREATE TABLE IF NOT EXISTS `Appointments` (
  `appID` int(11) NOT NULL AUTO_INCREMENT,
  `appDate` date NOT NULL,
  `appTime` time NOT NULL,
  `appBookingDateTime` datetime NOT NULL,
  `appOffID` mediumint(9) NOT NULL,
  `appUserID` int(11) NOT NULL,
  PRIMARY KEY (`appID`),
  KEY `appOffID` (`appOffID`),
  KEY `appUserID` (`appUserID`),
  KEY `appDate` (`appDate`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=3 ;

--
-- Dump dei dati per la tabella `Appointments`
--

INSERT INTO `Appointments` (`appID`, `appDate`, `appTime`, `appBookingDateTime`, `appOffID`, `appUserID`) VALUES
(1, '2017-06-05', '15:00:00', '2017-05-02 21:55:00', 1, 4),
(2, '2017-06-20', '17:00:00', '2017-05-02 22:00:00', 1, 2);

-- --------------------------------------------------------

--
-- Struttura della tabella `Bank_accounts`
--

CREATE TABLE IF NOT EXISTS `Bank_accounts` (
  `bnkIBAN` varchar(50) NOT NULL,
  `bnkBankName` text NOT NULL,
  `bnkHolder` text NOT NULL,
  `bnkUserID` int(11) NOT NULL,
  PRIMARY KEY (`bnkIBAN`),
  KEY `bnkUserID` (`bnkUserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `Bank_accounts`
--

INSERT INTO `Bank_accounts` (`bnkIBAN`, `bnkBankName`, `bnkHolder`, `bnkUserID`) VALUES
('IE29AIBK93115212345678', 'Barclays Bank Ireland', 'Alphabet Inc', 2),
('IE31YIBK85615212345678', 'Bank of Ireland', 'Alphabet Inc', 2),
('IT60J0927311101000000123456', 'Mediolanum', 'Andrea Altomare', 1),
('IT60X0542811101000000123456', 'Unicredit', 'Andrea Altomare', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `Blocked`
--

CREATE TABLE IF NOT EXISTS `Blocked` (
  `blkID` int(11) NOT NULL AUTO_INCREMENT,
  `blkBlockedUserID` int(11) NOT NULL,
  `blkUserID` int(11) NOT NULL,
  PRIMARY KEY (`blkID`),
  KEY `blkBlockedUserID` (`blkBlockedUserID`),
  KEY `blkUserID` (`blkUserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `Categories`
--

CREATE TABLE IF NOT EXISTS `Categories` (
  `catID` smallint(6) NOT NULL AUTO_INCREMENT,
  `catName` varchar(100) NOT NULL,
  `catInfo` text,
  PRIMARY KEY (`catID`),
  UNIQUE KEY `catName` (`catName`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=5 ;

--
-- Dump dei dati per la tabella `Categories`
--

INSERT INTO `Categories` (`catID`, `catName`, `catInfo`) VALUES
(1, 'Tech', 'Technology-related services.'),
(2, 'Home working', 'Home care services.'),
(3, 'Other', 'Other type of services.'),
(4, 'Repair', 'Repair service.');

-- --------------------------------------------------------

--
-- Struttura della tabella `Cities`
--

CREATE TABLE IF NOT EXISTS `Cities` (
  `cyID` smallint(6) NOT NULL AUTO_INCREMENT,
  `cyName` text NOT NULL,
  `cyZipCode` varchar(10) NOT NULL,
  `cyDistrict` varchar(100) NOT NULL,
  `cyState` varchar(100) NOT NULL,
  `cyCountry` varchar(2) NOT NULL,
  PRIMARY KEY (`cyID`),
  KEY `cyCountry` (`cyCountry`),
  KEY `cyDistrict` (`cyDistrict`),
  KEY `cyState` (`cyState`),
  KEY `cyZipCode` (`cyZipCode`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=22 ;

--
-- Dump dei dati per la tabella `Cities`
--

INSERT INTO `Cities` (`cyID`, `cyName`, `cyZipCode`, `cyDistrict`, `cyState`, `cyCountry`) VALUES
(1, 'Milano', '20121', 'MI', 'Lombardia', 'IT'),
(2, 'Roma', '00118', 'RM', 'Lazio', 'IT'),
(3, 'Aosta', '11100', 'AO', 'Valle d''Aosta', 'IT'),
(4, 'Torino', '10121', 'TO', 'Piemonte', 'IT'),
(5, 'Genova', '16121', 'GE', 'Liguria', 'IT'),
(6, 'Trento', '38121', 'TN', 'Trentino-Alto Adige', 'IT'),
(7, 'Venezia', '30121', 'VE', 'Veneto', 'IT'),
(8, 'Trieste', '34121', 'TS', 'Friuli-Venezia Giulia', 'IT'),
(9, 'Bologna', '40121', 'BO', 'Emilia-Romagna', 'IT'),
(10, 'Firenze', '50121', 'FI', 'Toscana', 'IT'),
(11, 'Ancona', '60121', 'AN', 'Marche', 'IT'),
(12, 'Perugia', '06121', 'PG', 'Umbria', 'IT'),
(13, 'L''Aquila', '67100', 'AQ', 'Abruzzo', 'IT'),
(14, 'Campobasso', '86100', 'CB', 'Molise', 'IT'),
(15, 'Napoli', '80121', 'NA', 'Campania', 'IT'),
(16, 'Potenza', '85100', 'PZ', 'Basilicata', 'IT'),
(17, 'Bari', '70121', 'BA', 'Puglia', 'IT'),
(18, 'Catanzaro', '88100', 'CZ', 'Calabria', 'IT'),
(19, 'Palermo', '90121', 'PA', 'Sicilia', 'IT'),
(20, 'Cagliari', '09121', 'CA', 'Sardegna', 'IT'),
(21, 'Jesi', '60035', 'AN', 'Marche', 'IT');

-- --------------------------------------------------------

--
-- Struttura della tabella `Companies`
--

CREATE TABLE IF NOT EXISTS `Companies` (
  `coP_Iva` varchar(12) NOT NULL,
  `coName` text NOT NULL,
  `coAddress` text NOT NULL,
  `coHouseNumber` varchar(10) NOT NULL,
  `coApartmentInfo` text,
  `coTel` varchar(18) DEFAULT NULL,
  `coLinkedin` text,
  `coWebsite` text,
  `coCyID` smallint(6) NOT NULL,
  PRIMARY KEY (`coP_Iva`),
  KEY `coCyID` (`coCyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `Companies`
--

INSERT INTO `Companies` (`coP_Iva`, `coName`, `coAddress`, `coHouseNumber`, `coApartmentInfo`, `coTel`, `coLinkedin`, `coWebsite`, `coCyID`) VALUES
('99999999999', 'Aireem', 'Piazza Gae Aulenti', '1', 'Aireem Tower', '+020011100200', 'www.linkedin.com/company-beta/0001/', 'www.aireem.com', 1),
('9X99999A', 'Alphabet', 'Street of Innovation', '2', 'Alphabet and Google european Headquarter', '+3530044281234567', 'www.linkedin.com/company-beta/00001/', 'www.abc.xyz', 2);

-- --------------------------------------------------------

--
-- Struttura della tabella `Currencies`
--

CREATE TABLE IF NOT EXISTS `Currencies` (
  `curID` smallint(3) unsigned NOT NULL,
  `curCode` varchar(3) NOT NULL,
  `curDecimal` tinyint(1) DEFAULT NULL,
  `curName` varchar(50) NOT NULL,
  `curCoID` varchar(2) NOT NULL,
  PRIMARY KEY (`curID`),
  UNIQUE KEY `curCode` (`curCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `Currencies`
--

INSERT INTO `Currencies` (`curID`, `curCode`, `curDecimal`, `curName`, `curCoID`) VALUES
(0, 'OTH', NULL, 'Other', ''),
(111, 'BTC', 8, 'Bitcoin', ''),
(826, 'GBP', 2, 'British Pound', ''),
(840, 'USD', 2, 'United States Dollar', ''),
(978, 'EUR', 2, 'Euro', ''),
(999, 'XXX', NULL, 'No currency', '');

-- --------------------------------------------------------

--
-- Struttura della tabella `Messages`
--

CREATE TABLE IF NOT EXISTS `Messages` (
  `msgID` int(11) NOT NULL AUTO_INCREMENT,
  `msgText` text,
  `msgImg` text,
  `msgSeDateTime` datetime NOT NULL,
  `msgDeDateTime` datetime DEFAULT NULL,
  `msgReDateTime` datetime DEFAULT NULL,
  `msgSenderUserID` int(11) NOT NULL,
  `msgReceiverUserID` int(11) NOT NULL,
  PRIMARY KEY (`msgID`),
  KEY `msgSenderUserID` (`msgSenderUserID`),
  KEY `msgReceiverUserID` (`msgReceiverUserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `Notifications`
--

CREATE TABLE IF NOT EXISTS `Notifications` (
  `notID` int(11) NOT NULL AUTO_INCREMENT,
  `notInfo` text NOT NULL,
  `notDateTime` datetime NOT NULL,
  `notNotifierUserID` int(11) NOT NULL,
  `notUserID` int(11) NOT NULL,
  PRIMARY KEY (`notID`),
  KEY `notNotifierUserID` (`notNotifierUserID`),
  KEY `notUserID` (`notUserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `Offers`
--

CREATE TABLE IF NOT EXISTS `Offers` (
  `offID` mediumint(9) NOT NULL AUTO_INCREMENT,
  `offInfo` text,
  `offWorkExperience` tinyint(3) unsigned DEFAULT NULL,
  `offSkills` text,
  `offCost` decimal(12,2) unsigned DEFAULT NULL,
  `offHourlyCost` tinyint(1) NOT NULL,
  `offCostToBeDetermined` tinyint(1) NOT NULL,
  `offHomeWorking` tinyint(1) NOT NULL,
  `offMon` tinyint(1) NOT NULL,
  `offTue` tinyint(1) NOT NULL,
  `offWed` tinyint(1) NOT NULL,
  `offThu` tinyint(1) NOT NULL,
  `offFri` tinyint(1) NOT NULL,
  `offSat` tinyint(1) NOT NULL,
  `offSun` tinyint(1) NOT NULL,
  `offStartTime` time NOT NULL,
  `offEndTime` time NOT NULL,
  `offCurID` smallint(3) unsigned NOT NULL,
  `offPrfID` smallint(6) NOT NULL,
  `offUserID` int(11) NOT NULL,
  PRIMARY KEY (`offID`),
  KEY `offPrfID` (`offPrfID`),
  KEY `offUserID` (`offUserID`),
  KEY `offCurID` (`offCurID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=23 ;

--
-- Dump dei dati per la tabella `Offers`
--

INSERT INTO `Offers` (`offID`, `offInfo`, `offWorkExperience`, `offSkills`, `offCost`, `offHourlyCost`, `offCostToBeDetermined`, `offHomeWorking`, `offMon`, `offTue`, `offWed`, `offThu`, `offFri`, `offSat`, `offSun`, `offStartTime`, `offEndTime`, `offCurID`, `offPrfID`, `offUserID`) VALUES
(1, 'Web design for companies and people. Personal portfolio and lot more!', 5, 'HTML, CSS, JavaSCript programming\r\n- Adobe Muse.', '100.00', 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, '09:00:00', '18:00:00', 978, 1, 1),
(3, 'Tech support, computer repairing, major operating system installation.', 10, 'I know how to use Linux.', '21.00', 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, '00:00:00', '23:59:59', 840, 2, 4),
(4, NULL, 2, 'Polite and sensitive.', '30.00', 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, '16:00:00', '20:00:00', 978, 3, 4),
(10, 'Badante anziani', 11, 'Badante Gentilezza', '17.00', 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, '23:14:00', '23:14:00', 978, 10, 4),
(12, 'Riparazione componenti hardware PC', 3, '- Hardware,\r\n- Case Full Tower e Mid Tower,\r\n- riparazioni.', '14.00', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '09:00:00', '18:00:00', 978, 12, 1),
(13, 'Riparazioni di computer di tutti i tipi. Pulizia ventole e assemblaggio nuovi pc.', 5, 'Assemblaggio, Riparazione.', '15.00', 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, '08:30:00', '19:00:00', 978, 12, 4),
(14, 'Realizzo cortometraggi per piccole imprese che lo richiedono.', 4, 'Montaggio video, Adobe Premiere CC, Final Cut Pro, Sony Vegas.', '30.00', 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, '17:00:00', '20:00:00', 978, 13, 4),
(15, 'Editing video professionale. Servizio freelance.', 7, 'Utilizzo di iMovie e Final Cut Pro. Conoscenza ambiente Apple', '25.00', 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, '09:30:00', '17:00:00', 978, 14, 1),
(19, 'Assemblo computer desktop.', 4, 'Conoscenza componenti di ultima generazione, montaggio pc.', '15.00', 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, '09:00:00', '17:00:00', 978, 18, 12);

-- --------------------------------------------------------

--
-- Struttura della tabella `Payment_methods`
--

CREATE TABLE IF NOT EXISTS `Payment_methods` (
  `pmtID` int(11) NOT NULL AUTO_INCREMENT,
  `pmtCardHolder` text NOT NULL,
  `pmtCardType` text NOT NULL,
  `pmtCardNumber` varchar(16) NOT NULL,
  `pmtCardExpDate` date NOT NULL,
  `pmtCardSecurityCode` varchar(4) NOT NULL,
  `pmtUserID` int(11) NOT NULL,
  PRIMARY KEY (`pmtID`),
  KEY `pmtUserID` (`pmtUserID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=5 ;

--
-- Dump dei dati per la tabella `Payment_methods`
--

INSERT INTO `Payment_methods` (`pmtID`, `pmtCardHolder`, `pmtCardType`, `pmtCardNumber`, `pmtCardExpDate`, `pmtCardSecurityCode`, `pmtUserID`) VALUES
(1, 'Andrea Altomare', 'MasterCard', '0000111122223333', '2030-01-01', '111', 1),
(2, 'Andrea Altomare', 'Visa', '1111999988882222', '2020-02-01', '777', 1),
(3, 'Alphabet Inc', 'American Express', '7777555544448888', '2025-07-01', '222', 2),
(4, 'Alphabet Inc', 'Maestro', '1111000099997777', '2022-12-01', '555', 2);

-- --------------------------------------------------------

--
-- Struttura della tabella `PayPal_accounts`
--

CREATE TABLE IF NOT EXISTS `PayPal_accounts` (
  `pypID` int(11) NOT NULL AUTO_INCREMENT,
  `pypEmail` varchar(100) NOT NULL,
  `pypUserID` int(11) NOT NULL,
  PRIMARY KEY (`pypID`),
  KEY `pypUserID` (`pypUserID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=5 ;

--
-- Dump dei dati per la tabella `PayPal_accounts`
--

INSERT INTO `PayPal_accounts` (`pypID`, `pypEmail`, `pypUserID`) VALUES
(1, 'and.altomare@gmail.com', 1),
(2, 'andreaaltomare@gmail.com', 1),
(3, 'credit@abc.xyz', 2),
(4, 'alphabet@abc.xyz', 2);

-- --------------------------------------------------------

--
-- Struttura della tabella `People`
--

CREATE TABLE IF NOT EXISTS `People` (
  `pplPersonCode` int(11) NOT NULL AUTO_INCREMENT,
  `pplName` text NOT NULL,
  `pplSurname` text NOT NULL,
  `pplBirthdate` date NOT NULL,
  `pplGender` varchar(1) DEFAULT NULL,
  `pplQualification` text,
  `pplOccupation` text,
  `pplBio` text,
  `pplAddress` text NOT NULL,
  `pplHouseNumber` varchar(10) NOT NULL,
  `pplApartmentInfo` text,
  `pplTel` varchar(18) DEFAULT NULL,
  `pplCell` varchar(18) DEFAULT NULL,
  `pplCV` text,
  `pplLinkedin` text,
  `pplWebsite` text,
  `pplCyID` smallint(6) NOT NULL,
  PRIMARY KEY (`pplPersonCode`),
  KEY `pplCyID` (`pplCyID`),
  KEY `pplCyID_2` (`pplCyID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=10 ;

--
-- Dump dei dati per la tabella `People`
--

INSERT INTO `People` (`pplPersonCode`, `pplName`, `pplSurname`, `pplBirthdate`, `pplGender`, `pplQualification`, `pplOccupation`, `pplBio`, `pplAddress`, `pplHouseNumber`, `pplApartmentInfo`, `pplTel`, `pplCell`, `pplCV`, `pplLinkedin`, `pplWebsite`, `pplCyID`) VALUES
(1, 'Andrea', 'Altomare', '1998-03-23', 'M', 'Diploma di istruzione tecnica - Informatica', 'Software analyst at Aireem', 'Ragazzo europeo diplomato in un Istituto Tecnico. Ho competenze informatiche.', 'Via Libero Grassi', '7', 'Piano terra, Scala C', '0731203513', '3898986840', 'www.cvonline.org/cvandreaaltomare', 'www.linkedin.com/in/andrea-altomare/', 'www.andreaaltomare.com', 1),
(2, 'Chiara', 'Rossi', '1990-01-01', 'F', 'Laurea magistrale in Matematica', 'Docente universitaria', 'Ragazza europea laureata in matematica con l''obiettivo di lavorare per la sezione Ricerca & Sviluppo di una grande impresa.', 'Via Giuseppe Garibaldi', '1', 'Piano terra, Scala A', '+020011203040', '+023991002001', 'www.cvonline.org/cvchiararossi', NULL, NULL, 1),
(3, 'Carlo', 'Rossi', '1993-02-15', 'M', 'Laurea', 'Ingegnere a Starbucks', 'Ragazzo di Torino', 'Via Montale', '11', 'Piano 2', '+390002225511', '+395555553338', 'http://www.cvonline.com/carlorossi-cv', 'http://www.linkedin.com/in/carlo-rossi-23235225', 'www.carlorossi.com', 10),
(6, 'Walter', 'Bianchi', '1990-03-01', 'M', 'Dottorato di ricerca', 'Chimico presso me stesso', 'Chimico di brba e los pollos hermanos', 'Via America', '1', 'Scala A', '+390731456732', '3827563011', NULL, '', 'www.whalterbianchi.com', 21),
(9, 'Alessandro', 'Mazzini', '1992-02-12', 'M', 'Laurea magistrale', 'Broker at Morgan Stanley', 'Ragazzo con spiccato interesse per economia e finanza.', 'Via Mazzini', '2', '', '3267832551', '0211988475', NULL, '', '', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `Performances`
--

CREATE TABLE IF NOT EXISTS `Performances` (
  `prfID` smallint(6) NOT NULL AUTO_INCREMENT,
  `prfName` varchar(150) NOT NULL,
  `prfInfo` text,
  `prfCatID` smallint(6) NOT NULL,
  PRIMARY KEY (`prfID`),
  UNIQUE KEY `prfName` (`prfName`),
  KEY `prfCatID` (`prfCatID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=21 ;

--
-- Dump dei dati per la tabella `Performances`
--

INSERT INTO `Performances` (`prfID`, `prfName`, `prfInfo`, `prfCatID`) VALUES
(1, 'Web Design', 'Web Design service: build website on-demand, briefing, wireframing, mockups, front-end programming...', 1),
(2, 'IT Support', 'IT support to repair computers or to resolve technical problems.', 1),
(3, 'Babysitting', 'Home babysitting service.', 2),
(4, 'Caregiver', 'Home caregiver service. For elders and people with disabilities.', 2),
(5, 'Riparazioni computer', NULL, 1),
(6, 'Spazzino', NULL, 3),
(7, 'Dogsitter', NULL, 2),
(8, 'Tagliaerba', NULL, 3),
(9, 'Fotografo', NULL, 3),
(10, 'Badante', NULL, 2),
(11, 'Programmatore', NULL, 1),
(12, 'Riparazione computer', NULL, 1),
(13, 'Video Making', NULL, 1),
(14, 'Video editing', NULL, 1),
(15, 'programmatore computer', NULL, 1),
(16, 'computer design', NULL, 1),
(17, 'computer grafica', NULL, 1),
(18, 'Assemblaggio computer', NULL, 1),
(19, 'Servizio riparazioni', NULL, 4),
(20, 'riparazioni', NULL, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `Reports`
--

CREATE TABLE IF NOT EXISTS `Reports` (
  `repID` int(11) NOT NULL AUTO_INCREMENT,
  `repComment` text,
  `repAbuID` tinyint(4) NOT NULL,
  `repReportedUser` int(11) NOT NULL,
  `repReportingUser` int(11) NOT NULL,
  PRIMARY KEY (`repID`),
  KEY `repAbuID` (`repAbuID`),
  KEY `repReportedUser` (`repReportedUser`),
  KEY `repReportingUser` (`repReportingUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `Reviews`
--

CREATE TABLE IF NOT EXISTS `Reviews` (
  `revID` int(11) NOT NULL AUTO_INCREMENT,
  `revTitle` text NOT NULL,
  `revRating` tinyint(1) unsigned NOT NULL,
  `revComment` text,
  `revDate` date NOT NULL,
  `revOffID` mediumint(9) NOT NULL,
  `revUserID` int(11) NOT NULL,
  PRIMARY KEY (`revID`),
  KEY `revOffID` (`revOffID`),
  KEY `revUserID` (`revUserID`),
  KEY `revRating` (`revRating`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=22 ;

--
-- Dump dei dati per la tabella `Reviews`
--

INSERT INTO `Reviews` (`revID`, `revTitle`, `revRating`, `revComment`, `revDate`, `revOffID`, `revUserID`) VALUES
(1, 'Sito web fantastico!', 5, 'Il sito web realizzato è perfettamente conforme a quanto avevo in mente. Consiglio assolutamente!', '2017-06-01', 1, 4),
(2, 'Sito di e-commerce realizzato molto bene.', 4, 'La piattaforma di e-commerce commissionata è stata realizzata quasi alla perfezione, solo una piccola mancanza nel database ma nulla di difettoso.', '2017-05-10', 1, 2),
(3, 'Molto bravo', 5, 'Riparazione effettuata velocemente, tutto a posto con il computer ora!', '2017-06-10', 12, 6),
(4, 'Buono, solo un piccolo ritardo', 3, 'Il pc funziona bene, c''è solo stato un piccolo ritardo, per questo ho dato tre stelle.', '2017-06-01', 12, 4),
(5, 'Manca qualcosa', 2, 'Sono stati risolti solo alcuni problemi al mio computer, non riesco ancora ad utilizzare Photoshop.', '2017-06-05', 13, 6),
(6, 'Tutto a posto', 4, 'Ho portato il computer ad effettuare una pulizia interna. Ora non esce più polvere dall''apertura per la ventola.', '2017-06-03', 13, 1),
(7, 'Bel video!', 5, 'Il cortometraggio commissionato è fantastico sotto tutti i punti di vista. Ben fatto!', '2017-05-11', 14, 1),
(8, 'Soddisfatto', 4, 'Contento di aver lavorato con Chiara Rossi. Molto capace e creativa durante il montaggio.', '2017-05-22', 14, 6),
(9, 'Buon montaggio', 3, 'L''editing aggiuntivo del video commissionato alla nostra agenzia pubblicitaria ha apportato le migliorie sperate. Si poteva fare un po'' meglio con il suono ma va abbastanza bene anche così.', '2017-05-26', 15, 4),
(10, 'Non ci siamo', 2, 'Il video è editato male, spero sia stata solo una svista e non si ripeterà la prossima volta.', '2017-05-20', 15, 6),
(15, 'Servizio appena creato', 0, 'Il servizio Ã¨ stato appena creato.', '2017-06-11', 19, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `Types`
--

CREATE TABLE IF NOT EXISTS `Types` (
  `typID` tinyint(4) NOT NULL AUTO_INCREMENT,
  `typName` varchar(50) NOT NULL,
  `typInfo` text,
  PRIMARY KEY (`typID`),
  UNIQUE KEY `typName` (`typName`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=6 ;

--
-- Dump dei dati per la tabella `Types`
--

INSERT INTO `Types` (`typID`, `typName`, `typInfo`) VALUES
(1, 'Scam', 'Scam and fraud abuses.'),
(2, 'Identity', 'Identity-related abuses, such as identity theft, etc.'),
(3, 'Harassment', 'Abuses which involve every kind of harassment on other users.'),
(4, 'Inappropriate content', 'Uploaded content which should not be online, such as pornography, etc.'),
(5, 'Spam', 'Spam abuse.');

-- --------------------------------------------------------

--
-- Struttura della tabella `Users`
--

CREATE TABLE IF NOT EXISTS `Users` (
  `usrID` int(11) NOT NULL AUTO_INCREMENT,
  `usrEmail` varchar(100) NOT NULL,
  `usrPassword` varchar(100) NOT NULL,
  `usrUsername` varchar(100) NOT NULL,
  `usrProPic` text,
  `usrPremium` tinyint(1) NOT NULL,
  `usrRegistrationDate` datetime NOT NULL,
  `usrIPAddress` varchar(15) DEFAULT NULL,
  `usrPersonCode` int(11) DEFAULT NULL,
  `usrP_Iva` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`usrID`),
  UNIQUE KEY `usrEmail` (`usrEmail`),
  UNIQUE KEY `usrUsername` (`usrUsername`),
  KEY `usrPersonCode` (`usrPersonCode`),
  KEY `usrP_Iva` (`usrP_Iva`),
  KEY `usrPassword` (`usrPassword`),
  KEY `usrPremium` (`usrPremium`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=13 ;

--
-- Dump dei dati per la tabella `Users`
--

INSERT INTO `Users` (`usrID`, `usrEmail`, `usrPassword`, `usrUsername`, `usrProPic`, `usrPremium`, `usrRegistrationDate`, `usrIPAddress`, `usrPersonCode`, `usrP_Iva`) VALUES
(1, 'and.altomare@gmail.com', 'aireempw', 'andrea.altomare', 'images/andrea_altomare-propic.png', 1, '0000-00-00 00:00:00', '', 1, NULL),
(2, 'staff@abc.xyz', 'alphabetpw', 'alphabet_inc', 'images/default-propic.png', 0, '0000-00-00 00:00:00', '', NULL, '9X99999A'),
(4, 'chiara.rossi@gmail.com', 'chiararossipw', 'chia_rossi', 'images/chia_rossi-propic.png', 0, '0000-00-00 00:00:00', '', 2, NULL),
(5, 'company@aireem.com', 'aireemcompanypw', 'aireem_company', 'images/default-propic.png', 1, '0000-00-00 00:00:00', '', NULL, '99999999999'),
(6, 'carlorossi@gmail.com', 'carlorossiii', 'carlo12', 'images/default-propic.png', 0, '2017-05-16 10:22:00', '10.0.0.1', 3, NULL),
(9, 'walterbianchi@gmail.com', 'breaking', 'walterissimo', 'images/default-propic.png', 0, '2017-05-17 18:59:03', NULL, 6, NULL),
(12, 'alessandro.mazzini@gmail.com', 'mazzinipw', 'ale.mazzini', 'images/ale_mazzini-propic.png', 0, '2017-06-11 21:33:47', NULL, 9, NULL);

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `Abuses`
--
ALTER TABLE `Abuses`
  ADD CONSTRAINT `Abuses_ibfk_1` FOREIGN KEY (`abuTypID`) REFERENCES `Types` (`typID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Appointments`
--
ALTER TABLE `Appointments`
  ADD CONSTRAINT `Appointments_ibfk_1` FOREIGN KEY (`appOffID`) REFERENCES `Offers` (`offID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Appointments_ibfk_2` FOREIGN KEY (`appUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Bank_accounts`
--
ALTER TABLE `Bank_accounts`
  ADD CONSTRAINT `Bank_accounts_ibfk_1` FOREIGN KEY (`bnkUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Blocked`
--
ALTER TABLE `Blocked`
  ADD CONSTRAINT `Blocked_ibfk_1` FOREIGN KEY (`blkBlockedUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Blocked_ibfk_2` FOREIGN KEY (`blkUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Companies`
--
ALTER TABLE `Companies`
  ADD CONSTRAINT `Companies_ibfk_1` FOREIGN KEY (`coCyID`) REFERENCES `Cities` (`cyID`);

--
-- Limiti per la tabella `Messages`
--
ALTER TABLE `Messages`
  ADD CONSTRAINT `Messages_ibfk_1` FOREIGN KEY (`msgSenderUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Messages_ibfk_2` FOREIGN KEY (`msgReceiverUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Notifications`
--
ALTER TABLE `Notifications`
  ADD CONSTRAINT `Notifications_ibfk_1` FOREIGN KEY (`notNotifierUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Notifications_ibfk_2` FOREIGN KEY (`notUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Offers`
--
ALTER TABLE `Offers`
  ADD CONSTRAINT `Offers_ibfk_1` FOREIGN KEY (`offPrfID`) REFERENCES `Performances` (`prfID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Offers_ibfk_2` FOREIGN KEY (`offUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Offers_ibfk_3` FOREIGN KEY (`offCurID`) REFERENCES `Currencies` (`curID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Payment_methods`
--
ALTER TABLE `Payment_methods`
  ADD CONSTRAINT `Payment_methods_ibfk_1` FOREIGN KEY (`pmtUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `PayPal_accounts`
--
ALTER TABLE `PayPal_accounts`
  ADD CONSTRAINT `PayPal_accounts_ibfk_1` FOREIGN KEY (`pypUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `People`
--
ALTER TABLE `People`
  ADD CONSTRAINT `People_ibfk_1` FOREIGN KEY (`pplCyID`) REFERENCES `Cities` (`cyID`);

--
-- Limiti per la tabella `Performances`
--
ALTER TABLE `Performances`
  ADD CONSTRAINT `Performances_ibfk_1` FOREIGN KEY (`prfCatID`) REFERENCES `Categories` (`catID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Reports`
--
ALTER TABLE `Reports`
  ADD CONSTRAINT `Reports_ibfk_1` FOREIGN KEY (`repAbuID`) REFERENCES `Abuses` (`abuID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Reports_ibfk_2` FOREIGN KEY (`repReportedUser`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Reports_ibfk_3` FOREIGN KEY (`repReportingUser`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Reviews`
--
ALTER TABLE `Reviews`
  ADD CONSTRAINT `Reviews_ibfk_1` FOREIGN KEY (`revOffID`) REFERENCES `Offers` (`offID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Reviews_ibfk_2` FOREIGN KEY (`revUserID`) REFERENCES `Users` (`usrID`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Limiti per la tabella `Users`
--
ALTER TABLE `Users`
  ADD CONSTRAINT `Users_ibfk_1` FOREIGN KEY (`usrPersonCode`) REFERENCES `People` (`pplPersonCode`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `Users_ibfk_2` FOREIGN KEY (`usrP_Iva`) REFERENCES `Companies` (`coP_Iva`) ON DELETE NO ACTION ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
