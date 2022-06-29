create TABLE IF NOT EXISTS `user`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL ,
    `password` VARCHAR(20) NOT NULL ,
    PRIMARY KEY (`id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `upperCategory`(
    `id` INT UNSIGNED,
    `upper_cat` VARCHAR(20) NOT NULL ,
    primary key (`id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create  TABLE IF NOT EXISTS `subCategory`(
    `id` INT UNSIGNED,
    `sub_cat` VARCHAR(20) NOT NULL ,
    `upper_cat_id` INT UNSIGNED NOT NULL ,
    primary key (`id`),
    foreign key (`upper_cat_id`) references upperCategory(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `concept`(
    `id` INT UNSIGNED,
    `concept` VARCHAR(20) NOT NULL ,
    `importance` FLOAT NOT NULL ,
    `sub_cat_id` INT UNSIGNED NOT NULL ,
    `upper_cat_id` INT UNSIGNED NOT NULL ,
    primary key (`id`),
    foreign key (`upper_cat_id`) references upperCategory(id),
    foreign key (`sub_cat_id`) references subCategory(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `relation`(
    `id` INT UNSIGNED,
    `relation` VARCHAR(20) NOT NULL ,
    primary key (`id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `tail`(
    `id` INT UNSIGNED,
    `tail` VARCHAR(20) NOT NULL ,
    primary key (`id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `bigram`(
    `id` INT UNSIGNED,
    `concept_id` INT UNSIGNED NOT NULL ,
    `relation_id` INT UNSIGNED NOT NULL ,
    primary key (`id`),
    foreign key (`concept_id`) references concept(id),
    foreign key (`relation_id`) references relation(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `triple`(
    `id` INT UNSIGNED,
    `bigram_id` INT UNSIGNED NOT NULL ,
    `tail_id` INT UNSIGNED NOT NULL ,
    primary key (`id`),
    foreign key (`bigram_id`) references bigram(id),
    foreign key (`tail_id`) references  tail(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;
# !!!!!!
# create  TABLE IF NOT EXISTS `conceptTestLog`(
#     `id` INT UNSIGNED AUTO_INCREMENT,
#     `state` BOOLEAN NOT NULL ,
#     `time` INT UNSIGNED NOT NULL COMMENT '按秒计算',
#     primary key (`id`)
# )ENGINE = InnoDB DEFAULT CHARSET = utf8;
#
# create TABLE IF NOT EXISTS `conceptLearnLog`(
#     `id` INT UNSIGNED AUTO_INCREMENT,
#     `state` BOOLEAN NOT NULL ,
#     primary key (`id`)
# )ENGINE = InnoDB DEFAULT CHARSET = utf8;

# create  TABLE IF NOT EXISTS `userConcept`(
#     `id` INT UNSIGNED AUTO_INCREMENT,
#     `user_id` INT UNSIGNED NOT NULL ,
#     `concept_id` INT UNSIGNED NOT NULL ,
#     `test_log_id` INT UNSIGNED,
#     `learn_log_id` INT UNSIGNED,
#     primary key (`id`),
#     foreign key (`user_id`) references user(id),
#     foreign key (`concept_id`) references concept(id),
#     foreign key (`test_log_id`) references  conceptTestLog(id),
#     foreign key (`learn_log_id`) references conceptLearnLog(id)
# )ENGINE = InnoDB DEFAULT CHARSET = utf8;
create  TABLE IF NOT EXISTS `userConceptLearn`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL ,
    `concept_id` INT UNSIGNED NOT NULL ,
    `state` INT UNSIGNED NOT NULL,
    `createDate` DATE COMMENT '创建日期',
    `time` INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '按秒计算',
    primary key (`id`),
    foreign key (`user_id`) references user(id),
    foreign key (`concept_id`) references concept(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create  TABLE IF NOT EXISTS `userConceptTest`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL ,
    `concept_id` INT UNSIGNED NOT NULL ,
    `state` INT UNSIGNED NOT NULL ,
    `createDate` DATE COMMENT '创建日期',
    `time` INT UNSIGNED NOT NULL COMMENT '按秒计算',
    primary key (`id`),
    foreign key (`user_id`) references user(id),
    foreign key (`concept_id`) references concept(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

# create TABLE IF NOT EXISTS  `bigram_learn_log`(
#     `id` INT UNSIGNED AUTO_INCREMENT,
#     `state` BOOLEAN NOT NULL ,
#     `answer` VARCHAR(20),
#     primary key (`id`)
# )ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `userBigram`(
    `id` INT UNSIGNED AUTO_INCREMENT ,
    `user_id` INT UNSIGNED NOT NULL ,
    `bigram_id` INT UNSIGNED NOT NULL ,
    `state` BOOLEAN NOT NULL ,
    `answer` VARCHAR(20) ,
    `createDate` DATE COMMENT '创建日期',
    primary key (`id`),
    foreign key (`user_id`) references user(id),
    foreign key (`bigram_id`) references bigram(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `conceptSimilarity`(
    `id` INT UNSIGNED,
    `concept_1_id` INT UNSIGNED NOT NULL ,
    `concept_2_id` INT UNSIGNED NOT NULL ,
    `similarity` FLOAT NOT NULL ,
    primary key (id),
    foreign key (concept_1_id)references concept(id),
    foreign key (concept_2_id)references concept(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `trainPlan`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL ,
    `path_id` INT UNSIGNED NOT NULL ,
    primary key (id),
    foreign key (user_id)references user(id),
    foreign key (path_id)references conceptSimilarity(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

create TABLE IF NOT EXISTS `trainPlanNode`(
    `id` INT UNSIGNED AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL ,
    `concept_id` INT UNSIGNED NOT NULL ,
    primary key (id),
    foreign key (user_id)references user(id),
    foreign key (concept_id)references concept(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

# DROP TABLE concept;
# DROP TABLE conceptSimilarity;

# load data infile '/Users/anthony/Documents/Study/FinalProject/datasetCSV/upperCat.csv'
#     into table upperCategory;
#
# SHOW VARIABLES LIKE "secure_file_priv";
# show global variables like '%secure%';
#
# SET GLOBAL local_infile=1;
#
# show variables like 'local_infile';
# set global  local_infile=on;
#
# SELECT * from upperCategory;
# drop TABLE userBigram;
# drop TABLE bigram_learn_log;
# drop TABLE userConcept;
# drop TABLE conceptLearnLog;
# drop TABLE conceptTestLog;
# drop table trainPlan;
# drop table trainPlanNode;
# drop TABLE userBigram;
# drop TABLE userConceptLearn;
# drop TABLE userConceptTest;
# drop table user;
