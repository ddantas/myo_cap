
import Settings
import Board

settings = Settings.Settings()
settings.load()

board = Board.Board(settings)
board.openComm('COM3')

board.setFucGenFreq(200)
#board.serial.write(b'ai')



#Notes: Serial Port not opened yet before a start