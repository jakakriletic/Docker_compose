CREATE DATABASE test_baza;
USE test_baza;
CREATE TABLE company (
    company_name varchar(255) PRIMARY KEY,
    ceo varchar(255),
    founded_year int,
    industry varchar(255),
    main_activity varchar(255)
);