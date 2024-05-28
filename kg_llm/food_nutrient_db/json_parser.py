# import os
# import csv
# import json


# cwd = os.getcwd()
# filename = 'HealthEffect.csv'
# file_path = os.path.join(cwd, filename)


# def csv_to_json(csv_file_path, json_file_path):
#     # Open the CSV file and read its contents
#     with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
#         # Assuming the CSV file has headers, we'll use them as keys for the JSON objects
#         reader = csv.DictReader(csv_file)
        
#         # Convert each row to a JSON object and store them in a list
#         json_data = [row for row in reader]
    
#     # Write the JSON data to a file
#     with open(json_file_path, 'w', encoding='utf-8') as json_file:
#         # Use the json.dump() function to write the JSON data to the file
#         json.dump(json_data, json_file, indent=4)


# csv_to_json(file_path, 'health_effects.json')
