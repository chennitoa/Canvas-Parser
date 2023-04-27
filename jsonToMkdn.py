from markdownify import markdownify as md
import configparser
import json
import re
import os
import requests
import time

        

class MkdnParser:

    def __init__(self, file):
        # Get api key for making file download requests later
        self.mParser = configparser.ConfigParser()
        if os.path.isfile('config.ini'):
            self.mParser.read('config.ini')
        else:
            API_URL = input('API URL: ')
            API_KEY = input('API Token: ')
            self.mParser['CANVAS CLONE'] = {}
            self.mParser['CANVAS CLONE']['api_url'] = API_URL
            self.mParser['CANVAS CLONE']['api_key'] = API_KEY
            with open("config.ini", "w") as configfile:
                self.mParser.write(configfile)

        self.file = './CodEvalTooling/' + file
        with open(self.file) as infile:
            self.file_dict = json.load(infile)

        self.dir_name = file.split(".")[0] + '/'

        if not os.path.exists('./CodEvalTooling/' + self.dir_name):
            os.makedirs('./CodEvalTooling/' + self.dir_name)


    def check_links(self, s):
        """
        Checks if the given link is a canvas file, if so, downloads the file and gives a path to the file
        
        Keyword arguments:
        s -- re.Match object containing a link
        Return: string
        """
        link = s.group(1)
        filename = s.group(2)
        headers = {'Authorization': 'Bearer ' + self.mParser['CANVAS CLONE']['api_key']}
        response = requests.get(link, headers)
        if 'Content-Length' in response.headers:
            with open('CodEvalTooling/' + self.dir_name + filename, 'wb') as outfile:
                outfile.write(response.content)

    
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
        linkPattern = r'<a[^>]*?href="([^"]*)"[^>]*>([^<]*)'

        linkTags = re.sub(linkPattern, self.check_links, self.file_dict['description'])
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

        with open('./CodEvalTooling/' + self.dir_name + filename, 'wb') as outfile:
            outfile.write(file_mkdn_encoded)
        

def main():

    if not os.path.exists('./CodEvalTooling/'):
        os.makedirs('./CodEvalTooling/')

    file_to_parse = input("Give filename to parse: ")
    
    mParser = MkdnParser(file_to_parse)    

    mParser.clean_description()
    mParser.parse_links_to_files()

    mParser.write_to_mkdn('PA 01.txt')

if __name__ == '__main__':
    main()