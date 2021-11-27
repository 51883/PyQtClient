#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月11日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.DonateDialog
@description: Donation dialog
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from UiFiles.Ui_DonateDialog import Ui_FormDonateDialog
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class DonateDialog(MoveDialog, Ui_FormDonateDialog):

    def __init__(self, alipayImg, wechatImg, *args, **kwargs):
        super(DonateDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Automatic destruction after turning off
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # Load mouse style
        ThemeManager.loadCursor(self)
        # Load mouse style
        ThemeManager.loadCursor(self.labelAlipayImg)
        ThemeManager.loadCursor(self.labelWechatImg,
                                ThemeManager.CursorPointer)
        # Load picture
        self.labelAlipayImg.setPixmap(QPixmap(alipayImg).scaled(
            300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.labelWechatImg.setPixmap(QPixmap(wechatImg).scaled(
            300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
