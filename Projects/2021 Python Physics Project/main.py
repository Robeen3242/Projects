'''
title: canon ball
author: Robin Liu
date-created: 2021-10-4
'''
import math

###MAIN PROGRAM FUNCTIONS - Functions repeated within the code.
def intro():
    '''
    Introduces user to program.
    :return:
    '''
    print('''Welcome to the Navy's Cannon )perator. The use of this program is to calculate the distance a cannon ball 
    will travel from the cannon.''')

def menu():
    '''
    User chooses type of problem.
    :return: (int)
    '''
    print('''Choose a scenario.
    1. Cannon is aimed horizontally.
     ________ 
    |        | \ 
    |        |  \ 
    |________|   \     
    2. Cannon is aimed at an angle towards something else of the same height.
          _
        /  \ 
    ___/    \___
    3. Cannon is aimed at an angle towards something below the ships height.
          _
        /  \ 
    ___/    \ 
             \ 
              \___    
    4. Cannon is aimed at an angle towards something above the ships height.
          _
        /  \____
    ___/    
    
    ''')
    SCENARIO = input(">")
    #checks if the number input is within the parameters
    SCENARIO = checkInt(SCENARIO)
    if SCENARIO > 0 and SCENARIO < 5:
        return SCENARIO
    else:
        print(f"Your answer: {SCENARIO} is not suitable. Please choose ONE of the above.")
        return menu()

def checkInt(SCENARIO):
    '''
    Checks if the answer input into menu() is an integer
    :param SCENARIO: (int)
    :return: (int)
    '''
    if SCENARIO .isnumeric():
        return int(SCENARIO)
    else:
        #Asks user for new input.
        print(f"Your choice: {SCENARIO} is not what we asked you for. Please try again.")
        INPUT_NEW = input(">")
        return checkInt(INPUT_NEW)

def checkAngle(ANGLE):
    '''
    Makes sure that the angle is within 0 and 90 degrees.
    :param ANGLE: (string)
    :return: (none)
    '''
    if ANGLE < 90 and ANGLE > 0:
        return ANGLE
    else:
        print("This angle is not practical. Input a new one.")
        NEW_ANGLE = input(">")
        return checkAngle(NEW_ANGLE)

def again():
    '''
    Asks user if they wat to make another calculation.
    :return: (none)
    '''

    ANSWER = input("Would you like to make another calculation? (Y/n)")
    if ANSWER == "" or ANSWER == "Y" or ANSWER == "y":
        return True
    elif ANSWER == "N" or ANSWER == "n":
        return False
    else:
        print("You have not selected a correct option.")
        return again()

def checkFloat(NUMBER):
    '''
    Checks if the input is a float.
    :param NUMBER: (string)
    :return: (float)
    '''
    try:
        NUMBER = float(NUMBER)
        return NUMBER
    except ValueError:
        print("You did not enter a number!")
        NEW_NUM = input("Please enter a number:")
        return checkFloat(NEW_NUM)

def answer(DISTANCE,TIME):
    '''
    Prints the answer.
    :param DISTANCE: (float)
    :param TIME: (float)
    :return: (none)
    '''
    print(f"The cannon ball will travel {DISTANCE} meters in {TIME} seconds. ")

###SCENARIO 1 FUNCTIONS
def getValue1():
    '''
    Gets the values required for Scenario 1.
    :return: (float)
    '''
    ##Asks user for their values.
    SPEED = input("What is the cannon ball's horizontal speed (m/s)?  ")
    HEIGHT = input("What is the maximum height the cannon ball will reach (meters)?  ")
    SPEED = checkFloat(SPEED)
    HEIGHT = checkFloat(HEIGHT)
    return SPEED,HEIGHT

def calc1(SPEED,HEIGHT):
    '''
    Calculates the TIME and DISTANCE for scenario 1.
    :param SPEED: (float)
    :param HEIGHT: (float)
    :return: (float)
    '''
    TIME_SQUARED = (2*HEIGHT)/9.81
    TIME = math.sqrt(TIME_SQUARED)
    DISTANCE = SPEED*TIME
    return DISTANCE, TIME

###SCENARIO 2 FUNCTIONS
def getValue2():
    '''
    Gets the values required for Scenario 2.
    :return: (float)
    '''
    SPEED = input("What is the velocity of the cannon ball (m/s)?  ")
    ANGLE = input("What angle is the cannon ball aimed at (degrees)?  ")
    SPEED = checkFloat(SPEED)
    ANGLE = checkFloat(ANGLE)
    ANGLE = checkAngle(ANGLE)
    return SPEED, ANGLE

def calc2(SPEED, ANGLE):
    '''
    Calculates TIME and DISTANCE for scenario 2.
    :param SPEED: (float)
    :param ANGLE: (float)
    :return: (float)
    '''
    ANGLE = math.radians(ANGLE)
    VX = SPEED*math.cos(ANGLE)
    VY = SPEED*math.sin(ANGLE)
    TIME = (2*VY/9.81)
    DISTANCE = VX*TIME
    return DISTANCE, TIME


