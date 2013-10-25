# utils.py

import codecs, bz2, gzip

def open_with_unicode(file_name, compression_type, mode):
    assert compression_type in [None, 'gzip', 'bzip2']
    assert mode in ['r', 'w']
    if compression_type == None:
        if mode == 'r':
            return codecs.getreader('utf-8')(open(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(open(file_name, mode))
    elif compression_type == 'gzip':
        if mode == 'r':
            return codecs.getreader('utf-8')(gzip.GzipFile(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(gzip.GzipFile(file_name, mode))
    elif compression_type == 'bzip2':
        if mode == 'r':
            return codecs.getreader('utf-8')(bz2.BZ2File(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(bz2.BZ2File(file_name, mode))


def split_file_into_chunks(file_name, directory, lines_per_chunk):

    """
    Assumes bzip2 compression.
    """

    file_obj = open_with_unicode(file_name, 'bzip2', 'r')
    current_line_number = 0
    current_file_number = 0
    end_of_file = False
    while not end_of_file:
        current_filename = directory + '%03d' % current_file_number + '.bz2'
        current_file_obj = open_with_unicode(current_filename, 'bzip2', 'w')
        current_file_obj.write(file_obj.readline())
        current_line_number += 1
        while current_line_number % lines_per_chunk > 0:
            current_line = file_obj.readline()
            end_of_file = current_line == ''
            current_file_obj.write(current_line)
            current_line_number += 1
        current_file_number += 1
    return

def partition_by_list(s, p_list):

    """
    Returns a tuple with the substrings of s partitioned around the
    elements of p_list.  It is designed to be used with a
    regex.findall in order to tokenise.

    Example: 
    >>> s = u"This is a sentence I'd like to tokenise."
    >>> partition_by_list(s, regex.findall(r'\p{P}|\p{S}|\p{Z}', s))
    (u'This', u' ', u'is', u' ', u'a', u' ', u'sentence', u' ', u'I',
    u"'", u'd', u' ', u'like', u' ', u'to', u' ', u'tokenise', u'.')
    """

    if s == '': return []
    if p_list == []: return [s]
    p = list(s.partition(p_list[0]))
    if p[0] == '': return [p[1],] + partition_by_list(p[2], p_list[1:])
    if p[1] == '': return [p[0]]
    return [p[0], p[1]] + partition_by_list(p[2], p_list[1:])
    
def precision_recall_f_measure(true_positives, false_positives, false_negatives):

    if true_positives == 0:
        precision = recall = f_measure = 0
        
    else:
        precision = (0.0 + true_positives)/(true_positives + false_positives)
        recall = (0.0 + true_positives)/(true_positives + false_negatives)
        f_measure = (2 * precision * recall)/(precision + recall)

    return (precision, recall, f_measure)
