import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test_database"]
patients = mydb["patients"]
cases = mydb["cases"]

myquery = {"Name": "/^Chad/",'Blood Type': "/^O/"}

mydoc = patients.find(myquery)

for x in mydoc:
  print(x)