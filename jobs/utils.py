"""FHEE Utils"""
import csv
import re
import collections

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

class peekable(object):
    """ An iterator that supports a peek operation.  Example usage:
    >>> p = peekable(range(4))
    >>> p.peek()
    0
    >>> p.next(1)
    [0]
    >>> p.peek(3)
    [1, 2, 3]
    >>> p.next(2)
    [1, 2]
    >>> p.peek(2)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> p.peek(1)
    [3]
    >>> p.next(2)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> p.next()
    3
    """
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._cache = collections.deque()
    def __iter__(self):
        return self
    def _fillcache(self, n):
        if n is None:
            n = 1
        while len(self._cache) < n:
            self._cache.append(self._iterable.next())
    def next(self, n=None):
        self._fillcache(n)
        if n is None:
            result = self._cache.popleft()
        else:
            result = [self._cache.popleft() for i in range(n)]
        return result
    def peek(self, n=None):
        self._fillcache(n)
        if n is None:
            result = self._cache[0]
        else:
            result = [self._cache[i] for i in range(n)]
        return result