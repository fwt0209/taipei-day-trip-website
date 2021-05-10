from flask import *
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="fwt",
  password="12345678",
  database="taipei_day_trip_website"
#   ,auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor(dictionary=True, buffered=True)

app=Flask(__name__, static_folder="public", static_url_path="/")
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
		pagination="ORDER BY MRT DESC LIMIT %(startIndex)s, %(items)s "

		SQL = selectAllAttractions + whereKeyword + pagination
		
		if not keyword:
			SQL=selectAllAttractions + pagination
			del values["keyword"]


		mycursor.execute(SQL, values)
		result=mycursor.fetchall()
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


if __name__=="__main__":
  app.run(host="0.0.0.0", port="3000")
