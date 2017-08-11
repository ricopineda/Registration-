from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'secret'
mysql = MySQLConnector(app,'registration')

@app.route('/')
def index():


	return render_template('index.html')


@app.route('/process', methods=['POST'])
def create():
	if len(request.form['first_name']) < 2:
		flash("First Name must be more than two characters!")
	elif len(request.form['last_name']) < 2:
		flash("Last Name must be more than two characters!")
	elif len(request.form['email']) < 2:
		flash("Email must be more than two characters!")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
	elif len(request.form['password']) < 2:
		flash("Password must be more than two characters!")
	else:
		flash("Success!")
		query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"

		data = {
         	'first_name': request.form['first_name'],
         	'last_name': request.form['last_name'],
         	'email': request.form['email'],
         	'password': request.form['password'],

       	}

		mysql.query_db(query, data)
	return redirect('/')

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	query = "SELECT email, password FROM users WHERE email = :email" 
	data = {
		'email': email,
		'password': password
	}
	info = mysql.query_db(query, data)
	print info
	if info:
		if email == info[0]["email"] and password == info[0]["password"]:
			return render_template('success.html')

		
		else:
			flash("WRONG")
		return redirect('/')
	else:
		flash("WRONG")
	return redirect('/')	

app.run(debug=True)

# @app.route('/process', methods=['POST'])
# def create():
#     print request.form['first_name']
#     print request.form['last_name']
#     print request.form['email']
#     print request.form['password']
#     # add a friend to the database!
#     return redirect('/')

















