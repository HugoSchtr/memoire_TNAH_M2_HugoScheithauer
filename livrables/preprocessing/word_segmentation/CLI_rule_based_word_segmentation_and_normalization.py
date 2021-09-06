import glob
import json
import os
import re

import click
from bs4 import BeautifulSoup
import spacy


def open_and_parse(source):
    """
    Opens an XML file and parsed its content with BeautifulSoup

    :param source: source file to be opened and parsed
    :type source: xml file
    :return: parsed source
    :rtype: BeautifulSoup object
    """

    # parse the xml file with BeautifulSoup
    with open(source, 'r', encoding='utf-8') as fh:
        file_content = fh.read()
    parsed_source = BeautifulSoup(file_content, 'xml')
    return parsed_source


def get_transcription_list(xml_tree):
    """
    Finds text nodes in PAGE XML and get them ready for NER processing

    :param xml_tree: XML tree
    :type xml_tree: BeautifulSoup object
    :return: Entries list
    :rtype: list
    """

    # we create a list for storing all entries
    transcriptions = []
    # get the text region labelled as structure {type:col_5;}
    col_5 = xml_tree.find_all('TextRegion', custom="structure {type:Col_5;}")

    # split the text from said text region into entries with the custom attribute
    for col in col_5:
        baselines = col.find_all('TextLine')
        for baseline in baselines:
            if baseline.has_attr('custom'):
                # handles main date line (page's first line), create an index
                if baseline['custom'] == 'structure {type:Main_date;}':
                    transcriptions.append([baseline.text.strip('\n').strip(' ').replace('\n', '')])
                # for each first_line, we create an index which is itself a list
                elif baseline['custom'] == 'structure {type:First_line;}':
                    transcriptions.append([baseline.text.strip('\n').strip(' ').replace('\n', '')])
            else:
                # if the line is not a first line, then it is appended to last index
                if len(transcriptions) >= 1:
                    if transcriptions[-1] == transcriptions[0]:
                        transcriptions.append([baseline.text.strip('\n').strip(' ').replace('\n', '')])
                    else:
                        transcriptions[-1].append(baseline.text.strip('\n').strip(' ').replace('\n', ''))

    # all index are joined to reconstruct entries
    transcriptions = [[' '.join(transcription)] for transcription in transcriptions]
    # then all sublist are flattened into a list of string indexes
    transcriptions_flat_list = [entry for sublist in transcriptions for entry in sublist]

    return transcriptions_flat_list


