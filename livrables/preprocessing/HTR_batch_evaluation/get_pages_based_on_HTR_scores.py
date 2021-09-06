import glob
import json
import os
from shutil import copy

from bs4 import BeautifulSoup

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


def open_and_get_json_first_key(json_file_path):
    """
    Opens a JSON file and get its first key

    Args:
        json_file_path: (str) path to JSON file

    Returns: JSON file for processing and JSON file first key
    """

    with open(json_file_path, 'r', encoding='utf-8') as fh:
        json_stats = json.load(fh)
        json_first_key = [key for key in json_stats.keys()]
        json_first_key = ''.join(json_first_key)

    return json_stats, json_first_key


def get_page_based_on_cer_score(json_file, json_first_key, cer_score=float):
    """
    Get a page list from JSON file based on a CER score (<=)

    Args:
        json_file: opened JSON file
        json_first_key: opened JSON file's first key
        cer_score: CER score chosen by user to select page

    Returns: a counter storing how many page were selected, and a list storing page name that were selected
    """

    counter = 0
    selected_pages = {}

    for model in json_file[json_first_key]:
        for document in model:
            selected_pages[document] = []
            for page in model[document]:
                for dict_score in page:
                    for data in page[dict_score]:
                        if data == 'cer':
                            cer = float(page[dict_score][data])
                            if cer <= cer_score:
                                selected_pages[document].append(dict_score)
                                counter += 1

    return counter, selected_pages

json_stats, json_first_key = open_and_get_json_first_key('doc_156_HTR_scores.json')
decompte, page_list = get_page_based_on_cer_score(json_stats, json_first_key, 0.15)
print(decompte)
print(page_list)

if not os.path.exists('ner_candidates'):
    os.mkdir('ner_candidates')

for file in glob.glob(os.path.join('region_segmentation_model_data/doc_156/HTR/doc_156_generic_lectau_26', '*.xml')):
    pagexml = file.split('/')[-1]
    for pagexml_candidate in page_list['generic_lectaurep_26']:
        pagexml_candidate += '.xml'
        if pagexml == pagexml_candidate:
            print(pagexml, pagexml_candidate)
            if not os.path.exists(f'./ner_candidates/{pagexml}'):
                os.mknod(f'./ner_candidates/{pagexml}')
            copy(file, f'./ner_candidates/{pagexml}')

# TODO: transformer en fonction
