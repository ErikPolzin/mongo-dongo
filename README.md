# MongoDongo

Scripts to create, import to, inspect and test a Mongo DB.

## Installation

Follow the instructions to [the install MongoDB shell](https://www.mongodb.com/docs/manual/administration/install-community/).
Then install [pymongo](https://pymongo.readthedocs.io/en/stable/installation.html) with pip.

## Usage

Use the `mongoshlongo` script, for example:

```bash
python3 mongoshlongo.py convert healthcare_dataset.csv data.json
```
Converts the CSV data into structured JSON data for inserting into the db.

```bash
python3 mongoshlongo.py import test_database data.json
```
Imports JSON data into the `test_database` DB.