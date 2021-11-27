#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.TwinkleDialog
@description: windows Dialog Border Flashing
"""
import os

from PyQt5.QtWidgets import QDialog

if os.name == 'nt':
    import ctypes.wintypes

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

WM_NCACTIVATE = 0x0086


class TwinkleDialog:

    def setTarget(self, widget):
        """Set flashing target control
        :param widget:        Target control
        """
        self._targetWidget = widget
        self._targetWidget.setProperty('_active', True)

    def activeAnimation(self, actived):
        """Border flashing animation
        :param actived: Activate now
        """
        if not hasattr(self, '_targetWidget'):
            return
        self._targetWidget.setProperty('_active', actived)
        # Refresh style
        self.style().polish(self._targetWidget)

    if os.name == 'nt':

        def nativeEvent(self, eventType, message):
            retval, result = QDialog.nativeEvent(self, eventType, message)
            if eventType == 'windows_generic_MSG' and hasattr(self, '_targetWidget'):
                msg = ctypes.wintypes.MSG.from_address(message.__int__())
                if msg.message == WM_NCACTIVATE:
                    # Draw the border effect of the modal window
                    self.activeAnimation(msg.wParam == 1)
            return retval, result
