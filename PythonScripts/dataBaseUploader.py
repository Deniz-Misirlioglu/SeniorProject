import pymongo
from pymongo import MongoClient
from datetime import datetime
import csv

# Connect to MongoDB
cluster = MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@hideandseekdata.nkcn2sb.mongodb.net/?retryWrites=true&w=majority')
db = cluster['HAS-Data']
collection = db['HAS-Garland']

# Path to your CSV file

hiderCSV = "test\hider2.csv"
seekerCSV = "test\seeker2.csv"


seeker_score = 0;
hider_score = 0;

x_hider_values = [];
y_hider_values = [];
z_hider_values = [];

x_seeker_values = [];
y_seeker_values = [];
z_seeker_values = [];

# Read data from CSV for the hider and insert into MongoDB
with open(hiderCSV, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    first_row = next(csv_reader, None)
    x_hider_values.append(first_row[0])
    y_hider_values.append(first_row[1])
    z_hider_values.append(first_row[2])
    hider_score = float(first_row[3])

    for row in csv_reader:
        if len(row) >= 4:
            row.pop(3)
        x, y, z = map(float, row)
        x_hider_values.append(x)
        y_hider_values.append(y)
        z_hider_values.append(z)


# Read data from CSV for the hider and insert into MongoDB
with open(seekerCSV, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    first_row = next(csv_reader, None)
    x_seeker_values.append(first_row[0])
    y_seeker_values.append(first_row[1])
    z_seeker_values.append(first_row[2])
    seeker_score = float(first_row[3])

    for row in csv_reader:
        if len(row) >= 4:
            row.pop(3)
        x, y, z = map(float, row)
        x_seeker_values.append(x)
        y_seeker_values.append(y)
        z_seeker_values.append(z)



current_datetime = datetime.now()

document = { 
            'Date': current_datetime,
            'Hider': hider_score,
            'Seeker': seeker_score,
            'xHider': x_hider_values,
            'yHider': y_hider_values,
            'zHider': z_hider_values,
            'xSeeker': x_seeker_values,
            'ySeeker': y_seeker_values,
            'zSeeker': z_seeker_values,
        }

print(document);
collection.insert_one(document)


print("Data inserted successfully.")
