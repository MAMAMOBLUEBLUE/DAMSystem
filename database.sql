/*
SQLyog Community v13.3.0 (64 bit)
MySQL - 10.4.32-MariaDB : Database - qrdatabase
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE `qrdatabase`;

/*Table structure for table `books` */

DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `accession_number` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `YEAR` varchar(20) DEFAULT NULL,
  `call_number` varchar(100) DEFAULT NULL,
  `STATUS` varchar(50) DEFAULT 'Available',
  PRIMARY KEY (`accession_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `books` */

insert  into `books`(`accession_number`,`title`,`author`,`publisher`,`YEAR`,`call_number`,`STATUS`) values 
('ACC-0001','Introduction to Algorithms','Thomas Cormen','MIT Press','2009','QA76.6 C66','Available'),
('ACC-0002','Clean Code','Robert Martin','Prentice Hall','2008','QA76.76 C66','Available'),
('ACC-0003','The Pragmatic Programmer','Andrew Hunt','Addison-Wesley','1999','QA76.6 H86','Available'),
('ACC-0004','Design Patterns','Erich Gamma','Addison-Wesley','1994','QA76.64 D47','Available'),
('ACC-0006','Structure and Interpretation of Computer Programs','Harold Abelson','MIT Press','1996','QA76.6 A23','Available'),
('ACC-0007','Code Complete','Steve McConnell','Microsoft Press','2004','QA76.76 M33','Available'),
('ACC-0008','Refactoring','Martin Fowler','Addison-Wesley','1999','QA76.76 R43','Available'),
('ACC-0009','The Mythical Man-Month','Frederick Brooks','Addison-Wesley','1995','QA76.76 M98','Available'),
('ACC-0010','Head First Design Patterns','Eric Freeman','O\'Reilly','2004','QA76.64 F73','Available'),
('ACC-0011','Effective Java','Joshua Bloch','Addison-Wesley','2018','QA76.73 J38','Available'),
('ACC-0012','JavaScript: The Good Parts','Douglas Crockford','O\'Reilly','2008','QA76.73 J39','Available'),
('ACC-0013','Python Crash Course','Eric Matthes','No Starch Press','2019','QA76.73 P98','Available'),
('ACC-0014','Learning React','Alex Banks','O\'Reilly','2020','QA76.76 R42','Available'),
('ACC-0015','Pro ASP.NET Core 6','Adam Freeman','Apress','2022','QA76.625 F74','Available'),
('ACC-0016','Domain-Driven Design','Eric Evans','Addison-Wesley','2003','QA76.76 D47','Available'),
('ACC-0017','Test Driven Development','Kent Beck','Addison-Wesley','2002','QA76.76 T48','Available'),
('ACC-0018','The Clean Coder','Robert Martin','Prentice Hall','2011','QA76.76 C67','Available'),
('ACC-0019','Working Effectively with Legacy Code','Michael Feathers','Prentice Hall','2004','QA76.76 L43','Available'),
('ACC-0020','Patterns of Enterprise Application Architecture','Martin Fowler','Addison-Wesley','2002','QA76.76 E58','Available'),
('ACC-0021','Computer Networking: A Top-Down Approach','James Kurose','Pearson','2021','TK5105.875 K87','Available'),
('ACC-0022','Operating System Concepts','Abraham Silberschatz','Wiley','2018','QA76.76 O63','Available'),
('ACC-0023','Database System Concepts','Abraham Silberschatz','McGraw-Hill','2019','QA76.9 D3','Available'),
('ACC-00234','asd','asd','asd','asd','asd','Available'),
('ACC-0024','Compilers: Principles Techniques and Tools','Alfred Aho','Pearson','2006','QA76.76 C65','Available'),
('ACC-0025','Modern Operating Systems','Andrew Tanenbaum','Pearson','2014','QA76.76 O63','Available'),
('ACC-0026','The C Programming Language','Brian Kernighan','Prentice Hall','1988','QA76.73 C15','Available'),
('ACC-0027','The Art of Computer Programming Vol 1','Donald Knuth','Addison-Wesley','1997','QA76.6 K68','Available'),
('ACC-0028','Don\'t Make Me Think','Steve Krug','New Riders','2014','QA76.9 H85','Available'),
('ACC-0029','Sprint','Jake Knapp','Simon & Schuster','2016','HD69 P75','Available'),
('ACC-0030','Hooked','Nir Eyal','Portfolio','2014','HF5415.153 E93','Available'),
('ACC-0031','Deep Learning','Ian Goodfellow','MIT Press','2016','Q325.5 G66','Available'),
('ACC-0032','Hands-On Machine Learning','Aurélien Géron','O\'Reilly','2019','Q325.5 G47','Available'),
('ACC-0033','Pattern Recognition and Machine Learning','Christopher Bishop','Springer','2006','Q327 B57','Available'),
('ACC-0034','Data Science for Business','Foster Provost','O\'Reilly','2013','HF5548.2 P76','Available'),
('ACC-0035','The Signal and the Noise','Nate Silver','Penguin','2012','QA279.5 S55','Available'),
('ACC-0036','Superintelligence','Nick Bostrom','Oxford University Press','2014','Q335 B67','Available'),
('ACC-0037','Life 3.0','Max Tegmark','Knopf','2017','Q335 T44','Available'),
('ACC-0038','Thinking Fast and Slow','Daniel Kahneman','Farrar Straus and Giroux','2011','BF441 K23','Available'),
('ACC-0039','Atomic Habits','James Clear','Avery','2018','BF637 H32','Borrowed'),
('ACC-0040','Essentialism','Greg McKeown','Crown Currency','2014','BF637 S4','Available'),
('ACC-0041','Principles','Ray Dalio','Simon & Schuster','2017','HG4928.5 D35','Available'),
('ACC-0042','Zero to One','Peter Thiel','Crown Business','2014','HD62.5 T54','Available'),
('ACC-0043','The Lean Startup','Eric Ries','Crown Business','2011','HD62.5 R54','Available'),
('ACC-0044','Start with Why','Simon Sinek','Portfolio','2009','HD57.7 S55','Available'),
('ACC-0045','Good to Great','Jim Collins','HarperBusiness','2001','HD57.7 C65','Available'),
('ACC-0046','Rich Dad Poor Dad','Robert Kiyosaki','Plata Publishing','2017','HG179 K59','Available'),
('ACC-0047','The Psychology of Money','Morgan Housel','Harriman House','2020','HG222.3 H68','Available'),
('ACC-0048','Measure What Matters','John Doerr','Portfolio','2018','HD58.9 D64','Available'),
('ACC-0049','Grit','Angela Duckworth','Scribner','2016','BF637 P4','Available'),
('ACC-0050','Mindset','Carol Dweck','Random House','2006','BF637 S4','Available'),
('ACC-0088','NewBOOK','NewBOOK','NewBOOK','2022','Q335 R85','Available');

/*Table structure for table `due_soon_notifications` */

DROP TABLE IF EXISTS `due_soon_notifications`;

CREATE TABLE `due_soon_notifications` (
  `tx_id` varchar(80) NOT NULL,
  `student_number` varchar(50) NOT NULL,
  `accession_number` varchar(100) NOT NULL,
  `sent_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`tx_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `due_soon_notifications` */

insert  into `due_soon_notifications`(`tx_id`,`student_number`,`accession_number`,`sent_at`) values 
('01d39d27-ce4','23-0000','ACC-0007','2025-11-22 12:18:05'),
('1e901b9b-d74','23-0000','ACC-0016','2025-11-15 09:52:05'),
('28a424c7-28a','23-0717','ACC-0020','2025-11-22 21:06:03'),
('2d418184-576','23-0717','ACC-0009','2025-11-04 00:28:20'),
('306d80f1-664','23-0717','ACC-0005','2025-11-23 18:53:28'),
('3962b84d-d48','23-0717','ACC-0055','2025-11-22 14:11:34'),
('48fc2042-849','23-0717','ACC-0005','2025-11-23 02:49:03'),
('4b2b56a7-9b1','23-0717','ACC-0012','2025-11-22 21:21:03'),
('5da8fce5-7cb','23-0717','ACC-0001','2025-11-22 15:00:03'),
('61a3c3ed-986','23-0717','ACC-0005','2025-11-23 00:00:47'),
('625e1c6d-213','23-0717','ACC-0039','2025-11-22 23:55:45'),
('6f1a3d1d-3be','23-0717','ACC-0021','2025-11-23 21:16:43'),
('86cb37de-fbd','23-0717','ACC-00234','2025-11-24 13:32:35'),
('8ac418c9-28f','23-0717','ACC-0010','2025-11-22 16:35:03'),
('95013040-da4','23-0717','ACC-0001','2025-11-03 22:55:10'),
('96073d73-2af','23-0717','ACC-0012','2025-11-04 02:43:33'),
('c9bb60bc-af8','23-0717','ACC-0034','2025-11-23 21:06:40'),
('db86f442-5ac','23-0717','ACC-0005','2025-11-23 14:52:05'),
('e6d34227-271','23-0717','ACC-0006','2025-11-04 00:17:04'),
('edc8435a-bcc','23-0717','ACC-0005','2025-11-23 18:37:31'),
('ee255a6a-15c','23-2000','ACC-0044','2025-11-22 13:15:14');

/*Table structure for table `lost_book_resolutions` */

DROP TABLE IF EXISTS `lost_book_resolutions`;

CREATE TABLE `lost_book_resolutions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tx_id` varchar(80) NOT NULL,
  `student_number` varchar(50) NOT NULL,
  `accession_number` varchar(100) NOT NULL,
  `resolution_type` enum('same_book','similar_value') NOT NULL,
  `status` enum('pending','resolved') DEFAULT 'pending',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `tx_id` (`tx_id`),
  KEY `student_number` (`student_number`),
  CONSTRAINT `lost_book_resolutions_ibfk_1` FOREIGN KEY (`tx_id`) REFERENCES `transactions` (`tx_id`) ON DELETE CASCADE,
  CONSTRAINT `lost_book_resolutions_ibfk_2` FOREIGN KEY (`student_number`) REFERENCES `students` (`student_number`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `lost_book_resolutions` */

insert  into `lost_book_resolutions`(`id`,`tx_id`,`student_number`,`accession_number`,`resolution_type`,`status`,`created_at`) values 
(7,'fa8a1cce-624','23-0717','ACC-0005','same_book','resolved','2025-11-23 17:47:09'),
(8,'a0916634-e30','23-0717','ACC-0024','similar_value','resolved','2025-11-23 17:48:45'),
(9,'b41c2130-2de','23-0717','ACC-0024','same_book','resolved','2025-11-23 18:03:55'),
(10,'28160293-18e','23-0717','ACC-0024','similar_value','pending','2025-11-23 18:32:27'),
(11,'098bcef6-5de','23-0717','ACC-0005','same_book','resolved','2025-11-23 18:45:49'),
(12,'1dbbdd49-ada','23-0717','ACC-0005','similar_value','resolved','2025-11-23 19:12:36'),
(13,'a0bc9f43-9a4','23-0717','ACC-0005','similar_value','resolved','2025-11-23 19:29:04'),
(14,'595de1eb-427','23-0717','ACC-0039','same_book','resolved','2025-11-23 19:31:53'),
(15,'f7037662-428','23-0717','ACC-0035','similar_value','resolved','2025-11-23 20:04:30'),
(16,'f8de023d-70b','23-0717','ACC-0002','similar_value','resolved','2025-11-23 20:06:16'),
(17,'72ecccb2-f8d','23-0717','ACC-0001','similar_value','resolved','2025-11-23 20:17:56'),
(18,'ffb96d7c-8bb','23-0717','ACC-0003','similar_value','resolved','2025-11-23 20:30:08'),
(19,'0bd778a3-1e3','23-0717','ACC-0042','similar_value','resolved','2025-11-23 20:36:34'),
(20,'d070c219-bc0','23-0717','ACC-0007	','similar_value','pending','2025-11-23 20:43:21'),
(21,'ff8d1fb7-628','23-0717','ACC-0024','similar_value','resolved','2025-11-23 20:45:43'),
(22,'aee9f7ef-404','23-0717','ACC-0034','similar_value','resolved','2025-11-23 21:08:39'),
(23,'2bf357a6-604','23-0717','ACC-0021','similar_value','resolved','2025-11-23 21:09:50'),
(24,'9488a6cd-d42','23-0717','ACC-0021','similar_value','resolved','2025-11-23 21:16:54'),
(25,'24c1f366-7f6','23-0717','ACC-0024','similar_value','resolved','2025-11-23 23:27:34'),
(26,'8f8bc04b-8c7','23-0717','ACC-0039','similar_value','resolved','2025-11-24 13:43:52'),
(27,'591c4056-919','23-0717','ACC-0002','similar_value','resolved','2025-11-26 13:52:36'),
(28,'6087da9d-432','23-0717','ACC-0005','similar_value','resolved','2025-11-26 18:40:01');

/*Table structure for table `payments` */

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_number` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`payment_id`),
  KEY `student_number` (`student_number`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`student_number`) REFERENCES `students` (`student_number`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `payments` */

insert  into `payments`(`payment_id`,`student_number`,`amount`,`payment_date`) values 
(1,'23-0717',5.00,'2025-11-23 02:22:05'),
(2,'23-0717',5.00,'2025-11-23 02:22:10'),
(3,'23-0717',5.00,'2025-11-23 02:24:31'),
(4,'23-0717',5.00,'2025-11-23 02:38:34'),
(5,'23-0717',60.00,'2025-11-23 14:34:18'),
(6,'23-0717',60.00,'2025-11-23 14:50:46'),
(7,'23-0717',120.00,'2025-11-23 15:03:36'),
(8,'23-0717',120.00,'2025-11-23 15:03:41'),
(9,'23-0717',125.00,'2025-11-23 15:09:13'),
(10,'23-0717',130.00,'2025-11-23 15:14:52'),
(11,'23-0717',130.00,'2025-11-23 15:20:04'),
(12,'23-0717',5.00,'2025-11-23 16:10:37'),
(14,'23-0717',5.00,'2025-11-23 17:46:12'),
(15,'23-0717',230.00,'2025-11-23 21:32:37'),
(16,'23-0717',1685.00,'2025-11-23 21:35:57'),
(17,'23-0717',1480.00,'2025-11-26 14:03:04'),
(18,'23-0717',245.00,'2025-11-26 14:08:26'),
(19,'23-0717',385.00,'2025-11-26 18:44:55');

/*Table structure for table `students` */

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_number` varchar(50) NOT NULL,
  `student_name` varchar(200) NOT NULL,
  `course` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `PASSWORD` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_number` (`student_number`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `students` */

insert  into `students`(`id`,`student_number`,`student_name`,`course`,`department`,`contact`,`PASSWORD`) values 
(50,'23-0717','Aldrin S. Samson','BSCS','CCSICT','aldrinsamson07@gmail.com','Aldrin123456@'),
(61,'23-2001','Mary angel C. Nayga','CCSICT','CS','aldrinsamson07@gmail.com','Aldrin1234'),
(62,'23-2002','Doerson Bernardo','CCSICT','CS','aldrinsamson07@gmail.com','sad'),
(63,'23-2003','Student1','course1','dept1','aldrinsamson07@gmail.com','Aldrin123456@'),
(64,'23-9999','Aldrin samson','CS','ccsict','aldrinsamson07@gmail.com','aldrin9999'),
(65,'23-7777','Pepito Manaloto','CS','CCSICT','aldrinsamson07@gmail.com','pepito7777'),
(66,'23-2009','Aldrin Samson','CS','CCSICT','aldrinsamson07@gmail.com','aldrin2009');

/*Table structure for table `transactions` */

DROP TABLE IF EXISTS `transactions`;

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tx_id` varchar(80) NOT NULL,
  `student_number` varchar(50) NOT NULL,
  `accession_number` varchar(100) DEFAULT NULL,
  `call_number` varchar(100) DEFAULT NULL,
  `action_type` enum('borrow','return','lost') NOT NULL,
  `DATE` datetime NOT NULL DEFAULT current_timestamp(),
  `due_date` datetime DEFAULT NULL,
  `returned_date` datetime DEFAULT NULL,
  `note` text DEFAULT NULL,
  `is_penalty_paid` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tx_id` (`tx_id`),
  KEY `accession_number` (`accession_number`),
  KEY `student_number` (`student_number`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`accession_number`) REFERENCES `books` (`accession_number`) ON DELETE SET NULL,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`student_number`) REFERENCES `students` (`student_number`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `transactions` */

insert  into `transactions`(`id`,`tx_id`,`student_number`,`accession_number`,`call_number`,`action_type`,`DATE`,`due_date`,`returned_date`,`note`,`is_penalty_paid`) values 
(1,'625e1c6d-213','23-0717',NULL,'BF637 H32','borrow','2025-11-22 23:51:45','2025-11-23 04:53:00','2025-11-23 02:39:36',NULL,1),
(2,'61a3c3ed-986','23-0717','ACC-0088','Q335 R87','borrow','2025-11-22 23:59:49','2025-11-23 04:01:00','2025-11-23 02:39:36',NULL,1),
(3,'cf57610a-aad','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-23 02:19:40','2025-11-23 02:19:00','2025-11-23 02:23:50',NULL,1),
(4,'e22162fb-ccf','23-0717','ACC-0002','QA76.76 C66','return','2025-11-23 02:23:50','2025-11-23 02:19:00','2025-11-23 02:23:50',NULL,1),
(5,'2bc79304-4c9','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-23 02:37:08','2025-11-23 02:37:00','2025-11-23 02:39:36',NULL,1),
(6,'cc770fb3-2e5','23-0717','ACC-0002','QA76.76 C66','return','2025-11-23 02:39:36','2025-11-23 02:37:00','2025-11-23 02:39:36',NULL,1),
(7,'619db315-d63','23-0717','ACC-0088','Q335 R87','return','2025-11-23 02:39:36','2025-11-23 04:01:00','2025-11-23 02:39:36',NULL,1),
(8,'cb676b54-623','23-0717',NULL,'BF637 H32','return','2025-11-23 02:39:36','2025-11-23 04:53:00','2025-11-23 02:39:36',NULL,1),
(9,'b43ebfdb-315','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 02:39:53','2025-11-23 02:41:00','2025-11-23 02:42:13',NULL,1),
(10,'eb6e54ee-68f','23-0717','ACC-0088','Q335 R87','return','2025-11-23 02:42:13','2025-11-23 02:41:00','2025-11-23 02:42:13',NULL,1),
(11,'48fc2042-849','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 02:48:44','2025-11-23 02:49:00','2025-11-23 02:51:06',NULL,1),
(12,'dd106af7-edb','23-0717','ACC-0088','Q335 R87','return','2025-11-23 02:51:06','2025-11-23 02:49:00','2025-11-23 02:51:06',NULL,1),
(13,'b9b71fbf-635','23-0717',NULL,'BF637 H32','borrow','2025-11-23 02:51:37','2025-11-23 02:52:00','2025-11-23 14:36:14',NULL,1),
(14,'620f7b44-6e4','23-0717',NULL,'BF637 H32','return','2025-11-23 14:36:14','2025-11-23 02:52:00','2025-11-23 14:36:14',NULL,1),
(15,'db86f442-5ac','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 14:50:14','2025-11-23 15:02:00','2025-11-23 15:09:48',NULL,1),
(16,'7af5204c-9a8','23-0717',NULL,'BF637 H32','borrow','2025-11-23 14:52:36','2025-11-23 14:52:00','2025-11-23 15:09:48',NULL,1),
(17,'b955d9c3-025','23-0717',NULL,'BF637 H32','return','2025-11-23 15:09:48','2025-11-23 14:52:00','2025-11-23 15:09:48',NULL,1),
(18,'e02aed2b-f87','23-0717','ACC-0088','Q335 R87','return','2025-11-23 15:09:48','2025-11-23 15:02:00','2025-11-23 15:09:48',NULL,1),
(19,'7efa67b0-b6b','23-0717',NULL,'BF637 H32','borrow','2025-11-23 15:25:59','2025-11-23 15:25:00','2025-11-23 16:11:44',NULL,1),
(20,'4e215e9f-d2b','23-0717',NULL,'BF637 H32','return','2025-11-23 16:11:44','2025-11-23 15:25:00','2025-11-23 16:11:44',NULL,1),
(21,'31f3a05e-7c4','23-0717',NULL,'QA76.76 M33','borrow','2025-11-23 16:12:11','2025-11-23 16:12:00','2025-11-23 16:13:34',NULL,1),
(22,'f006231d-39f','23-0717',NULL,'QA76.76 M33','lost','2025-11-23 16:13:02','2025-11-23 16:12:00',NULL,NULL,1),
(23,'aae5e901-b8f','23-0717',NULL,'QA76.76 M33','lost','2025-11-23 16:13:08','2025-11-23 16:12:00',NULL,NULL,1),
(24,'8fc17aa2-dd8','23-0717',NULL,'QA76.76 M33','return','2025-11-23 16:13:34','2025-11-23 16:12:00','2025-11-23 16:13:34',NULL,1),
(25,'ee32d912-3ea','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 16:15:43','2025-11-23 16:15:00','2025-11-23 16:19:52',NULL,1),
(26,'cd25e8b5-82b','23-0717','ACC-0088','Q335 R87','lost','2025-11-23 16:16:10','2025-11-23 16:15:00',NULL,NULL,1),
(27,'dbfeee10-d57','23-0717','ACC-0088',NULL,'return','2025-11-23 16:17:10',NULL,'2025-11-23 16:17:10',NULL,1),
(28,'ad462555-7ed','23-0717','ACC-0088','Q335 R87','return','2025-11-23 16:19:52','2025-11-23 16:15:00','2025-11-23 16:19:52',NULL,1),
(29,'acd02ab4-ab8','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 16:44:20','2025-11-23 16:44:00','2025-11-23 17:06:31',NULL,1),
(30,'742e321c-f3a','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 16:44:26','2025-11-23 16:44:00','2025-11-23 17:06:31',NULL,1),
(31,'9c53c746-4e7','23-0717',NULL,'BF637 H32','borrow','2025-11-23 16:45:08','2025-11-23 16:45:00','2025-11-23 17:04:00',NULL,1),
(32,'d3724e4f-316','23-0717',NULL,'BF637 H32','lost','2025-11-23 16:47:14','2025-11-23 16:45:00',NULL,NULL,1),
(33,'dad057b5-69e','23-0717',NULL,NULL,'return','2025-11-23 16:48:45',NULL,'2025-11-23 16:48:45',NULL,1),
(34,'43dfe1c2-403','23-0717',NULL,'BF637 H32','lost','2025-11-23 16:53:04','2025-11-23 16:45:00',NULL,NULL,1),
(35,'f8f0421f-029','23-0717',NULL,NULL,'return','2025-11-23 16:53:20',NULL,'2025-11-23 16:53:20',NULL,1),
(36,'c00546f3-18d','23-0717',NULL,'BF637 H32','borrow','2025-11-23 17:03:09','2025-11-23 17:03:00','2025-11-23 17:04:00',NULL,1),
(37,'ea616c64-0a0','23-0717',NULL,'BF637 H32','lost','2025-11-23 17:03:36','2025-11-23 17:03:00',NULL,NULL,1),
(38,'3210b2a5-5ae','23-0717',NULL,NULL,'return','2025-11-23 17:04:00',NULL,'2025-11-23 17:04:00',NULL,1),
(39,'3838f5c0-cee','23-0717','ACC-0088','Q335 R87','return','2025-11-23 17:06:31','2025-11-23 16:44:00','2025-11-23 17:06:31',NULL,1),
(40,'35a1a79e-b70','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 17:45:15','2025-11-23 17:45:00','2025-11-23 17:47:09',NULL,1),
(41,'fa8a1cce-624','23-0717','ACC-0088','Q335 R87','lost','2025-11-23 17:47:09','2025-11-23 17:45:00',NULL,NULL,1),
(42,'8e24c81c-5dc','23-0717','ACC-0088',NULL,'return','2025-11-23 17:47:51',NULL,'2025-11-23 17:47:51',NULL,1),
(43,'d6e59267-840','23-0717',NULL,'QA76.76 C65','borrow','2025-11-23 17:48:33','2025-11-23 17:48:00','2025-11-23 17:48:45',NULL,1),
(44,'a0916634-e30','23-0717',NULL,'QA76.76 C65','lost','2025-11-23 17:48:45','2025-11-23 17:48:00','2025-11-23 20:46:08',NULL,1),
(45,'245ec5ea-c49','23-0717',NULL,NULL,'return','2025-11-23 18:01:09',NULL,'2025-11-23 18:01:09',NULL,1),
(46,'9db1759a-dab','23-0717',NULL,'QA76.76 C65','borrow','2025-11-23 18:03:41','2025-11-23 18:03:00','2025-11-23 18:03:55',NULL,1),
(47,'b41c2130-2de','23-0717',NULL,'QA76.76 C65','lost','2025-11-23 18:03:55','2025-11-23 18:03:00','2025-11-23 20:46:08',NULL,1),
(48,'6867d56c-de6','23-0717',NULL,NULL,'return','2025-11-23 18:04:05',NULL,'2025-11-23 18:04:05',NULL,1),
(49,'ed0addef-2b1','23-0717',NULL,'QA76.76 C65','borrow','2025-11-23 18:30:58','2025-11-23 18:30:00','2025-11-23 18:32:27',NULL,1),
(50,'edc8435a-bcc','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 18:32:09','2025-11-23 23:33:00','2025-11-23 18:45:49',NULL,1),
(51,'28160293-18e','23-0717',NULL,'QA76.76 C65','lost','2025-11-23 18:32:27','2025-11-23 18:30:00','2025-11-23 20:46:08',NULL,1),
(52,'5353ef5e-95f','23-0717',NULL,'BF637 H32','borrow','2025-11-23 18:43:27','2025-11-23 23:45:00','2025-11-23 18:45:29',NULL,1),
(53,'5bc5336a-940','23-0717',NULL,'BF637 H32','return','2025-11-23 18:45:29','2025-11-23 23:45:00','2025-11-23 18:45:29',NULL,1),
(54,'098bcef6-5de','23-0717','ACC-0088','Q335 R87','lost','2025-11-23 18:45:49','2025-11-23 23:33:00',NULL,NULL,1),
(55,'ec4ce7ba-679','23-0717','ACC-0088',NULL,'return','2025-11-23 18:48:43',NULL,'2025-11-23 18:48:43',NULL,1),
(56,'306d80f1-664','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 18:50:14','2025-11-23 23:52:00','2025-11-23 19:12:36',NULL,1),
(57,'1dbbdd49-ada','23-0717','ACC-0088','Q335 R87','lost','2025-11-23 19:12:36','2025-11-23 23:52:00',NULL,NULL,1),
(58,'eff52ef2-cf9','23-0717','ACC-0088',NULL,'return','2025-11-23 19:23:22',NULL,'2025-11-23 19:23:22',NULL,1),
(59,'a907565c-a0c','23-0717','ACC-0088','Q335 R87','borrow','2025-11-23 19:27:40','2025-11-24 00:29:00','2025-11-23 19:29:04',NULL,1),
(60,'a0bc9f43-9a4','23-0717','ACC-0088','Q335 R87','lost','2025-11-23 19:29:04','2025-11-24 00:29:00',NULL,NULL,1),
(61,'fda9f8bc-733','23-0717','ACC-0088',NULL,'return','2025-11-23 19:30:04',NULL,'2025-11-23 19:30:04',NULL,1),
(62,'4cb3d55c-1fe','23-0717',NULL,'BF637 H32','borrow','2025-11-23 19:31:44','2025-11-24 19:31:00','2025-11-23 19:31:53',NULL,1),
(63,'595de1eb-427','23-0717',NULL,'BF637 H32','lost','2025-11-23 19:31:53','2025-11-24 19:31:00',NULL,NULL,1),
(64,'c93a8702-d7c','23-0717',NULL,NULL,'return','2025-11-23 19:47:44',NULL,'2025-11-23 19:47:44',NULL,1),
(65,'2245badc-51e','23-0717','ACC-0035','QA279.5 S55','borrow','2025-11-23 20:04:08','2025-11-23 22:04:00','2025-11-23 20:04:30',NULL,1),
(66,'f7037662-428','23-0717','ACC-0035','QA279.5 S55','lost','2025-11-23 20:04:30','2025-11-23 22:04:00',NULL,NULL,1),
(67,'f2763e91-351','23-0717','ACC-0035',NULL,'return','2025-11-23 20:04:57',NULL,'2025-11-23 20:04:57',NULL,1),
(68,'314dcd54-327','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-23 20:05:47','2025-11-23 22:05:00','2025-11-23 20:06:16',NULL,1),
(69,'f8de023d-70b','23-0717','ACC-0002','QA76.76 C66','lost','2025-11-23 20:06:16','2025-11-23 22:05:00','2025-11-23 20:16:54',NULL,1),
(70,'3d07cae7-664','23-0717','ACC-0002',NULL,'return','2025-11-23 20:16:54',NULL,'2025-11-23 20:16:54',NULL,1),
(71,'a8c9de82-52e','23-0717','ACC-0001','QA76.6 C66','borrow','2025-11-23 20:17:32','2025-11-23 20:19:00','2025-11-23 20:17:56',NULL,1),
(72,'72ecccb2-f8d','23-0717','ACC-0001','QA76.6 C66','lost','2025-11-23 20:17:56','2025-11-23 20:19:00','2025-11-23 20:18:45',NULL,1),
(73,'c0c6bdd4-b36','23-0717','ACC-0001',NULL,'return','2025-11-23 20:18:45',NULL,'2025-11-23 20:18:45',NULL,1),
(74,'e65f6e03-7cf','23-0717','ACC-0003','QA76.6 H86','borrow','2025-11-23 20:29:54','2025-11-24 20:29:00','2025-11-23 20:30:08',NULL,1),
(75,'ffb96d7c-8bb','23-0717','ACC-0003','QA76.6 H86','lost','2025-11-23 20:30:08','2025-11-24 20:29:00','2025-11-23 20:30:37',NULL,1),
(76,'427a6a3f-5ca','23-0717','ACC-0003',NULL,'return','2025-11-23 20:30:37',NULL,'2025-11-23 20:30:37',NULL,1),
(77,'5d519e07-7f5','23-0717','ACC-0042','HD62.5 T54','borrow','2025-11-23 20:34:57','2025-11-23 20:38:00','2025-11-23 20:36:34',NULL,1),
(78,'0bd778a3-1e3','23-0717','ACC-0042','HD62.5 T54','lost','2025-11-23 20:36:34','2025-11-23 20:38:00','2025-11-23 20:36:53',NULL,1),
(79,'e79bf518-3ee','23-0717','ACC-0042',NULL,'return','2025-11-23 20:36:53',NULL,'2025-11-23 20:36:53',NULL,1),
(80,'5e717154-ae2','23-0717',NULL,'a','borrow','2025-11-23 20:37:31','2025-11-23 20:39:00','2025-11-23 20:37:47',NULL,1),
(81,'32b54fb7-4d7','23-0717',NULL,'a','return','2025-11-23 20:37:47','2025-11-23 20:39:00','2025-11-23 20:37:47',NULL,1),
(82,'fea7dc5a-4fc','23-0717',NULL,'a','borrow','2025-11-23 20:42:33','2025-11-23 20:45:00','2025-11-23 20:43:21',NULL,1),
(83,'d070c219-bc0','23-0717',NULL,'a','lost','2025-11-23 20:43:21','2025-11-23 20:45:00',NULL,NULL,1),
(84,'cab05e0f-bf4','23-0717',NULL,'QA76.76 C65','borrow','2025-11-23 20:45:09','2025-11-23 20:47:00','2025-11-23 20:45:43',NULL,1),
(85,'ff8d1fb7-628','23-0717',NULL,'QA76.76 C65','lost','2025-11-23 20:45:43','2025-11-23 20:47:00','2025-11-23 20:46:08',NULL,1),
(86,'f46b68e5-9b1','23-0717',NULL,NULL,'return','2025-11-23 20:46:08',NULL,'2025-11-23 20:46:08',NULL,1),
(87,'f96cf835-cc0','23-0717',NULL,'TK5105.875 K87','borrow','2025-11-23 21:01:02','2025-11-23 12:00:00','2025-11-23 21:09:50',NULL,1),
(88,'c9bb60bc-af8','23-0717','ACC-0034','HF5548.2 P76','borrow','2025-11-23 21:03:09','2025-11-23 23:05:00','2025-11-23 21:08:39',NULL,1),
(89,'8e7ac64b-e43','23-0717',NULL,'QA76.9 D3','borrow','2025-11-23 21:05:14','2025-11-23 14:08:00','2025-11-23 21:08:18',NULL,1),
(90,'b6d27a64-af4','23-0717',NULL,'QA76.9 D3','return','2025-11-23 21:08:18','2025-11-23 14:08:00','2025-11-23 21:08:18',NULL,1),
(91,'aee9f7ef-404','23-0717','ACC-0034','HF5548.2 P76','lost','2025-11-23 21:08:39','2025-11-23 23:05:00','2025-11-23 21:08:58',NULL,1),
(92,'b3fd8c33-cf3','23-0717','ACC-0034',NULL,'return','2025-11-23 21:08:58',NULL,'2025-11-23 21:08:58',NULL,1),
(93,'2bf357a6-604','23-0717',NULL,'TK5105.875 K87','lost','2025-11-23 21:09:50','2025-11-23 12:00:00','2025-11-23 21:10:09',NULL,1),
(94,'47a66f07-fd7','23-0717',NULL,NULL,'return','2025-11-23 21:10:09',NULL,'2025-11-23 21:10:09',NULL,1),
(95,'6f1a3d1d-3be','23-0717',NULL,'TK5105.875 K87','borrow','2025-11-23 21:16:28','2025-11-23 23:16:00','2025-11-23 21:16:54',NULL,1),
(96,'9488a6cd-d42','23-0717',NULL,'TK5105.875 K87','lost','2025-11-23 21:16:54','2025-11-23 23:16:00','2025-11-23 21:17:27',NULL,1),
(97,'7c9d20e8-814','23-0717',NULL,NULL,'return','2025-11-23 21:17:27',NULL,'2025-11-23 21:17:27',NULL,1),
(98,'5a6457d6-87e','23-0717',NULL,'QA76.9 D3','borrow','2025-11-23 21:35:30','2025-11-09 21:35:00','2025-11-23 23:20:33',NULL,1),
(99,'03b3897c-9ef','23-0717',NULL,'QA76.9 D3','return','2025-11-23 23:20:33','2025-11-09 21:35:00','2025-11-23 23:20:33',NULL,1),
(100,'ca586230-185','23-0717','ACC-0021','TK5105.875 K87','borrow','2025-11-23 23:26:26','2025-11-23 23:28:00','2025-11-26 14:05:11',NULL,1),
(101,'2001731d-46e','23-0717','ACC-0022','QA76.76 O63','borrow','2025-11-23 23:26:46','2025-11-23 23:28:00','2025-11-26 14:05:07',NULL,1),
(102,'89902bb1-03b','23-0717','ACC-0023','QA76.9 D3','borrow','2025-11-23 23:26:59','2025-11-23 23:28:00','2025-11-26 14:05:03',NULL,1),
(103,'92a75269-fb0','23-0717','ACC-0024','QA76.76 C65','borrow','2025-11-23 23:27:18','2025-11-23 23:28:00','2025-11-23 23:27:34',NULL,1),
(104,'24c1f366-7f6','23-0717','ACC-0024','QA76.76 C65','lost','2025-11-23 23:27:34','2025-11-23 23:28:00','2025-11-26 18:42:36',NULL,1),
(105,'86cb37de-fbd','23-0717','ACC-00234','asd','borrow','2025-11-24 13:24:15','2025-11-24 18:26:00','2025-11-26 14:04:58',NULL,1),
(106,'3a806be3-412','23-0717','ACC-0039','BF637 H32','borrow','2025-11-24 13:43:39','2025-11-24 17:43:00','2025-11-24 13:43:52',NULL,1),
(107,'8f8bc04b-8c7','23-0717','ACC-0039','BF637 H32','lost','2025-11-24 13:43:52','2025-11-24 17:43:00','2025-11-24 17:00:56',NULL,1),
(108,'59e29a69-b95','23-0717','ACC-0039',NULL,'return','2025-11-24 17:00:56',NULL,'2025-11-24 17:00:56',NULL,1),
(109,'6350b9b3-b4a','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-26 13:48:41','2025-11-28 13:48:00','2025-11-26 13:49:23',NULL,1),
(110,'79f88558-a71','23-0717','ACC-0002','QA76.76 C66','return','2025-11-26 13:49:23','2025-11-28 13:48:00','2025-11-26 13:49:23',NULL,1),
(111,'45af03a6-6b2','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-26 13:50:16','2025-11-28 13:48:00','2025-11-26 13:52:36',NULL,1),
(112,'591c4056-919','23-0717','ACC-0002','QA76.76 C66','lost','2025-11-26 13:52:36','2025-11-28 13:48:00','2025-11-26 13:56:29',NULL,1),
(113,'dfb0b79f-095','23-0717','ACC-0002',NULL,'return','2025-11-26 13:56:29',NULL,'2025-11-26 13:56:29',NULL,1),
(114,'d46ab5ca-8b6','23-0717','ACC-0005','Q335 R87','borrow','2025-11-26 14:03:52','2025-11-24 14:03:00','2025-11-26 18:40:01',NULL,1),
(115,'a90aa89f-673','23-0717','ACC-00234','asd','return','2025-11-26 14:04:58','2025-11-24 18:26:00','2025-11-26 14:04:58',NULL,1),
(116,'85331798-17c','23-0717','ACC-0023','QA76.9 D3','return','2025-11-26 14:05:03','2025-11-23 23:28:00','2025-11-26 14:05:03',NULL,1),
(117,'1064a37f-690','23-0717','ACC-0022','QA76.76 O63','return','2025-11-26 14:05:07','2025-11-23 23:28:00','2025-11-26 14:05:07',NULL,1),
(118,'bcceea2c-fd5','23-0717','ACC-0021','TK5105.875 K87','return','2025-11-26 14:05:11','2025-11-23 23:28:00','2025-11-26 14:05:11',NULL,1),
(119,'405f4f13-8c0','23-0717','ACC-0039','BF637 H32','borrow','2025-11-26 14:09:12','2025-11-23 14:09:00',NULL,NULL,1),
(120,'309ce96e-84a','23-0717','ACC-0002','QA76.76 C66','borrow','2025-11-26 18:37:46','2025-11-28 18:37:00','2025-11-26 18:38:30',NULL,1),
(121,'ca83cccf-73f','23-0717','ACC-0002','QA76.76 C66','return','2025-11-26 18:38:30','2025-11-28 18:37:00','2025-11-26 18:38:30',NULL,1),
(122,'6087da9d-432','23-0717','ACC-0005','Q335 R87','lost','2025-11-26 18:40:01','2025-11-24 14:03:00','2025-11-26 18:41:34',NULL,1),
(123,'d6492603-3e2','23-0717','ACC-0005',NULL,'return','2025-11-26 18:41:34',NULL,'2025-11-26 18:41:34','Resolved (Book Deleted) - Original: Artificial Intelligence: A Modern Approach',1),
(124,'091b47bc-0ad','23-0717','ACC-0024',NULL,'return','2025-11-26 18:42:36',NULL,'2025-11-26 18:42:36','Replacement Received (Resolved Lost Book)',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
