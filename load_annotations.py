# Import relevant libraries 
import os
import re
import pandas as pd
import numpy as np

# Define a function to parse a line of text from the file
def parse_line(line):
    if line.startswith('*'):
        return {'speaker': line[1:4], 'utterance': line[5:].strip()}
    elif line.startswith('%'):
        return {line[:4]: line[5:]}
    else:
        return {}
    
# Initialize an empty list to store parsed data
data = []

# Path to the folder containing the txt files
folder_path = 'annotated_data'

# Walk through the directory tree
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path) as f:
                dialogue_id = os.path.basename(file_path)
                utt_id = 0
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parsed = parse_line(line)
                    if 'speaker' in parsed:
                        data.append({
                            'dialogue_id': dialogue_id,
                            'utt_id': utt_id,
                            'speaker': parsed.get('speaker'),
                            'utterance': parsed.get('utterance'),
                            '%mor': '',
                            '%gra': '',
                            '%adu': '',
                            '%cof': ''
                        })
                        utt_id = (utt_id + 1) % 2 
                    else:
                        key = list(parsed.keys())[0]
                        data[-1][key] = parsed[key]

# Create a DataFrame from the parsed data
df = pd.DataFrame(data)

# Iterate over each column in the DataFrame
for col in df.columns:
    if df[col].dtype == "object": 
        df[col] = df[col].str.lstrip()  # Remove whitespace from each element in the column using str.lstrip() method
        
# Replace empty strings and whitespace with NaN
df.replace({'': np.nan, ' ': np.nan}, inplace=True)

# Save dataframe to csv
df.to_csv('out1.csv', index=False)
