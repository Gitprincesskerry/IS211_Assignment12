# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This is Kerry Rainford's Week 12 Assignment

import sqlite3 as kerrydb

student = (
    (1,'John','Smith'),
    (2,'Kerry','Rainford'),
    (3,'Shane','Sudal'),
    (4,'Danny','Love')
    )

quiz = (
    (1,'Python Basics',5, '2020-02-05'),
    (2,'Python Flask',10, '2020-03-25'),
    (3,'Python Recursion',5, '2020-04-25'),
    (4,'Python Data Types',10, '2020-01-23')
    )

studentresults = (
    (1,1, 85),
    (2,2, 98),
    (3,3, 99),
    (4,6, 99)
    )

con = kerrydb.connect('hw13.db')
#con.text_factory = str

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS student")
    cur.execute("CREATE TABLE student(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT)")
    cur.executemany("INSERT INTO student VALUES(?, ?, ?)", student)


    cur.execute("DROP TABLE IF EXISTS quiz")
    cur.execute("CREATE TABLE quiz(id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, question_total INTEGER, date_quiz_taken DATE)")
    cur.executemany("INSERT INTO quiz VALUES(?, ?, ?, ?)", quiz)

    cur.execute("DROP TABLE IF EXISTS studentresults")
    cur.execute("CREATE TABLE studentresults(student_id INTEGER , quiz_id INTEGER, score INTEGER)")
    cur.executemany("INSERT INTO studentresults VALUES(?, ?, ?)", studentresults)
