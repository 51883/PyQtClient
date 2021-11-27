#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.LoginDialog
@description: Login dialog
"""
import base64
import os

from PyQt5.QtCore import Qt, pyqtSlot, QVariant, QTimer
from PyQt5.QtWidgets import QCompleter

from UiFiles.Ui_LoginDialog import Ui_FormLoginDialog
from Utils import Constants
from Utils.CommonUtil import AppLog, Setting, Signals
from Utils.GitThread import LoginThread
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog
from Widgets.Dialogs.TwinkleDialog import TwinkleDialog


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginDialog(MoveDialog, TwinkleDialog, Ui_FormLoginDialog):

    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Set flashing target control
        self.setTarget(self.widgetLogin)
        # Automatic destruction after turning off
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # Load mouse style
        ThemeManager.loadCursor(self)
        # Load mouse style
        ThemeManager.loadCursor(self.buttonHead, ThemeManager.CursorPointer)
        # Is it logged in?
        self._isLogin = False
        Signals.loginErrored.connect(self.onLoginErrored)
        Signals.loginSuccessed.connect(self.onLoginSuccessed)
        QTimer.singleShot(100, self.initAccount)

    def initAccount(self):
        # Automatically populate account password
        self._accounts = Setting.value('accounts', {}, QVariant)
        completer = QCompleter(self._accounts.keys(), self.lineEditAccount)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        # Automatic filling completion
        completer.setCompletionMode(QCompleter.InlineCompletion)
        # Set ObjectName to set the style
        # completer.popup().setObjectName('lineEditAccountAuto')
        self.lineEditAccount.setCompleter(completer)

        # Read the stored account password
        account = Setting.value('account', '', str)
        self.lineEditAccount.setText(account)

    def on_lineEditAccount_textChanged(self, account):
        """Enter the box edit the completion signal, find if the avatar file exists
        """
        if account not in self._accounts:  # does not exist
            return
        # Fill password
        try:
            self.lineEditPassword.setText(base64.b85decode(
                self._accounts[account][1].encode()).decode())
        except Exception as e:
            self.lineEditPassword.setText('')
            AppLog.exception(e)
        # Update avatar
        path = os.path.join(Constants.ImageDir, self._accounts[account][0]).replace(
            '\\', '/') + '.jpg'
        if os.path.exists(path) and self.buttonHead.image != path:
            # Replace avatar
            self.buttonHead.image = path

    def onLoginErrored(self, message):
        AppLog.debug('onLoginErrored')
        self._isLogin = False
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        AppLog.error(message)
        if message:
            self.labelNotice.setText(message)

    def onLoginSuccessed(self, uid, name):
        AppLog.debug('onLoginSuccessed')
        self._isLogin = False
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        # Instant GitHub Access Object with Account Password
        account = self.lineEditAccount.text().strip()
        password = self.lineEditPassword.text().strip()
        Constants._Account = account
        Constants._Password = password
        Constants._Username = name
        # Storage account password
        Setting.setValue('account', account)
        if account not in self._accounts:
            # Update account array
            self._accounts[account] = [
                uid, base64.b85encode(password.encode()).decode()]
            Setting.setValue('accounts', self._accounts)
        self.accept()

    def setEnabled(self, enabled):
        self.buttonClose.setEnabled(enabled)
        self.lineEditAccount.setEnabled(enabled)
        self.lineEditPassword.setEnabled(enabled)
        self.buttonLogin.setEnabled(enabled)

    @pyqtSlot()
    def on_buttonLogin_clicked(self):
        # Login click
        account = self.lineEditAccount.text().strip()
        password = self.lineEditPassword.text().strip()
        if not account:
            self.labelNotice.setText(self.tr('Incorrect account'))
            return
        if not password:
            self.labelNotice.setText(self.tr('Incorrect password'))
            return
        self.labelNotice.setText('')
        self.setEnabled(False)
        self.buttonLogin.showWaiting(True)
        LoginThread.start(account, password)
