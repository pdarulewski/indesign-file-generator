from Parser import Parser
from InddGenerator import InddGenerator
from ScheduleGenerator import ScheduleGenerator
import argparse
import ntpath
import os

def main():
    parser = argparse.ArgumentParser(description='Creating indd files and schedules based on xlsx file.')
    parser.add_argument('-f','--file', help='Path to xlsx file.', required=True)
    parser.add_argument('-d', '--destination', help='Path to destination directory', required=True)
    args = vars(parser.parse_args())

    month = os.path.splitext(ntpath.basename(args['file']))[0]
    
    parser = Parser(args['file'])
    parser.read_from_file()
    parser.write_to_json(month + ".json")

    data = parser.get_data()

    indd_generator = InddGenerator(data, args['destination'], month)
    indd_generator.parse_file_properties()
    indd_generator.generate_indd_files()

    schedule_generator = ScheduleGenerator(data)
    schedule_generator.generate_txt_schedules(data, args['destination'])
    schedule_generator.generate_schedules(data, args['destination'])


if __name__ == "__main__":
    main()