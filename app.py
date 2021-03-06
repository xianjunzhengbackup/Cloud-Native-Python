from flask import Flask,jsonify,request,abort
import sqlite3
from time import gmtime,strftime
     
app = Flask(__name__)      

"""
curl http://localhost:5000/api/v2/tweets -v
run above command to send GET request 
"""
@app.route('/api/v2/tweets',methods=['GET'])
def get_tweets():
	return list_tweets()
def list_tweets():
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	tweet_list=[]
	cursor=conn.execute("SELECT username,body,tweet_time,id from tweets")
	for row in cursor:
		a_dict={}
		a_dict['username']=row[0]
		a_dict['body']=row[1]
		a_dict['tweet_time']=row[2]
		a_dict['id']=row[3]
		tweet_list.append(a_dict)
	conn.close()
	return jsonify({'tweets_list':tweet_list})

"""
$ for x in $(seq 14 20)
> do 
> curl -i -H "Content-Type: application/json" -X POST -d '{"username":"jun'$x'","body":"xxxx"}' http://localhost:5000/api/v2/tweets
> sleep 1
> done

run above command , could automatically add multiple tweets
-d '{"username":"jun'$x'".....exits for a reason
"""
@app.route('/api/v2/tweets',methods=['POST'])
def add_tweets():
	print("-------------------------------")
	print(request.json)
	print("-------------------------------")
	if not request.json or not 'username' in request.json or not 'body' in request.json:
		abort(400)
	tweet={'username':request.json['username'],'body':request.json['body'],'created_at':strftime("%Y-%m-%dT%H:%M:%SZ",gmtime())}
	return jsonify({'status':add_tweet(tweet)}),200

def add_tweet(tweet):
	conn=sqlite3.connect("mydb.db")
	print("Open database successfully")
	tweet_list=[]
	cursor=conn.cursor()
	cursor.execute("SELECT * from tweets where username=?",(tweet['username'],))
	data=cursor.fetchall()
	if len(data) != 0:
		abort(409)
	else:
		cursor.execute("insert into tweets (username,body,tweet_time) values(?,?,?)",(tweet['username'],tweet['body'],tweet['created_at']))
		conn.commit()
		return "Success"

"""
curl -i -H "Content-Type:application/json" http://localhost:5000/api/v2/1
"""
@app.route('/api/v2/tweets/<int:user_id>',methods=['GET'])
def get_tweet(user_id):
	return list_tweet(user_id)

def list_tweet(user_id):
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	tweet_list=[]
	cursor=conn.cursor()
	cursor.execute("SELECT * from tweets where id=?",(user_id,))
	data=cursor.fetchall()
	if len(data) != 0:
		tweet={}
		tweet['username']=data[0][0]
		tweet['body']=data[0][1]
		tweet['tweet_time']=data[0][3]
		tweet['id']=data[0][2]
	conn.close()
	return(jsonify(tweet),200)
		
"""
curl -i -H "Content-Type: application/json" http://localhost:5000/api/v1/users

The above command could send GET command to server
"""
@app.route('/api/v1/users',methods=['GET'])
def get_users():
	return list_users()

def list_users():
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	api_list=[]
	cursor=conn.execute("SELECT username,name,email,password,id from users")
	for row in cursor:
		a_dict={}
		a_dict['username']=row[0]
		a_dict['name']=row[1]
		a_dict['email']=row[2]
		a_dict['password']=row[3]
		a_dict['id']=row[4]
		api_list.append(a_dict)

	conn.close()
	return jsonify({'user_list':api_list})	

"""
curl http://localhost:5000/api/v1/users/2
"""
@app.route('/api/v1/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
	return list_user(user_id)

def list_user(user_id):
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	api_list=[]
	cursor=conn.cursor()
	cursor.execute("SELECT * from users where id=?",(user_id,))
	data=cursor.fetchall()
	if len(data) != 0:
		user={}
		user['username']=data[0][0]
		user['name']=data[0][1]
		user['email']=data[0][2]
		user['password']=data[0][3]
		user['id']=data[0][4]
	conn.close()
	return jsonify(user)
"""
curl -i -H "Content-Type: application/json"-X POST -d '{"username":"jun11","email":"jun11@email","password":"111","name":"jun111"}' http://localhost:5000/api/v1/users

The above command could post data to the server
"""
@app.route('/api/v1/users',methods=['POST'])
def create_user():
	if not request.json or not 'username' in request.json\
or not 'email' in request.json or not 'password' in request.json:
		abort(400)
	user={'username':request.json['username'],\
'email':request.json['email'],\
'name':request.json['name'],\
'password':request.json['password']}
	return jsonify({'status':add_user(user)}),201

def add_user(new_user):
	conn=sqlite3.connect("mydb.db")
	print("Open database successfully");
	api_list=[]
	cursor=conn.cursor()
	cursor.execute("SELECT * from users where username=? or email=?",(new_user['username'],new_user['email']))
	data=cursor.fetchall()
	if len(data) != 0:
		abort(409)
	else:
		cursor.execute("insert into users (username,email,password,name) values(?,?,?,?)",(new_user['username'],new_user['email'],new_user['password'],new_user['name']))
		conn.commit()
		return "Success"
	conn.close()
	return jsonify(a_dict)

"""
curl -i -H "Content-Type: application/json" -X delete -d '{"username":"jun1"}' http://localhost:5000/api/v1/users
Use the above command to delete user
"""
@app.route('/api/v1/users',methods=['DELETE'])
def delete_user():
	if not request.json or not 'username' in request.json:
		abort(400)
	user=request.json['username']
	return jsonify({'status':del_user(user)}),200

def del_user(del_user):
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	cursor=conn.cursor()
	cursor.execute("SELECT * from users where username=?",(del_user,))
	data=cursor.fetchall()
	print("Data",data)
	if len(data) == 0:
		abort(404)
	else:
		cursor.execute("delete from users where username==?",(del_user,))
		conn.commit()
		return "Success"
	conn.close()

"""
curl -i -H "Content-Type: application/json" -X put -d '{"password":"2222"}' http://localhost:5000/api/v1/users/4
run above command to modify password for userid==4
"""
@app.route('/api/v1/users/<int:user_id>',methods=['PUT'])
def update_users(user_id):
	user={}
	if not request.json:
		abort(400)
	user['id']=user_id
	key_list=request.json.keys()
	for i in key_list:
		user[i]=request.json[i]
	print(user)
	return jsonify({'status':update_user(user)}),200

def update_user(user):
	conn=sqlite3.connect('mydb.db')
	print("Opened database successfully")
	cursor=conn.cursor()
	cursor.execute("SELECT * from users where id=? ",(user['id'],))
	data=cursor.fetchall()
	if len(data) == 0:
		abort(404)
	else:
		key_list=user.keys()
		for i in key_list:
			if i != "id":
				print(user,i)
				cursor.execute("""UPDATE users SET {0} = ? WHERE id=?""".format(i),(user[i],user['id']))
				conn.commit()
		return("Successfully")

if __name__ == "__main__":      
	app.run(host='0.0.0.0', port=5000, debug=True) 
