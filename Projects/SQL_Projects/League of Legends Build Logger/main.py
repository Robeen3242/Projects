'''
Title: LOL Build Database
Author: Robin Liu
Date Created: 2022-01-10
'''


from flask import Flask, render_template, request, redirect
from pathlib import Path
import sqlite3
# --- Global Variables --- #
DB_NAME = "build.db"
FIRST_RUN = True
if (Path.cwd() / DB_NAME).exists(): #Checks if a database exists already.
    FIRST_RUN = False

CHAMPIONS = ["aatrox", "ahri", "akali", "akshan", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe", "aurelion sol", "azir"
"bard", "blitzcrank","brand", "braum", "caitlyn", "camille", "cassiopeia", "cho'gath", "corki", "darius", "diana",
"dr mundo", "draven", "ekko", "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen", "gnar",
"gragas", "graves", "gwen", "hecarim", "heimerdinger", "illaoi", "irelia", "ivern", "janna", "jarvan iv", "jax", "jayce", "jhin",
"jinx", "kai'sa", "kalista", "karma", "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "kha'zix", "kindred", "kled",
"kog'maw", "leblanc", "lee sin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux", "malphite", "malzahar", "maokai", "master yi",
"miss fortune", "mordekaiser", "morgana", "nami", "nasus", "nautilus", "neeko", "nidalee", "nocturne", "nunu and willump", "olaf",
"orianna", "ornn", "pantheon", "poppy", "pyke", "qiyana", "quinn", "rakan", "rammus", "rek'sai", "rell", "renekton", "rengar",
"riven", "rumble", "ryze", "samira", "sejuani", "senna", "seraphine", "sett", "shaco", "shen", "shyvana", "singed", "sion", "sivir",
"skarner", "sona", "soraka", "swain", "sylas", "syndra", "tahm kench", "taliyah", "talon", "taric", "teemo", "thresh", "tristana",
"trundle", "tryndamere", "twisted fate", "twitch", "udyr", "urgot", "varus", "vayne", "veigar", "vel'koz", "vex", "vi", "viego",
"viktor", "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xin zhao", "yasuo", "yone", "yorick", "yuumi", "zac",
"zed", "ziggs", "zilean", "zoe", "zyra"]

PATHS = [["Overheal", "Triumph", "Presence of Mind", "Legend: Alacrity", "Legend: Tenacity", "Legend: Bloodline", "Coup de Grace",
"Cut Down", "Last Stand"], ["Cheap Shot", "Taste of Blood", "Sudden Impact", "Zombie Ward", "Ghost Poro", "Eyeball Collection",
"Ravenous Hunter", "Ingenious Hunter", "Relentless Hunter", "Ultimate Hunter"], ["Nullifying Orb", "Manaflow Band", "Nimbus Cloak",
"Transcendence","Celerity", "Absolute Focus", "Scorch", "Waterwalking", "Gathering Storm"], ["Demolish", "Font of Life",
"Shield Bash", "Conditioning", "Second Wind", "Bone Plating", "Overgrowth", "Revitalize", "Unflinching"], ["Hextech Flashtraption",
"Magical Footwear", "Perfect Timing", "Future's Market", "Minion Dematerializer", "Biscuit Delivery", "Cosmic Insight",
"Approach Velocity", "Time Warp Tonic"]]

ROWS = [["Overheal", "Triumph", "Presence of Mind"], ["Legend: Alacrity", "Legend: Tenacity", "Legend: Bloodline"], ["Coup de Grace",
"Cut Down", "Last Stand"], ["Cheap Shot", "Taste of Blood", "Sudden Impact"], ["Zombie Ward", "Ghost Poro", "Eyeball Collection"],
["Ravenous Hunter", "Ingenious Hunter", "Relentless Hunter", "Ultimate Hunter"], ["Nullifying Orb", "Manaflow Band", "Nimbus Cloak"],
["Transcendence", "Celerity", "Absolute Focus"], ["Scorch", "Waterwalking", "Gathering Storm"], ["Demolish", "Font of Life",
"Shield Bash"], ["Conditioning", "Second Wind", "Bone Plating"], ["Overgrowth", "Revitalize", "Unflinching"], ["Hextech Flashtraption",
"Magical Footwear", "Perfect Timing"], ["Future's Market", "Minion Dematerializer", "Biscuit Delivery"], ["Cosmic Insight",
"Approach Velocity", "Time Warp Tonic"]]
# --- Flask Variables --- #
app = Flask(__name__)


@app.route('/delete/<id>') #This is a button that deletes the build. The "id" is the identification key of the build used to single out a build.
def deleteBuildWeb(id):
    """Transfers build id from webpage to program

    Args:
        id (Integer): Primary key of build.

    Returns:
        String: An alert will be made.
    """
    deleteBuild(id)
    return redirect('/')
