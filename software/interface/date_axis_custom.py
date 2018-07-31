from settings import Settings

import pyqtgraph as pg

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        settings = Settings().load()
        vMin = float(settings['vMin'])
        vMax = float(settings['vMax'])
        amplitude = (vMax - vMin)
        for x in values:
            print(round( (x % amplitude) + vMin, 2))
            strns.append(round( (x % amplitude) + vMin, 2))
        return strns
