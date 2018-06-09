from openpyxl import load_workbook
import os
from pprint import pprint
import json
import re
import traceback
import logging
import pathlib

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('parser')

class Parser:

    __infile = None
    __filename = None
    __month = None
    __full_data = {}
    __cities = ['ldz', 'rz', 'tor']
    __col_names = ['date', 'title', 'format', 'state', 'info', 'comment']

    def __init__(self, path):
        self.__infile = path
        splitted = os.path.split(path)
        self.__filename = splitted[1]

    def get_data(self):
        return self.__full_data

    def read_from_file(self):
        try:
            wb = load_workbook(filename=self.__infile, read_only=True)
            logger.warning('%s', 'Workbook was read.')
        except Exception:
            print("File was not read.")
            traceback.print_exc()

        self.__full_data['cities'] = []
        counter = 0
        try:
            for ws in wb:
                city = {}
                events = []
                for row in list(ws.rows)[1:]:
                    rows = {}
                    prop = 0
                    for cell in row:
                        if prop == 2:
                            formats = []
                            pattern = re.compile(r'fb|[A-Z][0-9]|[a-z][0-9]')
                            for shape in re.findall(pattern, cell.value):
                                formats.append(shape)
                            rows[self.__col_names[prop]] = formats
                        else:
                            rows[self.__col_names[prop]] = cell.value
                        prop += 1

                    events.append(rows)
                
                city['city'] = self.__cities[counter]
                city['events'] = events
                counter += 1
                self.__full_data['cities'].append(city)
            pprint(self.__full_data)
            # logger.warning('%s', self.__full_data)
        except Exception:
            print("Data was not parsed.")
            traceback.print_exc()

    def write_to_json(self, outfile):
        pattern = re.compile(r'.*(?=\.)')
        self.__month = re.match(pattern, self.__filename)
        try:
            filename = 'Data\\' + self.__month.group() + '.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w') as outfile:
                json.dump(self.__full_data, outfile)
            logger.warning('%s', "JSON was saved.")

        except Exception:
            print("Data was not parsed.")
            traceback.print_exc()

