# -*- coding: utf-8 -*-

DATA_PATH = "myograph/config/data"

class Textfile:

    def __init__(self):
        self.initVariables()

    def initVariables(self):
        self.data = []
        self.header = []
        self.data_init = []
        self.data_init.append('')
        self.data_header = ''
        self.id = 0
        self.temp_data = []

        for x in range(1001):
            self.temp_data.append('')

        self.count_data = 0

    def initFile(self, num_cols, format, name_cols):
        if(self.data_header):
            self.data_header = self.data_header + '/' + str(name_cols)
        else:
            self.data_header = '# ' + str(name_cols)

        self.data_init.append([])
        self.id += 1
        self.data_init[self.id].append([])
        self.data_init[self.id].append(format)
        self.data_init[self.id].append(num_cols)
        self.data_init[self.id].append(name_cols)

        return self.id

    def writeHeaderLine(self, msg):
        self.header.append('## %s \n' % (msg))
    
    def writeMetadataLine(self, msg, value):
        self.header.append('# %s: %s \n' % (msg, value))

    def saveLog(self, id, values):
        try:
            self.data_init[id][0] = values
            data_aux = ""
            for value in self.data_init[1:]:
                if(data_aux):
                    data_aux = '%s;%s' % (data_aux, value[1] % tuple(value[0]))
                else:
                    data_aux = value[1] % tuple(value[0])

            self.data.append(data_aux + '\n')
        except Exception as e:
            pass

    def saveFile(self, filename):
        try:
            output = open(DATA_PATH + filename, 'a')
            output.writelines(self.header)
            output.write(str(self.data_header + '\n'))
            output.writelines(self.data)
            self.initVariables()
            output.close()
        except Exception as e:
           print(e)