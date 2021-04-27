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

mycursor = mydb.cursor(dictionary=True)

def getAttractionList(data):  
  attractionsRawSource=data["result"]["results"]
  return mapItems(attractionsRawSource)

def mapItems(data):
  return list(map(mapItemsCondition,data))
 
def mapItemsCondition(data):
  fileList=getFileList(data["file"]) 
  return {
    "info":data["info"],
    "stitle":data["stitle"],
    "longitude":data["longitude"],
    "latitude":data["latitude"],
    "MRT":data["MRT"],
    "serial_no":data["SERIAL_NO"],
    "cat1":data["CAT1"],
    "cat2":data["CAT2"],
    "memo_time":data["MEMO_TIME"],
    "idpt":data["idpt"],
    "xbody":data["xbody"],
    "address":data["address"],
    "file":fileList
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
    insertAttractionFiles(attraction_id, item["file"])



def insertUpdateAttractionData(data):  
  insertSQL=("INSERT INTO attractions "
  "(info, stitle, longitude, MRT, serial_no, cat1, cat2, memo_time, idpt, xbody, latitude, address) "
  "VALUES "
  "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
  updateSQL=("ON DUPLICATE KEY UPDATE "
  "info=%s, "
  "stitle=%s, "
  "longitude=%s, "
  "MRT=%s, "
  "cat1=%s, "
  "cat2=%s, "
  "memo_time=%s, "
  "idpt=%s, "
  "xbody=%s, "
  "latitude=%s, "
  "address=%s, "
  "updatedCounter=updatedCounter+1")
  SQL = insertSQL + updateSQL
  insertValues=(data["info"], data["stitle"], data["longitude"], data["MRT"], data["serial_no"], data["cat1"], data["cat2"], data["memo_time"], data["idpt"], data["xbody"], data["latitude"], data["address"])
  updateValues=(data["info"], data["stitle"], data["longitude"], data["MRT"], data["cat1"], data["cat2"], data["memo_time"], data["idpt"], data["xbody"], data["latitude"], data["address"])
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
  "(attraction_id, picturePath) "
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