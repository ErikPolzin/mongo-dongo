"""This script automatically runs one query for every teamamte in the team."""
from pprint import pprint
import sys

from pymongo import MongoClient

if len(sys.argv) < 2:
    raise ValueError("Must specify a database name to run test cases")

# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client[sys.argv[1]]

# Stuart
print("Stuart: Patients sorted by Name:")
print("--------------------------------")
res1 = db.patients.find().sort("Name", 1)
pprint(list(res1)[:3])  # First 3
print("...")

# Erik
print("===============================================")
print("Erik: Find the hospital with the most patients:")
print("-----------------------------------------------")
res2 = db.cases.aggregate([
    {"$group": {"_id": "$Hospital", "count": {"$count": {}}}},
    {"$sort": {"count":-1}},
    {"$limit": 1}])
print(list(res2))

# Ryan
print("===============================")
print("Ryan: Deleting Tiffany Ramirez:")
print("-------------------------------")
res3 = db.patients.delete_one({"Name": "Tiffany Ramirez"})
print("Deleted count:", res3.deleted_count)

# Richard
print("============================")
print("Richard: Add Duration column")
print("----------------------------")
res4 = db.cases.aggregate([
    {
        "$project": {
            'Medical Condition': 1,
            'Doctor': 1,
            'Hospital': 1,
            'Room Number': 1,
            'Admission Type': 1,
            'Medication': 1,
            'Test Results': 1,
            'Billing.Insurance Provider': 1,
            'Billing.Billing Amount': 1,
            'PatientId': 1,
            'Duration': {
                "$divide": [
                    {"$subtract": ["$Discharge Date", "$Date of Admission"]}, 
                    86400000  # Number of milliseconds in a day
                ]
            }
        }
    }
])
pprint(list(res4)[:2])
print("...")


# Bianca
print("=======================================")
print("Bianca: Find the ealiest admitted case:")
print("---------------------------------------")
res5 = db.cases.find().sort({"Date of Admission":1}).limit(1)
pprint(list(res5))
