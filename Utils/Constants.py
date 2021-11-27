#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Constants
@description: constant
"""

from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkRequest


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

RoleRoot = Qt.UserRole + 1            # Root catalog
RolePath = Qt.UserRole + 2          # Item absolute
RoleValue = Qt.UserRole + 3         # Item current progress bar
RoleTotal = Qt.UserRole + 4         # Item progress bar total value
RoleCode = Qt.UserRole + 5          # Item code

HomeFile = 'Resources/Markdown/index.html'

ConfigFile = 'Resources/Data/Config.ini'
UpgradeFile = 'Resources/Data/Upgrade/Upgrade.{}.zip'

ImageDir = 'Resources/Images/Avatars'
ImageAvatar = 'Resources/Images/Avatars/avatar.png'

LogName = 'PyQtClient'
LogFormatterDebug = '[%(asctime)s %(name)s %(module)s:%(funcName)s:%(lineno)s] %(levelname)-8s %(message)s'
LogFormatter = '[%(asctime)s %(name)s] %(levelname)-8s %(message)s'
LogFile = 'Resources/Data/app.log'

DirWallpaper = 'Resources/Images/Wallpaper'      # Wallpaper catalog
DirThemes = 'Resources/Themes'                   # Topic catalog
DirErrors = 'Resources/Data/Errors'              # Error log directory
DirProject = 'Resources/Data/Projects'           # Local project catalog
DirProjects = 'Resources/Data/Projects/PyQt'     # Local project catalog
DirCurrent = 'Resources/Data/Projects/PyQt'      # Current readme.md directory
CurrentReadme = ''                               # Current load readme.md path

AttrCallback = QNetworkRequest.User + 1
AttrFilePath = QNetworkRequest.User + 2
UrlProject = 'https://github.com/PyQt5/PyQtClient'
UrlQQ = 'tencent://message/?uin=892768447'
UrlGroup = 'tencent://groupwpa/?subcmd=all&param=7B2267726F757055696E223A3234363236393931392C2274696D655374616D70223A313531383537323831357D0A'
UrlIssues = 'https://github.com/PyQt5/PyQtClient/issues/new'
UrlGetAppsByCategory = 'http://bizhi.ludashi.com/live/wallpaper/categoryList?category={category}&pageno={pageno}&count={count}&type=1&_={time}'

_Sha = ''
_Account = ''
_Password = ''
_Username = ''
