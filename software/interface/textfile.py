import datetime
import sys, os

mainPath = os.path.realpath(os.path.dirname(sys.argv[0])).replace("/leap_cap/src","")

class Textfile():
    def __init__(self):
        self.start_variables()

    def init(self, numCols, format, nameCols):
        for x in range(numCols):
            if(self.data_header):
                self.data_header = self.data_header + str(format) + " " + str(nameCols) + str(x)
            else:
                self.data_header = str(nameCols) + str(x)
        self.temp_log.append("")
        self.id += 1
        return self.id

    def message_save(self, msg):
        self.header.append("## "+msg)
    
    def metadata_save(self, msg, value):
        self.header.append("# "+msg+": "+str(value))

    # def metadata_load(self, msg, value):
    #     # Do anything
    
    def log(self, id, values):
        self.temp_log[id] = values
        data_aux = ""
        for value in self.temp_log[1:]:
            if(data_aux):
                data_aux = data_aux + ", " + value 
            else:
                data_aux = value
        self.temp_data[self.count_data] = data_aux+"\n"
        self.count_data += 1        
        if(self.count_data >= 1000):
            self.data.append(self.temp_data)
            self.count_data = 0

    def save(self, filename):
        try:
            output = open(mainPath+"/data/" + filename + ".log", "a")
            for line in self.header:
                output.write(str(line+'\n'))
            output.write(str(self.data_header+'\n'))
            for lines in self.data:
                output.writelines(lines)
            output.close()
        except IOError:
           print("err!")

    def start_variables(self):
        self.data = []
        self.header = []
        self.temp_log = []
        self.temp_log.append("")
        self.data_header = ""
        self.id = 0
        self.temp_data = []
        for x in range(1000):
            self.temp_data.append("")
        self.count_data = 0