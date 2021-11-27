#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.CommonUtil
@description: Public tool
"""
import ctypes
import hashlib
import logging
import os
import platform
import subprocess

from PyQt5.QtCore import QSettings, QTextCodec, QObject, pyqtSignal

from Utils.Constants import LogName, LogFormatterDebug, LogFormatter, ConfigFile


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


def qBound(miv, cv, mxv):
    return max(min(cv, mxv), miv)


def openFolder(path):
    """Open folder
    :param path:        File / folder
    """
    system = platform.system()
    if system.startswith('Window'):
        try:
            path = path.replace('/', '\\')
            ctypes.windll.ole32.CoInitialize(None)
            pidl = ctypes.windll.shell32.ILCreateFromPathW(path)
            ctypes.windll.shell32.SHOpenFolderAndSelectItems(
                pidl, 0, None, 0)
            ctypes.windll.shell32.ILFree(pidl)
            ctypes.windll.ole32.CoUninitialize()
        except:
            path = os.path.dirname(path).replace('/', '\\')
            subprocess.call(['explorer', path])
    elif system.startswith('Darwin'):
        path = os.path.dirname(path).replace('\\', '/')
        subprocess.call(['open', path])
    else:
        path = os.path.dirname(path).replace('\\', '/')
        subprocess.call(['nautilus', path])


def git_blob_hash(path):
    """Git mode calculation file Sha1
    :param path: file path
    """
    data = open(path, 'rb').read().replace(b'\r\n', b'\n')
    data = b'blob ' + str(len(data)).encode() + b'\0' + data
    return hashlib.sha1(data).hexdigest()


def initLog(name, file=None, level=logging.DEBUG, formatter=None):
    """Initializing log record configuration
    :param name:            log name
    :param file:            log file
    :param level:           log level
    :param formatter:       log formatter
    """

    formatter = formatter or logging.Formatter(
        LogFormatterDebug if level == logging.DEBUG else LogFormatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if file != None:
        file = os.path.abspath(str(file))
        file_handler = logging.FileHandler(file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


AppLog = logging.getLogger(LogName)


class Setting:

    _Setting = None

    @classmethod
    def init(cls, parent=None):
        """Initialization configuration example
        :param cls:
        :param parent:
        """
        if not cls._Setting:
            cls._Setting = QSettings(ConfigFile, QSettings.IniFormat, parent)
            cls._Setting.setIniCodec(QTextCodec.codecForName('utf-8'))

    @classmethod
    def value(cls, key, default=None, typ=None):
        """Get the value in the configuration
        :param cls:
        :param key:        Key name
        :param default:    Defaults
        :param typ:        type
        """
        cls.init()
        if default != None and typ != None:
            return cls._Setting.value(key, default, typ)
        if default != None:
            return cls._Setting.value(key, default)
        return cls._Setting.value(key)

    @classmethod
    def setValue(cls, key, value):
        """Update the value in the configuration
        :param cls:
        :param key:        Key name
        :param value:      Key value
        """
        cls.init()
        cls._Setting.setValue(key, value)
        cls._Setting.sync()


class _Signals(QObject):

    # Display code
    showCoded = pyqtSignal(str)
    # showReadme.md
    showReadmed = pyqtSignal(str)
    # Load URL
    urlLoaded = pyqtSignal(str)
    # Operation example signal
    runExampled = pyqtSignal(str)
    # Filter screening catalog
    filterChanged = pyqtSignal(str)
    # Update schedule (current value, max)
    progressUpdated = pyqtSignal(int, int)
    # Close progress bar
    progressStoped = pyqtSignal()
    # Clone completed
    cloneFinished = pyqtSignal(str)
    # Jump to Item
    itemJumped = pyqtSignal(str)

    # Display Update Dialog
    updateDialogShowed = pyqtSignal()
    # Update version of the text change
    updateTextChanged = pyqtSignal(str, str, str)
    # update completed
    updateFinished = pyqtSignal(str)
    # Update schedule (current value, minimum, max)
    updateProgressChanged = pyqtSignal(int, int, int)

    # Login failed
    loginErrored = pyqtSignal(str)
    # Sign in successfully send users ID and nickname
    loginSuccessed = pyqtSignal(str, str)

    # Add colorful item
    colourfulItemAdded = pyqtSignal(int, int, str, object)
    # Add colorful item to complete
    colourfulItemAddFinished = pyqtSignal()
    # Colorful items click, color
    colourfulItemClicked = pyqtSignal(str, object)

    # Add theme Item
    themeItemAdded = pyqtSignal(int, int, str, object)
    # Add the topic Item
    themeItemAddFinished = pyqtSignal()
    # Main push Item click, path
    themeItemClicked = pyqtSignal(str, object)

    # Category image download Complete and add Item
    pictureItemAdded = pyqtSignal(object, int, str, str)
    # Category Image Item Click, Path
    pictureItemClicked = pyqtSignal(str, object)
    # Single classification download
    pictureDownFinished = pyqtSignal(object)


# To put it bluntly, it is the global signal definition.
Signals = _Signals()
