class LoadSettings():
    
    def capture(self):
        try:
            output = open("config/capture.config", "r")
            data = output.readlines()
            return data
        except IOError:
            if(type == capture_file): data = [2000, 4, 1, 12]
            else: data = [1000, 0.0, 1.0, 100.0, -2.0, 2.0]
            return data

    def display(self):
        try:
            output = open("config/display.config", "r")
            data = output.readlines()
            return data
        except IOError:
            if(type == capture_file): data = [2000, 4, 1, 12]
            else: data = [1000, 0.0, 1.0, 100.0, -2.0, 2.0]
            return data