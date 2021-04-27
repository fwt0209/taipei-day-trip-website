from flask import *
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="taipei_day_trip_website"
  ,auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor(dictionary=True)

app=Flask(__name__)
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
	# values["keyword"]=f"%{keyword}%"
	values["keyword"]=keyword
	selectSQL="SELECT COUNT(1) count FROM attractions "
	# where="WHERE stitle LIKE %(keyword)s "
	where="WHERE cat2=%(keyword)s "
	SQL=selectSQL+where
	mycursor.execute(SQL, values)
	result=mycursor.fetchone()
	return result["count"]

@app.route("/api/attractions" , methods=['GET'])
def apiGetAttractionsByPage():
	output={}
	values={}
	if not request.args.get('page'):
		return

	limit=12
	keyword=request.args.get('keyword')
	total=countData(keyword)
	page=int(request.args.get('page'))
	values["keyword"]=keyword
	# values["keyword"]=f"%{keyword}%"
	values["startIndex"]=(page-1)*limit
	values["endIndex"]=page*limit
	values["items"]=limit

	if values["endIndex"]<total:
		output["next"]={
			"page":page+1,
			"limit":limit
		}

	if values["startIndex"]>0:
		output["previous"]={
			"page":page-1,
			"limit":limit
		}

	selectAllAttractions=("SELECT atrac.*,  atracFile.picturePath "+
	"FROM attractions atrac "+
	"LEFT JOIN attractionFiles atracFile on atracFile.attraction_id=atrac.serial_no ")
	# whereKeyword="WHERE stitle LIKE %(keyword)s "
	whereKeyword="WHERE cat2=%(keyword)s "
	pagination="ORDER BY MRT DESC LIMIT %(startIndex)s, %(items)s "

	SQL=selectAllAttractions + whereKeyword + pagination

	if not values["keyword"]:
		SQL=selectAllAttractions + pagination
		del values["keyword"]
	
	mycursor.execute(SQL, values)
	print(mycursor.statement)
	# mycursor.execute(SQL, {'keyword': '公共藝術', 'startIndex': 12, 'items': 12})
	result=mycursor.fetchall()
	output["data"]=result
	if not output["data"]:
		return json.dumps({
			"error":True,
			"message": "沒有更多資料"
		})
	return json.dumps(output)


@app.route("/api/attractions/<attractionId>" , methods=['GET'])
def apiGetAttractionsByID(attractionId):
	output={}
	SQL=("SELECT atrac.* "+
	"FROM attractions atrac "+
	"LEFT JOIN attractionFiles atracFile on atracFile.attraction_id=atrac.serial_no "+
	"WHERE serial_no=%s")
	values=(attractionId,)
	mycursor.execute(SQL,values)
	result=mycursor.fetchone()
	output["data"]=result
	return output

if __name__=="__main__":
  app.run(host="0.0.0.0", port="3000")
