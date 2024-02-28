import argparse
import csv
import json

from pymongo import MongoClient

SCHEMA: dict[str, tuple[str, ...]] = {
    "Patient": ("Name", "Age", "Gender", "Blood Type"),
    "Case": (
        "Medical Condition", "Date of Admission", "Doctor",
        "Hospital", "Room Number", "Admission Type",
        "Discharge Date", "Medication", "Test Results"),
    "Billing": ("Insurance Provider", "Billing Amount")
}


def import_data(db_name: str, json_path: str, collection_name: str = "patient") -> None:
    """Import data from JSON and store it in MongoDongo."""
    client = MongoClient()
    db = client[db_name]
    with open(json_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
        print(f"Inserting {len(data)} elements...")
        db[collection_name].drop()
        db[collection_name].insert_many(data)
        print(f"Done, {db[collection_name].count_documents({})} elements in {db_name}")


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