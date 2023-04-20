from markdownify import markdownify as md
import json
import re
import os

class mkdnParser:
    def __init__(self, file):
        self.file = file
        with open(file) as infile:
            self.file_dict = json.load(infile)

    def write_to_mkdn(self, filename):
        """
        Opens the file, reads the file and writes it to markdown
        
        Keyword arguments:
        filename -- string, file to write to
        Return: None
        """
        file_mkdn = ''
        file_mkdn += 'CRT_HW START ' + self.file_dict['name'] + '\n'

        file_mkdn += md(self.file_dict['description'].replace(r'\n', ''), autolinks = False, escape_asterisks = False, escape_underscores = False, heading_style = 'ATX', strip = ['ul'])

        file_mkdn += '\nCRT_HW END'
        file_mkdn_encoded = bytes(file_mkdn, 'utf-8')

        with open(filename, 'wb') as outfile:
            outfile.write(file_mkdn_encoded)
        
def main():
    parser = mkdnParser('./CodEvalTooling/CNVS_A00023.json')
    if not os.path.exists('./CodEvalTooling/'):
        os.makedirs('./CodEvalTooling/')
    
    parser.write_to_mkdn('./CodEvalTooling/PA 01.txt')

if __name__ == '__main__':
    main()