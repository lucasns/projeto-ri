import cPickle as pickle
import csv


#IO Functions
def read_file(file_path):
    content = None
    with open(file_path, 'rb') as f:
        content = pickle.load(f)

    return content


def read_file_multiple(file_path):
    with open(file_path, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def save_csv(file_path, rows):
    with open(file_path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
