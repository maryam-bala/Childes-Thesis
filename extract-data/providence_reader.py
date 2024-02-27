import os
import pandas as pd
import xml.etree.ElementTree as ET
import re

# Function to extract participant information
def extract_participants(root, dialogue_id):
    participants = []
    for participant in root.findall('.//pb:participant', ns):
        speaker_id = participant.attrib.get('id')
        speaker_name_elem = participant.find('pb:name', ns)
        speaker_name = speaker_name_elem.text if speaker_name_elem is not None else None
        role_elem = participant.find('pb:role', ns)
        role = role_elem.text if role_elem is not None else None
        age_elem = participant.find('pb:age', ns)
        age = age_elem.text if age_elem is not None else None
        sex_elem = participant.find('pb:sex', ns)
        sex = sex_elem.text if sex_elem is not None else None
        
        participant_data = {
            'dialogue_id': dialogue_id,
            'speaker_id': speaker_id,
            'speaker_name': speaker_name,
            'role': role,
            'age': age,
            'sex': sex
        }
        participants.append(participant_data)
    return participants

# Function to extract utterance information
def extract_utterances(root, dialogue_id):
    utterances = []
    excluded_words = ['xxx', 'yyy', 'www']

    uID = 0 # Initialize uID for counting utterances 
    for utterance in root.findall('.//pb:u', ns):
        orthography_elements = utterance.findall('.//pb:orthography/pb:g', ns)
        morphology_elements = utterance.findall('.//pb:groupTier[@tierName="Morphology"]/pb:tg', ns)
        gra_elements = utterance.findall('.//pb:groupTier[@tierName="GRASP"]/pb:tg', ns)

        utterance_text = ''
        utterance_length = 0
        mor_text = ''
        gra_text = ''

        for element in orthography_elements:
            word_text = ' '.join([w.text.strip() for w in element.findall('pb:w', ns) if w.text])
            punctuation = element.find('pb:p', ns)
            if punctuation is not None:
                word_text += f" {punctuation.text} "
            utterance_text += word_text + ' '

            # Count words for this utterance if not in excluded words
            if not any(excluded_word in word_text for excluded_word in excluded_words):
                utterance_length += len(re.findall(r'\b\w+\b', word_text))

        utterance_text = utterance_text.strip()

        for mor_element in morphology_elements:
            mor_words = []
            for w in mor_element.findall('pb:w', ns):
                if '(' not in w.text and ')' not in w.text:
                    mor_words.append(w.text)

            mor_text += ' '.join(mor_words) + ' '
        
        mor_text = mor_text.strip()

        for gra_element in gra_elements:
            gra_words = [w.text for w in gra_element.findall('pb:w', ns) if w.text]
            gra_text += ' '.join(gra_words) + ' '

        gra_text = gra_text.strip()

        utterance_data = {
            'dialogue_id': dialogue_id, 
            'uID' : uID,
            'speaker': utterance.attrib.get('speaker'),
            'utterance': utterance_text,
            'utterance_length': utterance_length,
            '%mor': mor_text,
            '%gra' :gra_text,
            
        }
        utterances.append(utterance_data)

        uID += 1 # Increment uID for the next utterance
    return utterances

# Create DataFrames
participants_data_under_2 = []
utterances_data_under_2 = []
participants_data_2_4 = []
utterances_data_2_4 = []

# Define the namespaces
ns = {'pb': 'http://phon.ling.mun.ca/ns/phonbank'}

# Define the input and output directories
input_dir = 'Providence'
output_dir = 'processed_Providence'

# Iterate through folders inside the input directory
for folder_name in ['Providence_under_2', 'Providence_2_4']:
    folder_path = os.path.join(input_dir, folder_name)
    
    # Iterate through XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)

            # Load the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract dialogue_id
            dialogue_id = f"{folder_name}/{os.path.splitext(filename)[0]}.xml"

            # Extract participant and utterance information
            if folder_name == 'Providence_under_2':
                participants_data_under_2.extend(extract_participants(root, dialogue_id))
                utterances_data_under_2.extend(extract_utterances(root, dialogue_id))
            elif folder_name == 'Providence_2_4':
                participants_data_2_4.extend(extract_participants(root, dialogue_id))
                utterances_data_2_4.extend(extract_utterances(root, dialogue_id))

# Create DataFrames for under 2 age group
participants_df_under_2 = pd.DataFrame(participants_data_under_2)
utterances_df_under_2 = pd.DataFrame(utterances_data_under_2)

# Create DataFrames for 2 to 4 age group
participants_df_2_4 = pd.DataFrame(participants_data_2_4)
utterances_df_2_4 = pd.DataFrame(utterances_data_2_4)

# Left join on dialogue_id and speaker for each age group
merged_df_under_2 = utterances_df_under_2.merge(participants_df_under_2,
                                     left_on=['dialogue_id', 'speaker'],
                                     right_on=['dialogue_id', 'speaker_id'],
                                     how='left')

merged_df_2_4 = utterances_df_2_4.merge(participants_df_2_4,
                                     left_on=['dialogue_id', 'speaker'],
                                     right_on=['dialogue_id', 'speaker_id'],
                                     how='left')


# Save only the merged dataframes
merged_df_under_2.to_csv(os.path.join(output_dir, 'Providence_under_2.csv'), index=False)
merged_df_2_4.to_csv(os.path.join(output_dir, 'Providence_2_4.csv'), index=False)
