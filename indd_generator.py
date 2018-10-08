import logging
import os
import sys
import traceback
from pprint import pprint
from shutil import copyfile

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('indd_generator')
logger.setLevel(logging.DEBUG)

class InddGenerator:
    __filenames = []
    __fileformats = []
    __cities = []
    __data = None
    __destination = None
    __month = None

    def __init__(self, data, destination, month):
        self.__data = data
        self.__destination = destination
        self.__month = month
        self._parse_file_properties()

    def _parse_file_properties(self):
        for city in self.__data['cities']:
            for event in city['events']:
                self.__cities.append(city['city'])
                formats = ""
                self.__fileformats.append([])
                for shape in event['format']:
                    self.__fileformats[-1].append(shape)
                    formats += shape + "_"
                self.__filenames.append("{}_{}_{}_{}.indd".format(
                    str(event['date']).replace(".", "_"),
                    event['title'].replace(" ", "_"),
                    formats,
                    city['city']
                ))

    def _create_working_dirs(self):
        working_dir = self.__destination
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
            os.makedirs("{}/{}_rozkłady_fb/".format(working_dir, self.__month))
            os.makedirs("{}/{}_rozkłady_a6/".format(working_dir, self.__month))
            os.makedirs("{}/ldz/".format(working_dir))
            os.makedirs("{}/rz/".format(working_dir))
            os.makedirs("{}/tor/".format(working_dir))

    def _create_indd_file(self, input_file, output_file):
        copyfile(input_file, output_file)

    def generate_files(self):
        # self._create_working_dirs()
        # self._generate_posters()
        self._generate_schedules()

    def _generate_posters(self):
        try:
            for filename, fileformat, city in zip(
                self.__filenames, self.__fileformats, self.__cities):

                self._create_indd_file(
                    'templates/{}.indd'.format(fileformat[0]),
                    '{}/{}/{}'.format(self.__destination, city, filename))

                logger.info('%s', '{} file was generated.'.format(filename))

            logger.info('%s', 'All indd files were generated.')

        except Exception:
            logger.error("An error occurred while generating indd files.")
            traceback.print_exc()
            sys.exit()

    def _generate_schedules(self):
        cities = ['ldz', 'rz', 'tor']
        input_files = [
            'a6_schedule_ldz',
            'a6_schedule_rz',
            'a6_schedule_tor'
        ]

        try:
            for city, input_file in zip(cities, input_files):
                self._create_indd_file(
                    'templates/{}.indd'.format(input_file),
                    '{0}/{1}_rozkłady_a6/{1}_rozkład_a6_{2}.indd'.format(
                        self.__destination, self.__month, city))

                logger.info('%s',
                    'A6 schedule for {} file was generated.'.format(city))

            self._create_indd_file(
                'templates/fb_schedule.indd',
                    '{0}/{1}_rozkłady_fb.indd'.format(
                        self.__destination, self.__month))

            logger.info('%s', 'All indd files were generated.')

        except Exception:
            logger.error("An error occurred while generating indd files.")
            traceback.print_exc()
            sys.exit()
