#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月8日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.ProgressButton
@description: 
"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, Qt, QRectF,\
    QSequentialAnimationGroup, QPauseAnimation, QParallelAnimationGroup,\
    QPropertyAnimation
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QPushButton


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class CircleItem(QObject):

    _x = 0  # X coordinate
    _opacity = 1  # Transparency 0 ~ 1
    valueChanged = pyqtSignal()

    @pyqtProperty(float)
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.valueChanged.emit()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity


class ProgressButton(QPushButton):

    _waiting = False
    _circleRadius = 3  # radius
    _circleColor = QColor(255, 255, 255)  # Circle color

    def __init__(self, *args, **kwargs):
        super(ProgressButton, self).__init__(*args, **kwargs)
        self._oldText = ''
        self._items = []

    def showWaiting(self, show=True):
        self.setEnabled(not show)
        self._waiting = show
        if show:
            self._oldText = self.text()
            self.setText('')
            self._items.clear()
            self._initAnimations()
            for _, animation in self._items:
                animation.start()
        else:
            self.setText(self._oldText)
            for _, animation in self._items:
                animation.stop()

    def paintEvent(self, event):
        if not self._waiting:
            # Give the original drawing
            super(ProgressButton, self).paintEvent(event)
            return
        # Customize
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        for item, _ in self._items:
            painter.save()
            color = self._circleColor.toRgb()
            color.setAlphaF(item.opacity)
            painter.setBrush(color)
            diameter = 2 * self._circleRadius
            painter.drawRoundedRect(
                QRectF(
                    item.x / 100 * self.width() - diameter,
                    (self.height() - self._circleRadius) / 2,
                    diameter, diameter
                ), self._circleRadius, self._circleRadius)
            painter.restore()

    def _initAnimations(self):
        for index in range(5):  # 5 small round
            item = CircleItem(self)
            item.valueChanged.connect(self.update)
            # String cartoon group
            seqAnimation = QSequentialAnimationGroup(self)
            seqAnimation.setLoopCount(-1)
            self._items.append((item, seqAnimation))

            # Temporary delay animation
            seqAnimation.addAnimation(QPauseAnimation(150 * index, self))

            # Acceleration, parallel animation group 1
            parAnimation1 = QParallelAnimationGroup(self)
            # transparency
            parAnimation1.addAnimation(QPropertyAnimation(
                item, b'opacity', self, duration=400, startValue=0, endValue=1.0))
            # X coordinate
            parAnimation1.addAnimation(QPropertyAnimation(
                item, b'x', self, duration=400, startValue=0, endValue=25.0))
            seqAnimation.addAnimation(parAnimation1)
            ##

            # Uniformity
            seqAnimation.addAnimation(QPropertyAnimation(
                item, b'x', self, duration=2000, startValue=25.0, endValue=75.0))

            # Acceleration, parallel animation group 2
            parAnimation2 = QParallelAnimationGroup(self)
            # transparency
            parAnimation2.addAnimation(QPropertyAnimation(
                item, b'opacity', self, duration=400, startValue=1.0, endValue=0))
            # X coordinate
            parAnimation2.addAnimation(QPropertyAnimation(
                item, b'x', self, duration=400, startValue=75.0, endValue=100.0))
            seqAnimation.addAnimation(parAnimation2)
            ##

            # Temporary delay animation
            seqAnimation.addAnimation(
                QPauseAnimation((5 - index - 1) * 150, self))

    @pyqtProperty(int)
    def circleRadius(self):
        return self._circleRadius

    @circleRadius.setter
    def circleRadius(self, radius):
        if self._circleRadius != radius:
            self._circleRadius = radius
            self.update()

    @pyqtProperty(QColor)
    def circleColor(self):
        return self._circleColor

    @circleColor.setter
    def circleColor(self, color):
        if self._circleColor != color:
            self._circleColor = color
            self.update()
