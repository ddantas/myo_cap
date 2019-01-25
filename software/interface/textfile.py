import datetime
import sys, os

mainPath = os.path.realpath(os.path.dirname(sys.argv[0])).replace("/leap_cap/src","")

class Textfile():
    def __init__(self):
        self.start_variables()

    def init(self, numCols, format, nameCols):
        '''
        Initialize a thread.

        Keyword arguments:
        numCols -- number of columns
        format -- format to print data
        nameCols -- name of columns
        '''
        if(self.data_header):
            self.data_header = self.data_header + ";" + str(nameCols) + "/" + str(format)
        else:
            self.data_header =  "# " + str(nameCols) + "/" + str(format)
        self.data_init.append([])
        self.id += 1
        self.data_init[self.id].append([])
        self.data_init[self.id].append(format)
        self.data_init[self.id].append(numCols)
        self.data_init[self.id].append(nameCols)
        return self.id

    def message_save(self, msg):
        '''
        Add message to header.

        Keyword arguments:
        msg -- the message 
        '''
        self.header.append("## %s \n" % (msg) )
    
    def metadata_save(self, msg, value):
        '''
        Add parameter to header.

        Keyword arguments:
        msg -- parameter name
        value -- parameter value 
        '''
        self.header.append("# %s: %s \n" % (msg, value) )

    # def metadata_load(self, msg, value):
    #     # Do anything

    def log(self, id, values):
        '''
        Store the data in memory.

        Keyword arguments:
        id -- log id
        value -- data
        '''
        try:
            self.data_init[id][0] = map(float, values)
            data_aux = ""
            for value in self.data_init[1:]:
                if(data_aux):
                    data_aux = "%s;%s" % (data_aux, value[1] % tuple(value[0]))
                else:
                    data_aux = value[1] % tuple(value[0])
            self.data.append(data_aux+"\n")

        except Exception as e:
            pass

    def save(self, filename):
        '''
        Store the data in the file.

        Keyword arguments:
        filename -- relative path
        '''
        try:
            output = open(mainPath + filename, "a")
            output.writelines(self.header)
            output.write(str(self.data_header+'\n'))
            output.writelines(self.data)
            output.close()
        except Exception as e:
           print(e)

    def start_variables(self):
        '''
        Start all variables.
        '''
        self.data = []
        self.header = []
        self.data_init = []
        self.data_init.append("")
        self.data_header = ""
        self.id = 0
        self.temp_data = []
        for x in range(1001):
            self.temp_data.append("")
        self.count_data = 0