# InDesign-file-generation

In my spare time, I am a graphic designer. In my work, I was facing a situation when I had to generate manually a lot of project files which was time-consuming for me. Thus, I wanted to automate the process. The code is suitable only for a given layout of the *.xlsx* file, however, maybe you might find something handy in it.

The *Python* project was written in object-oriented paradigm in order to help me generating *InDesign* project files based on *Excel* worksheet. The code consists of three files:
* *Main.py* - main function with argument parser from a command line
* *Parser.py* - reading data from a worksheet, parsing it to JSON files. Data consist of the name and the location of the event, the format of the poster and the date.
* *FileGenerator.py* - creating simple text schedules (needed to my work) and generate *.indd* files with proper names, formats, slugs, bleeds and margins basing on the previously parsed data.

In the project, I used *openpyxl* to read data from the worksheet and *win32com* to open my distribution of *Adobe InDesign*.