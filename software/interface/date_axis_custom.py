from settings import Settings

import pyqtgraph as pg

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        settings = Settings().load()
        vMin = ( int(settings['vMin'] / settings['vertTick']) - 1 ) * settings['vertTick']
        vMax = ( int(settings['vMax'] / settings['vertTick']) + 1 ) * settings['vertTick']
        amplitude = (vMax - vMin)
        for x in values:
            strns.append(round( (x % amplitude) + vMin, 2))
        return strns
