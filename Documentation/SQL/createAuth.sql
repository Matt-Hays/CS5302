GRANT all ON lahmansbaseballdb.* TO 'web'@'localhost';

CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password_hash` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `ix_user_username` (`username`)
) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4;
