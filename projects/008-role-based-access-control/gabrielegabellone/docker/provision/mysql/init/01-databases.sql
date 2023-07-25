CREATE DATABASE IF NOT EXISTS `user_management_system`;
CREATE DATABASE IF NOT EXISTS `test_user_management_system`;

CREATE USER 'root'@'%' IDENTIFIED BY 'local';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';