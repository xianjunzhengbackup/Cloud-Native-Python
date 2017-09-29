from flask import Flask ,jsonify
import sqlite3
     
app = Flask(__name__)      

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

if __name__ == "__main__":      
	app.run(host='0.0.0.0', port=5000, debug=True) 
