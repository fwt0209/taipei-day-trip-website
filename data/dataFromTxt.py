import urllib.request as request
import json

def getAttractionList(data):  
  attractionsRawSource=data["result"]["results"]
  return mapItems(attractionsRawSource)

def mapItems(data):
  return list(map(mapItemsCondition,data))
 
def mapItemsCondition(data):
  fileList=getFileList(data["file"]) 
  return {
    "stitle":data["stitle"],
    "longitude":data["longitude"],
    "latitude":data["latitude"],
    "file":fileList
    }

def keepJpgPng(data):
  for index, value in enumerate(data):
    if (
    ".JPG" not in data[index] and 
    ".jpg" not in data[index] and 
    ".PNG" not in data[index] and 
    ".png" not in data[index]):
      del data[index]
  return(data)

def addUrlHeader(data):
  for index, value in enumerate(data):
    data[index]="http://{}".format(value)
  return data

def getFileList(data):
  fileList=data.split("http://")
  del(fileList[0])
  keepPictures=keepJpgPng(fileList)
  fileList=addUrlHeader(fileList)
  return fileList



with open("./taipei-attractions.json", mode="r", encoding="utf-8") as file:
  data=json.load(file)
  attractionList=getAttractionList(data)