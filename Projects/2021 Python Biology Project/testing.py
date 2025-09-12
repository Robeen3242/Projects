'''
title: Population tracker  
author: Robin Liu
date-created: 2021-12-07
'''
import sqlite3
# --- VARIABLES --- #
FILENAME = "1905-2017.csv"

CONNECTION = sqlite3.connect("MAIN.db")
CURSOR = CONNECTION.cursor()

# --- INPUTS --- #
def readfile():
    FILE = open(FILENAME)
    TEXT = FILE.readlines()
    FILE.close
    for i in range(len(TEXT)):
        if i != len(TEXT) - 1:
            TEXT[i] = TEXT[i][:-1]
            TEXT[len(TEXT) - 1] = TEXT[len(TEXT) - 1][:-1]
    return TEXT

def createPop():
    try:
        MAIN_TABLE = CURSOR.execute('''
            CREATE TABLE main (
                area TEXT NOT NULL,
                pop_year TEXT NOT NULL,
                survey_year TEXT,
                survey_month TEXT,
                survey_day TEXT,
                species TEXT,
                unkown_age_sex TEXT,
                a_male TEXT,
                a_female TEXT,
                a_unkown TEXT,
                yearling TEXT,
                calf TEXT,
                survey_total TEXT,
                correction TEXT,
                captive TEXT,
                removed TEXT,
                fall_population TEXT NOT NULL,
                comment TEXT,
                method TEXT NOT NULL
            )
        ;''')
        return MAIN_TABLE
    except sqlite3.OperationalError:
        pass

def menu():
    print('''Welcome to Elk Island National Park's online database for mammal populations!
Please choose an option:
    1. Search Population Growth
    2. Add New Year With Data
    3. Edit Year
    4. Exit
    
    ''')
    CHOICE = input("> ")
    CHOICE = turnInt(CHOICE)

    if 0 < CHOICE < 5:
        pass
    else:
        print("The number you have input is not within the range given.")
        return menu()

    return CHOICE

def getYearRange():
    START = input("Start year:")
    END = input("End year: ")

    START = testYearLength(START)
    START = testYearDate(START)

    END = testYearLength(END)
    END = testYearDate(END)
 
    YEAR_RANGE = [START, END]    
    return YEAR_RANGE

def getAnimal():
    print('''Choose an animal:
    1. Bison
    2. Elk
    3. Moose
    ''')
    SPECIES = ""
    ANIMAL = input("> ")
    ANIMAL = turnInt(ANIMAL)
    if 0 < ANIMAL < 4:
        pass
    else:
        print("The number you have submitted is not an option.")
        return getAnimal()

    if ANIMAL == 1:
        SPECIES = "Bison"
        return SPECIES
    elif ANIMAL == 2:
        SPECIES = "Elk"
        return SPECIES
    elif ANIMAL == 3: 
        SPECIES = "Moose"
        return SPECIES

def getArea():
    AREA = input("Which area was this survey conducted? > ")
    return AREA
# --- PROCESSING --- #
def processInfo(TEXT):
    del TEXT[0]
    del TEXT[-1]
    for i in range(len(TEXT)):
        TEXT[i] = TEXT[i].split(',') 
    return TEXT

def addInfo(SPLIT):
    for i in range(len(SPLIT)):
        ROW = SPLIT[i]
        while len(ROW) > 19:
            ROW[18] = ROW[18] + ROW[19]
            del ROW[19]
        CURSOR.execute('''
            INSERT INTO
                main(
                    area,
                    pop_year,
                    survey_year,
                    survey_month,
                    survey_day,
                    species,
                    unkown_age_sex,
                    a_male,
                    a_female,
                    a_unkown,
                    yearling,
                    calf,
                    survey_total,
                    correction,
                    captive,
                    removed,
                    fall_population,
                    comment,
                    method
                )
            VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
        ;''', ROW)
    CONNECTION.commit()


def filtration(YEARS, ANIMAL, AREA):
    START = YEARS[0]
    END = YEARS[1]
    INFO_START = filterYear(START, ANIMAL, AREA)
    print(INFO_START)
    

def filterYear(YEAR, ANIMAL, AREA):
    INFO = CURSOR.execute('''
        SELECT
            *
        FROM
            main
        WHERE
            area = ?
            pop_year = ?
            species = ?
    ;''',[YEAR, ANIMAL, AREA]).fetchall()
    return INFO

# --- OUTPUTS --- #
def turnInt(NUMBER):
    if NUMBER.isnumeric():
        NUMBER = int(NUMBER)
        return NUMBER
    else:
        print("You did not choose a number. Please try again.")
        NEW_NUM = input("Input a number: ")
        return turnInt(NEW_NUM)

def testYearLength(YEAR):
    if len(YEAR) != 4:
        print("One of the options above is not a year.")
        NEW_YEAR = input("Please enter an actual year: ")
        return testYearLength(NEW_YEAR)
    else:
        return YEAR

def testYearDate(YEAR):
    YEAR = turnInt(YEAR)
    if YEAR < 1904:
        print("The data on the database only goes back to 1905. Please choose a year above that:")
        NEW_YEAR = input("Please choose another year: ")
        return testYearDate(NEW_YEAR)
    else:
        YEAR = str(YEAR)
        return YEAR
        

def testing():
    INFO = CURSOR.execute('''
        SELECT
            *
        FROM
            main
    ;''').fetchone()
    print

### --- MAIN PROGRAM CODE --- ###
if __name__ == "__main__":
    MAIN = createPop()
    TEXT = readfile()
    SPLIT = processInfo(TEXT)
    addInfo(SPLIT)
    CHOICE = menu()
    while True:
        if CHOICE == 1:
            YEARS = getYearRange()
            ANIMAL = getAnimal()
            AREA = getArea()
            filtration(YEARS, ANIMAL, AREA)
        elif CHOICE == 2:
            pass
        elif CHOICE == 3:
            pass
        elif CHOICE == 4:
            pass

######RASPBERRY PI
### 1. sudo apt update
### 2. sudo apt install sqlitebrowser

######AT HOME
### 1. Google classroom link