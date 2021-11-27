#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月30日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.PreviewWidget
@description: Theme preview
"""
import os

from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect

from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from UiFiles.Ui_PreviewWidget import Ui_FormPreviewWidget
from Utils.CommonUtil import Setting
from Utils.GradientUtils import GradientUtils
from Utils.ThemeManager import ThemeManager


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class PreviewWidget(QWidget, Ui_FormPreviewWidget):

    Theme = 0
    Color = 1
    Picture = 2

    def __init__(self, *args, **kwargs):
        super(PreviewWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # Support style
        # Picture edge shadow effect
        effect = QGraphicsDropShadowEffect(self.labelPreviewImage)
        effect.setBlurRadius(40)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.labelPreviewImage.setGraphicsEffect(effect)
        # Mouse style
        ThemeManager.loadCursor(self, ThemeManager.CursorDefault)
        ThemeManager.loadCursor(self.buttonPreviewApply,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(self.buttonPreviewClose,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(self.buttonPreviewNext,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(
            self.buttonPreviewPrevious, ThemeManager.CursorPointer)

    def setTitle(self, title):
        """Set the title
        :param title:
        """
        self.labelPreviewTitle.setText(title)
        self.setWindowTitle(title)

    def setPixmap(self, which, poc):
        """Set pictures
        :param which:        Theme = 0,Color = 1,Picture = 2
        :param poc:          color or path
        """
        self._which = which
        self._poc = poc
        if not hasattr(self, '_UiMainWindow'):
            # Create a hidden main interface
            self._UiMainWindow = QWidget()
            ui = Ui_FormMainWindow()
            ui.setupUi(self._UiMainWindow)
            # Modify the name to prevent the app's style impact
            ui.widgetMain.setObjectName('widgetMain1')
            self._UiMainWindow.setAttribute(Qt.WA_TranslucentBackground, True)
            self._UiMainWindow.setWindowFlags(
                self.windowFlags() | Qt.FramelessWindowHint)
            self._UiMainWindow.hide()
        if which == self.Theme:
            self.labelPreviewImage.setPixmap(
                QPixmap(poc).scaledToWidth(400, Qt.SmoothTransformation))
            return
        elif which == self.Color:
            ThemeManager.loadColourfulTheme(poc, self._UiMainWindow, {
                                            'widgetMain': 'widgetMain1'})
        elif which == self.Picture:
            ThemeManager.loadPictureTheme(poc, self._UiMainWindow, {
                                          'widgetMain': 'widgetMain1'})
        # Screenshot of hidden window
        # As for why it is delayed, it may not be refreshed after setting the style.
        self._UiMainWindow.repaint()
        QTimer.singleShot(100, self._updatePixmap)

    def _updatePixmap(self):
        poc = self._UiMainWindow.grab().scaledToWidth(400, Qt.SmoothTransformation)
        self.labelPreviewImage.setPixmap(poc)

    @pyqtSlot()
    def on_buttonPreviewClose_clicked(self):
        """Hide yourself
        """
        self.setVisible(False)

    @pyqtSlot()
    def on_buttonPreviewApply_clicked(self):
        """Set the subject
        """
        if self._which == self.Theme:
            ThemeManager.loadUserTheme(
                os.path.basename(os.path.dirname(self._poc)))
            Setting.setValue('picture', None)
            Setting.setValue('colourful', None)
        elif self._which == self.Color:
            ThemeManager.loadColourfulTheme(self._poc)
            if isinstance(self._poc, QColor):
                Setting.setValue('colourful', self._poc)
            else:
                # Gradient needs to be converted to dictionary data
                Setting.setValue('colourful', GradientUtils.toJson(self._poc))
            Setting.setValue('picture', None)
        elif self._which == self.Picture:
            ThemeManager.loadPictureTheme(self._poc)
            Setting.setValue('colourful', None)
            Setting.setValue('picture', self._poc.replace('\\', '/'))
