import os
import shutil
from nltk.corpus.reader import CHILDESCorpusReader

# Set the path to the corpora folder
corpora_root = 'corporas'

# Create a CHILDESCorpusReader
corpus_reader = CHILDESCorpusReader(corpora_root, '.*.xml')

# Define the target child age ranges (in months)
min_age_1_2 = 12
max_age_1_2 = 24
min_age_2_4 = 25
max_age_2_4 = 48 

# Create folders to store selected files
output_folder_1 = os.path.join(os.path.dirname(corpora_root), 'corpora1')
output_folder_2 = os.path.join(os.path.dirname(corpora_root), 'corpora2')

os.makedirs(output_folder_1, exist_ok=True)
os.makedirs(output_folder_2, exist_ok=True)

# Iterate through each subfolder in the corpora directory
for folder_name in os.listdir(corpora_root):
    folder_path = os.path.join(corpora_root, folder_name)

    if os.path.isdir(folder_path):
        # Create folders to store selected files for the current subfolder
        output_folder_1_2 = os.path.join(output_folder_1, f"{folder_name} 1-2")
        output_folder_2_4 = os.path.join(output_folder_2, f"{folder_name} 2-4")

        os.makedirs(output_folder_1_2, exist_ok=True)
        os.makedirs(output_folder_2_4, exist_ok=True)

        # Get a list of all file IDs
        all_file_ids = corpus_reader.fileids()

        # Filter file IDs based on the current subfolder
        file_ids_in_subfolder = [file_id for file_id in all_file_ids if file_id.startswith(f"{folder_name}/")]

        # Iterate through each file and filter based on child age
        for file_id in file_ids_in_subfolder:
            # Extract age from the file
            age_list = corpus_reader.age(file_id, month=True)

            # Check if there is valid age information
            if age_list and age_list[0] is not None:
                age = age_list[0]
                # Check if the age is within the target range for the current subfolder
                if min_age_1_2 <= age <= max_age_1_2:
                    source_path = os.path.join(corpora_root, file_id)
                    destination_path = os.path.join(output_folder_1_2, os.path.basename(file_id))
                    shutil.copy(source_path, destination_path)
                elif min_age_2_4 <= age <= max_age_2_4:
                    source_path = os.path.join(corpora_root, file_id)
                    destination_path = os.path.join(output_folder_2_4, os.path.basename(file_id))
                    shutil.copy(source_path, destination_path)

print("Files have been moved based on child age to corpora1 and corpora2.")
