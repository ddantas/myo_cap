# -*- coding: utf-8 -*-

from Board import Board

BAUDRATE = 921600
ADC_BITS = 12

class Tiva(Board):

    def __init__(self, settings):
        # set tiva parameters
        self.settings = settings
        self.settings.setBaudrate(BAUDRATE)
        self.settings.setBitsPerSample(ADC_BITS)

        # supeclass constructor
        super(Tiva, self).__init__(settings)