import os 
import pandas as pd
import xml.etree.ElementTree as ET
import re

# Load the XML file
tree = ET.parse('011116.xml')
root = tree.getroot()


# Path containing CHILDES XML files
dir_childes_corpus = 'Providence'

# Extract the directory name
input_directory_name = os.path.basename(os.path.normpath(dir_childes_corpus))

# Create a new folder called 'processed' if it doesn't exist
processed_folder = f'processed_{input_directory_name}'
os.makedirs(processed_folder, exist_ok=True)


# Define the namespace
ns = {'pb': 'http://phon.ling.mun.ca/ns/phonbank'}

# Function to extract participant information
def extract_participants(root):
    participants = []
    for participant in root.findall('.//pb:participant', ns):
        participant_data = {
            'speaker_id': participant.attrib.get('id'),
            'speaker_name': participant.find('pb:name', ns).text,
            'role': participant.find('pb:role', ns).text,
            #'birthday': participant.find('pb:birthday', ns).text,
            'age': participant.find('pb:age', ns).text,
            'sex': participant.find('pb:sex', ns).text
            #'language': participant.find('pb:language', ns).text
        }
        participants.append(participant_data)
    return participants

# Function to extract utterance information
def extract_utterances(root):
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
                utterance_length += len(re.findall(r'\w+', word_text))

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
            'speaker': utterance.attrib.get('speaker'),
            'uID' : uID,
            #'id': utterance.attrib.get('id'),
            'utterance': utterance_text,
            'utterance_length': utterance_length,
            '%mor': mor_text,
            'gra' :gra_text
        }
        utterances.append(utterance_data)

        uID += 1 # Increment uID for the next utterance
    return utterances


# Extract participant and utterance information
participants_data = extract_participants(root)
utterances_data = extract_utterances(root)

# Create DataFrames
participants_df = pd.DataFrame(participants_data)
utterances_df = pd.DataFrame(utterances_data)

# Save DataFrames to CSV files
participants_df.to_csv('participants.csv', index=False)
utterances_df.to_csv('utterances.csv', index=False)


