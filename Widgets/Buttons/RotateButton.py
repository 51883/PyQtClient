#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.RotateButton
@description:
"""
import os

from PyQt5.QtCore import Qt, pyqtProperty, QRectF, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath, QImage
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, \
    QStyleOptionButton, QStylePainter, QStyle

from Widgets.ToolTip import ToolTip


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class RotateButton(QPushButton):

    STARTVALUE = 0  # Start rotation angle
    ENDVALUE = 360  # End rotation angle
    DURATION = 540  # Animation completed total time

    def __init__(self, *args, image='', **kwargs):
        super(RotateButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self._angle = 0  # angle
        self._padding = 10  # Shadow margin
        self._image = ''  # Picture path
        self._shadowColor = QColor(33, 33, 33)  # Shadow color
        self._pixmap = None  # Picture object
        # Attribute animation
        self._animation = QPropertyAnimation(self, b'angle', self)
        self._animation.setLoopCount(1)  # Only loop once
        self.setPixmap(image)
        # Binding prompt box
        ToolTip.bind(self)

    def paintEvent(self, event):
        """Plot event"""
        text = self.text()
        option = QStyleOptionButton()
        self.initStyleOption(option)
        option.text = ''  # Do not draw text
        painter = QStylePainter(self)
        painter.setRenderHint(QStylePainter.Antialiasing)
        painter.setRenderHint(QStylePainter.HighQualityAntialiasing)
        painter.setRenderHint(QStylePainter.SmoothPixmapTransform)
        painter.drawControl(QStyle.CE_PushButton, option)
        # Transform coordinates are in the middle
        painter.translate(self.rect().center())
        painter.rotate(self._angle)  # Rotate

        # Draw picture
        if self._pixmap and not self._pixmap.isNull():
            w = self.width()
            h = self.height()
            pos = QPointF(-self._pixmap.width() / 2, -
                          self._pixmap.height() / 2)
            painter.drawPixmap(pos, self._pixmap)
        elif text:
            # Picture text after transform coordinates
            fm = self.fontMetrics()
            w = fm.width(text)
            h = fm.height()
            rect = QRectF(0 - w * 2, 0 - h, w * 2 * 2, h * 2)
            painter.drawText(rect, Qt.AlignCenter, text)
        else:
            super(RotateButton, self).paintEvent(event)

    def enterEvent(self, _):
        """Mouse entering event"""
        # Set shadow
        # Border shadow effect
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(self._padding * 2)
        effect.setOffset(0, 0)
        effect.setColor(self._shadowColor)
        self.setGraphicsEffect(effect)

        # Open rotating animation
        self._animation.stop()
        cv = self._animation.currentValue() or self.STARTVALUE
        self._animation.setDuration(self.DURATION if cv == 0 else int(
            cv / self.ENDVALUE * self.DURATION))
        self._animation.setStartValue(cv)
        self._animation.setEndValue(self.ENDVALUE)
        self._animation.start()

    def leaveEvent(self, _):
        """Mouse leave event"""
        # Cancel shadow
        self.setGraphicsEffect(None)

        # Rotating animation
        self._animation.stop()
        cv = self._animation.currentValue() or self.ENDVALUE
        self._animation.setDuration(int(cv / self.ENDVALUE * self.DURATION))
        self._animation.setStartValue(cv)
        self._animation.setEndValue(self.STARTVALUE)
        self._animation.start()

    def setPixmap(self, path):
        if not os.path.exists(path):
            self._image = ''
            self._pixmap = None
            return
        self._image = path
        size = min(self.width(), self.height()) - self.padding  # Requires a margin border
        radius = int(size / 2)
        image = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)  # Fill background is transparent
        pixmap = QPixmap(path).scaled(
            size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        # QPainter
        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # QPainterPath
        path = QPainterPath()
        path.addRoundedRect(0, 0, size, size, radius, radius)
        # Cutting
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        self._pixmap = QPixmap.fromImage(image)
        self.update()

    def pixmap(self):
        return self._pixmap

    @pyqtProperty(str)
    def image(self):
        return self._image

    @image.setter
    def image(self, path):
        self.setPixmap(path)

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    @pyqtProperty(int)
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value

    @pyqtProperty(QColor)
    def shadowColor(self):
        return self._shadowColor

    @shadowColor.setter
    def shadowColor(self, color):
        self._shadowColor = QColor(color)
