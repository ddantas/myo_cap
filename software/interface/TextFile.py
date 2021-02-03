# -*- coding: utf-8 -*-

import numpy as np

DATA_PATH = 'data/'

class TextFile():

    def __init__(self):
        self.initVariables()

    def initVariables(self):
        self.header = []
        self.data_header = ''
        self.data = []
        self.id = 0
        self.line = []

    def initFile(self, format, name_cols):
        if len(self.data_header):
            self.data_header = self.data_header + ';' + name_cols
        else:
            self.data_header = '# ' + name_cols
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
            self.data.append(aux + '\n')
        except Exception as e:
            print(e)

    def writeHeaderLine(self, msg):
        self.header.append('## %s \n' % (msg))
    
    def writeMetadataLine(self, msg, value):
        self.header.append('# %s: %s \n' % (msg, value))

    def saveFile(self, file_name):
        try:
            output = open(DATA_PATH + file_name, 'a')
            output.writelines(self.header)
            output.write(str(self.data_header + '\n'))
            output.writelines(self.data)
            output.close()
        except Exception as e:
           print(e)

    def getLog(self, pos):
        return np.fromstring(self.data[pos], dtype=np.uint16, sep=';')
    
    def getLogLength(self):
        return len(self.data)