from datetime import datetime, timedelta
from random import randint

PARENT_FOLDER = "/home/michau/Pulpit/VSC/Laby/Sem3/BD/company-db/"
COLUMN_FILE = "columns/column_"
FILE_NAME_1 = PARENT_FOLDER + COLUMN_FILE + "1.txt"
FILE_NAME_2 = PARENT_FOLDER + COLUMN_FILE + "2.txt"
FILE_NAME_3 = PARENT_FOLDER + COLUMN_FILE + "3.txt"
FILE_NAME_4 = PARENT_FOLDER + COLUMN_FILE + "4.txt"
DATABASE_FILE = PARENT_FOLDER + "database-small/companies-data.sql"


START_DATE = datetime(1, 1, 1)
END_DATE = datetime(2023, 1, 1)

SQL_START_SCRIPT = """
SET GLOBAL max_allowed_packet=1073741824;

SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';
SET @old_autocommit=@@autocommit;

USE companies;
"""

SQL_INSERT_SCRIPT = """
SET AUTOCOMMIT=0;
INSERT INTO"""

SQL_COMMIT = ";\nCOMMIT;\n"

SQL_END_SCRIPT = """
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET autocommit=@old_autocommit;
"""


pesel_set = set()

def random_date(start_date, end_date):
    total_days = (end_date - start_date).days
    random_days = randint(0, total_days)

    random_date = start_date + timedelta(days=random_days)
    return random_date


def generate_pesel(birth_date):
    new_pesel = str(birth_date)[2:10].replace("-", "") + f"{randint(0,99999):05}"
    while new_pesel in pesel_set:
        new_pesel = str(birth_date)[2:10].replace("-", "") + f"{randint(0,99999):05}"
    pesel_set.add(new_pesel)
    return new_pesel


with open(FILE_NAME_1) as first_name_file, open(FILE_NAME_2) as last_name_file, open(FILE_NAME_3) as company_name_file, open(FILE_NAME_4) as city_address_file, open(DATABASE_FILE, "w+") as save:
    first_name = first_name_file.read().upper().split('\n')[1:]
    last_name = last_name_file.read().upper().split('\n')[1:]
    company_name = company_name_file.read().upper().split('\n')[1:]
    city_address = city_address_file.read().upper().split('\n')[1:]
    
    
    company_table = list(map(list, zip(company_name, city_address, first_name, last_name)))
    conv_company_table = []
    employment_table = []
    employees_table = []
    finances_table = []
    employee_id = 0

    for ind, elem in enumerate(company_table):
        if elem[0].count(",") == 0 and len(elem[0]) <= 50:
            conv_company_table.append(elem)
    
    for ind, elem in enumerate(conv_company_table):
        ceo_birth_date = random_date(datetime(1960, 1, 1), datetime(2000, 1, 1))
        fake_ceo_pesel = generate_pesel(ceo_birth_date)
        company_creation_date = random_date(random_date(ceo_birth_date + timedelta(days=18 * 365), datetime(2020, 1, 1)), END_DATE)

        conv_company_table[ind].insert(0, ind + 1)
        conv_company_table[ind].insert(3, str(company_creation_date)[:10])
        conv_company_table[ind].append(fake_ceo_pesel)
        all_dismissed = True if randint(1,100) == 1 else False
        no_employees = 0

        for no_emp in range(randint(10,200)):
            employee_id += 1
            if no_emp == 0 and randint(1,5) == 5:
                employees_table.append((employee_id, *elem[4:6], fake_ceo_pesel))
                employment_table.append((ind + 1, employee_id, elem[1], str(company_creation_date)[:10], 'NULL', randint(627000, 1070000)))
                continue

            date_of_employment = random_date(company_creation_date, END_DATE)
            date_of_dismissal = 'NULL' if randint(1,7) <= 4 and not all_dismissed else str(random_date(date_of_employment, END_DATE))[:10]

            if date_of_dismissal == 'NULL': no_employees += 1

            employees_table.append((employee_id, first_name[randint(0,1999)],
             last_name[randint(0,1999)], generate_pesel(START_DATE + ( date_of_employment - random_date(datetime(18,1,1), datetime(70, 1, 1))))))

            employment_table.append((ind + 1, employee_id, elem[1], str(date_of_employment)[:10], date_of_dismissal, randint(6000, 75000)))
        
        for i in range(4*12):
            spendings = no_employees * randint(6000, 7500) + randint(0, 10000 + no_employees * 1000)
            finances_table.append((ind + 1, elem[1], int(2020 + i / 12), (i + 1) % 12 + 1, int(spendings * (2 - randint(0, 20) / 10)) + randint(0, 10000 + no_employees * 1000), spendings))


    final_company_table = ',\n'.join(map(str, map(tuple, conv_company_table)))
    final_employees_table = ',\n'.join(map(str, map(tuple, employees_table)))
    final_employment_table = ',\n'.join(map(str, map(tuple, employment_table)))
    final_finances_table = ',\n'.join(map(str, finances_table))

    save.write(SQL_START_SCRIPT)
    save.write(SQL_INSERT_SCRIPT + " company VALUES " + final_company_table + SQL_COMMIT)
    save.write(SQL_INSERT_SCRIPT + " employee VALUES " + final_employees_table + SQL_COMMIT)
    save.write(SQL_INSERT_SCRIPT + " employment VALUES " + final_employment_table.replace("'NULL'", "NULL") + SQL_COMMIT)
    save.write(SQL_INSERT_SCRIPT + " finances VALUES " + final_finances_table + SQL_COMMIT)
    save.write(SQL_END_SCRIPT)