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
    """Reads the csv file.

    Returns:
        list: Data in the file.
    """
    FILE = open(FILENAME)
    TEXT = FILE.readlines()
    FILE.close
    for i in range(len(TEXT)): ##The for loop here puts the data into a 2d array in which the list within the list is a row.
        if i != len(TEXT) - 1:
            TEXT[i] = TEXT[i][:-1]
            TEXT[len(TEXT) - 1] = TEXT[len(TEXT) - 1][:-1]
    return TEXT

def createPop():
    """Creates the table.
    """
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
    """This is the user interface.
    """

    print('''Welcome to Elk Island National Park's online database for mammal populations!
Please choose an option:
    1. Search Population Growth
    2. Add New Year With Data
    3. Delete Year
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

def getYear(CHOICE):
    """Returns year for specific choice.

    Args:
        CHOICE (int): 

    Returns:
        list or string: The year(s)
    """
    if CHOICE == 1:
        START = input("Start year:")
        END = input("End year: ")

        START = testYearLength(START)
        START = testYearDate(START)

        END = testYearLength(END)
        END = testYearDate(END)
    
        YEAR_RANGE = [START, END]
        if int(YEAR_RANGE[0]) > int(YEAR_RANGE[1]):
            print("The start year cannot be after than the end year.")    
            return getYear(CHOICE)
        else:
            pass
        return YEAR_RANGE
    else:
        YEAR = input("Input year:")
        YEAR = testYearLength(YEAR)
        YEAR = testYearDate(YEAR)
        return YEAR

def getAnimal(CHOICE):
    """Chooses animal for specific function.

    Args:
        CHOICE (int): 

    Returns:
        string: 
    """
    if CHOICE == 1:
        print('''Choose an animal:
        1. Bison
        2. Elk
        3. Moose
        4. Deer
        5. All
        ''')
        SPECIES = ""
        ANIMAL = input("> ")
        ANIMAL = turnInt(ANIMAL)
        if 0 < ANIMAL < 6:
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
        elif ANIMAL == 4:
            SPECIES = "Deer"
            return SPECIES
        elif ANIMAL == 5:
            SPECIES = "All"
            return SPECIES
    else:
        print('''Choose an animal:
        1. Bison
        2. Elk
        3. Moose
        4. Deer
        ''')
        SPECIES = ""
        ANIMAL = input("> ")
        ANIMAL = turnInt(ANIMAL)
        if 0 < ANIMAL < 5:
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
        elif ANIMAL == 4:
            SPECIES = "Deer"
            return SPECIES
        

def getInfo():
    """User inputs information to add.

    Returns:
        list: 
    """
    print("Input the coressponding data into the forms below.")
    AREA = input("Area (required) (Sample: North): ")
    if not (AREA == "North" or AREA == "South"):
        print("That is not a listed area.")
        return getInfo()
    else:
        pass

    POP_YEAR = input("Population year (required): ")
    POP_YEAR = testYearLength(POP_YEAR)
    POP_YEAR = testYearDate(POP_YEAR)

    SURVEY_YEAR = input("Survey year: ")
    SURVEY_MONTH = input("Survey month: ")
    SURVEY_DAY = input("Survey day: ")

    SPECIES = input("Species (Bison, Elk, OR Deer) (required): ")
    SPECIES = checkInputSpecies(SPECIES)

    UNKOWN_AGE = input("Number of unkown age and sex: ")
    A_MALE = input("Number of adult males: ")
    A_FEMALE = input("Number of adult females: ")
    A_UNKOWN = input("Number of unkown adults: ")
    YEARLING = input("Yearling count: ")
    CALF = input("Calf count: ")
    SURVEY_TOT = input("Survey total: ")
    CORRECTION = input("Correction error: ")
    CAPTIVE = input("Captive animals: ")
    REMOVED = input("Removed animals: ")

    FALL_POP = input("Fall population (required): ")
    FALL_POP = turnInt(FALL_POP)
    FALL_POP = str(FALL_POP)

    COMMENT = input("Comment: ")
    METHOD = input("Method (required): ")

    USER_INPUT = [AREA, POP_YEAR, SURVEY_YEAR, SURVEY_MONTH, SURVEY_DAY, SPECIES, UNKOWN_AGE, A_MALE, A_FEMALE, A_UNKOWN, YEARLING, CALF, SURVEY_TOT, CORRECTION, CAPTIVE, REMOVED, FALL_POP, COMMENT, METHOD]
    
    return USER_INPUT
    
def saveFile(USER_INPUT):
    """Saves the added data to the file.
    """
    USER_INPUT = ",".join(USER_INPUT)
    FILE = open(FILENAME, 'x')
    FILE.write(USER_INPUT)
    FILE.close()
    print("Data saved.")
    return menu()

def again():
    """Asks user if they want to exit the program.
    """
    CHOICE = input("Are you sure you want to exit? (Y/n) > ")

    if CHOICE == "yes" or CHOICE == "Yes" or CHOICE == "" or CHOICE == "y" or CHOICE == "Y" or CHOICE == "YES":
        print("Thank you for using the program.")
        exit
    elif CHOICE == "no" or CHOICE == "No" or CHOICE == "n" or CHOICE == "N" or CHOICE == "NO":
        return menu()
    else:
        print("Please enter YES or NO.")

def getArea():
    """User chooses an area as a filter method.

    Returns:
        string: 
    """
    AREA = input(f"What is the area of the data set? (North or South) > ")
    if not (AREA == "North" or AREA == "South"):
        print("That is not a listed area.")
        return getArea()
    else:
        return AREA

# --- PROCESSING --- #

def checkBlank(DATA):
    """If necessary data is blank this subroutine will force the user to input necessary conditions.

    Args:
        DATA (string): Data input

    Returns:
        DATA: 
    """
    if DATA == "":
        print("The above feild is required.")
        NEW_DATA = input("Try again > ")
        return checkBlank(NEW_DATA)
    else:
        return DATA

def processInfo(TEXT):
    """Removes unecessary information.

    Args:
        TEXT (LIST): Row info

    Returns:
        list: 
    """
    del TEXT[0]
    del TEXT[-1]
    for i in range(len(TEXT)):
        TEXT[i] = TEXT[i].split(',') 
    return TEXT

def addInfo(SPLIT):
    """Adds info to the database

    Args:
        SPLIT (data that has been processed): 
    """
    for i in range(len(SPLIT)): ##This specific line will join the survey method if there are multiple because this line can appear as "Method1, Method2"
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

def checkInputSpecies(SPECIES): 
    """Checks if the species is one in the database

    Args:
        SPECIES (string): 

    Returns:
        [string]: 
    """
    if not (SPECIES == "Elk" or SPECIES == "Deer" or  SPECIES == "Bison" or SPECIES == "Moose"):
        print("You have not put in the correct species.")
        NEW_INPUT = input("> ")
        return checkInputSpecies(NEW_INPUT)
    else:
        return SPECIES


# --- OUTPUTS --- #
def turnInt(NUMBER):
    """Checks and turns number into integer.

    Args:
        NUMBER (string): 

    Returns:
        int: 
    """
    if NUMBER.isnumeric():
        NUMBER = int(NUMBER)
        return NUMBER
    else:
        print("You did not choose a number. Please try again.")
        NEW_NUM = input("Input a number: ")
        return turnInt(NEW_NUM)

def testYearLength(YEAR):
    """Checks if the years length is 4 characters long.

    Args:
        YEAR (string): 

    Returns:
        string: 
    """
    if len(YEAR) != 4:
        print("One of the options above is not a year.")
        NEW_YEAR = input("Please enter an actual year: ")
        return testYearLength(NEW_YEAR)
    else:
        return YEAR

def testYearDate(YEAR):
    """Makes sure that year cannot be bellow when the database has started.

    Args:
        YEAR (string): 

    Returns:
        string: New year.
    """
    YEAR = turnInt(YEAR)
    if YEAR < 1904:
        print("The data on the database only goes back to 1905. Please choose a year above that:")
        NEW_YEAR = input("Please choose another year: ")
        return testYearDate(NEW_YEAR)
    else:
        YEAR = str(YEAR)
        return YEAR

def insertUserInput(INPUTS):
    """Saves data to database

    Args:
        INPUTS (list): User inputed data
    """
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
        ;''', INPUTS)
    CONNECTION.commit()
    print("Your data has been added successfully!")

