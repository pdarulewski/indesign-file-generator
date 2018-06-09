from pprint import pprint
import traceback
import logging
import os

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('file_generator')

class FileGenerator:
    __filenames = []
    __fileformats= []

    def __init__(self):
        pass

    def generate_schedules(self, data):
        for city in data['cities']:
            content = ""
            for event in city['events']:
                content += event['date'] + "_" + event['title'] + u'\r\n'
            try:
                with open("Schedules\\" + city['city'] + '.txt', 'wb') as out:
                    out.write(content.encode('utf8'))
                    logger.warning('%s', 'Schedule was generated for: ' + city['city'])
            except Exception:
                print("File was not written.")
                traceback.print_exc()

    def generate_indd_files(self, data, month):
        try:
            import win32com.client
            app = win32com.client.Dispatch('InDesign.Application.CC.2018')
            for filename, fileformat in zip(self.__filenames, self.__fileformats):
                self.__generate_indd_file(filename, fileformat, month, app)
            logger.warning('%s', 'All indd files was generated.')
            print(self.__filenames)
            pprint(self.__fileformats)
        except Exception:
            print("An error occurred while generating indd files.")
            traceback.print_exc()

    def __generate_indd_file(self, filename, fileformat, month, app):
        idPortrait = 1751738216
        myDocument = app.Documents.Add()
        try:
            if("b2" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "684mm"
                myDocument.DocumentPreferences.PageWidth = "484mm"
            elif("a2" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "594mm"
                myDocument.DocumentPreferences.PageWidth = "420mm"
            elif("a3" in fileformat):
                myDocument.DocumentPreferences.PageHeight = "420mm"
                myDocument.DocumentPreferences.PageWidth = "297mm"
            else: # for fb / b1
                myDocument.DocumentPreferences.PageHeight = "1000mm"
                myDocument.DocumentPreferences.PageWidth = "707mm"

            myDocument.DocumentPreferences.PageOrientation = idPortrait

            myDocument.DocumentPreferences.DocumentBleedBottomOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedTopOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedInsideOrLeftOffset = "5mm"
            myDocument.DocumentPreferences.DocumentBleedOutsideOrRightOffset = "5mm"

            myDocument.DocumentPreferences.SlugBottomOffset = "0mm"
            myDocument.DocumentPreferences.SlugTopOffset = "0mm"
            myDocument.DocumentPreferences.SlugInsideOrLeftOffset = "0mm"
            myDocument.DocumentPreferences.SlugRightOrOutsideOffset = "0mm"

            myDocument.MarginPreferences.Left = "12.7mm"
            myDocument.MarginPreferences.Right = "12.7mm"
            myDocument.MarginPreferences.Top = "12.7mm"
            myDocument.MarginPreferences.Bottom = "12.7mm"
            
            myDocument.DocumentPreferences.FacingPages = False

            myDocument.DocumentPreferences.PagesPerDocument = 1

        except Exception as e:
            print(e)
        try:
            myFile = r'C:\Users\ray3n\Desktop\Grafika\Bajka\Script' + '\\' + month
            if not os.path.exists(myFile):
                os.makedirs(myFile)
            myFile = myFile + '\\' + filename
            myDocument = myDocument.Save(myFile)
            myDocument.Close()
            logger.warning('%s', myFile + ' was generated.')
        except Exception:
            print("An error occurred while generating indd files.")
            traceback.print_exc()

    def parse_file_properties(self, data):
        for city in data['cities']:
            for event in city['events']:
                formats = ""
                self.__fileformats.append([])
                for shape in event['format']:
                    self.__fileformats[-1].append(shape)
                    formats += shape + "_"
                self.__filenames.append(
                    event['date'].replace(".", "_") + "_" + event['title'].replace(" ", "_") +
                    "_" + formats + city['city'] + ".indd")
        