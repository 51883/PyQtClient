#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.ThemeThread
@description: 
"""
import os
from pathlib import Path
from time import time

from PyQt5.QtCore import QObject, QThread, QRunnable
from PyQt5.QtGui import QLinearGradient, QColor
import requests

from Utils.CommonUtil import AppLog, Signals
from Utils.Constants import DirThemes, UrlGetAppsByCategory, DirWallpaper


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

Headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6824.400 QQBrowser/10.3.3137.400'
}


def splistList(src, length):
    # Aliquot list
    return [src[i:i + length] for i in range(len(src)) if i % length == 0]


class ColourfulThread(QObject):
    """Get all color schemes
    """

    def __init__(self, width, height, *args, **kwargs):
        super(ColourfulThread, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    @classmethod
    def start(cls, width, height, parent=None):
        """Start thread
        :param cls:
        :param width:
        :param height:
        :param parent:
        """
        cls._thread = QThread(parent)
        cls._worker = ColourfulThread(width, height)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('colourful thread started')

    def run(self):
        AppLog.info('start get all colourful')
        # Midnight Paris
        mcolor = QLinearGradient(0, 0, self.width, self.height)
        mcolor.ex = 1
        mcolor.ey = 1
        mcolor.startColor = QColor(20, 179, 255, 255)
        mcolor.endColor = QColor(226, 14, 255, 255)
        mcolor.setColorAt(0, mcolor.startColor)
        mcolor.setColorAt(1, mcolor.endColor)
        # Caosary
        pcolor = QLinearGradient(0, 0, self.width, self.height)
        pcolor.ex = 1
        pcolor.ey = 1
        pcolor.startColor = QColor(0, 173, 246, 255)
        pcolor.endColor = QColor(0, 234, 155, 255)
        pcolor.setColorAt(0, pcolor.startColor)
        pcolor.setColorAt(1, pcolor.endColor)
        # Autumn warm sun
        acolor = QLinearGradient(0, 0, self.width, self.height)
        acolor.ex = 1
        acolor.ey = 1
        acolor.startColor = QColor(255, 128, 27, 255)
        acolor.endColor = QColor(255, 0, 14, 255)
        acolor.setColorAt(0, acolor.startColor)
        acolor.setColorAt(1, acolor.endColor)

        defaults = splistList([
            [self.tr('MidnightParis'), mcolor],             # Midnight Paris
            [self.tr('PrimroseGreenOnion'), pcolor],        # Caosary
            [self.tr('AutumnSun'), acolor],                 # Autumn warm sun
            [self.tr('LightGray'), QColor(236, 236, 236)],  # Putty
            [self.tr('DarkBlack'), QColor(33, 33, 33)],     # Dark black
            [self.tr('BlueGreen'), QColor(0, 190, 172)],    # blue-green
            [self.tr('Orange'), QColor(255, 152, 0)],       # Orange
            [self.tr('Brown'), QColor(140, 100, 80)],       # Brown
            [self.tr('Green'), QColor(121, 190, 60)],       # green
            [self.tr('Pink'), QColor(236, 98, 161)],        # pink
            [self.tr('Purple'), QColor(103, 58, 183)],      # Purple
            [self.tr('Blue'), QColor(0, 188, 212)],         # blue
            [self.tr('GreyBlue'), QColor(80, 126, 164)],    # grey blue
            [self.tr('Red'), QColor(244, 94, 99)],          # Red
        ], 5)

        for row, default in enumerate(defaults):
            for col, (name, color) in enumerate(default):
                Signals.colourfulItemAdded.emit(row, col, name, color)
                QThread.msleep(100)
                QThread.yieldCurrentThread()

        Signals.colourfulItemAddFinished.emit()
        AppLog.info('colourful thread end')


class ThemeThread(QObject):
    """Get all themes (local and clouds)
    """

    def __init__(self, width, height, *args, **kwargs):
        super(ThemeThread, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    @classmethod
    def start(cls, width, height, parent=None):
        """Start thread
        :param cls:
        :param width:        width
        :param height:        height
        :param parent:
        """
        cls._thread = QThread(parent)
        cls._worker = ThemeThread(width, height)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('theme thread started')

    def run(self):
        AppLog.info('start get all theme')

        defaults = [[p.parent.name, str(p)]
                    for p in Path(DirThemes).rglob('style.qss')]

        defaults = splistList(defaults, 5)

        for row, default in enumerate(defaults):
            for col, (name, path) in enumerate(default):
                Signals.themeItemAdded.emit(row, col, name, path)
                QThread.msleep(100)
                QThread.yieldCurrentThread()

        Signals.themeItemAddFinished.emit()
        AppLog.info('theme thread end')


class GetAllCategoryRunnable(QRunnable):

    def __init__(self, category, widget, *args, **kwargs):
        super(GetAllCategoryRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)
        self.category = category
        self.widget = widget

    def download(self, index, title, url):
        try:
            dirPath = os.path.join(DirWallpaper, self.category)
            os.makedirs(dirPath, exist_ok=True)
            path = os.path.join(dirPath, os.path.basename(url))
            if os.path.exists(path) and os.path.isfile(path):
                Signals.pictureItemAdded.emit(
                    self.widget, index, title, path)
                return
            req = requests.get(url, headers=Headers)
            if req.status_code == 200:
                with open(path, 'wb') as fp:
                    fp.write(req.content)
                Signals.pictureItemAdded.emit(
                    self.widget, index, title, path)
        except Exception as e:
            AppLog.exception(e)

    def run(self):
        try:
            req = requests.get(UrlGetAppsByCategory.format(
                category=self.category, pageno=1, count=20, time=time()))
            content = req.json()
            errno = content.get('errno', 0)
            AppLog.debug('errno: %s', errno)
            AppLog.debug('msg: %s', content.get('msg', ''))
            if errno != 0:
                return

            content = content.get('data', {})
            AppLog.debug('total_count: %s', content.get('total_count', ''))
            AppLog.debug('total_page: %s', content.get('total_page', ''))
            items = content.get('list', [])

            for i, item in enumerate(items):
                title = item.get('title', '')
                url = item.get('image', None)
                if not url:
                    continue
                self.download(i, title, url)
                QThread.msleep(200)
                QThread.yieldCurrentThread()
        except Exception as e:
            AppLog.exception(e)
        Signals.pictureDownFinished.emit(self.widget)
