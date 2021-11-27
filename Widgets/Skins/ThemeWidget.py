#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ThemeWidget
@description: 
"""
import os

from Utils.CommonUtil import Signals
from Utils.ThemeThread import ThemeThread
from Widgets.Skins.SkinBaseWidget import PixmapWidth, PixmapHeight,\
    SkinBaseItemWidget, SkinBaseWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ThemeWidget(SkinBaseWidget):

    def __init__(self, *args, **kwargs):
        super(ThemeWidget, self).__init__(*args, **kwargs)
        self._index = 0
        Signals.themeItemAdded.connect(self.onThemeItemAdded)
        Signals.themeItemAddFinished.connect(
            self.onThemeItemAddFinished)

    def init(self):
        """Initialization theme
        """
        if self.gridLayout.count() > 0:
            return
        ThemeThread.start(PixmapWidth, PixmapHeight)

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

    def onThemeItemAddFinished(self):
        """Add completion
        """
        return

    def onThemeItemAdded(self, row, col, name, path):
        """
        :param row:            Row
        :param col:            List
        :param name:           name
        :param path:           path
        """
        self.lastRow = row
        self.lastCol = col
        self.gridLayout.addWidget(
            SkinBaseItemWidget(
                name, os.path.join(os.path.dirname(path), 'preview.png'),
                Signals.themeItemClicked, self), row, col)
