
# MongoDongo - Assignment 1

Scripts to create, import to, inspect and test a Mongo DB.

By Erik, Richard, Bianca, Ryan and Stuart (aka Data?IBarelyKnowHer :smile:)

***

## File Structure

 - **healthcare_dataset.csv:** original dataset
 - **mongoshlongo.py:** Code to convert dataset into a MongoDB dataset
 - **autoScript.py:** Runs one query for each team member
 - **validators.json:** Some database strucutre rules
 - **CSC4013Z_Assignment1.pdf:** Report containing all assignment questions

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
***
Imports JSON data into the `healthcare_db` DB.

### Running test cases

Use `mongotest.py` to run the automated tests on a given database, like so:
```bash
python3 mongotest.py healthcare_db
```