@app.route('/', methods=['GET', 'POST']) #This is a webpage used to view current builds. getBuilds() extracts data from database and is sent to be displayed in search.
def index():
    """Transfers build information from database to webpage
    """
    QUERY_BUILD = getBuilds()
    return render_template("index.html", build=QUERY_BUILD)

@app.route('/precision', methods=['GET', 'POST']) #The following webpages are the same in function. It takes information from the web page
def precision():                                  #and is then put into a list. This list will go through a series of tests. Once these tests
                                                  #have passed it will be added to the database, returning an alert saying it has been added.
    """A webpage to get information.              

    Returns:
        list: List of necessary data
    """
    ALERT = ""                                    
    if request.form:
        NAME = request.form.get("name")
        CHAMP = request.form.get("champion")
        CHAMP = CHAMP.title()
        KEYSTONE = request.form.get("keystone")
        ROW_1 = request.form.get("row_1")
        ROW_2 = request.form.get("row_2")
        ROW_3 = request.form.get("row_3")
        S_ROW_1 = request.form.get("second_one")
        S_ROW_2 = request.form.get("second_two")
        SHARD_ONE = request.form.get("shard_one")
        SHARD_TWO = request.form.get("shard_two")
        SHARD_THREE = request.form.get("shard_three")
        DESCRIPTION = request.form.get("description")
        PRIMARY_KEY = getID()
        BUILD_INFO = [NAME, CHAMP, KEYSTONE, ROW_1, ROW_2, ROW_3, S_ROW_1, S_ROW_2, SHARD_ONE, SHARD_TWO, SHARD_THREE, DESCRIPTION, PRIMARY_KEY]


        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)
        CHECK_FOUR = descriptionVariety(BUILD_INFO)

        if CHECK is True and CHECK_ONE is True and CHECK_TWO is True and CHECK_THREE is True and CHECK_FOUR is True:
            addBuild(BUILD_INFO)
            ALERT = "Your build has been saved."
        else:
            ALERT = "The information you put in is wrong or a build with the same description already exists. The build has not been saved. Please try again."
    return render_template("precision.html", alert=ALERT)

@app.route('/domination', methods=['GET', 'POST'])
def domination():
    ALERT = ""
    if request.form:
        NAME = request.form.get("name")
        CHAMP = request.form.get("champion")
        KEYSTONE = request.form.get("keystone")
        ROW_1 = request.form.get("row_1")
        ROW_2 = request.form.get("row_2")
        ROW_3 = request.form.get("row_3")
        S_ROW_1 = request.form.get("second_one")
        S_ROW_2 = request.form.get("second_two")
        SHARD_ONE = request.form.get("shard_one")
        SHARD_TWO = request.form.get("shard_two")
        SHARD_THREE = request.form.get("shard_three")
        DESCRIPTION = request.form.get("description")
        PRIMARY_KEY = getID()
        BUILD_INFO = [NAME, CHAMP, KEYSTONE, ROW_1, ROW_2, ROW_3, S_ROW_1, S_ROW_2, SHARD_ONE, SHARD_TWO, SHARD_THREE, DESCRIPTION, PRIMARY_KEY]


        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)

        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)
        CHECK_FOUR = descriptionVariety(BUILD_INFO)

        if CHECK is True and CHECK_ONE is True and CHECK_TWO is True and CHECK_THREE is True and CHECK_FOUR is True:
            addBuild(BUILD_INFO)
            ALERT = "Your build has been saved."
        else:
            ALERT = "The information you put in is wrong or a build with the same description already exists. The build has not been saved. Please try again."
    return render_template("domination.html", alert=ALERT)

@app.route('/sorcery', methods=['GET', 'POST'])
def sorcery():
    ALERT = ""
    if request.form:
        NAME = request.form.get("name")
        CHAMP = request.form.get("champion")
        KEYSTONE = request.form.get("keystone")
        ROW_1 = request.form.get("row_1")
        ROW_2 = request.form.get("row_2")
        ROW_3 = request.form.get("row_3")
        S_ROW_1 = request.form.get("second_one")
        S_ROW_2 = request.form.get("second_two")
        SHARD_ONE = request.form.get("shard_one")
        SHARD_TWO = request.form.get("shard_two")
        SHARD_THREE = request.form.get("shard_three")
        DESCRIPTION = request.form.get("description")
        PRIMARY_KEY = getID()
        BUILD_INFO = [NAME, CHAMP, KEYSTONE, ROW_1, ROW_2, ROW_3, S_ROW_1, S_ROW_2, SHARD_ONE, SHARD_TWO, SHARD_THREE, DESCRIPTION, PRIMARY_KEY]


        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)
        CHECK_FOUR = descriptionVariety(BUILD_INFO)

        if CHECK is True and CHECK_ONE is True and CHECK_TWO is True and CHECK_THREE is True and CHECK_FOUR is True:
            addBuild(BUILD_INFO)
            ALERT = "Your build has been saved."
        else:
            ALERT = "The information you put in is wrong or a build with the same description already exists. The build has not been saved. Please try again."
    return render_template("sorcery.html", alert=ALERT)

