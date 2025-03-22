'''
title: flask web app for contacts
author: robin liu
date-created: 2021-06-23
'''

from flask import Flask, render_template, request, redirect
from pathlib import Path
import sqlite3
# --- GLOBAL VARIABLES --- #
DB_NAME = "flask.db"
FIRST_RUN = True
if (Path.cwd() / DB_NAME).exists():
    FIRST_RUN = False





# --- FLASK --- #
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form:
        FIRST_NAME = request.form.get("first_name")
        LAST_NAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        if getOneContact(EMAIL) is None:
            createContact(FIRST_NAME, LAST_NAME, EMAIL)
            ALERT = "Successfully added a new contact!"
            return render_template("index.html")
        else:
            ALERT = "A contact with the given email already exists."
    QUERY_CONTACTS = getAllContacts
    return render_template("index.html", alert=ALERT, contacts=QUERY_CONTACTS)

@app.route('/delete/<id>')
def deleteContactPage(id):
    deleteContact(id)
    return redirect('/')
# --- DATABASE --- #
###INPUTS
def createTable():
    """creates database table on first run
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        CREATE TABLE
            contacts(
                first_name TEXT NOT NULL,
                last_name TEXT,
                email TEXT PRIMARY KEY
            )

    ;''')
    CONNECTION.commit()
    CONNECTION.close()

def createContact(FIRST_NAME, LAST_NAME, EMAIL):
    """Adds contact to the database

    Args:
        FIRST_NAME (string): 
        LAST_NAME (string): 
        EMAIL (string): 
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.curosr()
    CURSOR.execute('''
        INSERT INTO
            contacts
        VALUES (
            ?, ?, ?
        )
    
    ;''', [FIRST_NAME, LAST_NAME, EMAIL])
    CONNECTION.commit()
    CONNECTION.close()
###PROCESSING

def deleteContact(EMAIL):
    """delete a contact

    Args:
        EMAIL (str): primary key
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute('''
        DELETE FROM
            contacts
        WHERE
            email = ?
    ;''', [EMAIL])
    CONNECTION.commit()
    CONNECTION.close()


###OUTPUTS
def getOneContact(EMAIL):
    """returns value of single contact

    Args:
        EMAIL (str): 
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CONTACT = CURSOR.execute('''
        SELECT
            *
        FROM
            contacts
        WHERE 
            email = ?
    ;''', [EMAIL]).fetchone()
    CONNECTION.close()
    return CONTACT

def getAllContacts():
    """returns every row i nthe contacts database
    Returns:
        CONTACTS (list):
    """
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor
    CONTACTS = CURSOR.execute('''
        SELECT
            *
        FROM
            contacts
        ORDER BY
            first_name
    ;''').fetchall()
    CONNECTION.close()
    return CONTACTS

if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)