def filtrationSingle(YEARS, ANIMAL):
    """Filters single animal

    Args:
        YEARS (string): 
        ANIMAL (string): 
    """
    try:
        START_DATA = CURSOR.execute('''
            SELECT
                *
            FROM 
                main
            WHERE
                pop_year = ?
            AND
                species = ?
            LIMIT
                2
        ;''', [YEARS[0], ANIMAL]).fetchall()

        END_DATA = CURSOR.execute('''
            SELECT
                *
            FROM 
                main
            WHERE
                pop_year = ?
            AND
                species = ?
            LIMIT
                2
        ;''', [YEARS[1], ANIMAL]).fetchall()

        POP_START = int(START_DATA[0][16]) + int(START_DATA[1][16])
        POP_END = int(END_DATA[0][16]) + int(END_DATA[1][16])
        POP = [POP_START, POP_END]
        GROWTH_SINGLE = calc(POP, YEARS)
        print(f"The population growth from {YEARS[0]} - {YEARS[1]} of {ANIMAL} is: {GROWTH_SINGLE}.")
        return menu()
    except ValueError:
        print("The data is unavailable.")
        return menu()

def calc(POP, YEARS):
    """Calculates the growth rate.

    Args:
        POP (int): Populations of starting and end year.
        YEARS (int): Years that the user is using as reference.

    Returns:
        int: growth rate
    """
    POP_DIFF = POP[1] - POP[0]
    YEAR_DIFF = int(YEARS[1]) - int(YEARS[0])
    GROWTH = POP_DIFF/YEAR_DIFF
    return GROWTH

