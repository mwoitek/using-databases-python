"""Second programming assignment of the course 'Using Databases with Python'."""


import sqlite3


# Create a Connection object:
conn = sqlite3.connect('emaildb.sqlite')

# Create a Cursor object:
cur = conn.cursor()

# Make sure we always start fresh:
cur.execute('DROP TABLE IF EXISTS Counts')

# Create a table for storing the number of email messages per organization:
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# In this case, I think it's easier to first create a dictionary for storing
# the relevant data. Then I'll insert the content of this dictionary into the
# table 'Counts'.
counts = {}

# Read the text file, and load the 'counts' dictionary:
with open('mbox.txt', 'r') as text_file:
    for line in text_file:
        # Skip irrelevant lines:
        if not line.startswith('From: '):
            continue
        email = line.split(' ')[1]
        domain = email.split('@')[1]
        if domain in counts:
            counts[domain] += 1
        else:
            counts[domain] = 1


def count_generator(counts):
    for domain, count in counts.items():
        yield (domain, count)


# Insert the content of the 'counts' dictionary into the 'Counts' table:
cur.executemany(
    'INSERT INTO Counts (org, count) VALUES (?, ?)',
    count_generator(counts)
)

# Commit the changes:
conn.commit()

# Close the connection:
conn.close()
