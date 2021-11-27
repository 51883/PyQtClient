#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月27日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.SkinBaseWidget
@description: 
"""
import os

from PyQt5.QtCore import Qt, QSize, pyqtProperty
from PyQt5.QtGui import QColor, QPainter, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget

from UiFiles.Ui_ScrollArea import Ui_FormScrollArea
from Utils.ThemeManager import ThemeManager


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

PixmapWidth = 158
PixmapHeight = 152              # size of picture
MarginBottom = 26               # Bottom text


class SkinBaseItemWidget(QWidget):

    def __init__(self, name, colorimg, signal, *args, **kwargs):
        super(SkinBaseItemWidget, self).__init__(*args, **kwargs)
        self.setObjectName('skinBaseItemWidget')
        # Load mouse style
        ThemeManager.loadCursor(self, ThemeManager.CursorPointer)
        self.name = name
        self.colorimg = colorimg
        self.hovered = False
        self.signal = signal
        self.colorHover = QColor(0, 0, 0, 40)
        self._textHoverColor = QColor(18, 183, 245)
        self.textColor = QColor(102, 102, 102)
        self.image = None
        # picture
        if isinstance(self.colorimg, str) and os.path.isfile(self.colorimg):
            self.image = QPixmap(self.colorimg).scaled(
                PixmapWidth, PixmapHeight,
                Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    def click(self):
        self.signal.emit(self.name, self.colorimg)

    def mousePressEvent(self, event):
        super(SkinBaseItemWidget, self).mousePressEvent(event)
        self.hovered = True
        self.textColor = self._textHoverColor
        self.update()

    def mouseReleaseEvent(self, event):
        super(SkinBaseItemWidget, self).mouseReleaseEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()
        self.signal.emit(self.name, self.colorimg)

    def enterEvent(self, event):
        super(SkinBaseItemWidget, self).enterEvent(event)
        self.hovered = True
        self.textColor = QColor(Qt.black)
        self.update()

    def leaveEvent(self, event):
        super(SkinBaseItemWidget, self).leaveEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()

    def paintEvent(self, event):
        super(SkinBaseItemWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # Draw color square
        painter.save()
        painter.setPen(Qt.NoPen)
        if self.image != None:
            # Draw picture
            painter.drawPixmap(0, 0, self.image)
        else:
            # Painting color
            painter.setBrush(QBrush(self.colorimg))
            painter.drawRoundedRect(
                0, 0, PixmapWidth, PixmapHeight, 2, 2)
        if self.hovered:
            # Draw a layer of gray
            painter.setBrush(QBrush(self.colorHover))
            painter.drawRoundedRect(
                0, 0, PixmapWidth, PixmapHeight, 2, 2)
        painter.restore()
        # Draw text
        painter.setPen(self.textColor)
        painter.drawText(0, 0, PixmapWidth, PixmapHeight + MarginBottom,
                         Qt.AlignHCenter | Qt.AlignBottom, self.name)
        painter.end()

    def sizeHint(self):
        return QSize(PixmapWidth, PixmapHeight + MarginBottom)

    @pyqtProperty(QColor)
    def textHoverColor(self):
        return self._textHoverColor

    @textHoverColor.setter
    def textHoverColor(self, color):
        self._textHoverColor = QColor(color)


class SkinBaseWidget(QWidget, Ui_FormScrollArea):

    def __init__(self, *args, **kwargs):
        super(SkinBaseWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
