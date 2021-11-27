#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月26日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Dialogs.IssuesDialog
@description: Feedback dialog
"""
from PyQt5.QtCore import Qt

from UiFiles.Ui_IssuesDialog import Ui_FormIssuesDialog
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class IssuesDialog(MoveDialog, Ui_FormIssuesDialog):

    def __init__(self, *args, **kwargs):
        super(IssuesDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Automatic destruction after turning off
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # Load mouse style
        ThemeManager.loadCursor(self)
