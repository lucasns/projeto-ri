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


#Info Format
class MovieTime(object):
    def __init__(self, min):
        self.min = min

    def __str__(self):
        hr = self.min / 60
        min = self.min % 60
        return str(hr) + " hr " + str(min) + " min"

    def quartile(self):
        qrt = ""
        if self.min > 180:
            qrt = "[3-n)"
        elif self.min > 120:
            qrt = "[2-3)"
        elif self.min > 60:
            qrt = "[1-2)"
        else:
            qrt = "[0-1)"

        return qrt

    @classmethod
    def convert_min(cls, string):
        '''str min -> int min'''
        min = re.search('([0-9]{1,2}) ?min', string.lower())
        time = 0
        if min is not None:
            time = string.split()[0]
        
        return cls(int(time))

    @classmethod
    def convert_hr_min(cls, string):
        '''str (h min) -> int min'''
        hr = re.search('([0-9]{1,2}) ?h', string.lower())
        min = re.search('([0-9]{1,2}) ?min', string.lower())
        time = 0
        if hr is not None:
            time += int(hr.group(1)) * 60
                    
        if min is not None:
            time += int(min.group(1))

        return cls(time)

    @classmethod
    def convert_hr_min_sec(cls, string):
        '''str (hh:mm:ss) -> int min'''
        full_time = re.search('[0-9]{2}:[0-9]{2}:[0-9]{2}', string.lower())
        time = 0
        if full_time is not None:
            full_time = full_time.group(0).split(':')
            time = int(full_time[0]) * 60 + int(full_time[1])

        return cls(time)


class MovieDate(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def convert_date(cls, date_str):
        '''str -> MovieDate'''
        day = re.search('([0-9]{2})[ |,]', date_str.lower())
        month = re.search('([a-zA-Z]{3})', date_str.lower())
        year = re.search('([0-9]{4})', date_str.lower())

        day = day.group(1) if day else None
        month = month.group(1).title() if month else None
        year = year.group(1) if year else None

        return cls(day, month, year)
