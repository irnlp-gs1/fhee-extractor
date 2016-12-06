"""FHEE Utils"""
import csv
import re

def get_fhee_inverted_dict(dict_path='../dict/fhee_dict.tsv'):
    """Get FHEE inverted dictionary (category => word)

    Blanks and special characters (e.g. -) in a multi-word expression are removed.

    Args:
        dict_path (str): path to dictionary file

    Returns:
        inverted_dict (:obj:dict)
    """
    inverted_dict = {}
    non_char_pattern = re.compile(r'[^가-힣a-zA-Z]+', re.UNICODE)

    with open(dict_path, 'r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin, delimiter='\t')
        for item in reader:
            category, word = item['category'].strip(), re.sub(non_char_pattern, '', item['word'])
            inverted_dict[word] = category

    return inverted_dict
