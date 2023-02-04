-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 16, 2021 at 08:52 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `users`
--

-- --------------------------------------------------------

--
-- Table structure for table `adregister`
--

CREATE TABLE `adregister` (
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `emailaddress` varchar(150) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phoneno` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adregister`
--

INSERT INTO `adregister` (`firstname`, `lastname`, `emailaddress`, `password`, `phoneno`) VALUES
('HARRISH', 'PT', 'harrisharri2001@gmail.com', 'harrish', '8838767837'),
('ratna', 'vel', 'rat@gmail.com', 'rat', '9999998768');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `emailaddress` varchar(100) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phoneno` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`emailaddress`, `firstname`, `lastname`, `password`, `phoneno`) VALUES
('chandru1@gmail.com', 'rat', 'navel', 'chand', '8838767837'),
('chandru@gmail.com', 'rat', 'navel', 'chandru1', '8838767837'),
('harrish@gmail.com', 'HARRISH', 'PT', 'harrish', '8838767837'),
('harrisharri2001@gmail.com', 'HARRISH', 'PT', 'harrish', '9047744459'),
('harrisharri@gmail.com', 'HARRISH', 'PT', 'harrish', '8838767837'),
('jeya@gmail.com', 'jeyavel', 'sjr', 'jeyavel', '9087654321'),
('jeyavel@gmail.com', 'sjr', 'jeya', 'j', '9087654321'),
('nag@gmail.com', 'Nagarajan', 'S', 'naga', '9876543201'),
('rat@gmail.com', 'rat', 'rathan', 'rat', '9999987680');

-- --------------------------------------------------------

--
-- Table structure for table `responses`
--

CREATE TABLE `responses` (
  `id` int(100) NOT NULL,
  `emailaddress` varchar(100) NOT NULL,
  `results` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `answers` varchar(100) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `responses`
--

INSERT INTO `responses` (`id`, `emailaddress`, `results`, `subject`, `answers`, `time`) VALUES
(1, 'harrisharri2001@gmail.com', '1', 'php', 'a,a,c,d,0,0,0,0,0,', '2021-04-27 12:16:13'),
(2, 'harrisharri2001@gmail.com', '5', 'php', 'a,c,d,e,0,0,0,0,0,', '2021-04-27 12:15:58'),
(3, 'harrisharri2001@gmail.com', '3', 'php', 'a,d,c,0,0,0,0,0,0,', '2021-04-29 05:23:24'),
(4, 'rat@gmail.com', '2', 'php', 'a,b,0,0,0,0,0,0,0,', '2021-04-29 05:25:22'),
(5, 'jeyavel@gmail.com', '', 'php', 'a,a,d,b,0,0,0,0,0,', '2021-06-16 18:51:01');

-- --------------------------------------------------------

--
-- Table structure for table `upload`
--

CREATE TABLE `upload` (
  `audio` varchar(250) NOT NULL,
  `question_no` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `test_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `upload`
--

INSERT INTO `upload` (`audio`, `question_no`, `subject`, `test_name`) VALUES
('1.mp3', '1', 'php', 'test1'),
('2.mp3', '2', 'php', 'test1'),
('3.mp3', '3', 'php', 'test'),
('4.mp3', '4', 'php', 'test'),
('1.mp3', '1', 'python', 'test'),
('2.mp3', '2', 'python', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `upload1`
--

CREATE TABLE `upload1` (
  `audio` varchar(1000) NOT NULL,
  `question_no` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `lesson_name` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `upload1`
--

INSERT INTO `upload1` (`audio`, `question_no`, `subject`, `lesson_name`) VALUES
('lesson1.mp3', '1', 'php', 'lesson 1'),
('lesson2.mp3', '2', 'php', 'lesson 2'),
('lesson3.mp3', '3', 'php', 'lesson 3'),
('lesson4.mp3', '4', 'php', 'lesson 4'),
('lesson1.mp3', '1', 'python', 'lesson 1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adregister`
--
ALTER TABLE `adregister`
  ADD PRIMARY KEY (`emailaddress`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`emailaddress`);

--
-- Indexes for table `responses`
--
ALTER TABLE `responses`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `responses`
--
ALTER TABLE `responses`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
