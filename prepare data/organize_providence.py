import os
import shutil
import xml.etree.ElementTree as ET
#from datetime import datetime, timedelta

# Define the target child age ranges in months
min_age_1_2 = 12
max_age_1_2 = 23
min_age_2_4 = 24
max_age_2_4 = 48

# Namespace dictionary
namespaces = {'ns': 'http://phon.ling.mun.ca/ns/phonbank'}

# Function to convert ISO 8601 duration to months
def iso8601_to_months(duration):
    parts = duration.split('P')[1].split('Y')
    years = int(parts[0]) if len(parts) > 1 else 0
    months = int(parts[1].split('M')[0]) if 'M' in parts[1] else 0
    days = int(parts[1].split('M')[1].split('D')[0]) if 'D' in parts[1] else 0
    
    total_months = years * 12 + months
    if days > 15:
        total_months += 1
    
    return total_months

# Move files based on child age
def move_files_by_age(src_folder, dest_folder_1_2, dest_folder_2_4):
    for filename in os.listdir(src_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(src_folder, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find the target child's age
            child_age_element = root.find(".//ns:participant[@id='CHI']/ns:age", namespaces)
            if child_age_element is None:
                print(f"No child age found in file: {filename}")
                continue
            
            age_string = child_age_element.text
            print(f"Child age in file {filename}: {age_string}")
            
            age_in_months = iso8601_to_months(age_string)
            
            # Move the file to the appropriate folder based on age
            if min_age_1_2 <= age_in_months <= max_age_1_2:
                shutil.move(file_path, os.path.join(dest_folder_1_2, filename))
                print(f"Moved {filename} to {dest_folder_1_2}")
            elif min_age_2_4 <= age_in_months <= max_age_2_4:
                shutil.move(file_path, os.path.join(dest_folder_2_4, filename))

# Define source and destination folders
src_folder = "Providence"
dest_folder_1_2 = "Providence_under_2"
dest_folder_2_4 = "Providence_2_4"

# Create destination folders if they don't exist
os.makedirs(dest_folder_1_2, exist_ok=True)
os.makedirs(dest_folder_2_4, exist_ok=True)

# Move files based on child age
move_files_by_age(src_folder, dest_folder_1_2, dest_folder_2_4)
