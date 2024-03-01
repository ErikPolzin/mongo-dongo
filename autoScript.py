from pymongo import MongoClient
from datetime import datetime

"""
    This script automatically runs one query for every teamamte in the team
"""


# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['healthcare_db'] 
collection = db['cases']  

# Stuart
print("Patients sorted by Name:")
patients_sorted = db.patients.find().sort("Name", 1)
for patient in patients_sorted:
    print(patient)

# Erik
print("\nMost common medical condition:")
most_common_condition = db.cases.aggregate([
    { "$group": { "_id": "$Medical Condition", "count": { "$sum": 1 } } },
    { "$sort": {"count": -1} },
    { "$limit": 1 }
])
for condition in most_common_condition:
    print(condition)

# Ryan
print("\nDeleting Tiffany Ramirez:")
result = db.patients.delete_one({"Name": "Tiffany Ramirez"})
print("Deleted count:", result.deleted_count)

# Richard
result = [
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
]

results = collection.aggregate(result)

# Printing the results
for document in results:
    print(document)


# Bianca
print("Find the ealiest addmitted case:")
first_patient = db.cases.find().sort({"Date of Admission":1}).limit(1)
for patient in first_patient:
    print(patient)