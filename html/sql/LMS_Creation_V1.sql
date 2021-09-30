DROP DATABASE IF EXISTS LMSDB;

CREATE DATABASE LMSDB;
USE LMSDB;

/* Table = USER */

DROP TABLE IF EXISTS `USERS`;
CREATE TABLE IF NOT EXISTS `USERS` (
  `USERID` INT NOT NULL AUTO_INCREMENT,
  `NAME` varchar(64) NOT NULL,
  `EMAIL` varchar(64) NOT NULL,
  `DEPARTMENT` varchar(64) NOT NULL,
  `DESIGNATION` varchar(64) NOT NULL, 
  PRIMARY KEY (`USERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = ADMINS */
DROP TABLE IF EXISTS `ADMINS`;
CREATE TABLE IF NOT EXISTS `ADMINS` (
  `USERID` INT NOT NULL,
  PRIMARY KEY (`USERID`),
  CONSTRAINT FK_ADMINS FOREIGN KEY (USERID) REFERENCES USERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = TRAINERS */
DROP TABLE IF EXISTS `TRAINERS`;
CREATE TABLE IF NOT EXISTS `TRAINERS` (
  `USERID` INT NOT NULL,
  PRIMARY KEY (`USERID`),
  CONSTRAINT FK_TRAINERS FOREIGN KEY (USERID) REFERENCES USERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = LEARNERS */
DROP TABLE IF EXISTS `LEARNERS`;
CREATE TABLE IF NOT EXISTS `LEARNERS` (
  `USERID` INT NOT NULL,
  PRIMARY KEY (`USERID`),
  CONSTRAINT FK_LEARNERS FOREIGN KEY (USERID) REFERENCES USERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = COURSE */
DROP TABLE IF EXISTS `COURSE`;
CREATE TABLE IF NOT EXISTS `COURSE` (
  `COURSE_ID` INT NOT NULL AUTO_INCREMENT,
  `COURSE_NAME` VARCHAR(64) NOT NULL,
  `COURSE_DESCRIPTION` VARCHAR(255),
  `STARTDATE` DATETIME NOT NULL,
  `ENDDATE` DATETIME NOT NULL,
  `STARTENROLLMENTDATE` DATETIME,
  `ENDENROLLMENTDATE` DATETIME,
  PRIMARY KEY (`COURSE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



/* Table = Course_Prerequisite */
DROP TABLE IF EXISTS `COURSE_PREREQUISITE`;
CREATE TABLE IF NOT EXISTS `COURSE_PREREQUISITE` (
  `COURSE_ID` INT NOT NULL,
  `PREREQ_COURSE_ID` INT NOT NULL,
  PRIMARY KEY (`COURSE_ID`, `PREREQ_COURSE_ID`),
  CONSTRAINT FK_PREREQ FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID),
  CONSTRAINT FK_PREREQ2 FOREIGN KEY (PREREQ_COURSE_ID) REFERENCES COURSE(COURSE_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = LEARNER_COMPLETED_COURSE */
DROP TABLE IF EXISTS `LEARNER_BADGES`;
CREATE TABLE IF NOT EXISTS `LEARNER_BADGES` (
  `USERID` INT NOT NULL,
  `COURSE_ID` INT NOT NULL,
  PRIMARY KEY (`USERID`, `COURSE_ID`),
  CONSTRAINT FK_LEARNER_BADGES FOREIGN KEY (USERID) REFERENCES USERS(USERID),
  CONSTRAINT FK_LEARNER_BADGES2 FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



/* Table = CLASSES */
DROP TABLE IF EXISTS `CLASSES`;
CREATE TABLE IF NOT EXISTS `CLASSES` (
  `COURSE_ID` INT NOT NULL,
  `CLASS_ID` INT NOT NULL AUTO_INCREMENT,
  `SLOTS` INT NOT NULL,
  PRIMARY KEY ( `CLASS_ID` ),
  CONSTRAINT FK_CLASSES FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `COURSE_ENROLLMENT`;
CREATE TABLE IF NOT EXISTS `COURSE_ENROLLMENT` (
  `ENROLLMENT_ID` INT NOT NULL AUTO_INCREMENT,
  `COURSE_ID` INT NOT NULL,
  `USERID` INT NOT NULL,
  `CLASS_ID` INT NOT NULL,
  `IS_ENROLLED` BOOLEAN,
  PRIMARY KEY (`ENROLLMENT_ID`),
  CONSTRAINT FK_COURSE_ENROLLMENT FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID),
  CONSTRAINT FK_COURSE_ENROLLMENT2 FOREIGN KEY (USERID) REFERENCES LEARNERS(USERID),
  CONSTRAINT FK_COURSE_ENROLLMENT3 FOREIGN KEY (CLASS_ID) REFERENCES CLASSES(CLASS_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = SECTIONS */
DROP TABLE IF EXISTS `SECTIONS`;
CREATE TABLE IF NOT EXISTS `SECTIONS` (
  `SECTION_ID` INT NOT NULL AUTO_INCREMENT,
  `CLASS_ID` INT NOT NULL,
  `SECTION_TITLE` VARCHAR(255),
  PRIMARY KEY ( `SECTION_ID` ),
  CONSTRAINT FK_SECTIONS FOREIGN KEY (CLASS_ID) REFERENCES CLASSES(CLASS_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = VIEWABLE_SECTION */
DROP TABLE IF EXISTS `VIEWABLE_SECTION`;
CREATE TABLE IF NOT EXISTS `VIEWABLE_SECTION` (
  `SECTION_ID` INT NOT NULL,
  `USERID` INT NOT NULL,
  `CLASS_ID` INT NOT NULL,
  `VIEWABLE` BOOLEAN,
  PRIMARY KEY ( `SECTION_ID`, `CLASS_ID`, `USERID` ),
  CONSTRAINT FK_VIEWABLE_SECTIONS FOREIGN KEY (CLASS_ID) REFERENCES CLASSES(CLASS_ID),
  CONSTRAINT FK_VIEWABLE_SECTIONS2 FOREIGN KEY (SECTION_ID) REFERENCES SECTIONS(SECTION_ID),
  CONSTRAINT FK_VIEWABLE_SECTIONS3 FOREIGN KEY (USERID) REFERENCES LEARNERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = SECTION_MATERIALS */
DROP TABLE IF EXISTS `SECTION_MATERIALS`;
CREATE TABLE IF NOT EXISTS `SECTIONS_MATERIALS` (
  `SECTION_ID` INT NOT NULL,
  `MATERIAL_ID` INT NOT NULL AUTO_INCREMENT,
  `MATERIAL_TITLE` TEXT,
  `MATERIAL_CONTENT` TEXT,
  PRIMARY KEY ( `MATERIAL_ID` ),
  CONSTRAINT FK_SECTIONS_MATERIALS FOREIGN KEY (SECTION_ID) REFERENCES SECTIONS(SECTION_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



/* Table = QUIZZES */
DROP TABLE IF EXISTS `QUIZZES`;
CREATE TABLE IF NOT EXISTS `QUIZZES` (
  `QUIZ_ID` INT NOT NULL AUTO_INCREMENT,
  `SECTION_ID` INT NOT NULL,
  `TIME_LIMIT` INT NOT NULL,
  PRIMARY KEY ( `QUIZ_ID`, `SECTION_ID` ),
  CONSTRAINT FK_QUIZZES FOREIGN KEY (SECTION_ID) REFERENCES SECTIONS(SECTION_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = QUIZ_QUESTION */
DROP TABLE IF EXISTS `QUIZ_QUESTION`;
CREATE TABLE IF NOT EXISTS `QUIZ_QUESTION` (
  `QUESTION_ID` INT NOT NULL AUTO_INCREMENT,
  `QUIZ_ID` INT NOT NULL,
  `QORDER` INT NOT NULL,
  `QUESTION_TYPE` VARCHAR(64) NOT NULL,
  `QUESTION` TEXT ,
  PRIMARY KEY (`QUESTION_ID`),
  CONSTRAINT FK_QUIZ_QUESTION FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = MCQ_OPTIONS */
DROP TABLE IF EXISTS `MCQ_OPTIONS`;
CREATE TABLE IF NOT EXISTS `MCQ_OPTIONS` (
  `QUESTION_ID` INT NOT NULL,
  `OPTION_ORDER` INT NOT NULL,
  `OPTION_CONTENT` TEXT NOT NULL,
  `CORRECT_OPTION` BOOLEAN NOT NULL,
  PRIMARY KEY ( `QUESTION_ID`, `OPTION_ORDER` ),
  CONSTRAINT FK_MCQ_OPTIONS FOREIGN KEY (QUESTION_ID) REFERENCES QUIZ_QUESTION(QUESTION_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = TrueFalseQ */
DROP TABLE IF EXISTS `TRUEFALSEQ`;
CREATE TABLE IF NOT EXISTS `TRUEFALSEQ` (
  `QUESTION_ID` INT NOT NULL,
  `ANSWER` BOOLEAN NOT NULL,
  PRIMARY KEY ( `QUESTION_ID`),
  CONSTRAINT FK_TrueFalseQ FOREIGN KEY (QUESTION_ID) REFERENCES QUIZ_QUESTION(QUESTION_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = FINAL_QUIZ */
DROP TABLE IF EXISTS `FINAL_QUIZ`;
CREATE TABLE IF NOT EXISTS `FINAL_QUIZ` (
  `QUIZ_ID` INT NOT NULL,
  `PASSING_SCORE` INT NOT NULL,
  PRIMARY KEY (`QUIZ_ID`),
  CONSTRAINT FK_FINALQ FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table = QUIZ_SCORE */
DROP TABLE IF EXISTS `QUIZ_SCORE`;
CREATE TABLE IF NOT EXISTS `QUIZ_SCORE` (
  `QUIZ_ID` INT NOT NULL,
  `USERID` INT NOT NULL,
  `QUIZ_SCORE` INT,
  PRIMARY KEY (`QUIZ_ID`, `USERID` ),
  CONSTRAINT FK_QUIZ_SCORE FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID),
  CONSTRAINT FK_QUIZ_SCORE2 FOREIGN KEY (USERID) REFERENCES USERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* Table = TRAINERASSIGNMENT */
DROP TABLE IF EXISTS `TRAINERASSIGNMENT`;
CREATE TABLE IF NOT EXISTS `TRAINERASSIGNMENT` (
  `COURSE_ID` INT NOT NULL,
  `CLASS_ID` INT NOT NULL,
  `USERID` INT NOT NULL,
  PRIMARY KEY (`COURSE_ID`,`USERID`,`CLASS_ID`),
  CONSTRAINT FK_TRAINASSIGNMENT FOREIGN KEY (CLASS_ID) REFERENCES CLASSES(CLASS_ID),
  CONSTRAINT FK_TRAINASSIGNMENT2 FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID),
  CONSTRAINT FK_TRAINASSIGNMENT3 FOREIGN KEY (USERID) REFERENCES TRAINERS(USERID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



/* INSERT COMMANDS */


INSERT INTO `USERS` (`NAME`,`EMAIL`,`DEPARTMENT`,`DESIGNATION`) VALUES
('Xing Jie', 'xjwang.2019@smu.edu.sg','SCIS','Human Resource'),
('Guang Qi', 'guangqi.2019@smu.edu.sg','SCIS','Learner'),
('Tze Kiat', 'tzekiat.2019@smu.edu.sg','SOA', 'Trainer'),
('Jia Fang', 'jiafang.2019@smu.edu.sg','SOL','Learner'),
('Wei Quan', 'weiquan.2019@smu.edu.sg','SOE','Trainer');


INSERT INTO `ADMINS` (`USERID`) VALUES
('1');

INSERT INTO `TRAINERS` (`USERID`) VALUES
('3'),
('5');

INSERT INTO `LEARNERS` (`USERID`) VALUES
('2'),
('4');

INSERT INTO `COURSE` (`COURSE_NAME`, `COURSE_DESCRIPTION`,`STARTDATE`,`ENDDATE`,`STARTENROLLMENTDATE`,`ENDENROLLMENTDATE`) VALUES
('Dog walking course','A course to learn how to walk clients dog','2021-10-1','2021-11-28','2021-10-1','2021-10-8'),
('Strong breathing course','A course to learn how to breathe','2021-10-6','2021-12-1','2021-10-2','2021-10-9');
;

INSERT INTO `COURSE_PREREQUISITE` (`COURSE_ID`,`PREREQ_COURSE_ID`) VALUES
('2','1')
;

INSERT INTO `LEARNER_BADGES` (`USERID`,`COURSE_ID`) VALUES
('2','1'),
('4','2')
;

INSERT INTO `CLASSES` (`COURSE_ID`,`SLOTS`) VALUES
('1','40'),
('2','50')
;

INSERT INTO `SECTIONS` (`CLASS_ID`, `SECTION_TITLE`) VALUES
('1','Introduction to walking'),
('1', 'What is a dog?'),
('1', 'Dog instinct'),
('1', 'How to calm a dog'),
('2', 'Introduction to breathing'),
('2', 'What is air?'),
('1', 'What dogs like when walking'),
('2', 'Composition of air')
;

INSERT INTO `VIEWABLE_SECTION` ( `SECTION_ID`,`USERID`,`CLASS_ID`, `VIEWABLE`) VALUES
('1','2','1',TRUE),
('2','2','1',TRUE),
('3','2','1',TRUE),
('4','2','1',FALSE),
('5','2','1',FALSE)
;

INSERT INTO `SECTIONS_MATERIALS` (`SECTION_ID`, `MATERIAL_TITLE`, `MATERIAL_CONTENT`) VALUES
('1','The title is king','In the morning, I drink coffee & stare at the morning sun while thinking of the one. Every star we see is actually dead, we are just view the light that took lights years to arrive.'),
('2','Iphone', 'The iphone 13 is a new phone that at first glance look like the same as iphone 12 but the major upgrades are in the interior of the phone.')
;

INSERT INTO `QUIZZES` ( `SECTION_ID`,`TIME_LIMIT`) VALUES
('1','8'),
('2','6'),
('3','10'),
('4','12'),
('5','15'),
('6','20'),
('7','10')
;

INSERT INTO `QUIZ_QUESTION` (`QUIZ_ID`,`QORDER`,`QUESTION_TYPE`,`QUESTION`) VALUES
('1','1','MCQ','How many chinese is needed to solve a math question?'),
('1','2','MCQ','What is the Z69 printer used for?'),
('1','3','TF','Black ink is best for printing pictures.'), 
('1','4','TF','If a printer is broken, call help center first.'),
('1','5','MCQ','How many engineers can be working on a printer at a time?')
;

INSERT INTO `MCQ_OPTIONS` ( `QUESTION_ID`,`OPTION_ORDER`,`OPTION_CONTENT`, `CORRECT_OPTION`) VALUES
('1','1','The first option is wrong', FALSE),
('1','2','Sandwich is good', FALSE),
('1','3','Match can create fire', FALSE),
('1','4','Broken cup can hold no water', TRUE)
;

INSERT INTO `TRUEFALSEQ` ( `QUESTION_ID`,`ANSWER`) VALUES
('3', TRUE),
('4', FALSE)
;

INSERT INTO `FINAL_QUIZ` ( `QUIZ_ID`,`PASSING_SCORE`) VALUES
('1',50),
('2',60)
;

INSERT INTO `QUIZ_SCORE` ( `QUIZ_ID`,`USERID`, `QUIZ_SCORE`) VALUES
('1','2', 55),
('1','4', 70)
;

INSERT INTO `TRAINERASSIGNMENT` ( `COURSE_ID`,`CLASS_ID`, `USERID`) VALUES
('1','1','3'),
('2','1','5')
;

COMMIT;