def word_segmenter_and_normalizer(orig):
    """
    For each index in a list, spots words stuck together and split them using regex
    e.g. thisIsAnExample --> this Is An Example
    Then, normalize abbreviated words from transcription using a dictionary

    :param orig: entries list created from a LECTAUREP PAGE XML file
    :type orig: list
    :return: list of preprocessed entries
    :rtype: list
    """

    # Load a french language model from spaCy
    nlp = spacy.load("fr_core_news_lg")

    # Create an empty list that will later store preprocessed entries
    pre_processed_entries = []

    for entry in orig:
        # word segmentation using regex
        # regex are based on study of LECTAUREP's textual data and its recurrent errors
        letter_before_caps_splitted = re.sub(r"(\w)([A-Z])", r"\1 \2", entry)
        # undo previous correction of an abbreviation used in the répertoires de notaires
        correction_abbreviated_sson = re.sub("S Son", "SSon", letter_before_caps_splitted)
        blank_space_address_number = re.sub(r'(\d{2})([A-z])', r'\1 \2', correction_abbreviated_sson)
        special_character_before_caps_splitted = re.sub(r"(\))([A-Z])", r"\1 \2", blank_space_address_number)
        blank_space_address = re.sub("del'", "de l'", special_character_before_caps_splitted)
        blank_space_ruede = re.sub("ruede", "rue de", blank_space_address)
        blank_space_ruedu = re.sub("ruedu", "rue du", blank_space_ruede)
        blank_space_ruedela = re.sub("ruedela", "rue de la", blank_space_ruedu)
        blank_space_sondomicile = re.sub("sondomicile", "son domicile", blank_space_ruedela)
        blank_space_beginning_date = re.sub("([A-z])([1-9])", r"\1 \2", blank_space_sondomicile)
        blank_space_month_year = re.sub(r"([A-z])(\d{3,4})", r"\1 \2", blank_space_beginning_date)
        blank_space_before_parenthesis = re.sub(r"([A-z])(\()", r"\1 \2", blank_space_month_year)
        # First encoding for à : \xc3\xa0
        blank_space_before_à = re.sub(r"([^l\s])(à)", r"\1 \2", blank_space_before_parenthesis)
        blank_space_after_à = re.sub(r"(à)([A-z])", r"\1 \2", blank_space_before_à)
        # Second encoding for à : a\xcc\x80
        blank_space_before_à_2 = re.sub(r"([^l\s])(à)", r"\1 \2", blank_space_after_à)
        blank_space_after_à_2 = re.sub(r"(à)([A-z])", r"\1 \2", blank_space_before_à_2)
        # TODO: Espace entre jour et mois pour les dates ?

        # tokenizing entry for correction of abbreviated words with dictionary
        tokenized_entry = nlp(blank_space_after_à_2)
        # From the spaCy Doc object, create a list with each entry tokenized
        token_list = [token.text for token in tokenized_entry]

        # Open abbreviations dictionary
        with open("referentiels/referentiel_abreviations.json", 'r', encoding='utf-8') as fh:
            abreviations_json = json.load(fh)

            # Compare each token in each entry to the dictionary
            for i in range(len(token_list)):
                # Dict object used to store information on token if needed (original, normalized, correction)
                processed_token = {
                    "original token": token_list[i],
                    # Normalize the token for comparing it to the dictionary
                    "normalized token": token_list[i].lower()
                }

                for abreviation in abreviations_json:
                    if processed_token["normalized token"] == abreviation:
                        token_list[i] = abreviations_json[abreviation]
                        processed_token["corrected_token"] = abreviations_json[abreviation]
                        # TODO: Levenshtein string matching ?
                        # TODO: garder majuscule quand adresse
                        # TODO: correction en fonction du contexte
                        # Gde républicaine - Garde républicaine ; avenue de la Gde Armée - avenue de la Grande armée

        # 'De-tokenizing'
        token_list = ' '.join(token_list).replace(' , ', ', ').replace('( ', '(').replace(' )', ')').replace("' ", "'")
        token_list = token_list.replace(' . ', '. ').replace(' + ', '+ ').replace(' % ', '% ').replace(' - ', '-')
        token_list = token_list.replace('- ', '-').replace(' .', '.').replace(' ,', ',')  # Maybe not that robust
        # TODO: work within spaCy doc object if possible

        # artificial sentence segmentation
        pre_processed_entries.append(token_list + "¬")

    return pre_processed_entries


@click.group()
def group():
    """
    Command line interface created to transform LECTAUREP's XML PAGE documents into
    text data for annotation, with minimal word segmentation preprocessing.
    Given a directory, output a txt file with entries separated with a "¬" for each PAGE XML.
    """


@group.command("transform")
@click.argument("input_directory_path", type=str)
def run(input_directory_path):
    # we create the out directory that will store the resulting text files
    out_directory = 'out'
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)

    # given a directory path, loop through all xml files
    for filepath in glob.glob(os.path.join(input_directory_path, '*.xml')):
        source_name = filepath.split('/')[-1].replace('.xml', '')
        print(f"Starting transformation of {source_name}.xml")
        parsed_source = open_and_parse(filepath)
        entries = get_transcription_list(parsed_source)

        if entries:
            processed_entries = word_segmenter_and_normalizer(entries)

            # we use the xml file name for naming the text file output in out directory
            with open(f'out/entry_{source_name}.txt', 'w+', encoding='utf8') as created_file:
                for entry in processed_entries:
                    print(entry)
                    created_file.write(entry)
                    created_file.write('\n')

            print(f"Transformation of {source_name}.xml is done! \n")

        else:
            print('Col_5 cannot be found. Skipping current XML file. \n')


if __name__ == "__main__":
    group()
