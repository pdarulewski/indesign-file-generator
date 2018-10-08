import argparse
import ntpath
import os
from parser import Parser

from indd_generator import InddGenerator
from schedule_generator import ScheduleGenerator


def main():
    parser = argparse.ArgumentParser(description='Creating indd files and schedules based on xlsx file.')
    parser.add_argument('-f','--file', help='Path to xlsx file.', required=True)
    parser.add_argument('-d', '--destination', help='Path to destination directory', required=True)
    args = vars(parser.parse_args())

    parser = Parser(args['file'])
    parser.read_from_file()

    data = parser.get_data()
    month = os.path.splitext(ntpath.basename(args['file']))[0]

    indd_gen = InddGenerator(data, args['destination'], month)
    indd_gen.generate_files()

if __name__ == "__main__":
    main()
