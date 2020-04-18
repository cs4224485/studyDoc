/*
Navicat MariaDB Data Transfer

Source Server         : 192.168.0.104
Source Server Version : 50556
Source Host           : 192.168.0.104:3306
Source Database       : school

Target Server Type    : MariaDB
Target Server Version : 50556
File Encoding         : 65001

Date: 2018-04-18 10:38:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `caption` char(50) DEFAULT NULL,
  `grade_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES ('1', '一年一班', '1');
INSERT INTO `class` VALUES ('2', '二年一班', '2');
INSERT INTO `class` VALUES ('3', '三年一班', '3');
INSERT INTO `class` VALUES ('4', '一年二班', '1');
INSERT INTO `class` VALUES ('5', '一年三班', '1');
INSERT INTO `class` VALUES ('6', '一年四班', '1');
INSERT INTO `class` VALUES ('7', '二年二班', '2');
INSERT INTO `class` VALUES ('8', '二年三班', '2');
INSERT INTO `class` VALUES ('9', '三年二班', '3');
INSERT INTO `class` VALUES ('10', '五年一班', '5');
INSERT INTO `class` VALUES ('11', '五年二班', '5');
INSERT INTO `class` VALUES ('12', '五年三班', '5');
INSERT INTO `class` VALUES ('13', '五年四班', '5');
INSERT INTO `class` VALUES ('14', '一年五班', '1');
INSERT INTO `class` VALUES ('15', '一年六班', '1');

-- ----------------------------
-- Table structure for class_grade
-- ----------------------------
DROP TABLE IF EXISTS `class_grade`;
CREATE TABLE `class_grade` (
  `gid` int(11) NOT NULL AUTO_INCREMENT,
  `gname` char(30) DEFAULT NULL,
  PRIMARY KEY (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class_grade
-- ----------------------------
INSERT INTO `class_grade` VALUES ('1', '一年级');
INSERT INTO `class_grade` VALUES ('2', '二年级');
INSERT INTO `class_grade` VALUES ('3', '三年级');
INSERT INTO `class_grade` VALUES ('4', '四年级');
INSERT INTO `class_grade` VALUES ('5', '五年级');
INSERT INTO `class_grade` VALUES ('6', '六年级');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` char(30) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('1', '生物', '1');
INSERT INTO `course` VALUES ('2', '体育', '1');
INSERT INTO `course` VALUES ('3', '物理', '2');
INSERT INTO `course` VALUES ('4', '数学', '6');
INSERT INTO `course` VALUES ('5', '英语', '4');
INSERT INTO `course` VALUES ('6', '语文', '3');
INSERT INTO `course` VALUES ('7', '计算机', '2');

-- ----------------------------
-- Table structure for score
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of score
-- ----------------------------
INSERT INTO `score` VALUES ('1', '1', '1', '60');
INSERT INTO `score` VALUES ('2', '1', '2', '59');
INSERT INTO `score` VALUES ('3', '2', '2', '99');
INSERT INTO `score` VALUES ('4', '1', '3', '70');
INSERT INTO `score` VALUES ('6', '2', '3', '56');
INSERT INTO `score` VALUES ('7', '3', '1', '76');
INSERT INTO `score` VALUES ('8', '3', '2', '86');
INSERT INTO `score` VALUES ('9', '4', '1', '90');
INSERT INTO `score` VALUES ('10', '4', '2', '80');
INSERT INTO `score` VALUES ('11', '4', '3', '92');
INSERT INTO `score` VALUES ('13', '5', '1', '40');
INSERT INTO `score` VALUES ('14', '5', '2', '30');
INSERT INTO `score` VALUES ('15', '5', '3', '60');
INSERT INTO `score` VALUES ('16', '6', '1', '59');
INSERT INTO `score` VALUES ('17', '6', '2', '69');
INSERT INTO `score` VALUES ('18', '8', '1', '70');
INSERT INTO `score` VALUES ('21', '1', '4', '79');
INSERT INTO `score` VALUES ('22', '2', '4', '99');
INSERT INTO `score` VALUES ('23', '3', '4', '29');
INSERT INTO `score` VALUES ('24', '1', '5', '49');
INSERT INTO `score` VALUES ('25', '1', '6', '69');
INSERT INTO `score` VALUES ('26', '3', '6', '89');
INSERT INTO `score` VALUES ('27', '4', '5', '82');
INSERT INTO `score` VALUES ('28', '4', '6', '32');
INSERT INTO `score` VALUES ('43', '8', '2', '71');
INSERT INTO `score` VALUES ('44', '8', '6', '75');
INSERT INTO `score` VALUES ('45', '8', '5', '55');
INSERT INTO `score` VALUES ('46', '3', '3', '90');
INSERT INTO `score` VALUES ('47', '4', '3', '40');
INSERT INTO `score` VALUES ('48', '5', '3', '30');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` char(20) DEFAULT NULL,
  `gender` enum('女','男') DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1', '乔丹', '女', '1');
INSERT INTO `student` VALUES ('2', '艾弗森', '女', '1');
INSERT INTO `student` VALUES ('3', '科比', '男', '2');
INSERT INTO `student` VALUES ('4', '张三', '男', '3');
INSERT INTO `student` VALUES ('5', '李四', '女', '2');
INSERT INTO `student` VALUES ('6', '赵六', '女', '4');
INSERT INTO `student` VALUES ('7', '赵把', '女', '5');
INSERT INTO `student` VALUES ('8', '赵九', '男', '5');
INSERT INTO `student` VALUES ('9', '张三', '男', '3');
INSERT INTO `student` VALUES ('10', '张三', '男', '3');
INSERT INTO `student` VALUES ('11', '乔丹', '女', '4');

-- ----------------------------
-- Table structure for teach2cls
-- ----------------------------
DROP TABLE IF EXISTS `teach2cls`;
CREATE TABLE `teach2cls` (
  `tcid` int(11) NOT NULL AUTO_INCREMENT,
  `tid` int(11) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`tcid`),
  KEY `tid` (`tid`),
  KEY `cid` (`cid`),
  CONSTRAINT `teach2cls_ibfk_1` FOREIGN KEY (`tid`) REFERENCES `teacher` (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teach2cls
-- ----------------------------
INSERT INTO `teach2cls` VALUES ('1', '1', '1');
INSERT INTO `teach2cls` VALUES ('2', '1', '2');
INSERT INTO `teach2cls` VALUES ('3', '2', '1');
INSERT INTO `teach2cls` VALUES ('4', '3', '2');
INSERT INTO `teach2cls` VALUES ('14', '4', '3');
INSERT INTO `teach2cls` VALUES ('15', '4', '5');
INSERT INTO `teach2cls` VALUES ('16', '5', '6');
INSERT INTO `teach2cls` VALUES ('17', '6', '10');
INSERT INTO `teach2cls` VALUES ('18', '6', '14');
INSERT INTO `teach2cls` VALUES ('19', '6', '12');
INSERT INTO `teach2cls` VALUES ('20', '6', '13');

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` char(30) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('1', '张三');
INSERT INTO `teacher` VALUES ('2', '李四');
INSERT INTO `teacher` VALUES ('3', '王五');
INSERT INTO `teacher` VALUES ('4', '李源');
INSERT INTO `teacher` VALUES ('5', '李元霸');
INSERT INTO `teacher` VALUES ('6', '王宇');
INSERT INTO `teacher` VALUES ('7', 'alex');
