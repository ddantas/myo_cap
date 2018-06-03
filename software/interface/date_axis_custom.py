from load_settings import LoadSettings

import pyqtgraph as pg

# class to set axis label
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        disp_data = LoadSettings().display()
        amplitude_start = float(disp_data[4])
        amplitude_end = float(disp_data[5])
        amplitude = amplitude_end - amplitude_start
        for x in values:
            strns.append((x % amplitude) + (amplitude_start))
        return strns
