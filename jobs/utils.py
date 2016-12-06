import csv

def get_fhee_inverted_dict(dict_path='../dict/fhee_dict.tsv'):
    """Get FHEE inverted dictionary (category => word)
    
    Args:
        dict_path (str): path to dictionary file
    
    Returns:
        inverted_dict (:obj:dict)
    """
    inverted_dict = {}

    with open(dict_path, 'r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin, delimiter='\t')
        for item in reader:
            category, word = item['category'].strip(), item['word'].strip()
            inverted_dict[word] = category

    return inverted_dict