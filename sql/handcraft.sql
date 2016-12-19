/*
 Navicat Premium Data Transfer

 Source Server         : handcraft
 Source Server Type    : MySQL
 Source Server Version : 50616
 Source Host           : 172.21.50.32
 Source Database       : handcraft

 Target Server Type    : MySQL
 Target Server Version : 50616
 File Encoding         : utf-8

 Date: 12/19/2016 14:19:08 PM
*/

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_adapter`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_adapter`;
CREATE TABLE `hasset_adapter` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `adapter` varchar(10) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `switch` varchar(20) DEFAULT NULL,
  `port` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_asset`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_asset`;
CREATE TABLE `hasset_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` char(15) NOT NULL,
  `public_ip` char(15) DEFAULT NULL,
  `manage_ip` char(15) DEFAULT NULL,
  `idc_id` int(11) NOT NULL,
  `Manufacturer` varchar(50) DEFAULT NULL,
  `os` varchar(20) DEFAULT NULL,
  `sn` varchar(20) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `comment` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`),
  KEY `hasset_asset_7f604875` (`idc_id`),
  CONSTRAINT `idc_id_refs_id_e9dd803b` FOREIGN KEY (`idc_id`) REFERENCES `hasset_idc` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_asset_bis_group`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_asset_bis_group`;
CREATE TABLE `hasset_asset_bis_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `bisgroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_id` (`asset_id`,`bisgroup_id`),
  KEY `hasset_asset_bis_group_a64c0c36` (`asset_id`),
  KEY `hasset_asset_bis_group_fa5922c7` (`bisgroup_id`),
  CONSTRAINT `asset_id_refs_id_cab6a61e` FOREIGN KEY (`asset_id`) REFERENCES `hasset_asset` (`id`),
  CONSTRAINT `bisgroup_id_refs_id_b48dbe25` FOREIGN KEY (`bisgroup_id`) REFERENCES `hasset_bisgroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=516 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_asset_dept`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_asset_dept`;
CREATE TABLE `hasset_asset_dept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `dept_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_id` (`asset_id`,`dept_id`),
  KEY `hasset_asset_dept_a64c0c36` (`asset_id`),
  KEY `hasset_asset_dept_06f4fabe` (`dept_id`),
  CONSTRAINT `asset_id_refs_id_366bd45a` FOREIGN KEY (`asset_id`) REFERENCES `hasset_asset` (`id`),
  CONSTRAINT `dept_id_refs_id_7f631594` FOREIGN KEY (`dept_id`) REFERENCES `huser_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_assetalias`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_assetalias`;
CREATE TABLE `hasset_assetalias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `host_id` int(11) NOT NULL,
  `alias` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hasset_assetalias_6340c63c` (`user_id`),
  KEY `hasset_assetalias_27f00f5d` (`host_id`),
  CONSTRAINT `host_id_refs_id_be317c5d` FOREIGN KEY (`host_id`) REFERENCES `hasset_asset` (`id`),
  CONSTRAINT `user_id_refs_id_38349a61` FOREIGN KEY (`user_id`) REFERENCES `huser_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_bisgroup`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_bisgroup`;
CREATE TABLE `hasset_bisgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `comment` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `hasset_bisgroup_06f4fabe` (`dept_id`),
  CONSTRAINT `dept_id_refs_id_af665e18` FOREIGN KEY (`dept_id`) REFERENCES `huser_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hasset_idc`
-- ----------------------------
DROP TABLE IF EXISTS `hasset_idc`;
CREATE TABLE `hasset_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `comment` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hlog_alert`
-- ----------------------------
DROP TABLE IF EXISTS `hlog_alert`;
CREATE TABLE `hlog_alert` (
  `id` int(11) NOT NULL,
  `msg` varchar(20) NOT NULL,
  `time` datetime DEFAULT NULL,
  `is_finished` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hlog_log`
