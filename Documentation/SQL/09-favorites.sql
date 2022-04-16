CREATE
OR REPLACE TABLE `favorites` (
    `userID` int(11) NOT NULL,
    `playerID` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`userID`, `playerID`),
    CONSTRAINT `fk_user` FOREIGN KEY (`userID`) REFERENCES `users` (`id`),
    CONSTRAINT `fk_player` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
