import glob
import json
import os

from bs4 import BeautifulSoup
import click

import kami.metrics.evaluation as kamiscorer


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
    Finds text nodes in PAGE XML based on eScriptorium semantic annotation
    Reconstruct semantic units for each page

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
    # then all sublists are flattened into a list of string indexes
    transcriptions_flat_list = [entry for sublist in transcriptions for entry in sublist]
    # sublists are joined with \n, resulting in a string
    transcriptions_text = '\n'.join(transcriptions_flat_list)

    return transcriptions_text


def compare_htr_gt_with_kami(directory_path_GT, directory_path_HTR):
    """
    For each directory containing HTR PAGE XML, extracts semantic units and compare it to its ground truth
    with the KaMI python library


    Input directory structure:

      input
        ├── document
          ├── document ground truth containing PAGE XML files
          └── HTR
              ├── document HTR resulting from model 𝑥
              └── ...

    Requires in each HTR subdirectories a text file, storing HTR model name

    Args:
        directory_path_GT: (str) path to Ground truth directory
        directory_path_HTR: (str) path to directory containing HTR subdirectories

    Returns: a JSON formatted dictionary object containing batch evaluations of HTR PAGE XML and PAGE XML ground truth
    """

    out_directory = 'out'
    # Variable that will store the model name
    model_log = ''
    # Variables that will store each entry for a GT and HTR XML PAGE
    entries_GT_str = ''
    entries_HTR_str = ''
    # Variable that will store the JSON formatted dictionary object
    json_stats = {}

    # Variable storing a list of all path to HTR subdirectories, from the HTR directory
    subdirectories_HTR_list = os.listdir(directory_path_HTR)

    # We create an output directory, if it does not exist already, for saving the JSON output
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)

    # We store the document name from the GT directory name
    doc_name = directory_path_GT.split('/')[-1]
    # We create a key in the dictionary with it
    json_stats[doc_name] = []

    for subdir in subdirectories_HTR_list:
        # Iterating through each HTR subdirectory
        HTR_subdirectory_path = os.path.join(directory_path_HTR, subdir)
        print(f"Starting evaluation of {HTR_subdirectory_path}")

        # Get HTR model name from the text file
        for filepath_txt in glob.glob(os.path.join(HTR_subdirectory_path, '*.txt')):
            with open(filepath_txt, 'r', encoding='utf-8') as fh:
                model_log = fh.readline().strip('\n')
        json_stats[doc_name].append({model_log: []})

        # Iterate through all PAGE XML in the current HTR subdirectory
        for filepath_GT in glob.glob(os.path.join(directory_path_GT, '*.xml')):
            source_name_GT = filepath_GT.split('/')[-1].replace('.xml', '')
            for filepath_HTR in glob.glob(os.path.join(HTR_subdirectory_path, '*.xml')):
                source_name_HTR = filepath_HTR.split('/')[-1].replace('.xml', '')

                # While iterating through each PAGE XML file in the GT directory
                # Looks for the same file name in HTR subdirectory that was saved earlier
                if source_name_HTR == source_name_GT:
                    # When match is found, begins processing GT file and HTR file
                    parsed_source_GT = open_and_parse(filepath_GT)
                    entries_GT_str = get_transcription_list(parsed_source_GT)
                    parsed_source_HTR = open_and_parse(filepath_HTR)
                    entries_HTR_str = get_transcription_list(parsed_source_HTR)

            # Checks if there are actually strings to compare
            if entries_GT_str and entries_HTR_str:
                # Checks if strings are not made of blank spaces
                if not entries_GT_str.isspace() and not entries_HTR_str.isspace():
                    # Uses KaMI to get HTR metrics
                    scores = kamiscorer.Scorer(entries_GT_str, entries_HTR_str)
                    scores_dict = scores.board
                    json_stats[doc_name][-1][model_log].append({source_name_GT: scores_dict})

        print(f"{HTR_subdirectory_path}: done! \n")

    print("All evaluations are done")
    print(json.dumps(json_stats, sort_keys=True, indent=4))

    return json_stats


@click.group()
def group():
    """
    Command line interface to get scores for HTR performance, comparing a ground truth document with
    multiple automatic transcriptions

    Given an ground truth directory containing PAGE XML transcription files, and given a directory with subdirectories
    each containing PAGE XML automatic transcription files, iterate through each subdirectories and compare
    a PAGE XML ground truth file to a PAGE XML HTR file.

    Outputs a JSON file storing batch evaluation

    This CLI was made to help classify candidate for NER annotation based on the quality of the automatic transcription
    """


@group.command("evaluate")
@click.argument("GT_directory_path", type=str)
@click.argument("HTR_directory_path", type=str)
def run(gt_directory_path, htr_directory_path):
    json_stats = compare_htr_gt_with_kami(gt_directory_path, htr_directory_path)

    doc_name = gt_directory_path.split('/')[-2]

    with open(f'{doc_name}_HTR_scores.json', 'w+', encoding='utf-8') as json_output:
        json.dump(json_stats, json_output, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    group()