def filtrationAll(YEARS):
    """Filters all animals

    Args:
        YEARS (string): 
    """
    START_DATA = CURSOR.execute('''
        SELECT
            *
        FROM 
            main
        WHERE
            pop_year = ?
        LIMIT
            8
    ;''', [YEARS[0]]).fetchall()

    END_DATA = CURSOR.execute('''
        SELECT
            *
        FROM 
            main
        WHERE
            pop_year = ?
        LIMIT
            8
    ;''', [YEARS[1]]).fetchall()
    
    POP_START = addAll(START_DATA)
    POP_END = addAll(END_DATA)
    POP = [POP_START, POP_END]
    GROWTH_ALL = calc(POP, YEARS)
    print(f"The population growth from {YEARS[0]} - {YEARS[1]} of all animals is: {GROWTH_ALL}.")
    return menu()


def addAll(DATA):
    """Adds all the populations when the animal is "All"

    Args:
        DATA (list): Rows that were filtered

    Returns:
        int: Sum, which equals population of that year.
    """
    SUM = 0
    for i in range(len(DATA)):
        try:
            NUM = int(DATA[i][16])
            SUM = NUM + SUM
        except ValueError:
            continue
    return SUM

def filtrationDelete(YEAR, ANIMAL, AREA):
    """Deletes a row from the database

    Args:
        YEAR (string): 
        ANIMAL (string): 
        AREA (string): 
    """
    CURSOR.execute('''
        DELETE FROM
            main
        WHERE
            pop_year = ?
        AND
            species = ?
        AND
            area = ?
    ;''', [YEAR, ANIMAL, AREA])
    CONNECTION.commit()
    print("The data has been deleted.")
    return menu()

        



### --- MAIN PROGRAM CODE --- ###
if __name__ == "__main__":
    MAIN = createPop()
    TEXT = readfile()
    SPLIT = processInfo(TEXT)
    addInfo(SPLIT)
    CHOICE = menu()
    while True:
        if CHOICE == 1:
            YEARS = getYear(CHOICE)
            ANIMAL = getAnimal(CHOICE)
            print(ANIMAL)
            if ANIMAL == "All":
                filtrationAll(YEARS)
            else:
                filtrationSingle(YEARS, ANIMAL)
        elif CHOICE == 2:
            INPUTS = getInfo()
            insertUserInput(INPUTS)
            saveFile(INPUTS)
        elif CHOICE == 3:
            YEAR = getYear(CHOICE)
            ANIMAL = getAnimal(CHOICE)
            AREA = getArea()
            filtrationDelete(YEAR, ANIMAL, AREA)
        elif CHOICE == 4:
            again()