import urllib.request as request
import json
import mysql.connector
import copy

mydb = mysql.connector.connect(
  host="localhost",
  user="fwt",
  password="12345678",
  database="taipei_day_trip_website",
  charset='utf8'
  # auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor(dictionary=True, buffered=True)

def getAttractionList(data):  
  attractionsRawSource=data["result"]["results"]
  return mapItems(attractionsRawSource)

def mapItems(data):
  return list(map(mapItemsCondition,data))
 
def mapItemsCondition(data):
  fileList=getFileList(data["file"]) 
  return {
    "attraction_id":data["SERIAL_NO"],
    "name":data["stitle"],
    "category":data["CAT2"],
    "description":data["xbody"],
    "address":data["address"],
    "transport":data["info"],
    "mrt":data["MRT"],
    "latitude":data["latitude"],
    "longitude":data["longitude"],
    "images":fileList
    }

def keepJpgPng(data):
  for index, value in enumerate(data):
    if (
    ".JPG" not in value and 
    ".jpg" not in value and 
    ".PNG" not in value and 
    ".png" not in value):
      del data[index]
  return(data)

def addUrlHeader(data):
  for index, value in enumerate(data):
    data[index]=f"http://{value}"
  return data

def getFileList(data):
  fileList=data.split("http://")
  del(fileList[0])
  keepPictures=keepJpgPng(fileList)
  fileList=addUrlHeader(fileList)
  return fileList


def attractionsToDatabase(data):
  for item in data:
    attraction_id = item["attraction_id"]
    insertUpdateAttractionData(item)


def insertUpdateAttractionData(data):  
  insertSQL=("INSERT INTO attractions "
  "(attraction_id, name, category, description, address, transport, mrt, latitude, longitude, images) "
  "VALUES "
  "(%(attraction_id)s, %(name)s, %(category)s, %(description)s, %(address)s, %(transport)s, %(mrt)s, %(latitude)s, %(longitude)s, %(images)s)")
  updateSQL=("ON DUPLICATE KEY UPDATE "
  "name=%(name)s, "
  "category=%(category)s, "
  "description=%(description)s, "
  "address=%(address)s, "
  "transport=%(transport)s, "
  "mrt=%(mrt)s, "
  "latitude=%(latitude)s, "
  "longitude=%(longitude)s, "
  "images=%(images)s ")
  SQL = insertSQL + updateSQL
  values={}
  values["attraction_id"]=data["attraction_id"]
  values["name"]=data["name"]
  values["category"]=data["category"]
  values["description"]=data["description"]
  values["address"]=data["address"]
  values["transport"]=data["transport"]
  values["mrt"]=data["mrt"]
  values["latitude"]=data["latitude"]
  values["longitude"]=data["longitude"]
  values["images"]=json.dumps(data["images"])

  mycursor.execute(SQL, values)
  mydb.commit()



with open("./taipei-attractions.json", mode="r", encoding="utf-8") as file:
  data=json.load(file)
  attractionList=getAttractionList(data)
  attractionsToDatabase(attractionList)