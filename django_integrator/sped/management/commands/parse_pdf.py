import pathlib
from collections import Iterator

from django.core.management.base import BaseCommand, CommandError
from PyPDF2 import PdfFileReader


class Command(BaseCommand):
    def handle(self, *args, **options):
        PdfParser()


class PdfParser:
    NAME_INDICATOR = '2021-2022Student Name:'
    DOB = 'DOB:'
    AREA = 'AREA:'
    PAGE = 'Page'
    IEP_GOAL = 'IEP Goal:'
    GOAL_MSG = 'IEP goals should be related to the State Standards'

    def __init__(self):
        self.create_pdf()

    @staticmethod
    def filter_unicode(line):
        filtered_words = ''

        for word in line.split(' '):
            if u"\ufb01" not in word:
                filtered_words += word + ' '
        return filtered_words

    def parse_student_info(self, lines):
        iterator = iter(lines)
        name = ''
        area = ''
        goal = ''
        while True:
            try:
                line = next(iterator).strip()
                if self.NAME_INDICATOR in line:
                    name_and_iter = self.parse_name(iterator, line)
                    name = name_and_iter[0]
                    iterator = name_and_iter[1]
                elif self.AREA in line:
                    area_and_iter = self.parse_area(iterator, line, name)
                    area = area_and_iter[0]
                    iterator = area_and_iter[1]
                    self.parse_goal(iterator)

            except StopIteration:
                print('finished')
                break

    def parse_name(self, iterator, line) -> (str, Iterator):
        name = ''
        if self.NAME_INDICATOR in line and self.DOB not in line:
            name = line[len(self.NAME_INDICATOR):len(line)]
            line = next(iterator).strip()
            while self.DOB not in line:
                name += line
                line = next(iterator).strip()

        if self.DOB in line:
            name += line
            name = name.replace(self.DOB, '').strip()
        return name, iterator

    def parse_area(self, iterator, line, name) -> (str, Iterator):
        start = line.index(self.AREA, 0) + len(self.AREA)
        end = len(line)
        area = line[start:end].strip()
        line = next(iterator).strip()
        while self.IEP_GOAL not in line:
            if not any(char.isdigit() for char in line):
                area += line
            line = next(iterator).strip()
        area = area.replace(' ', '')
        # print(name, area)
        return area, iterator

    def parse_goal(self, iterator) -> (str, Iterator):
        line = next(iterator)
        goal = next(iterator)
        while 'Standard' not in :
            goal += next(iterator)
        return 'blah', iterator

    # while AREA not in line and GOAL_MSG not in line:
    #     if IEP_GOAL in line: print('^^^', line)
    #     line = next(iterator).strip()

    def create_pdf(self):
        pdf_path = pathlib.Path.cwd().joinpath('static', 'goals.pdf')
        with open(pdf_path, 'rb') as file:
            reader = PdfFileReader(file)
            pages = range(reader.getNumPages())
            filtered_text = []
            for page_num in pages:
                page = reader.getPage(page_num)
                page_lines = page.extractText().split('\n')
                for line in page_lines: filtered_text.append(PdfParser.filter_unicode(line))

            self.parse_student_info(filtered_text)
