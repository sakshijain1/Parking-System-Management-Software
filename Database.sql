-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 29, 2020 at 10:27 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parking`
--

-- --------------------------------------------------------

--
-- Table structure for table `bulletin_board`
--

CREATE TABLE `bulletin_board` (
  `Sno` varchar(100) NOT NULL,
  `Message` varchar(100) NOT NULL,
  `Start_Time_Date` datetime NOT NULL,
  `End_Time_Sate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bulletin_board`
--

INSERT INTO `bulletin_board` (`Sno`, `Message`, `Start_Time_Date`, `End_Time_Sate`) VALUES
('U22020-08-28T17:272020-08-28T17:29', 'U2', '2020-08-28 17:27:00', '2020-08-28 17:29:00'),
('M12020-08-28T17:292020-08-28T17:37', 'M1', '2020-08-28 17:29:00', '2020-08-28 17:37:00'),
('M22020-08-28T17:292020-08-28T17:35', 'M2', '2020-08-28 17:29:00', '2020-08-28 17:35:00'),
('U12020-08-28T17:302020-08-28T17:36', 'U1', '2020-08-28 17:30:00', '2020-08-28 17:36:00'),
('U22020-08-28T17:302020-08-28T17:39', 'U2', '2020-08-28 17:30:00', '2020-08-28 17:39:00'),
('UN2020-08-30T01:192020-08-30T01:21', 'UN', '2020-08-30 01:19:00', '2020-08-30 01:21:00');

-- --------------------------------------------------------

--
-- Table structure for table `emp_details`
--

CREATE TABLE `emp_details` (
  `Emp_Id` varchar(8) NOT NULL,
  `Emp_Name` varchar(100) NOT NULL,
  `Emp_contact` bigint(10) NOT NULL,
  `Gender` char(10) NOT NULL,
  `Emp_Password` varchar(50) NOT NULL,
  `isAdmin` char(10) NOT NULL,
  `AccessCard_No` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `emp_details`
--

INSERT INTO `emp_details` (`Emp_Id`, `Emp_Name`, `Emp_contact`, `Gender`, `Emp_Password`, `isAdmin`, `AccessCard_No`) VALUES
('1111', 'Ajay', 7985641256, 'Male', 'Ajay', 'N', ''),
('1212', 'Srushti', 1452123652, 'Female', 'srushti', 'N', ''),
('1313', 'sakshi', 458965236, 'Female', 'sakshi', 'Y', ''),
('2222', 'Paras', 7985681256, 'Male', 'Paras', 'Y', '');

-- --------------------------------------------------------

--
-- Table structure for table `emp_vehical_report`
--

CREATE TABLE `emp_vehical_report` (
  `Emp_Id` varchar(50) NOT NULL,
  `Emp_Name` varchar(100) NOT NULL,
  `Veh_No` varchar(50) NOT NULL,
  `In_Timedate` datetime(6) NOT NULL,
  `Out_Timedate` datetime(6) NOT NULL,
  `Veh_Type` varchar(20) NOT NULL,
  `Updated_date` date NOT NULL,
  `Building` varchar(255) NOT NULL,
  `City` varchar(20) NOT NULL,
  `slot_no` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `emp_vehical_report`
--

INSERT INTO `emp_vehical_report` (`Emp_Id`, `Emp_Name`, `Veh_No`, `In_Timedate`, `Out_Timedate`, `Veh_Type`, `Updated_date`, `Building`, `City`, `slot_no`) VALUES
('1313', 'sakshi', '', '2020-08-30 01:40:35.609063', '2020-08-30 01:52:52.000000', 'Two Wheeler', '2020-08-30', 'Building1', 'Pune', '1'),
('1212', 'Srushti', '', '2020-08-30 01:40:56.018579', '2020-08-30 01:53:03.000000', 'Four Wheeler', '2020-08-30', 'Building2', 'Pune', '1'),
('2222', 'Paras', '', '2020-08-30 01:44:12.433994', '2020-08-30 01:52:58.000000', 'Two Wheeler', '2020-08-30', 'Building1', 'Pune', '5'),
('9999', 'Farud', '', '2020-08-30 01:29:00.000000', '2020-08-30 01:51:07.000000', 'Four Wheeler', '2020-08-30', 'Building1', 'Pune', '1');

-- --------------------------------------------------------

--
-- Table structure for table `history_vehical_details`
--

CREATE TABLE `history_vehical_details` (
  `Emp_Id` varchar(50) NOT NULL,
  `Emp_Name` varchar(100) NOT NULL,
  `Veh_No` varchar(50) NOT NULL,
  `Veh_Company_Name` varchar(100) NOT NULL,
  `Veh_Model` varchar(50) NOT NULL,
  `Veh_Type` varchar(20) NOT NULL,
  `Updated_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Updated_by` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `history_vehical_details`
--

INSERT INTO `history_vehical_details` (`Emp_Id`, `Emp_Name`, `Veh_No`, `Veh_Company_Name`, `Veh_Model`, `Veh_Type`, `Updated_date`, `Updated_by`) VALUES
('1313', 'sakshi', 'MH01DA8907', 'Hyundai', 'i20', 'Four Wheeler', '2020-08-28 11:43:08', 'sakshi'),
('1212', 'Srushti', 'MH01DP2345', 'TATA', 'TATATX', 'Four Wheeler', '2020-08-28 11:45:10', 'Srushti'),
('1212', 'Srushti', 'MH01DP2347', 'TATA', 'TATATX', 'Four Wheeler', '2020-08-28 11:51:29', 'Srushti'),
('1313', 'sakshi', 'MH01DA1111', 'Hyundai', 'i2', 'Two Wheeler', '2020-08-29 19:50:06', 'sakshi'),
('1313', 'sakshi', 'MH01DA8907', 'Hyundai', 'i10', 'Four Wheeler', '2020-08-29 19:50:57', 'sakshi');

-- --------------------------------------------------------

--
-- Table structure for table `location_details`
--

CREATE TABLE `location_details` (
  `City` varchar(20) NOT NULL,
  `Building` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `location_details`
--

INSERT INTO `location_details` (`City`, `Building`) VALUES
('Pune', 'Building1'),
('Pune', 'Building2'),
('Pune', 'Building3'),
('Hyderabad', 'Building1'),
('Hyderabad', 'Building2');

-- --------------------------------------------------------

--
-- Table structure for table `real_time`
--

CREATE TABLE `real_time` (
  `Building` varchar(20) NOT NULL,
  `City` varchar(20) NOT NULL,
  `Specially_Abled_Two_Wheeler` varchar(20) NOT NULL,
  `Specially_Abled_Four_Wheeler` varchar(20) NOT NULL,
  `Two_Wheeler` varchar(20) NOT NULL,
  `Four_Wheeler` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `real_time`
--

INSERT INTO `real_time` (`Building`, `City`, `Specially_Abled_Two_Wheeler`, `Specially_Abled_Four_Wheeler`, `Two_Wheeler`, `Four_Wheeler`) VALUES
('Building1', 'Pune', '0', '0', '3', '0'),
('Building2', 'Pune', '0', '0', '0', '4'),
('Building3', 'Pune', '2', '0', '0', '0'),
('Building1', 'Hyderabad', '0', '0', '4', '0'),
('Building2', 'Hyderabad', '0', '1', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `total_slots`
--

CREATE TABLE `total_slots` (
  `City` varchar(100) NOT NULL,
  `Building` varchar(200) NOT NULL,
  `Veh_Type` varchar(100) NOT NULL,
  `Total_Allocated` int(100) NOT NULL,
  `Total_Available` varchar(20) NOT NULL DEFAULT '0',
  `Updated_date` datetime NOT NULL,
  `Updated_by` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `total_slots`
--

INSERT INTO `total_slots` (`City`, `Building`, `Veh_Type`, `Total_Allocated`, `Total_Available`, `Updated_date`, `Updated_by`) VALUES
('Pune', 'Building1', 'Two Wheeler', 5, '3', '2020-08-30 01:21:41', 'sakshi'),
('Pune', 'Building2', 'Four Wheeler', 5, '4', '2020-08-30 01:21:53', 'sakshi'),
('Pune', 'Building3', 'Specially Abled Two Wheeler', 2, '2', '2020-08-30 01:22:09', 'sakshi'),
('Hyderabad', 'Building1', 'Two Wheeler', 5, '4', '2020-08-30 01:22:32', 'sakshi'),
('Hyderabad', 'Building2', 'Specially Abled Four Wheeler', 2, '1', '2020-08-30 01:22:43', 'sakshi');

-- --------------------------------------------------------

--
-- Table structure for table `vehical_details`
--

CREATE TABLE `vehical_details` (
  `Emp_Id` varchar(50) NOT NULL,
  `Emp_Name` varchar(100) NOT NULL,
  `Veh_No` varchar(50) NOT NULL,
  `Veh_Company_Name` varchar(100) NOT NULL,
  `Veh_Model` varchar(50) NOT NULL,
  `Veh_Type` varchar(20) NOT NULL,
  `Updated_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Updated_by` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehical_details`
