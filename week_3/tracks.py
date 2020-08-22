"""Third programming assignment of the course 'Using Databases with Python'."""


import sqlite3
import xml.etree.ElementTree as ET


# Create a Connection object:
conn = sqlite3.connect('trackdb.sqlite')

# Create a Cursor object:
cur = conn.cursor()

# Make sure we always start fresh:
cur.executescript(
    """
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track
    """
)

# Create a table for storing the data related to the ARTISTS:
cur.execute(
    """
    CREATE TABLE Artist (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    )
    """
)

# Create a table for storing the data related to the GENRES:
cur.execute(
    """
    CREATE TABLE Genre (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    )
    """
)

# Create a table for storing the data related to the ALBUMS:
cur.execute(
    """
    CREATE TABLE Album (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id INTEGER,
        title TEXT UNIQUE
    )
    """
)

# Create a table for storing the data related to the TRACKS:
cur.execute(
    """
    CREATE TABLE Track (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT UNIQUE,
        album_id INTEGER,
        genre_id INTEGER,
        len INTEGER,
        rating INTEGER,
        count INTEGER
    )
    """
)

# Read the XML file:
tree = ET.parse('Library.xml')

# The path to the relevant entries is 'dict/dict/dict'. Find all entries in this path:
entries = tree.findall('dict/dict/dict')


def lookup(entry, key):
    """Helper function for extracting the relevant data from the XML file."""
    found = False
    for child in entry:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


# Loop over 'entries' to insert the relevant data into the database:
for entry in entries:

    # Check that the current entry contains information about a track. If it
    # doesn't, skip.
    if lookup(entry, 'Track ID') is None:
        continue

    # Try to retrieve the name of the ARTIST. If this information is missing, skip.
    artist = lookup(entry, 'Artist')
    if artist is None:
        continue

    # Try to retrieve the name of the GENRE. If this information is missing, skip.
    genre = lookup(entry, 'Genre')
    if genre is None:
        continue

    # Try to retrieve the name of the ALBUM. If this information is missing, skip.
    album = lookup(entry, 'Album')
    if album is None:
        continue

    # Try to retrieve the name of the TRACK. If this information is missing, skip.
    name = lookup(entry, 'Name')
    if name is None:
        continue

    # Retrieve the remaining relevant information on the TRACK:
    length = lookup(entry, 'Total Time')
    rating = lookup(entry, 'Rating')
    count = lookup(entry, 'Play Count')

    # Insert the data on the ARTIST into the database.
    # Use 'OR IGNORE' due to the uniqueness constraint on 'name'.
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))

    # Get the 'id' of the artist we just inserted into the database:
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    # Insert the data on the GENRE into the database.
    # Use 'OR IGNORE' due to the uniqueness constraint on 'name'.
    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))

    # Get the 'id' of the genre we just inserted into the database:
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    # Insert the data on the ALBUM into the database.
    # Use 'OR IGNORE' due to the uniqueness constraint on 'title'.
    cur.execute(
        'INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)',
        (artist_id, album)
    )

    # Get the 'id' of the album we just inserted into the database:
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    # Insert the data on the TRACK into the database:
    cur.execute(
        """
        INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, album_id, genre_id, length, rating, count)
    )

    # Commit the changes:
    conn.commit()

# Close the connection:
conn.close()
