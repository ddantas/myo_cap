# -*- coding: utf-8 -*-

import pyqtgraph as pg
import numpy as np

class WidgetGraph(pg.PlotWidget):

    def __init__(self, settings):
        # settings object
        self.settings = settings
        # set graphic colors
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # calling superclass constructor
        super(WidgetGraph, self).__init__()
        # configure graph
        self.configureGraph()

    def configureGraph(self):
        # update x axis informations
        self.updateAxisX()
        # update y axis informations
        self.updateAxisY()
        # configure size and interaction 
        self.setMenuEnabled(False, 'same')
        self.setMouseEnabled(False, False)
        self.disableAutoRange()
        self.hideButtons()
        self.getPlotItem().setContentsMargins(5, -20, 20, 5)
        # create plots
        self.createPlots()

    # configure x axis
    def updateAxisX(self):
        # set range
        self.setRange(xRange=(0, self.settings.getSwipe()), padding=0)
        # get axis x object
        axis_x = self.getAxis('bottom')
        # set label
        axis_x.setLabel(axis='bottom', text='Number of samples')
        # set ticks
        axis_x.setTickSpacing(self.settings.getSwipe(), self.settings.getHTick())
        # set grid
        axis_x.setGrid(70)

    # configure y axis
    def updateAxisY(self):
        # number of negative ticks
        num_ticks_neg = np.abs(np.round(self.settings.getVMin() / self.settings.getVTick()))
        # number of positive ticks
        num_ticks_pos = np.abs(np.round(self.settings.getVMax() / self.settings.getVTick()))
        # total ticks per channel
        self.num_ticks_ch = int(num_ticks_neg + num_ticks_pos)
        # y axis total ticks
        num_ticks_axis = (self.settings.getTotChannels() * self.num_ticks_ch) + 1
        # mininum tick
        if self.settings.getVMin() < 0:
            tick_min = (-1) * num_ticks_neg * self.settings.getVTick()
        else:
            tick_min = 0
        # array with tick index
        ticks_pos = list(range(num_ticks_axis))
        # set range
        self.setRange(yRange=(0, num_ticks_axis), padding=0)
        # get y axis object
        axis_y = self.getAxis('left')
        # set label
        axis_y.setLabel(axis='left', text='Voltage', units='volts')
        # set grid
        axis_y.setGrid(70)
        # set ticks
        axis_y.setTicks([[(p, self.tickString(p, self.num_ticks_ch, num_ticks_axis, tick_min)) for p in ticks_pos]])

    # generate each tick string of y axis
    def tickString(self, p, num_ticks_ch, num_ticks_axis, tick_min):
        if p == num_ticks_axis - 1:
            tick_pos_ch = num_ticks_ch
        else:
            tick_pos_ch = p % num_ticks_ch
        tick = tick_min + self.settings.getVTick() * tick_pos_ch
        return str(np.round(tick, 2))

    def createPlots(self):
        # clear plot objects
        self.clear()
        # reset positions at x axis
        self.swipe_pos = 0
        # list of plot objects
        self.channel_plot = []
        # offset per channel
        self.offset = self.num_ticks_ch * np.array(range(self.settings.getTotChannels()))
        # scale factor to plot at y axis
        self.scale_factor = self.num_ticks_ch / (2 ** self.settings.getBitsPerSample() - 1)
        # samples array
        self.samples = np.zeros(shape=(self.settings.getTotChannels(), self.settings.getSwipe()), dtype=np.float)
        # initializing plots
        for index_ch in range(self.settings.getTotChannels()):
            self.samples[index_ch, :] += self.offset[index_ch]
            self.channel_plot.append(self.plot(self.samples[index_ch, :]))

    def plotSamples(self, data):
        
        # evaluating samples values at y axis
        self.samples[:, self.swipe_pos] = (data * self.scale_factor) + self.offset[:]
        # plot when swipe_pos is multiple of htick or when swipe reaches the end of the x axis
        if (self.swipe_pos % self.settings.getHTick() == 0):# or (self.swipe_pos == self.settings.getSwipe()):
            for index_ch in range(self.settings.getTotChannels()):
                self.channel_plot[index_ch].setData(self.samples[index_ch], pen=pg.mkPen('r', width=0.4))
        if self.swipe_pos == self.settings.getSwipe() - 1:
            self.swipe_pos = 0
        else:
            self.swipe_pos += 1

    # return plot position
    def getSwipePos(self):
        return self.swipe_pos