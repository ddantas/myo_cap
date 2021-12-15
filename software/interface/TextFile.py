# -*- coding: utf-8 -*-
"""
Created on Thu May 13 19:45:40 2021

@author: Asaphe Magno
"""


# -*- coding: utf-8 -*-
import os
import numpy as np
import AuxFunctions as AuxFunc

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
        self.file_lines       = []
        
        # Log Parameters
        self.id   = 0
        self.line = []        

## File Methods ##############################################################################################################################    

    # Method: Cleans the file parameters.
    # Input : None
    # Output: None
    def cleanFileParam(self):
        self.header_lines = [];   self.metadata_lines = [];   self.data_header_line = '';   
        self.data_lines   = [];   self.metadata_dict  = {};   self.file_lines       = []
        
    def writeHeaderLine(self, msg):
        # Stores the header line into the header_lines variable.
        self.header_lines.append('## %s \n' % (msg))
        # Stores the header line into the file_lines variable.
        self.file_lines.append('## %s \n' % (msg))
    
    def writeMetadataLine(self, param, value):
        # Stores the metadata line into the metadata_lines variable.
        self.metadata_lines.append('# %s: %s \n' % (param, str(value) ))
        # Stores the metadata line into the file_lines variable.
        self.file_lines.append('# %s: %s \n' % (param, str(value) ))
        
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
        # Stores the metadata line
        metadata_line = line
        # Removes the unwanted chars.
        line = line.replace('# ','').replace(':','').replace('\n', '')
        # Splits the parameter name from the parameter value and stores the strings in metadata_line list.
        line = line.split(' ')         
        # Adds the metadata to the metadata_dict dictionary
        self.metadata_dict[ line[METADATA_NAME] ] = line[METADATA_VALUE]                
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

    # Method: Opens a text file and classify its lines putting them into the corresponding file variables: header_lines; data_header_line; data_lines. 
    #
    # Input : file_dir_and_name    -> Directory to the text file with the file name.
    #
    # Output: None.
    def loadFile(self, file_dir_and_name):
        # Char indexes
        FIRST_CHAR  = 0
        SECOND_CHAR = 1
        
        # Cleans the file parameters.
        self.cleanFileParam()        
        try:
            # Opens the file. 
            with open(file_dir_and_name, 'r') as file:
                # Data header not readed yet.
                data_header_readed = False   
                # Iterates through the lines. 
                for line in file:                     
                    # Stores the line of the file into the file_lines variable.
                    self.file_lines.append(line)
                    # True if it's a header line.
                    if line[FIRST_CHAR] == '#' and line[SECOND_CHAR] == '#':    self.header_lines.append(line)                                                                    
                    # True if it's a meta data line. Appends the extracted data from the line as a list of two strings to the metata_lines.
                    if line[FIRST_CHAR] == '#' and line[SECOND_CHAR] == ' ':    self.metadata_lines.append( self.extractMetadata(line) )                    
                    # True if it's a data line.
                    if line[FIRST_CHAR] != '#' and line[FIRST_CHAR] != '' and     data_header_readed:   self.data_lines.append(line)                        
                    # True if it's a data header line.
                    if line[FIRST_CHAR] != '#' and line[FIRST_CHAR] != '' and not data_header_readed:   self.data_header_line = line;      data_header_readed = True
                # Closes the file    
                file.close()
        except:
            AuxFunc.showMessage('Error!', 'Insert an compatible text file.')        
            
## Log Methods ###############################################################################################################################

    def initFile(self, format, name_cols):                
        if len(self.data_header_line):            self.data_header_line = self.data_header_line + ';' + name_cols
        else:                                     self.data_header_line = name_cols
        self.line.append('')            
        self.line[self.id] = []        
        self.line[self.id].append([])
        self.line[self.id].append(format)
        self.line[self.id].append(name_cols)
        self.id += 1
        return self.id - 1

    # updateLog: update log values.
    def updateLog(self, id, values):
        self.line[id][0] = values
  
    # logLine: creates a new line with all columns.
    def logLine(self):
        try:
            line = ''
            for column in self.line[0:]:
                if(len(line)):
                    line = '%s;%s' % (line, column[1] % tuple(column[0]))
                else:
                    line = column[1] % tuple(column[0])
            self.data_lines.append(line + '\n')
        except Exception as e:
            print(e)

    def getLog(self, pos):
        return np.fromstring(self.data_lines[pos], dtype=np.uint16, sep=';')
    
    def getLogLength(self):
        return len(self.data_lines)
    
    # saveFile: saves settings and log data to a csv file.
    def saveFile(self, path, file_name):
        try:
            if not os.path.exists(path):    os.makedirs(path) 
            output = open(path + file_name, 'a')
            output.writelines(self.file_lines)   
            output.write(str(self.data_header_line + '\n'))
            output.writelines(self.data_lines)
            output.close()
        except Exception as e:
            print(e)