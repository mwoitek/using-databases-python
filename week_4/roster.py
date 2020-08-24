"""Fourth programming assignment of the course 'Using Databases with Python'."""


import json
import sqlite3


# Create a Connection object:
conn = sqlite3.connect('rosterdb.sqlite')

# Create a Cursor object:
cur = conn.cursor()

# Make sure we always start fresh:
cur.executescript(
    """
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member
    """
)

# Create a table for storing the data related to the USERS:
cur.execute(
    """
    CREATE TABLE User (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    )
    """
)

# Create a table for storing the data related to the COURSES:
cur.execute(
    """
    CREATE TABLE Course (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT UNIQUE
    )
    """
)

# Create a table for storing the data related to MEMBERSHIP:
cur.execute(
    """
    CREATE TABLE Member (
        user_id INTEGER,
        course_id INTEGER,
        role INTEGER,
        PRIMARY KEY (user_id, course_id)
    )
    """
)

# Read the JSON file:
with open('roster_data.json', 'r') as json_file:
    str_data = json_file.read()
json_data = json.loads(str_data)

# Loop over the entries in the JSON file:
for entry in json_data:

    # Get the NAME of the USER:
    name = entry[0]
    # Get the TITLE of the COURSE:
    title = entry[1]
    # Get the ROLE of that user in that course:
    role = entry[2]

    # Insert the data on the USER into the database.
    # Use 'OR IGNORE' due to the uniqueness constraint on 'name'.
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))

    # Get the 'id' of the user we just inserted into the database:
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Insert the data on the COURSE into the database.
    # Use 'OR IGNORE' due to the uniqueness constraint on 'title'.
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title,))

    # Get the 'id' of the course we just inserted into the database:
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Insert the MEMBERSHIP data into the database:
    cur.execute(
        """
        INSERT OR REPLACE INTO Member (user_id, course_id, role)
        VALUES (?, ?, ?)
        """,
        (user_id, course_id, role)
    )

    # Commit the changes:
    conn.commit()

# Close the connection:
conn.close()
