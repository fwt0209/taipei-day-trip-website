import urllib.request as request
import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="taipei_day_trip_website",
  charset='utf8',
  auth_plugin="mysql_native_password"
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
    "serial_no":data["SERIAL_NO"],
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
    attraction_id = item["serial_no"]
    insertUpdateAttractionData(item)
    deleteAttractionFiles(attraction_id)
    insertAttractionFiles(attraction_id, item["images"])


def insertUpdateAttractionData(data):  
  insertSQL=("INSERT INTO attractions "
  "(serial_no, name, category, description, address, transport, mrt, latitude, longitude) "
  "VALUES "
  "(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
  updateSQL=("ON DUPLICATE KEY UPDATE "
  "name=%s, "
  "category=%s, "
  "description=%s, "
  "address=%s, "
  "transport=%s, "
  "mrt=%s, "
  "latitude=%s, "
  "longitude=%s ")
  SQL = insertSQL + updateSQL
  insertValues=(data["serial_no"],data["name"], data["category"], data["description"], data["address"], data["transport"], data["mrt"], data["latitude"], data["longitude"])
  updateValues=(data["name"], data["category"], data["description"], data["address"], data["transport"], data["mrt"], data["latitude"], data["longitude"])
  values = insertValues + updateValues

  mycursor.execute(SQL, values)
  mydb.commit()

def deleteAttractionFiles(attractionId):
  deleteSQL=("DELETE FROM attractionFiles "
  "WHERE attraction_id=%s")
  deleteValues=(attractionId,)
  mycursor.execute(deleteSQL, deleteValues)
  mydb.commit()

def insertAttractionFiles(attractionId, files):
  insertSQL=("INSERT INTO attractionFiles "
  "(attraction_id, path) "
  "VALUES "
  "(%s, %s)")
  for item in files:
    insertValue=(attractionId, item)
    mycursor.execute(insertSQL,insertValue)
    mydb.commit()


with open("./taipei-attractions.json", mode="r", encoding="utf-8") as file:
  data=json.load(file)
  attractionList=getAttractionList(data)
  attractionsToDatabase(attractionList)