-- ----------------------------
DROP TABLE IF EXISTS `hlog_log`;
CREATE TABLE `hlog_log` (
  `id` int(11) NOT NULL,
  `user` varchar(20) DEFAULT NULL,
  `host` varchar(20) DEFAULT NULL,
  `remote_ip` varchar(100) NOT NULL,
  `dept_name` varchar(20) NOT NULL,
  `log_path` varchar(100) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `pid` int(11) NOT NULL,
  `is_finished` tinyint(1) NOT NULL,
  `log_finished` tinyint(1) NOT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hlog_web_logs`
-- ----------------------------
DROP TABLE IF EXISTS `hlog_web_logs`;
CREATE TABLE `hlog_web_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(1024) DEFAULT NULL,
  `error` varchar(1024) DEFAULT NULL,
  `times` varchar(100) DEFAULT NULL,
  `header` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14079 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_dnspod`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_dnspod`;
CREATE TABLE `hmonit_dnspod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `type` varchar(1) DEFAULT NULL,
  `rule` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_dnspod_alarm`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_dnspod_alarm`;
CREATE TABLE `hmonit_dnspod_alarm` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `resolver` varchar(100) DEFAULT NULL,
  `frequency` varchar(3) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `sip` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_ip_alarm_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_ip_alarm_status`;
CREATE TABLE `hmonit_ip_alarm_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_ip_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_ip_status`;
CREATE TABLE `hmonit_ip_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_monit`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_monit`;
CREATE TABLE `hmonit_monit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `header` varchar(50) NOT NULL,
  `url` varchar(2048) NOT NULL,
  `ip` varchar(512) NOT NULL,
  `rule` varchar(1) DEFAULT NULL,
  `json` varchar(1) DEFAULT NULL,
  `json_array` varchar(50) DEFAULT NULL,
  `json_variable` varchar(50) DEFAULT NULL,
  `parameter` varchar(256) NOT NULL,
  `level` varchar(1) DEFAULT NULL,
  `route` varchar(1) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `date_monit` datetime DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_monit_contact`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_monit_contact`;
CREATE TABLE `hmonit_monit_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monit_id` int(11) NOT NULL,
  `usergroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usergroup_id_refs_id_c315dc46` (`usergroup_id`),
  KEY `monit_id` (`monit_id`,`usergroup_id`) USING BTREE,
  CONSTRAINT `monit_id_refs_id_11b0826e` FOREIGN KEY (`monit_id`) REFERENCES `hmonit_monit` (`id`),
  CONSTRAINT `usergroup_id_refs_id_c315dc46` FOREIGN KEY (`usergroup_id`) REFERENCES `huser_usergroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=490 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_port`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_port`;
CREATE TABLE `hmonit_port` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) DEFAULT NULL,
  `port` varchar(50) DEFAULT NULL,
  `rule` varchar(1) DEFAULT NULL,
  `time` varchar(10) DEFAULT NULL,
  `date` varchar(50) DEFAULT '2016-01-01 10:00:00',
  `route` varchar(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_port_alarm_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_port_alarm_status`;
CREATE TABLE `hmonit_port_alarm_status` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) DEFAULT NULL,
  `port` varchar(6) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `frequency` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_port_contact`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_port_contact`;
CREATE TABLE `hmonit_port_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) NOT NULL,
  `usergroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usergroup_id_refs_id_c315dc46` (`usergroup_id`),
  KEY `port_id` (`port_id`,`usergroup_id`) USING BTREE,
  CONSTRAINT `hmonit_port_contact_ibfk_1` FOREIGN KEY (`port_id`) REFERENCES `hmonit_port` (`id`),
  CONSTRAINT `hmonit_port_contact_ibfk_2` FOREIGN KEY (`usergroup_id`) REFERENCES `huser_usergroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_port_ip_alarm_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_port_ip_alarm_status`;
CREATE TABLE `hmonit_port_ip_alarm_status` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `frequency` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_web_alarm_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_web_alarm_status`;
CREATE TABLE `hmonit_web_alarm_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url` varchar(2048) NOT NULL,
  `status` varchar(255) NOT NULL,
  `information` varchar(2048) NOT NULL,
  `frequency` varchar(5) DEFAULT NULL,
  `header` varchar(50) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=360 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `hmonit_web_status`
-- ----------------------------
DROP TABLE IF EXISTS `hmonit_web_status`;
CREATE TABLE `hmonit_web_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url` varchar(2048) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `level` varchar(1) NOT NULL,
  `status` varchar(5) DEFAULT NULL,
  `date` varchar(255) NOT NULL,
  `information` varchar(2048) NOT NULL,
  `name1` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=786 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `huser_dept`
-- ----------------------------
DROP TABLE IF EXISTS `huser_dept`;
CREATE TABLE `huser_dept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `comment` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `huser_dept`
-- ----------------------------
BEGIN;
INSERT INTO `huser_dept` VALUES ('1', '???', '');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
--  Table structure for `huser_user`
-- ----------------------------
DROP TABLE IF EXISTS `huser_user`;
CREATE TABLE `huser_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(75) NOT NULL,
  `phone` varchar(80) NOT NULL,
  `role` varchar(2) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `date_joined` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `huser_user_06f4fabe` (`dept_id`),
  CONSTRAINT `dept_id_refs_id_78cb0bfa` FOREIGN KEY (`dept_id`) REFERENCES `huser_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `huser_user`
-- ----------------------------
BEGIN;
INSERT INTO `huser_user` VALUES  ('1', 'admin', 'e6e061838856bf47e1de730719fb2609', 'admin', 'admin@example.com', '11111111111', 'SU', '1', '1', null, '2016-12-19 06:37:11');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
--  Table structure for `huser_user_group`
-- ----------------------------
DROP TABLE IF EXISTS `huser_user_group`;
CREATE TABLE `huser_user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `usergroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`usergroup_id`),
  KEY `huser_user_group_6340c63c` (`user_id`),
  KEY `huser_user_group_d9f50f95` (`usergroup_id`),
  CONSTRAINT `usergroup_id_refs_id_5a8d9fc9` FOREIGN KEY (`usergroup_id`) REFERENCES `huser_usergroup` (`id`),
  CONSTRAINT `user_id_refs_id_fb2280e7` FOREIGN KEY (`user_id`) REFERENCES `huser_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=528 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `huser_user_group`
-- ----------------------------
BEGIN;
INSERT INTO `huser_user_group` VALUES ('267', '1', '1') ;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
--  Table structure for `huser_usergroup`
-- ----------------------------
DROP TABLE IF EXISTS `huser_usergroup`;
CREATE TABLE `huser_usergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `comment` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `huser_usergroup_06f4fabe` (`dept_id`),
  CONSTRAINT `dept_id_refs_id_f513b280` FOREIGN KEY (`dept_id`) REFERENCES `huser_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `huser_usergroup`
-- ----------------------------
BEGIN;
INSERT INTO `huser_usergroup` VALUES ('1', 'ops', '1', '');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
