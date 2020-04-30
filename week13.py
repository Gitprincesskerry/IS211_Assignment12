# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This is Kerry Rainford's Week 13 Assignment

import re, sqlite3
from flask import Flask, render_template, request, redirect, sessions, g, flash, url_for
app = Flask(__name__)
#app.secretkey = 'd\xe9X\x00\xbe~Uq\xebX\xae\x81\x1fs\t\xb4\x99\xa3\x87\xe6.\xd1_'
app.config.from_object(__name__)

secretkey= '#d\xe9X\x00\xbe~Uq\xebX\xae\x81\x1fs\t\xb4\x99\xa3\x87\xe6.\xd1_'
username = 'admin'
password = 'password'
hw13database = 'hw13.db'


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods = ['POST'])
def login():
    uname = request.form['username'].strip()
    pword = request.form['password'].strip()

    if uname == username and pword == password:
        return redirect(url_for('dashboard'))
    else:
        print('Invalid username or password')
        return redirect(url_for('home'))

def connect():
    return sqlite3.connect(app.config['hw13database'])


@app.before_request
def before_request():
    g.db = sqlite3.connect("hw13.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/dashboard')
def dashboard():
    student_table = g.db.execute("SELECT id, first_name, last_name FROM student").fetchall()
    quizzes = g.db.execute("select id, subject, question_total, date_quiz_taken from quiz").fetchall()
    return render_template('dashboard.html', students=student_table, quizzes=quizzes)


@app.route('/student/add')
def addstudent():
    return render_template('addstudent.html')


@app.route('/quiz/add')
def addquiz():
    return render_template('addquiz.html')


@app.route('/results/add')
def addresults():
    return render_template('quizresults.html')


if __name__ == "__main__":
    app.run()
