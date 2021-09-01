# -*- coding: utf-8 -*-
"""
Created on Thu May 13 19:45:40 2021

@author: asaph
"""


# -*- coding: utf-8 -*-

import numpy as np
# import AuxFunctions as AuxFunc

DATA_PATH = 'data/'

# Metadata indexes
METADATA_NAME  = 0
METADATA_VALUE = 1

class TextFile():

    def __init__(self):
        # File Parameters
        self.header_lines     = []
        self.metadata_lines   = []
        self.metadata_dict    = {}
        self.data_header_line = ''
        self.data_lines       = []
        
        # Log Parameters
        self.id   = 0
        self.line = []

## File Methods ##############################################################################################################################    

    def writeHeaderLine(self, msg):
        self.header_lines.append('## %s \n' % (msg))
    
    def writeMetadataLine(self, param, value):
        self.metadata_lines.append('# %s: %s \n' % (param, str(value) ))
        
    def getHeaderLine(self, line_number):
        return self.header_lines[line_number]

    def getHeaderLines(self):
        return self.header_lines  
    
    # Method: Extracts and splits the parameter name and the parameter value information and return them as strings in metadata_lines list.
    #         Note: The parameter value will need to be converted when it be interpreted. 
    #
    # Input : line           -> Type: String. A file line containing metadata.
    #
    # Output: metadata_line  -> [parameter name|parameter value]. A list containing the extracted data as strings.
    def extractMetadata(self, line):        
        # Removes the unwanted chars.
        line = line.replace('# ','').replace(':','').replace('\n', '')
        # Splits the parameter name from the parameter value and stores the strings in metadata_line list.
        metadata_line = line.split(' ')         
        # Adds the metadata to the metadata_dict dictionary
        self.metadata_dict[ metadata_line[METADATA_NAME] ] = metadata_line[METADATA_VALUE]                
        return metadata_line
           
    def getMetadataLine(self, line_number):
        return self.metadata_lines[line_number]
    
    def getMetadataLines(self):
        return self.metadata_lines

    def getDataHeaderLine(self):
        return self.data_header_line
    
    def getDataLine(self, line_number):
        return self.data_lines[line_number]
    
    def getDataLines(self):
        return self.data_lines
    
    def saveFile(self, data_path, file_name):
        try:
            output = open(data_path + file_name, 'a')
            output.writelines(self.header_lines)
            output.write(str(self.data_header_line + '\n'))
            output.writelines(self.data_lines)
            output.close()
        except Exception as e:
           print(e)

    # Method: Opens a text file and classify its lines putting them into the corresponding file variables: header_lines; data_header_line; data_lines. 
    #
    # Input : file_dir_and_name    -> Directory to the text file with the file name.
    #
    # Output: None.
    def openFile(self, file_dir_and_name):
        # Char indexes
        FIRST_CHAR  = 0
        SECOND_CHAR = 1
        
        # Clear the file parameters.
        self.header_lines = [];   self.metadata_lines = [];   self.data_header_line = '';   self.data_lines = [];    self.metadata_dict = {}   
        try:
            # Opens the file and iterates through the lines. 
            with open(file_dir_and_name, 'r') as file:
                for line in file:
                    # True if it's a header line.
                    if line[FIRST_CHAR] == '#' and line[SECOND_CHAR] == '#':    self.header_lines.append(line)                                                                    
                    # True if it's a meta data line. Appends the extracted data from the line as a list of two strings to the metata_lines.
                    if line[FIRST_CHAR] == '#' and line[SECOND_CHAR] == ' ':    self.metadata_lines.append( self.extractMetadata(line) )
                    # True if it's a data header line.
                    if line[FIRST_CHAR] == '['                             :    self.data_header_line.append(line)
                    # True if it's a data line.
                    if line[FIRST_CHAR] != '#' and line[SECOND_CHAR] != '' and line[SECOND_CHAR] != '[':    self.data_lines.append(line)                        
        except:
            # AuxFunc.showMessage('Error!', 'Insert an compatible text file.')
            print('Incompatible File')
            
## Log Methods ###############################################################################################################################

    def initFile(self, format, name_cols):
        if len(self.data_header_line):
            self.data_header_line = self.data_header_line + ';' + name_cols
        else:
            self.data_header_line = '# ' + name_cols
        self.line[self.id] = []        
        self.line[self.id].append([])
        self.line[self.id].append(format)
        self.line[self.id].append(name_cols)
        self.id += 1
        return self.id - 1

    def saveLog(self, id, values):
        try:
            self.line[id][0] = values
            aux = ''
            for value in self.line[0:]:
                if(len(aux)):
                    aux = '%s;%s' % (aux, value[1] % tuple(value[0]))
                else:
                    aux = value[1] % tuple(value[0])
            self.data_lines.append(aux + '\n')
        except Exception as e:
            print(e)

    def getLog(self, pos):
        return np.fromstring(self.data_lines[pos], dtype=np.uint16, sep=';')
    
    def getLogLength(self):
        return len(self.data_lines)