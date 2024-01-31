/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50744
 Source Host           : localhost:3306
 Source Schema         : tiktok

 Target Server Type    : MySQL
 Target Server Version : 50744
 File Encoding         : 65001

 Date: 31/01/2024 18:46:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for verification_code_logs
-- ----------------------------
DROP TABLE IF EXISTS `verification_code_logs`;
CREATE TABLE `verification_code_logs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `type` int(11) NULL DEFAULT NULL,
  `return_msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of verification_code_logs
-- ----------------------------
INSERT INTO `verification_code_logs` VALUES (1, 'https://p19-rc-captcha-sg.tiktokcdn.com/tos-alisg-i-749px8mig0-sg/3d_2385_3f314ac224c5fbe1e8f1763b5a30a3e6c0bf8cf6_1.jpg~tplv-749px8mig0-2.jpeg', 2301, '{\"code\": 0, \"message\": \"\", \"data\": {\"captchaId\": \"2301-7b8dc6c1-63a0-4aee-9c32-88e2a013e8c3\", \"captchaType\": \"2301\", \"recognition\": \"64,162|279,48\"}}', '2024-01-31 18:42:58');

SET FOREIGN_KEY_CHECKS = 1;
