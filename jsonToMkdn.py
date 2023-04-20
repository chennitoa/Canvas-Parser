from markdownify import markdownify as md
import json
import re
import os
import requests

def check_links(s):
        """
        Checks if the given link is a canvas file, if so, downloads the file and gives a path to the file
        
        Keyword arguments:
        s -- re.Match object containing a link
        Return: string
        """
        link = s.group(2)
        print(link)
        filename = s.group(3)
        print(filename)
        

class MkdnParser:
    def __init__(self, file):
        self.file = file
        with open(file) as infile:
            self.file_dict = json.load(infile)

    def clean_description(self):
        """
        Removes newline characters from the description in the assignment json
        
        Keyword arguments:
        Return: None
        """
        self.file_dict.update({'description': self.file_dict['description'].replace(r'\n', '')})

    def parse_links_to_files(self):
        """
        Takes json structure of assignment and takes files, downloads them and changes the locations in the json
        
        Keyword arguments:
        Return: None
        """
        linkPattern = r'<(a)[^>]*?href="([^"]*)"[^>]*>([^<]*)'

        linkTags = re.sub(linkPattern, check_links, self.file_dict['description'])
        # print(linkTags)

    def write_to_mkdn(self, filename):
        """
        Opens the file, reads the file and writes it to markdown
        
        Keyword arguments:
        filename -- string, file to write to
        Return: None
        """
        file_mkdn = ''
        file_mkdn += 'CRT_HW START ' + self.file_dict['name'] + '\n'

        file_mkdn += md(self.file_dict['description'], autolinks = False, escape_asterisks = False, escape_underscores = False, heading_style = 'ATX', strip = ['ul'])

        file_mkdn += '\nCRT_HW END'
        file_mkdn_encoded = bytes(file_mkdn, 'utf-8')

        with open(filename, 'wb') as outfile:
            outfile.write(file_mkdn_encoded)
        
def main():
    parser = MkdnParser('./CodEvalTooling/CNVS_A00024.json')
    if not os.path.exists('./CodEvalTooling/'):
        os.makedirs('./CodEvalTooling/')
    
    parser.clean_description()
    parser.parse_links_to_files()

    parser.write_to_mkdn('./CodEvalTooling/PA 01.txt')

if __name__ == '__main__':
    main()