import os
import pandas as pd
from lxml import etree
import re

# Function to get user input for the directory
def get_input_directory():
    dir_childes_corpus = input("Enter the directory containing CHILDES XML files: ")
    return dir_childes_corpus

# Path containing CHILDES XML files
dir_childes_corpus = get_input_directory()

# Extract the input directory name
input_directory_name = os.path.basename(os.path.normpath(dir_childes_corpus))

# Create a new folder called 'processed' if it doesn't exist
processed_folder = f'processed_{input_directory_name}'
os.makedirs(processed_folder, exist_ok=True)

# Empty lists to store speaker and utterance data
all_speakers_data = []
all_utterance_data = []

# Define namespaces
namespaces = {
    'tb': 'http://www.talkbank.org/ns/talkbank',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

for root, dirs, files in os.walk(dir_childes_corpus, topdown=False):
    for folder_name in dirs:
        folder_path = os.path.join(dir_childes_corpus, folder_name)

        # Lists to store data for each folder
        speakers_data = []
        utterance_data = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.xml'):
                file_path = os.path.join(folder_path, filename)

                # Parse XML data
                tree = etree.parse(file_path)

                # Extract dialogue_id from folder name and filename
                dialogue_id = f"{folder_name}/{os.path.splitext(filename)[0]}.xml"

                # Extract participant information
                for participant in tree.xpath("//tb:Participants/tb:participant", namespaces=namespaces):
                    speaker_info = {
                        'dialogue_id': dialogue_id,
                        'speaker_id': participant.get('id'),
                        'speaker_name': participant.get('name'),
                        'role': participant.get('role'),
                        'age': participant.get('age'),
                        'sex': participant.get('sex')
                    }
                    speakers_data.append(speaker_info)

                # Extract utterance information including morphemes count
                for utt in tree.xpath("//tb:u", namespaces=namespaces):
                    speaker = utt.get('who')
                    uID = utt.get('uID')  # Extract uID
                    #utterance_text = ' '.join(utt.xpath(".//tb:w/text()", namespaces=namespaces))

                    # Check if the utterance has text content
                    utterance_text = ''
                    for word_element in utt.xpath(".//tb:w/text()", namespaces=namespaces):
                        word_text = word_element.strip()
                        if word_text is not None:
                            utterance_text += word_text + ' '
    
                    # Check if the utterance has punctuation
                    punctuation = ''
                    for punct_element in utt.xpath(".//tb:t", namespaces=namespaces):
                        punct_type = punct_element.get('type')
                        if punct_type == 'q':
                            punctuation = ' ?'
                            break
                        elif punct_type == 'p':
                            punctuation = ' .'
                            break
                        elif punct_type =='e':
                            punctuation = ' !'
                            break

                    # Combine words and punctuation to form the utterance text
                    if utterance_text.strip():  # Check if there's text content in the utterance
                        utterance_text = utterance_text.strip()  # Remove trailing space
                        if punctuation:
                            utterance_text += punctuation                    

                    # Count morphemes
                    utterance_length = len(utt.xpath(".//tb:w/tb:mor", namespaces=namespaces))
                    
                    # New columns to store POS and grammatical info
                    pos_tags = []
                    #mor_tags = []
                    gra_relations = ''

                    for element in utt.xpath(".//tb:w/tb:mor|./tb:tagMarker", namespaces=namespaces):
                        pos_elem = element.find('tb:mw/tb:pos/tb:c', namespaces=namespaces)
                        stem_elem = element.find('tb:mw/tb:stem', namespaces=namespaces)
                        type_elem = element.find('tb:mw/tb:pos/tb:s', namespaces=namespaces)  # Morpheme type

                        if pos_elem is not None and stem_elem is not None:
                            pos = pos_elem.text
                            stem = stem_elem.text

                            # Check if <s> tag exists and include its content
                            if type_elem is not None:
                                morpheme_type = type_elem.text
                                pos_word = f"{pos}:{morpheme_type}|{stem}"
                            else:
                                pos_word = f"{pos}|{stem}"

                            pos_tags.append(pos_word)

                    # Join the list of POS tags
                    pos_tags = " ".join(pos_tags)
        
                    # Extract grammatical relations info
                    for gra in utt.xpath(".//tb:w/tb:mor/tb:gra|./tb:t/tb:mor/tb:gra", namespaces=namespaces):
                        index = gra.get('index')
                        head = gra.get('head')
                        relation = gra.get('relation')
                        gra_relations += f"{index}|{head}|{relation} "
    
                    # Clean up format for new columns
                    #pos_tags = re.sub(r'\s+$', '', pos_tags)
                    gra_relations = re.sub(r'\s+$', '', gra_relations)

                    utt_info = {
                        'dialogue_id': dialogue_id,
                        'uID': uID,
                        'speaker': speaker,
                        'utterance': utterance_text,
                        'utterance_length': utterance_length,
                        '%mor': pos_tags,
                        '%gra': gra_relations
                    }
                    utterance_data.append(utt_info)

        # Convert lists to dataframes for each folder
        df_speakers = pd.DataFrame(speakers_data)
        df_utts = pd.DataFrame(utterance_data)

        # Append dataframes to the overall lists
        all_speakers_data.append(df_speakers)
        all_utterance_data.append(df_utts)

# Concatenate dataframes for each folder
all_speakers_data = pd.concat(all_speakers_data, ignore_index=True)
all_utterance_data = pd.concat(all_utterance_data, ignore_index=True)

# Merge dataframes
merged_df = all_utterance_data.merge(all_speakers_data,
                                     left_on=['dialogue_id', 'speaker'],
                                     right_on=['dialogue_id', 'speaker_id'],
                                     how='left')

# Save each folder's data to a separate CSV file in the 'processed' folder
for folder_name in dirs:
    folder_csv_name = os.path.join(processed_folder, f"{folder_name}.csv")
    folder_df = merged_df[merged_df['dialogue_id'].str.startswith(folder_name + '/')]
    folder_df.to_csv(folder_csv_name, index=False)