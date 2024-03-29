import argparse
import csv
from datetime import datetime
import json
import sys

from pymongo import MongoClient


SCHEMA: dict[str, tuple[str, ...]] = {
    "Patient": ("Name", "Age", "Gender", "Blood Type"),
    "Case": (
        "Medical Condition", "Date of Admission", "Doctor",
        "Hospital", "Room Number", "Admission Type",
        "Discharge Date", "Medication", "Test Results"),
    "Billing": ("Insurance Provider", "Billing Amount")
}
with open("data/validators.json", encoding="utf-8") as vals_file:
    VALIDATORS = json.load(vals_file)


def _coerce_types(data: dict, validator: dict) -> dict:
    """Coerce JSON string types to db field types, as specified by the validator."""
    props = validator["$jsonSchema"]["properties"]
    for (k, v) in data.items():
        if k in props:
            t = props[k]["bsonType"]
            if t == "int":
                data[k] = int(v)
            elif t == "date":
                data[k] = datetime.strptime(v, '%Y-%m-%d')
    return data


def import_data(db_name: str, json_path: str) -> None:
    """Import data from JSON and store it in MongoDongo."""
    client = MongoClient()
    db = client[db_name]
    # Create collections
    db.create_collection("patients")
    db.create_collection("cases")
    # Create validators on collections, as specified in validators.json
    db.command("collMod", "patients", validator=VALIDATORS["patients"])
    db.command("collMod", "cases", validator=VALIDATORS["cases"])
    # Transfer data from input JSON file to mongodb
    with open(json_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
        print(f"Inserting {len(data)} elements...")
        for pdata in data:
            # Make sure fields have the correct type before inserting
            pdata = _coerce_types(pdata, VALIDATORS["patients"])
            cases = [_coerce_types(c, VALIDATORS["cases"]) for c in pdata.pop("Cases")]
            result = db.patients.insert_one(pdata)
            for c in cases:
                c["PatientId"] = result.inserted_id
            db.cases.insert_many(cases)
        print("Done")


def convert_data(input_csv: str, output_json: str) -> None:
    """Convert data from CSV to structured json."""
    print("Reading CSV data...")
    with open(input_csv, encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        output_data = []
        for r in reader:
            patient_data = {k: r[k] for k in SCHEMA["Patient"]}
            case_data = {k: r[k] for k in SCHEMA["Case"]}
            billing_data = {k: r[k] for k in SCHEMA["Billing"]}
            case_data["Billing"] = billing_data
            patient_data["Cases"] = [case_data]
            output_data.append(patient_data)
        print(f"Read {len(output_data)} lines from CSV")
    print("Writing output to JSON")
    with open(output_json, "w+", encoding="utf-8") as output_file:
        json.dump(output_data, output_file, indent=4)
    print("Done")


if __name__ == "__main__":
    print(sys.executable)
    parser = argparse.ArgumentParser(description='Shell commands for BigData assignment.')
    subparsers = parser.add_subparsers()
    convert_parser = subparsers.add_parser('convert')
    convert_parser.add_argument("input_csv")
    convert_parser.add_argument("output_json")
    convert_parser.set_defaults(func=convert_data)
    import_parser = subparsers.add_parser('import')
    import_parser.add_argument("db_name")
    import_parser.add_argument("json_path")
    import_parser.set_defaults(func=import_data)

    args = parser.parse_args()
    args.func(**{k: v for (k, v) in vars(args).items() if k != "func"})
