/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - onlinelibrary
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`onlinelibrary` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `onlinelibrary`;

/*Table structure for table `newbook` */

DROP TABLE IF EXISTS `newbook`;

CREATE TABLE `newbook` (
  `Id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `bname` varchar(200) DEFAULT NULL,
  `bid` varchar(200) DEFAULT 'BID0',
  `course` varchar(200) DEFAULT NULL,
  `year` varchar(200) DEFAULT NULL,
  `ref` varchar(200) DEFAULT NULL,
  `f1` tinytext,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `newbook` */

insert  into `newbook`(`Id`,`bname`,`bid`,`course`,`year`,`ref`,`f1`) values (1,'Java','BID1','MTECH','1st Year','W3schools','static/uploads/CE881_Assignment1.pdf');

/*Table structure for table `register` */

DROP TABLE IF EXISTS `register`;

CREATE TABLE `register` (
  `Id` int(20) unsigned NOT NULL,
  `Name` varchar(200) DEFAULT NULL,
  `Course` varchar(200) DEFAULT NULL,
  `Year` varchar(200) DEFAULT NULL,
  `Rollno` varchar(200) DEFAULT NULL,
  `Email` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `register` */

insert  into `register`(`Id`,`Name`,`Course`,`Year`,`Rollno`,`Email`,`password`) values (0,'Lakshmi','BTECH','4th Year','16HP1A0506','cse.takeoff@gmail.com','Lakshmi@1234');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
