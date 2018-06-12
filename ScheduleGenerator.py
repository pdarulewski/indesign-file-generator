import os
import sys
import traceback
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('schedule_generator')

class ScheduleGenerator:

    __data = None
    __destination = None

    def __init__(self, data, destination):
        self.__data = data
        self.__destination = destination
    
    def generate_txt_schedules(self):
        for city in self.__data['cities']:
            content = ""
            for event in city['events']:
                content += event['date'] + "_" + event['title'] + u'\r\n'
            try:
                with open(self.__destination + "\\Schedules\\" + city['city'] + '.txt', 'wb') as out:
                    out.write(content.encode('utf8'))
                    logger.warning('%s', 'Schedule was generated for: ' + city['city'])
            except Exception:
                print("File was not written.")
                traceback.print_exc()

    def generate_schedules(self):
        # TODO:
        # find previous files
        # make copy of them
        # rename
        pass
