from flask import Flask,render_template,request,jsonify,redirect,session
from flask import abort
import sqlite3

app=Flask(__name__)

@app.route('/adduser')
def adduser():
	return render_template("adduser.html")

if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)
