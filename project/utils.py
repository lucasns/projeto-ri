import cPickle as pickle
import csv
import re


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


#Convert Functions
def convert_min(string):
    '''(n min) to number of minutes'''
    min = re.search('([0-9]{1,2}) ?min', string.lower())
    if min is not None:
        return string.split()[0]
    else:
        return 0


def convert_hr_min(string):
    '''(n h n min) to number of minutes'''
    hr = re.search('([0-9]{1,2}) ?h', string.lower())
    min = re.search('([0-9]{1,2}) ?min', string.lower())
    time = 0
    if hr is not None:
        time += int(hr.group(1)) * 60
                    
    if min is not None:
        time += int(min.group(1))

    return time


def convert_hr_min_sec(string):
    '''(hh:mm:ss) to number of minutes'''
    full_time = re.search('[0-9]{2}:[0-9]{2}:[0-9]{2}', string.lower())
    if full_time is not None:
        full_time = full_time.group(0).split(':')
        return int(full_time[0]) * 60 + int(full_time[1])
    else:
        return 0


def convert_date(string):
    '''Return a tuple with (day, month, year)'''
    day = re.search('([0-9]{2})[ |,]', string.lower())
    month = re.search('([a-zA-Z]{3})', string.lower())
    year = re.search('([0-9]{4})', string.lower())

    day = day.group(1) if day else None
    month = month.group(1).title() if month else None
    year = year.group(1) if year else None

    return day, month, year
