import sqlite3

conn = sqlite3.connect('roster.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name        VARCHAR(128) UNIQUE
); 

CREATE TABLE Course (
    course_id     INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title         VARCHAR(128) UNIQUE
); 

CREATE TABLE Member (
    user_id       INTEGER,
    course_id     INTEGER,
    role          INTEGER,

    PRIMARY KEY (user_id, course_id)
); 

''')
handle = open('dataRoster.csv')

for line in handle:
    line = line.strip()
    pieces = line.split(',')
    if len(pieces) < 3 : continue

    name = pieces[0]
    title = pieces[1]
    tempo = pieces[2]
    if tempo == "Instructor":
        role = 1
    else:
        role = 0


    print(name, title,role)

    cur.execute('''INSERT OR IGNORE INTO User (name) 
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT user_id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) 
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT course_id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Member (user_id, course_id, role ) 
        VALUES ( ?, ?, ? )''', ( user_id, course_id, role  ) )


    conn.commit()


    