--

INSERT INTO `vehical_details` (`Emp_Id`, `Emp_Name`, `Veh_No`, `Veh_Company_Name`, `Veh_Model`, `Veh_Type`, `Updated_date`, `Updated_by`) VALUES
('1313', 'sakshi', 'MH01DA1111', 'Hyundai', 'i2', 'Two Wheeler', '2020-08-29 19:50:06', 'sakshi'),
('1313', 'sakshi', 'MH01DA8907', 'Hyundai', 'i10', 'Four Wheeler', '2020-08-29 19:50:57', 'sakshi'),
('1212', 'Srushti', 'MH01DP2347', 'TATA', 'TATATX', 'Four Wheeler', '2020-08-28 11:51:29', 'Srushti');

-- --------------------------------------------------------

--
-- Table structure for table `vehical_entry`
--

CREATE TABLE `vehical_entry` (
  `City` varchar(20) NOT NULL,
  `Building` varchar(200) NOT NULL,
  `Veh_Type` varchar(50) NOT NULL,
  `slot_no` int(200) NOT NULL,
  `Veh_No` varchar(100) DEFAULT 'NULL',
  `Status` varchar(20) NOT NULL DEFAULT 'Enable',
  `Message` varchar(255) NOT NULL,
  `PSID` varchar(20) DEFAULT 'NULL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehical_entry`
--

INSERT INTO `vehical_entry` (`City`, `Building`, `Veh_Type`, `slot_no`, `Veh_No`, `Status`, `Message`, `PSID`) VALUES
('Pune', 'Building1', 'Two Wheeler', 1, 'NULL', 'Enable', '', 'NULL'),
('Pune', 'Building1', 'Two Wheeler', 2, NULL, 'Disable', 'Temporary till 1hr', 'NULL'),
('Pune', 'Building1', 'Two Wheeler', 3, NULL, 'Disable', 'Temporary till 2hr', 'NULL'),
('Pune', 'Building1', 'Two Wheeler', 4, 'NULL', 'Enable', '', 'NULL'),
('Pune', 'Building1', 'Two Wheeler', 5, 'NULL', 'Enable', '', 'NULL'),
('Pune', 'Building2', 'Four Wheeler', 1, 'NULL', 'Enable', '', 'NULL'),
('Pune', 'Building2', 'Four Wheeler', 2, NULL, 'Disable', '', 'NULL'),
('Pune', 'Building2', 'Four Wheeler', 3, NULL, 'Enable', '', 'NULL'),
('Pune', 'Building2', 'Four Wheeler', 4, NULL, 'Enable', '', 'NULL'),
('Pune', 'Building2', 'Four Wheeler', 5, NULL, 'Enable', '', 'NULL'),
('Pune', 'Building3', 'Specially Abled Two Wheeler', 1, NULL, 'Enable', '', 'NULL'),
('Pune', 'Building3', 'Specially Abled Two Wheeler', 2, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building1', 'Two Wheeler', 1, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building1', 'Two Wheeler', 2, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building1', 'Two Wheeler', 3, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building1', 'Two Wheeler', 4, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building1', 'Two Wheeler', 5, NULL, 'Disable', '', 'NULL'),
('Hyderabad', 'Building2', 'Specially Abled Four Wheeler', 1, NULL, 'Enable', '', 'NULL'),
('Hyderabad', 'Building2', 'Specially Abled Four Wheeler', 2, NULL, 'Disable', '', 'NULL');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `emp_details`
--
ALTER TABLE `emp_details`
  ADD PRIMARY KEY (`Emp_Id`);

--
-- Indexes for table `emp_vehical_report`
--
ALTER TABLE `emp_vehical_report`
  ADD KEY `Emp_Id` (`Emp_Id`),
  ADD KEY `emp_report_ibfk_1` (`Veh_No`);

--
-- Indexes for table `vehical_details`
--
ALTER TABLE `vehical_details`
  ADD PRIMARY KEY (`Veh_No`),
  ADD KEY `vehical_details_ibfk_1` (`Emp_Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
