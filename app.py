from flask import *
import mysql.connector
from datetime import timedelta
import bcrypt
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="fwt",
  password="12345678",
  database="taipei_day_trip_website"
  ,auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor(dictionary=True, buffered=True)

app=Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key = os.urandom(128).hex()
app.permanent_session_lifetime = timedelta(days=2)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


def countData(keyword):
	values={}
	values["keyword"]=f"%{keyword}%"
	selectSQL="SELECT COUNT(1) count FROM attractions "
	where="WHERE name LIKE %(keyword)s "
	SQL=selectSQL+where
	if not keyword:
		SQL=selectSQL
	mycursor.execute(SQL, values)
	result=mycursor.fetchone()
	return result["count"]

@app.route("/api/attractions" , methods=['GET'])
def apiGetAttractionsByPage():
	try:
		output={}
		values={}

		limit=12
		page=request.args.get('page')
		keyword=request.args.get('keyword')

		if not page:
			page=1
		try:
			page=int(page)
		except ValueError:
			page=1

		values["keyword"]=f"%{keyword}%"
		values["startIndex"]=(page-1)*limit
		values["endIndex"]=page*limit
		values["items"]=limit

		selectAllAttractions=("SELECT * FROM attractions ")
		whereKeyword="WHERE name LIKE %(keyword)s "
		pagination="ORDER BY name DESC LIMIT %(startIndex)s, %(items)s "

		SQL = selectAllAttractions + whereKeyword + pagination
		
		if not keyword:
			SQL=selectAllAttractions + pagination
			del values["keyword"]


		mycursor.execute(SQL, values)
		result=mycursor.fetchall()
		print(mycursor.statement)
		if not result:
			return json.dumps({
				"error":True,
				"message": "沒有更多資料"
			})

		output["data"]=result

		total=countData(keyword)
		if values["endIndex"]<total:
			output["nextPage"]={
				"page":page+1,
				"limit":limit
			}

		if values["startIndex"]>0:
			output["previousPage"]={
				"page":page-1,
				"limit":limit
			}

		return json.dumps(output)
	except:
		return json.dumps({
				"error":True,
				"message": "伺服器內部錯誤"
		})



@app.route("/api/attraction/<attractionId>" , methods=['GET'])
def apiGetAttractionsByID(attractionId):
	try:
		output={}
		values={}
		SQL=("SELECT * FROM attractions WHERE attraction_id=%(attractionId)s")
		values["attractionId"]=attractionId
		mycursor.execute(SQL,values)
		result=mycursor.fetchone()
		if not result:
			return json.dumps({
				"error":True,
				"message": "沒有更多資料"
			})

		output["data"]=result
		return json.dumps(output)
	except:
		return json.dumps({
		"error":True,
		"message": "伺服器內部錯誤"
		})


@app.route("/api/user" , methods=["GET"])
def apiGetUser():
	print(request.cookies)
	print(session)
	output={}
	
	if 'email' in session:
		userInfo={}
		userInfo["id"]=session["id"]
		userInfo["name"]=session["name"]
		userInfo["email"]=session["email"]

		output["data"]=userInfo
		return json.dumps(output)
	output["data"]="null"
	return json.dumps(output)

@app.route("/api/user" , methods=["POST"])
def apiSignUp():
	output={}
	values={}
	output["ok"]=False
	output["msg"]="帳號已被註冊"
	data=request.json
	try:
		if data['email']=="" or data['password']=="" or data['name']=="":
			output["msg"]="資料輸入不完整，請再輸入一次"
			return json.dumps(output)
		
		password=data['password']
		values["email"]=data['email']
		values["name"]=data['name']
		sql="SELECT * FROM user WHERE email=%(email)s"
		mycursor.execute(sql,values)
		result=mycursor.fetchone()

		if result:
			return json.dumps(output)

		hashedPassword = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))
		sql="INSERT INTO user (name, email, password) VALUES (%(name)s, %(email)s, %(hashedPassword)s)"
		values["hashedPassword"]=hashedPassword
		mycursor.execute(sql,values)
		mydb.commit()

		output["ok"]=True
		output["msg"]="註冊成功"
		return json.dumps(output)
	except:
		output["msg"]="伺服器內部發生錯誤"
		return json.dumps(output)

@app.route('/api/user', methods=['PATCH'])
def apiLogin():
	output={}
	values={}
	output["ok"]=False
	output["msg"]="帳號或密碼輸入錯誤"
	data=request.json
	try:
		if data['email']=="" or data['password']=="":
			output["msg"]="資料輸入不完整，請再輸入一次"
			return json.dumps(output)

		values["email"]=data['email']
		password=data['password']
		sql="SELECT * FROM user WHERE email=%(email)s"
		mycursor.execute(sql,values)
		result=mycursor.fetchone()
		if not result:
			return json.dumps(output)
		if bcrypt.checkpw(password.encode("utf-8"), result["password"].encode("utf-8")):
			session['id'] = result["id"]
			session['name'] = result["name"]
			session['email'] = values["email"]
			output["ok"]=True
			output["msg"]="登入成功"
			return json.dumps(output)
		return json.dumps(output)
	except:
		output["msg"]="伺服器內部發生錯誤"
		return json.dumps(output)

@app.route('/api/user', methods=['DELETE'])
def apiLogout():
	output={}
	session.pop('id', None)
	session.pop('name', None)
	session.pop('email', None)
	output["ok"]=True
	return json.dumps(output)

if __name__=="__main__":
  app.run(host="0.0.0.0", port="3000")
