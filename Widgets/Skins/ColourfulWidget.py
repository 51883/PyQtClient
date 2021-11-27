#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ColourfulWidget
@description: Colorful control
"""

from PyQt5.QtWidgets import QPushButton

from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Utils.ThemeThread import ColourfulThread
from Widgets.Skins.SkinBaseWidget import SkinBaseWidget, SkinBaseItemWidget,\
    PixmapWidth, PixmapHeight


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ColourfulWidget(SkinBaseWidget):

    def __init__(self, *args, **kwargs):
        super(ColourfulWidget, self).__init__(*args, **kwargs)
        self._index = 0
        Signals.colourfulItemAdded.connect(self.onColourfulItemAdded)
        Signals.colourfulItemAddFinished.connect(
            self.onColourfulItemAddFinished)

    def init(self):
        """Initialize colorful
        """
        if self.gridLayout.count() > 0:
            return
        ColourfulThread.start(PixmapWidth, PixmapHeight)

    def doPreviewPrevious(self):
        """Previous
        """
        self._index -= 1
        self._index = max(self._index, 0)
        self.doPreview()

    def doPreviewNext(self):
        """Next
        """
        self._index += 1
        self._index = min(self._index, self.gridLayout.count() - 1)
        self.doPreview()

    def doPreview(self):
        """Actively send preview signals
        """
        self.gridLayout.itemAt(self._index).widget().click()

    def onColourfulItemAddFinished(self):
        """Add completion
        """
        return
        # Add a + button
        self.buttonAdd = QPushButton(
            '+', self, objectName='buttonAdd', clicked=self.onAddNewColor)
        # Load mouse style
        ThemeManager.loadCursor(self.buttonAdd, ThemeManager.CursorPointer)
        if self.lastCol == 4:
            self.lastCol = 0
            self.lastRow += 1
        else:
            self.lastCol += 1
        self.gridLayout.addWidget(self.buttonAdd, self.lastRow, self.lastCol)

    def onAddNewColor(self):
        """Add new color"""
        pass

    def onColourfulItemAdded(self, row, col, name, color):
        """
        :param row:            Row
        :param col:            List
        :param name:           name
        :param color:          colour
        """
        self.lastRow = row
        self.lastCol = col
        self.gridLayout.addWidget(
            SkinBaseItemWidget(name, color, Signals.colourfulItemClicked, self), row, col)
