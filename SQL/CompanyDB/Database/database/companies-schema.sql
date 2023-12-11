SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';



DROP SCHEMA IF EXISTS companies;
CREATE SCHEMA companies;
USE companies;



CREATE TABLE company (
    company_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    company_name VARCHAR(50) NOT NULL,
    company_city VARCHAR(50) NOT NULL,
    creation_date DATE NOT NULL,
    ceo_first_name VARCHAR(30) NOT NULL,
    ceo_last_name VARCHAR(30) NOT NULL,
    pesel CHAR(11),
    PRIMARY KEY (company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE employee (
    employee_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    pesel CHAR(11),
    PRIMARY KEY (employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE employment (
    company_id SMALLINT UNSIGNED NOT NULL,
    employee_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    company_name VARCHAR(50) NOT NULL,
    employment_date DATE NOT NULL,
    dismission_date DATE,
    salary INT NOT NULL,
    PRIMARY KEY (employee_id, company_id),
    KEY idx_fk_company_id (`company_id`),
    CONSTRAINT fk_employment_company FOREIGN KEY (company_id) REFERENCES company (company_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_employment_employee FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE finances (
    company_id SMALLINT UNSIGNED NOT NULL,
    company_name VARCHAR(50) NOT NULL,
    year SMALLINT NOT NULL,
    month TINYINT NOT NULL,
    income INT NOT NULL,
    outcome INT NOT NULL,
    KEY (company_id),
    KEY idx_fk_company_id (`company_id`),
    CONSTRAINT fk_finances_company FOREIGN KEY (company_id) REFERENCES company (company_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;