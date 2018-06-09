from Parser import Parser
from FileGenerator import FileGenerator
import argparse
import ntpath
import os

def main():
    parser = argparse.ArgumentParser(description='Creating indd files and schedules based on xlsx file.')
    parser.add_argument('-f','--file', help='Path to xlsx file.', required=True)
    args = vars(parser.parse_args())

    month = os.path.splitext(ntpath.basename(args['file']))[0]
    
    parser = Parser(args['file'])
    parser.read_from_file()
    parser.write_to_json(month + ".json")
    data = parser.get_data()
    file_generator = FileGenerator()
    file_generator.generate_schedules(data)
    file_generator.parse_file_properties(data)
    file_generator.generate_indd_files(data, month)


if __name__ == "__main__":
    main()