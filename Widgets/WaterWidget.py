#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.WaterWidget
@description: Water corrugation progress
"""
import math

from PyQt5.QtCore import pyqtProperty, QTimer, Qt
from PyQt5.QtGui import QColor, QPainterPath, QPainter
from PyQt5.QtWidgets import QWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class WaterWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaterWidget, self).__init__(*args, **kwargs)
        # Wave high percentage
        self._waterHeight = 1
        # density
        self._waterDensity = 1
        # Wave color 1
        self._waterFgColor = QColor(33, 178, 148)
        # Wave color 2
        self._waterBgColor = QColor(33, 178, 148, 100)
        self.minimum = 0
        self.maximum = 0
        self._value = 0
        self._offset = 0
        # Refresh the waves every 100ms (simulated wave dynamics)
        self._updateTimer = QTimer(self, timeout=self.update)
        self._updateTimer.start(100)

    def update(self):
        if self.minimum >= self.maximum:
            return
        super(WaterWidget, self).update()

    def paintEvent(self, event):
        super(WaterWidget, self).paintEvent(event)
        if self.minimum >= self.maximum:
            return
        if not self._updateTimer.isActive():
            return

        # Sinusoidal curve formula y = A * sin(ωx + φ) + k
        # Percentage of current value
        percent = 1 - (self._value - self.minimum) / \
            (self.maximum - self.minimum)
        # w Representation period, 6 is a person-definition
        w = 6 * self.waterDensity * math.pi / self.width()
        # A amplitude height percentage, 1/26 is a definition
        A = self.height() * self.waterHeight * 1 / 26
        # k Height percentage
        k = self.height() * percent

        # Wave 1
        waterPath1 = QPainterPath()
        waterPath1.moveTo(0, self.height())  # Start point in the lower left corner
        # Wave 2
        waterPath2 = QPainterPath()
        waterPath2.moveTo(0, self.height())  # Start point in the lower left corner

        # Offset
        self._offset += 0.6
        if self._offset > self.width() / 2:
            self._offset = 0

        for i in range(self.width() + 1):
            # Calculate the Y-axis point from the X-axis
            y = A * math.sin(w * i + self._offset) + k
            waterPath1.lineTo(i, y)

            # The first relative displacement required
            y = A * math.sin(w * i + self._offset + self.width() / 2 * A) + k
            waterPath2.lineTo(i, y)

        # Close two waves, forming a U-shaped upper plus wavy closed section
        waterPath1.lineTo(self.width(), self.height())
        waterPath1.lineTo(0, self.height())
        waterPath2.lineTo(self.width(), self.height())
        waterPath2.lineTo(0, self.height())

        # Start the path
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # Set no brush
        painter.setPen(Qt.NoPen)

        # Wave 1
        painter.save()
        painter.setBrush(self._waterBgColor)
        painter.drawPath(waterPath1)
        painter.restore()

        # Wave 2
        painter.save()
        painter.setBrush(self._waterFgColor)
        painter.drawPath(waterPath2)
        painter.restore()

    def stop(self):
        self.setValue(0, 0)
        self.setRange(0, 0)
        self._updateTimer.stop()
        self.repaint()

    def value(self):
        return self._value

    def setValue(self, value, maximum=0):
        self._value = value
        if maximum > 0:
            self.maximum = maximum

    def setRange(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def setMinimum(self, minimum):
        self.minimum = minimum

    def setMaximum(self, maximum):
        self.maximum = maximum

    @pyqtProperty(float)
    def waterHeight(self):
        return self._waterHeight

    @waterHeight.setter
    def waterHeight(self, height):
        self._waterHeight = height

    @pyqtProperty(float)
    def waterDensity(self):
        return self._waterDensity

    @waterDensity.setter
    def waterDensity(self, density):
        self._waterDensity = density

    @pyqtProperty(QColor)
    def waterFgColor(self):
        return self._waterFgColor

    @waterFgColor.setter
    def waterFgColor(self, color):
        self._waterFgColor = QColor(color)

    @pyqtProperty(QColor)
    def waterBgColor(self):
        return self._waterBgColor

    @waterBgColor.setter
    def waterBgColor(self, color):
        self._waterBgColor = QColor(color)
