/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.5-10.4.14-MariaDB : Database - py_insurance_management
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`py_insurance_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `py_insurance_management`;

/*Table structure for table `agent` */

DROP TABLE IF EXISTS `agent`;

CREATE TABLE `agent` (
  `agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `f_name` varchar(100) DEFAULT NULL,
  `l_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`agent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `agent` */

/*Table structure for table `claim` */

DROP TABLE IF EXISTS `claim`;

CREATE TABLE `claim` (
  `claim_id` int(11) NOT NULL AUTO_INCREMENT,
  `policy_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `cert_of_proof` varchar(100) DEFAULT NULL,
  `policy_doc` varchar(100) DEFAULT NULL,
  `id_proof` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`claim_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `claim` */

insert  into `claim`(`claim_id`,`policy_id`,`user_id`,`cert_of_proof`,`policy_doc`,`id_proof`,`status`) values (1,1,4,'static/certificate/9c0baf09-77e9-4b2a-a553-8e63946abf4dimg1.jpg','static/document_policy/4e676d66-7c47-4965-aef1-3f3c8c21d635policy_doc_1.pdf','static/id_proof/04920966-25c8-4844-8207-0048e19d426fpexels-pixabay-209977 (1).jpg','pending');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`user_id`,`complaint`,`reply`,`date`) values (1,4,'hi','reply-pending','2022-04-16'),(2,2,'hiii','reply-pending','2022-06-14 '),(3,2,'','reply-pending','2022-06-14');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','admin','admin'),(2,'aleena','a','client'),(3,'alen','alen','client'),(4,'alen','alen','client'),(5,'alen','alen','client'),(6,'a','a','client'),(7,'a','aa','client'),(8,'afeefa','afeefa','client');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `policy_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `payment` */

/*Table structure for table `policy` */

DROP TABLE IF EXISTS `policy`;

CREATE TABLE `policy` (
  `policy_id` int(11) NOT NULL AUTO_INCREMENT,
  `policy` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `sum_assured` varchar(100) DEFAULT NULL,
  `premium` varchar(100) DEFAULT NULL,
  `tenure` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`policy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `policy` */

insert  into `policy`(`policy_id`,`policy`,`category`,`sum_assured`,`premium`,`tenure`) values (1,'policy no.3045','house','5000','100','10'),(2,'policy no.3001','vehicle','10000','200','20');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `policy_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

/*Data for the table `request` */

insert  into `request`(`request_id`,`policy_id`,`user_id`,`date`,`status`) values (1,1,1,'2022-04-16','accept'),(6,1,4,'2022-04-27','accept'),(7,111,2,'2022-07-03','pending'),(8,1,4,'2022-07-14','pending'),(11,2,5,'2022-07-14','pending'),(13,1,10,'2022-07-15','accept');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob` varchar(100) DEFAULT NULL,
  `hname` varchar(100) DEFAULT NULL,
  `profile` varchar(1000) DEFAULT NULL,
  `id_proof` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`,`dob`,`hname`,`profile`,`id_proof`) values (4,2,'Aleena','k','kochi','9988776655','a@gmail.com','2022-07-13','kalarikkal','static/profile45c6def8-ea44-4977-9334-4cf7f8b10306team-3.jpg','static/id_proofc1e8a9f6-0525-40e1-abe4-71baf40b2cfc11.jpg'),(5,3,'Alen','M','kollam','9988775544','athira@gmail.com','1989-05-18','madathiveetil','static/profile0c75fb5e-9fe6-4d8d-beaf-454b1c800124team-2.jpg','static/id_proof9e153575-0a89-45bd-9b25-d703b310277c4.jpg'),(6,4,'Alen','M','kollam','9988775544','athira@gmail.com','1989-05-18','madathiveetil','static/profile59cc57e3-2009-4c39-b8f7-3b84cf14be94team-2.jpg','static/id_proof266bad65-5b64-460c-8bd9-9a4ac6af81954.jpg'),(7,5,'Alen','M','kollam','9988775544','athira@gmail.com','1989-05-18','madathiveetil','static/profile71d57a3f-7659-4645-89ff-c715826864d1team-2.jpg','static/id_proof6ad55988-c1df-4ad3-881a-0e9f6c15f3d34.jpg'),(8,6,'Athira','k','kozhikode','9988776655','a@gmail.com','1989-07-13','kalarikkal','static/profilee9d00763-8f83-403a-8f89-82a4aef35218img1.jpg.jpeg','static/id_proof4f8cddad-ec6e-4e45-a493-887ab143a70bdownload (2).png'),(9,7,'Athira','k','kozhikode','9988776655','a@gmail.com','1989-07-13','kalarikkal','static/profilee1320508-e3fe-44a1-8807-b0951826a702img1.jpg.jpeg','static/id_prooffaebc5f7-1f94-454c-9cf4-5d2c11900d57download (2).png'),(10,8,'Afeefa ','K H','ernakulam','7736510228','afeefa@gmail.com','1999-05-05','kollamparambil house','static/profilea5233de2-760a-4ca4-b464-1d12ffeab0f6IMG_1437_92f93c80-586c-471d-b9b6-aff74f565dc7_600x.jpg','static/id_proofebbad42a-9d44-454b-ab14-910b97d67575download.png');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