### SCENARIO 3 FUNCTIONS
def getValue3():
    '''
    Gets the values required for Scenario 3.
    :return: (float)
    '''
    SPEED = input("What is the speed of the cannon ball (m/s)?  ")
    ANGLE = input("What angle was the cannon ball aimed at (degrees)?  ")
    HEIGHT = input("What is the difference in height between where the cannon ball is fired"
                   " and where it lands BELOW the original ship (meters)?  ")
    SPEED = checkFloat(SPEED)
    ANGLE = checkFloat(ANGLE)
    HEIGHT = checkFloat(HEIGHT)
    ANGLE = checkAngle(ANGLE)
    return SPEED, ANGLE, HEIGHT

def calc3(SPEED, ANGLE, HEIGHT):
    '''
    Performs calculations for scenario 3.
    :param SPEED: (float)
    :param ANGLE: (float)
    :param HEIGHT: (float)
    :return: (float)
    '''
    ANGLE = math.radians(ANGLE)
    VX = SPEED * math.cos(ANGLE)
    VY = SPEED * math.sin(ANGLE)

    HEIGHT_UP = (VY*VY)/(2*9.81) ###Calculating the highest point of the cannon ball.
    HEIGHT_DOWN = HEIGHT_UP + HEIGHT ###Calculating the distance between highest point to lowest point.

    TIMEUP_SQ = (2*HEIGHT_UP)/9.81
    TIME_UP = math.sqrt(TIMEUP_SQ) ###Calculating time from origin to highest point.
    TIMEDOWN_SQ2 = (2*HEIGHT_DOWN)/9.81
    TIME_DOWN = math.sqrt(TIMEDOWN_SQ2) ###Calculating time from highest point to the ship below.
    TIME_TOTAL = TIME_UP + TIME_DOWN

    DISTANCE = TIME_TOTAL*VX
    return DISTANCE, TIME_TOTAL

###SCENARIO 4 FUNCTIONS
def getValue4():
    '''
    Gets the values required for Scenario 4.
    :return: (float)
    '''
    SPEED = input("What is the speed of the cannon ball (m/s)?  ")
    ANGLE = input("What angle was the cannon ball aimed at (degrees)?  ")
    HEIGHT = input("What is the difference in height between where the cannon ball is fired"
                   " and where it lands above the ship (meters)?  ")
    SPEED = checkFloat(SPEED)
    ANGLE = checkFloat(ANGLE)
    HEIGHT = checkFloat(HEIGHT)
    ANGLE = checkAngle(ANGLE)
    return SPEED, ANGLE, HEIGHT

def calc4(SPEED,ANGLE,HEIGHT):
    '''
    Performs calculations for scenario 4.
    :param SPEED: (float)
    :param ANGLE: (float)
    :param HEIGHT: (float)
    :return: (float)
    '''
    ANGLE = math.radians(ANGLE)
    VX = SPEED * math.cos(ANGLE)
    VY = SPEED * math.sin(ANGLE)

    HEIGHT_UP = (VY * VY) / (2 * 9.81)  ###Calculating the highest point of the cannon ball.
    HEIGHT_DOWN = HEIGHT_UP - HEIGHT

    TIMEUP_SQ = (2 * HEIGHT_UP) / 9.81
    TIME_UP = math.sqrt(TIMEUP_SQ)  ###Calculating time from origin to highest point.
    TIMEDOWN_SQ2 = (2 * HEIGHT_DOWN) / 9.81
    TIME_DOWN = math.sqrt(TIMEDOWN_SQ2)  ###Calculating time from highest point to the ship below.
    TIME_TOTAL = TIME_UP + TIME_DOWN

    DISTANCE = VX*TIME_TOTAL
    return DISTANCE, TIME_TOTAL

while True:
    ###MAIN PROGRAM
    intro()

    ###INPUT
    SCENARIO = menu()
    if SCENARIO == 1:
        ###INPUT
        SPEED, HEIGHT = getValue1()
        ###PROCESSING
        DISTANCE, TIME = calc1(SPEED, HEIGHT)
        ###OUTPUT
        answer(DISTANCE, TIME)
        again()
    elif SCENARIO == 2:
        ###INPUT
        SPEED, ANGLE = getValue2()
        ###PROCESSING
        DISTANCE, TIME = calc2(SPEED, ANGLE)
        ###OUTPUT
        answer(DISTANCE, TIME)
        again()
    elif SCENARIO == 3:
        ###INPUT
        SPEED, ANGLE, HEIGHT = getValue3()
        ###PROCESSING
        DISTANCE, TIME = calc3(SPEED, ANGLE, HEIGHT)
        ###OUTPUT
        answer(DISTANCE, TIME)
        again()
    elif SCENARIO == 4:
        ###INPUT
        SPEED, ANGLE, HEIGHT = getValue4()
        ###PROCESSING
        DISTANCE, TIME = calc4(SPEED, ANGLE, HEIGHT)
        ###OUTPUT
        answer(DISTANCE, TIME)
        again()