@app.route('/resolve', methods=['GET', 'POST'])
def resolve():
    ALERT = ""
    if request.form:
        NAME = request.form.get("name")
        CHAMP = request.form.get("champion")
        KEYSTONE = request.form.get("keystone")
        ROW_1 = request.form.get("row_1")
        ROW_2 = request.form.get("row_2")
        ROW_3 = request.form.get("row_3")
        S_ROW_1 = request.form.get("second_one")
        S_ROW_2 = request.form.get("second_two")
        SHARD_ONE = request.form.get("shard_one")
        SHARD_TWO = request.form.get("shard_two")
        SHARD_THREE = request.form.get("shard_three")
        DESCRIPTION = request.form.get("description")
        PRIMARY_KEY = getID()
        BUILD_INFO = [NAME, CHAMP, KEYSTONE, ROW_1, ROW_2, ROW_3, S_ROW_1, S_ROW_2, SHARD_ONE, SHARD_TWO, SHARD_THREE, DESCRIPTION, PRIMARY_KEY]


        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)
        CHECK_FOUR = descriptionVariety(BUILD_INFO)

        if CHECK is True and CHECK_ONE is True and CHECK_TWO is True and CHECK_THREE is True and CHECK_FOUR is True:
            addBuild(BUILD_INFO)
            ALERT = "Your build has been saved."
        else:
            ALERT = "The information you put in is wrong or a build with the same description already exists. The build has not been saved. Please try again."
    return render_template("resolve.html", alert=ALERT)

@app.route('/inspiration', methods=['GET', 'POST'])
def inspiration():
    ALERT = ""
    if request.form:
        NAME = request.form.get("name")
        CHAMP = request.form.get("champion")
        KEYSTONE = request.form.get("keystone")
        ROW_1 = request.form.get("row_1")
        ROW_2 = request.form.get("row_2")
        ROW_3 = request.form.get("row_3")
        S_ROW_1 = request.form.get("second_one")
        S_ROW_2 = request.form.get("second_two")
        SHARD_ONE = request.form.get("shard_one")
        SHARD_TWO = request.form.get("shard_two")
        SHARD_THREE = request.form.get("shard_three")
        DESCRIPTION = request.form.get("description")
        PRIMARY_KEY = getID()
        BUILD_INFO = [NAME, CHAMP, KEYSTONE, ROW_1, ROW_2, ROW_3, S_ROW_1, S_ROW_2, SHARD_ONE, SHARD_TWO, SHARD_THREE, DESCRIPTION, PRIMARY_KEY]

        CHECK = checkIntegrity(BUILD_INFO)
        CHECK_ONE = checkChampion(BUILD_INFO)
        CHECK_TWO = checkPathSecondary(BUILD_INFO)
        CHECK_THREE = checkRowDupe(BUILD_INFO)
        CHECK_FOUR = descriptionVariety(BUILD_INFO)

        if CHECK is True and CHECK_ONE is True and CHECK_TWO is True and CHECK_THREE is True and CHECK_FOUR is True:
            addBuild(BUILD_INFO)
            ALERT = "Your build has been saved."
        else:
            ALERT = "The information you put in is wrong or a build with the same description already exists. The build has not been saved. Please try again."
            
        
    return render_template("inspiration.html", alert=ALERT)   
# --- Database --- #
###INPUTS

