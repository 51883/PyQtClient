#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.UpdateDialog
@description: Update dialog
"""
from PyQt5.QtCore import Qt

from Widgets.Dialogs.MoveDialog import MoveDialog
from UiFiles.Ui_UpdateDialog import Ui_FormUpdateDialog
from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class UpdateDialog(MoveDialog, Ui_FormUpdateDialog):

    def __init__(self, *args, **kwargs):
        super(UpdateDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Automatic destruction after turning off
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # Load mouse style
        ThemeManager.loadCursor(self)
        Signals.updateTextChanged.connect(self.onUpdateTextChanged)
        Signals.updateProgressChanged.connect(self.onUpdateProgressChanged)
        Signals.updateFinished.connect(self.labelMessage.setText)

    def onUpdateTextChanged(self, ver1, ver2, text):
        self.labelMessage.setText(
            self.tr('Update Version {} to Version {}'.format(ver1, ver2)))
        self.plainTextEditDetail.setPlainText(text)

    def onUpdateProgressChanged(self, currentValue, minValue, maxValue):
        self.progressBarUpdate.setRange(minValue, maxValue)
        self.progressBarUpdate.setValue(currentValue)
