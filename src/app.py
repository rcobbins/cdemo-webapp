import os
import psycopg2
import json
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import requests

app = Flask(__name__)
dbhost = os.environ["PG_HOST"]
dbuser = os.environ["PG_USER"]
dbpass = os.environ["PG_PASS"]


@app.route('/')
def mainfunc():
	return render_template('list.html')

@app.route('/getrecord', methods=['GET'])
def getRecord():
	conn = psycopg2.connect("host='" + dbhost + "' user='" + dbuser +"' password='" + dbpass + "'")
	cur = conn.cursor()
	cur.execute("SELECT * from users")
	rows = cur.fetchall()
	requestList = []
	for row in rows:
		requestItem = {
			'id': row[0],
			'username': row[1],
			'company': row[4],
			'email': row[3],
			'phone': row[5]
		}
		requestList.append(requestItem)
	cur.close()
	conn.close()
	return json.dumps(requestList)

@app.route('/newUser', methods=['POST'])
def newUser():
	conn = psycopg2.connect("host='" + dbhost + "' user='" + dbuser +"' password='" + dbpass + "'")
	cur = conn.cursor()
	data = request.get_json()
	cur.execute("INSERT INTO users (username, password, company, email, phone) VALUES (%s, %s, %s, %s, %s)", (data['username'], data['password'], data['company'], data['email'], data['phone']))	
	conn.commit()
	cur.close()
	conn.close()
	for key, value in data.items():
		print(key + ": " + value)
	return 'Done'

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
	conn = psycopg2.connect("host='" + dbhost + "' user='" + dbuser +"' password='" + dbpass + "'")
	cur = conn.cursor()
	data = request.get_json()
	cur.execute("DELETE FROM users WHERE userid=%s", (data['user_id']))
	conn.commit()
	cur.close()
	conn.close()
	return 'Done'

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')