def createTable():     #This will create a table, the primary key is a number identifying a build as unique.
    """Creates table
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        CREATE TABLE 
            build (
                build_name TEXT NOT NULL,
                champion TEXT NOT NULL,
                p_keystone TEXT NOT NULL,
                p_one TEXT NOT NULL,
                p_two TEXT NOT NULL,
                p_three TEXT NOT NULL,
                s_one TEXT NOT NULL,
                s_two TEXT NOT NULL,
                shard_one TEXT NOT NULL,
                shard_two TEXT NOT NULL,
                shard_three TEXT NOT NULL,
                description TEXT NOT NULL,
                build INTEGER PRIMARY KEY
            )
    ;''')
    CONNECTION.commit()
    CONNECTION.close()

def deleteBuild(ID):  #The following code will delete the build using its primary key, returned from the web browser.
    """Deletes a build from the database.

    Args:
        ID (integer): Build's primary key
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        DELETE FROM
            build
        WHERE
            build = ?
    
    ;''', ID)
    CONNECTION.commit()
    CONNECTION.close()


###PROCESSING
def descriptionVariety(BUILD_INFO): #This function will check if the description is already used. A build with the same description is just the same build as another.
    """Checks if description is the same

    Args:
        BUILD_INFO (list): 

    Returns:
        bool:
    """
    global DB_NAME

    CHECK = 1

    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    BUILDS = CURSOR.execute('''
        SELECT
            *
        FROM
            build
    ;''').fetchall()

    for i in range(len(BUILDS)): #Checks all builds
        if BUILD_INFO[-2] in BUILDS[i]:
            CHECK = 0
            break #Will stop upon finding a match.
    if CHECK == 0:
        return False
    else:
        return True


def checkChampion(BUILD_INFO): #Checks if the champion is a champion in League of Legends
    """Checks if the champion exists in League of Legends

    Args:
        BUILD_INFO (list): 

    Returns:
        bool: 
    """
    CHAMP = BUILD_INFO[1].lower() 
    if CHAMP in CHAMPIONS:
        return True
    else:
        return False


def checkPathSecondary(BUILD_INFO): #Secondary runes must be of the same path. This will check for it using the PATHS dictionary.
    """Checks if the secondary path is the same.

    Args:
        BUILD_INFO (list): 

    Returns:
        bool: 
    """
    SECONDARY_FIRST = BUILD_INFO[-7]
    SECONDARY_SECOND = BUILD_INFO[-6]

    CHECK = 1
    for i in range(len(PATHS)):
        if SECONDARY_FIRST in PATHS[i] and SECONDARY_SECOND in PATHS[i]:
            CHECK = 0

    if CHECK == 0:
        return True
    else:
        return False

def checkRowDupe(BUILD_INFO): #Runes must not be in the same row. Due to the limitations of Python, there is no way to limit choices.
    """Checks if the two runes are in the same row

    Args:
        BUILD_INFO (list): 

    Returns:
        bool: 
    """
    SECONDARY_FIRST = BUILD_INFO[-7]
    SECONDARY_SECOND = BUILD_INFO[-6]
    CHECK = 1
    for i in range(len(ROWS)):
        if SECONDARY_FIRST in ROWS[i] and SECONDARY_SECOND in ROWS[i]: #Upon finding the two runes being in the same row, it will stop and return a failure.
            CHECK = 0
            break
    
    if CHECK == 0:
        return False
    else:
        return True

def checkIntegrity(BUILD_INFO): #All the data points in the program are necessary for builds. This function will check if the BUILD_INFO has all of them.
    """Checks if all data points are filled in.

    Args:
        BUILD_INFO (list): 

    Returns:
        bool: 
    """
    INTEGRITY = len(BUILD_INFO)
    if INTEGRITY != 13:
        return False
    else:
        return True

def getID(): #For some reason, the automatic Primary Key maker for sqlite3 decided not to work so I implemented an ID maker.
    """Creates an ID for the build.

    Returns:
        integer: ID of build for database 
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    LENGTH = CURSOR.execute('''
        SELECT
            *
        FROM
            build
    ;''').fetchall()

    LENGTH = len(LENGTH) #Length of ID to show the number of builds that exist
    PRIMARY_KEY = LENGTH + 1 #A +1 is necessary as the build being added is not currently within the database
    return PRIMARY_KEY
    
###OUTPUTS

def addBuild(BUILD_INFO): #Adds the build to the database using the checked list
    """Adds a build to the database

    Args:
        BUILD_INFO (list):
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()

    CURSOR.execute('''
    INSERT INTO
        build (
            build_name,
            champion,
            p_keystone,
            p_one,
            p_two,
            p_three,
            s_one,
            s_two,
            shard_one,
            shard_two,
            shard_three,
            description,
            build
        )
    VALUES(
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    ;''', BUILD_INFO)

    CONNECTION.commit()
    CONNECTION.close()

def getBuilds(): #The program will get all the builds in a list to be exported to the website
    """Gets the builds to be displayed for the user

    Returns:
        2d Array: List of all builds
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    BUILDS = CURSOR.execute('''
        SELECT
            *
        FROM
            build
    ;''').fetchall()
    return BUILDS




# --- MAIN PROGRAM --- ###
if __name__ == "__main__":  
    if FIRST_RUN: #The database will be created on first run.
        createTable()
    app.run(debug=True)
