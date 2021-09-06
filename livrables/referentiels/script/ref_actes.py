from datetime import datetime
import glob
import json
import os

from bs4 import BeautifulSoup


def open_and_parse(source):
    """
    Opens an XML file and parsed its content with BeautifulSoup

    :param source: source file to be opened and parsed
    :return: parsed source
    :rtype: BeautifulSoup object
    """

    with open(source, 'r', encoding='utf8') as fh:
        file_content = fh.read()
    parsed_source = BeautifulSoup(file_content, 'xml')
    return parsed_source


# Directory path where all XML files for processing are stored
directory = '../data/doc_97_actes/'
# Empty list for storing entities later
transcriptions_actes = []
# Creation of counters to document the creation of the dictionary in a log file
counter_page = 0
counter_line = 0
counter_empty_baselines = 0

# Processing of all XML files in the directory
for filepath in glob.glob(os.path.join(directory, '*.xml')):
    counter_page += 1
    xml_tree = open_and_parse(filepath)
    for acte in xml_tree:
        # Look for all text lines
        baselines = acte.find_all('TextLine')
        for baseline in baselines:
            counter_line += 1
            if baseline.has_attr('custom'):
                # for each first_line, we create an index which is itself a list
                #
                if baseline['custom'] == 'structure {type:First_line;}':
                    transcriptions_actes.append([baseline.text.strip('\n').strip(' ').replace('\n', '')])
            else:
                transcriptions_actes[-1].append(baseline.text.strip('\n').strip(' ').replace('\n', ''))

        # all index are joined to reconstruct units
        transcriptions_actes = [[' '.join(transcription)] for transcription in transcriptions_actes]
        # then all sublist are flattened into a list of string indexes
        transcriptions_actes_flat_list = [entry.lower() for sublist in transcriptions_actes for entry in sublist]

# Count how many baselines are empty (not transcribed)
for acte in transcriptions_actes_flat_list:
    if acte == '' or acte == ' ':
        counter_empty_baselines += 1

# Remove all duplicates to create dictionary
no_duplicate_transcription_actes_flat_list = list(set(transcriptions_actes_flat_list))
# Sort alphabetically previous list
no_duplicate_transcription_actes_flat_list = sorted(no_duplicate_transcription_actes_flat_list)

# Create a dictionary object for storing JSON format information
ref_actes = {}

# Count how many time an act in the list without duplicates appears in the list storing all baselines
# Then, add the pair {type of act: count} in a dictionary
for acte in no_duplicate_transcription_actes_flat_list:
    # Check if there is a transcription
    # If so, create a new key in the dictionary
    if acte and acte != ' ':
        ref_actes[acte] = transcriptions_actes_flat_list.count(acte)

# Create a JSON file with the dictionary object we have created
with open('referentiel_types_acte.json', 'w+', encoding='utf-8') as json_output:
    json.dump(ref_actes, json_output, ensure_ascii=False, indent=4)

# Create a log text file with metadata on the JSON file that was created
with open('referentiel_type_acte_log.txt', 'w+', encoding='utf-8') as log_output:
    log_output.write(str(datetime.now()))
    log_output.write('\n')
    log_output.write('Format: {type_of_act: frequency}')
    log_output.write('\n')
    log_output.write(f'Number of XML files: {counter_page}')
    log_output.write('\n')
    log_output.write(f'Number of baselines: {counter_line}')
    log_output.write('\n')
    log_output.write(f'Number of entities: {len(ref_actes)}')
    log_output.write('\n')
    log_output.write(f'Deleted entities: all baselines that were not transcribed ({counter_empty_baselines} in total)')
