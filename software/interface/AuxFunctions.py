import PyQt5

def showMessage(title, body):
    PyQt5.QtWidgets.QMessageBox.about(PyQt5.QtWidgets.QMainWindow(),title, body)

def patternStr(pattern, num_it, add_it):
    str_out = ''
    for i in range(num_it):
        str_out = str_out + pattern
        if add_it:
            str_out = str_out + str(i)

        if i < num_it - 1:
            str_out = str_out + ';'
    return str_out