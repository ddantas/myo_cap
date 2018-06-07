from settings import Settings

import pyqtgraph as pg

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        settings = Settings().load()
        amplitude_start = float(settings['vMin'])
        amplitude_end = float(settings['vMax'])
        amplitude = amplitude_end - amplitude_start
        for x in values:
            strns.append((x % amplitude) + (amplitude_start))
        return strns
