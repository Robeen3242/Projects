'''
title: Search and Sort Superheros
author: Robin Liu
date: 2023-03-04
'''
### INPUT
def getRawData(fileName):
    import csv
    tempLi = []
    fil = open(fileName)
    text = csv.reader(fil)
    for line in text:
    	tempLi.append(line)
    var = tempLi.pop(0)
    return tempLi, var

def menu():
    """
    This is a menu for the program so the user can perform multiple functions.
    :return:
    """
    print(
        """Welcome to the Marvel and DC database. To look view the general information of a specific super-hero or super-villian, please enter a valid Superhero ID.")
        Please select one of the following options by inputting the assigned number:
    1. View a hero/villain.
    2. Add a hero/villain.
    """)
    CHOICE = input("> ")
    if CHOICE == '1':
        ID = input("What is the Superhero ID? > ")
        checkValidID(ID, IDS)
        insertionSort(IDS)
        VALIDITY = checkValidID(ID, IDS)
        if VALIDITY[0] == False:
            print("The ID you have entered is either not valid or not within our database. Please try again.")
        else:
            getInfo(VALIDITY[1])
    elif CHOICE == '2':
        addID()
    else:
        print("You did not submit a valid response.")


def addID():
    """
    User adds information about a new person.
    :return: None
    """
    global FILENAME
    print("Please enter the new info. The 'Superhero ID' must have a letter at the beginning and must end in a three digit number.")
    INFO = []
    for i in range(len(headers)):
        INFO.append(input(f"{headers[i]}: ")) #Prompts the user to register information for the specific header collumn
    USED_ID = checkValidID(INFO[0], IDS)
    
    if USED_ID == True: #No two ID's can exist at once
        print("This ID already exists")
    else:
        print("""-------------------------
        The following data is the data input into the program:""")
        for i in range(len(headers)):
            print(f"{headers[i]}: {INFO[i]}")
        if ',' in INFO[1]: #
                print("If the superhero has additional names/aliases, please put brackets around each name.") #Removes formatting issue with commas in a likely place for commas to be input
                return addID()
        else:
            FINALIZE = input("Would you like to proceed? (Y/N) > ") #confirm with the user
            if FINALIZE.upper() == "Y" or "YES":
                rawArr.append(INFO)
                print("The new entry has been submitted and saved.")
                saveData(rawArr)
            elif FINALIZE.upper() == "N" or "NO":
                print("The following set of data has not been added.")
                return menu()
            else:
                print("You did not enter a valid response. Please try again.")
                return addID()
    
###PROCESSING
def insertionSort(IDS):
    """
    Sorts the ID's using insertion sort. Individual IDS are far easier to sort than the first value of entire
    lists and then sorting them like that.
    :param IDS: list (string)
    :return: 
    """
    for i in range(len(IDS)):
        IND = IDS[i] #reference index
        SORTED_IND = i - 1 #separates 'sorted' part of the list from 'unsorted' list
        while SORTED_IND >= 0 and IND < IDS[SORTED_IND]:
            # While there are still values to sort, run through the list
            IDS[SORTED_IND + 1] = IDS[SORTED_IND]
            SORTED_IND = SORTED_IND - 1  #Swapping
        IDS[SORTED_IND + 1] = IND

def checkValidID(ID, IDS):
    """
    Search for value within a list whilst checking if the ID is valid. Binary search itself is a check of whether or not the ID is in IDS
    or not which is why I have decided to include it here.
    :param ID: (string)
    :param IDS: (list)
    :return: list (bool, string)
    """
    ID = ID.upper() #removes variability for upper/lower
    ID = list(ID)   # convert to list because strings are immutable
    if len(ID)<4:                     #removes variability between m9 and m009 by inserting the necessary 0's
        for i in range(4-len(ID)):
            ID.insert(1, '0')
    ID = ''.join(ID) #Turning the list back into a string
    if ID[0].isnumeric() or len(ID) > 4: #If the first index is anything but a letter or the length of the ID is above 4, deny entry
        print("The Superhero ID is an identification code beginning with a letter number and a three digit number. The following input does not satisfy the conditions. Please try again.")
        return menu()
    elif ID[1].isnumeric() and ID[2].isnumeric() and ID[3].isnumeric(): #only continue if the three digits at the end are numbers
        SMALL_IND = 0
        LARGE_IND = len(IDS)
        while SMALL_IND < LARGE_IND:
            MIDPOINT_IND = (SMALL_IND + LARGE_IND) // 2
            if IDS[MIDPOINT_IND] == ID:
                return True, ID
            elif ID > IDS[MIDPOINT_IND]:
                SMALL_IND = MIDPOINT_IND + 1
            else:
                LARGE_IND = MIDPOINT_IND
        return False, ID #ID goes here so that it returns a list regardless of whether the check passed.
    else:
        print("The Superhero ID is an identification code beginning with a letter number and a three digit number. The following input does not satisfy the conditions. Please try again.")
        return menu()


def saveData(rawArr):
    """
    Saves changes to a file.
    :param LIST: (LIST)
    :return: none
    """
    global FILENAME
    FILE = open(FILENAME, 'w')
    FILE.writelines(','.join(headers) + '\n') #The following is for formatting the file the way it was found.
    for i in range(len(rawArr)):
        FILE.writelines(','.join(rawArr[i]) + '\n')
    FILE.close()

###OUTPUT 
def getInfo(ID):
    """
    Gets the info of the specific ID
    :param IDS: (string)
    :return: bool
    """
    for i in range(len(rawArr)):
        if rawArr[i][0] == ID:
            if len(rawArr[i])>11:        #This fixes a format issue if the file is saved to and ran again
                for j in range(8):
                    print(f"{headers[j]}: {rawArr[i][j]}")
                print(f"{headers[-3]}: {rawArr[i][8]} -{rawArr[i][9]}")
                print(f"{headers[-1]}: {rawArr[i][-1]}")
            else:
                for j in range(len(headers)):
                    print(f"{headers[j]}: {rawArr[i][j]}")


if __name__ == "__main__":
    FILENAME = 'comicbookCharData_mixed.csv'
    rawArr, headers = getRawData('comicBookCharData_mixed.csv')
    IDS = []
    for i in range(len(rawArr)):    #Pulling the ID's of every individual hero and adding it to a new list.
        IDS.append(rawArr[i][0])
    while True:
        menu()