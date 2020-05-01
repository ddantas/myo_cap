# -*- coding: utf-8 -*-

import Board

BAUDRATE = 921600
ADC_BITS = 12
V_MAX = 3.3
V_MIN = 0

class Tiva(Board.Board):

    def __init__(self, settings):
        # set tiva parameters
        self.settings = settings
        self.settings.setBaudrate(BAUDRATE)
        self.settings.setBitsPerSample(ADC_BITS)

        # supeclass constructor
        super(Tiva, self).__init__(settings)

    def getConstADC(self):
        return (V_MAX - V_MIN)/(2^ADC_BITS)