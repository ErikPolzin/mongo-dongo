
# MongoDongo

Scripts to create, import to, inspect and test a Mongo DB.

## Installation

Follow the instructions to [the install MongoDB shell](https://www.mongodb.com/docs/manual/administration/install-community/).
Then install [pymongo](https://pymongo.readthedocs.io/en/stable/installation.html) with pip.

## Usage

Use the `mongoshlongo` script, for example:

```bash
python3 mongoshlongo.py convert data/healthcare_dataset.csv data.json
```
Converts the CSV data into structured JSON data for inserting into the db.

```bash
python3 mongoshlongo.py import healthcare_db data.json
```
Imports JSON data into the `test_database` DB.

### Running test cases

Use `mongotest.py` to run the automated tests on a given database, like so:
```bash
python3 mongotest.py test_database
```