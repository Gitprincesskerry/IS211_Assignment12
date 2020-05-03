# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This is Kerry Rainford's Week 13 Assignment

import sqlite3
from flask import Flask, render_template, request, redirect, session, g, flash, url_for
from markupsafe import escape
app = Flask(__name__)
app.secret_key = 'kerrywillnotsay'

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
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        flash = "Invalid username or password. Try again!"
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
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        student_table = g.db.execute("SELECT id, first_name, last_name FROM student").fetchall()
        quizzes = g.db.execute("select id, subject, question_total, date_quiz_taken from quiz").fetchall()
        return render_template('dashboard.html', students=student_table, quizzes=quizzes)

@app.route('/student/add', methods = ['GET','POST'])
def addstudent():
    if session['logged_in'] is not True:
        return redirect('/login')

    elif request.method == 'GET':
        return render_template('addstudent.html')

    elif request.method == 'POST':
        g.db.execute("INSERT INTO student (first_name, last_name) VALUES(?, ?)",
                    [request.form['firstname'],request.form['lastname']])
        g.db.commit()
        return redirect(url_for('dashboard'))

@app.route('/quiz/add', methods = ['GET','POST'])
def addquiz():
    if session['logged_in'] is not True:
        return redirect('/login')

    elif request.method == 'GET':
        return render_template('addquiz.html')

    elif request.method == 'POST':
        g.db.execute("INSERT INTO quiz (subject, question_total, date_quiz_taken) VALUES(?, ?, ?)",
                    [request.form['subject'],request.form['numberofquizquestions'],request.form['dateofquiz']])
        g.db.commit()
        return redirect(url_for('dashboard'))

@app.route('/student/<id>', methods = ['GET'])
def quizresults(id):
    if session['logged_in'] is not True:
        return redirect('/login')

    else:

        cursor = g.db.cursor()
        cursor.execute("SELECT count(*) FROM studentresults WHERE student_id =" + id)
        count=cursor.fetchone()

        id_score = g.db.execute("SELECT student_id, score FROM studentresults WHERE student_id =" + id).fetchall()

        return render_template('quizresults.html', id_score=id_score, count=count)

@app.route('/results/add', methods = ['GET','POST'])
def addresults():
    if session['logged_in'] is not True:
        return redirect('/login')

    elif request.method == 'GET':
        id_score = g.db.execute("SELECT student_id, score FROM studentresults").fetchall()
        id_quiz = g.db.execute("SELECT id, subject FROM quiz").fetchall()

        return render_template('addscore.html', id_score=id_score,id_quiz=id_quiz)

    elif request.method == 'POST':
        print("test")
        g.db.execute("INSERT INTO studentresults (student_id, quiz_id, score) VALUES(?, ?, ?)",
                    [request.form['StudentID'],request.form['quizname'],request.form['Score']])
        g.db.commit()

        return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run()
