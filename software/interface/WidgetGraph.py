# -*- coding: utf-8 -*-

import pyqtgraph as pg
import numpy as np

class WidgetGraph(pg.PlotWidget):

    def __init__(self, settings):
        
        self.settings = settings

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        super(WidgetGraph, self).__init__()
        
        # Remove after tests
        self.settings.setShowChannels(5)

        self.configureGraph()

    def configureGraph(self):
        
        self.updateAxisX()
        self.updateAxisY()

        #self.setMenuEnabled(False, 'same')
        self.setMouseEnabled(False, False)
        self.disableAutoRange( )
        self.hideButtons()
        self.getPlotItem().setContentsMargins(10, 30, 30, 10)

    def updateAxisX(self):
        
        #self.setXRange(0, self.settings.getSwipe())
        self.setRange(xRange = ( 0 , self.settings.getSwipe() ) , padding = 0)
        
        self.axis_x = self.getAxis('bottom')
        self.axis_x.setLabel(axis='bottom', text='Number of samples')
        self.axis_x.setTickSpacing(self.settings.getSwipe(), self.settings.getHTick())
        self.axis_x.setGrid(70)

    def updateAxisY(self):
        
        num_ticks_neg = np.abs(np.round(self.settings.getVMin() / self.settings.getVTick()))
        num_ticks_pos = np.abs(np.round(self.settings.getVMax() / self.settings.getVTick()))
        self.num_ticks_ch = int(num_ticks_neg + num_ticks_pos)
        num_ticks_axis = (self.settings.getShowChannels() * self.num_ticks_ch) 

        if self.settings.getVMin() < 0:
            tick_min = (-1) * num_ticks_neg * self.settings.getVTick()
        else:
            tick_min = 0

        ticks_pos = list(range(num_ticks_axis + 1))

        #self.setYRange(0, num_ticks_axis)
        self.setRange(yRange = (0 , num_ticks_axis) , padding = 0)

        self.axis_y = self.getAxis('left')
        self.axis_y.setLabel(axis='left', text='Voltage', units='volts')
        self.axis_y.setGrid(70)
        self.axis_y.setTicks([[(p, self.tickString(p, self.num_ticks_ch, num_ticks_axis, tick_min)) for p in ticks_pos]])

        #print ( [[(p, self.tickString(p, num_ticks_ch, num_ticks_axis, tick_min)) for p in ticks_pos]] )

    def tickString(self, p, num_ticks_ch, num_ticks_axis, tick_min):
        
        if p == num_ticks_axis:
            tick_pos_ch = num_ticks_ch
        else:
            tick_pos_ch = p % num_ticks_ch

        tick = tick_min + self.settings.getVTick() * tick_pos_ch

        return str(np.round(tick, 2))