from pymongo import MongoClient
from datetime import datetime

# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['healthcare_db'] 
collection = db['cases']  


pipeline = [
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

results = collection.aggregate(pipeline)

# Printing the results
for document in results:
    print(document)
