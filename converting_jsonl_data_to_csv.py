import json
import csv


# Define the JSONL file path and the output CSV file path
jsonl_file_path = r'C:\Users\alias\Comp 6480 Natural Language Processing\Project\Project code\Project Data\data.jsonl'
csv_file_path = r'C:\Users\alias\Comp 6480 Natural Language Processing\Project\Project code\Project Data\data.csv'


# Read the JSONL file and convert each line to a dictionary
data = []
with open(jsonl_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        data.append(json.loads(line))
        
        
# Assuming all dictionaries have the same structure, get the headers from the first element
headers = data[0].keys()


# Write the data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for d in data:
        writer.writerow(d)