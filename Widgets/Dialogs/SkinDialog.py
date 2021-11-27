#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.SkinDialog
@description: 
"""

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QPushButton, QButtonGroup

from UiFiles.Ui_SkinDialog import Ui_FormSkinDialog
from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog
from Widgets.Layouts.FlowLayout import FlowLayout
from Widgets.Skins.PictureWidget import PictureWidget
from Widgets.Skins.PreviewWidget import PreviewWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class SkinDialog(MoveDialog, Ui_FormSkinDialog):

    def __init__(self, *args, **kwargs):
        super(SkinDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widgetBottom.setVisible(False)
        # Preview interface
        self.previewWidget = PreviewWidget(self.widgetSkinBg)
        self.previewWidget.setVisible(False)
        # Initialization signal groove
        self._initSignals()
        # Load mouse style
        ThemeManager.loadCursor(self)
        self.on_tabWidgetSkinMain_currentChanged(0)

    def _initSignals(self):
        Signals.pictureItemAdded.connect(self.onPictureItemAdded)
        Signals.pictureDownFinished.connect(self.onPictureDownFinished)
        # Click on a topic
        Signals.themeItemClicked.connect(self.onThemeItemClicked)
        # Click on color
        Signals.colourfulItemClicked.connect(self.onColourfulItemClicked)
        # Click on the picture
        Signals.pictureItemClicked.connect(self.onPictureItemClicked)
        # Previous
        self.previewWidget.buttonPreviewPrevious.clicked.connect(
            self.onPreviewPrevious)
        # Next
        self.previewWidget.buttonPreviewNext.clicked.connect(
            self.onPreviewNext)

    def onPreviewPrevious(self):
        """Previous
        """
        w = self.tabWidgetSkinMain.currentWidget()
        if w == self.tabPicture:
            self.categoryBtnGroups.checkedButton().property('widget').doPreviewPrevious()
        else:
            w.doPreviewPrevious()

    def onPreviewNext(self):
        """Next
        """
        w = self.tabWidgetSkinMain.currentWidget()
        if w == self.tabPicture:
            self.categoryBtnGroups.checkedButton().property('widget').doPreviewNext()
        else:
            w.doPreviewNext()

    def onThemeItemClicked(self, name, path):
        """
        :param name:        Theme name
        :param path:        Theme preview path
        """
        self.previewWidget.setVisible(True)
        self.previewWidget.setTitle(name)
        self.previewWidget.setPixmap(PreviewWidget.Theme, path)

    def onColourfulItemClicked(self, name, color):
        """
        :param name:        Color name
        :param color:       colour
        """
        self.previewWidget.setVisible(True)
        self.previewWidget.setTitle(name)
        self.previewWidget.setPixmap(PreviewWidget.Color, color)

    def onPictureItemClicked(self, name, path):
        """
        :param name:        Wallpaper name
        :param path:        Wallpaper path
        """
        self.previewWidget.setVisible(True)
        self.previewWidget.setTitle(name)
        self.previewWidget.setPixmap(PreviewWidget.Picture, path)

    def on_tabWidgetSkinMain_currentChanged(self, index):
        """Tab tag switch"""
        w = self.tabWidgetSkinMain.widget(index)
        if w == self.tabPicture:
            if self.stackedWidgetPictures.count() > 0:
                return
            self.initCategories()
        else:
            w.init()

    def initCategories(self):
        """Add a classification tab
        :param categories:        Classification
        """
        self.categoryLayout = FlowLayout(self.widgetCategories)
        self.categoryLayout.setSpacing(10)
        self.categoryBtnGroups = QButtonGroup(self)
        self.categoryBtnGroups.buttonToggled.connect(self.onCategoryChanged)
        for category in ('4K', '双屏', '美女', '动漫', '风景', '明星', '萌宠', '游戏', '科技', '其他'):
            button = QPushButton(category, self.widgetCategories)
            button.setCheckable(True)
            self.categoryBtnGroups.addButton(button)
            self.categoryLayout.addWidget(button)
            widget = PictureWidget(category, self.stackedWidgetPictures)
            button.setProperty('widget', widget)
            self.stackedWidgetPictures.addWidget(widget)
        self.categoryBtnGroups.buttons()[0].setChecked(True)

    def onCategoryChanged(self, button, toggled):
        """Classification switch
        :param button:        Category button
        :param toggled:       Is it selected?
        """
        if not toggled:
            return
        widget = button.property('widget')
        self.stackedWidgetPictures.setCurrentWidget(widget)
        runnable = widget.init()
        if runnable:
            if not hasattr(self, '_threadPool'):
                self._threadPool = QThreadPool(self)
                self._threadPool.setMaxThreadCount(5)
            widget.showWaiting()
            self._threadPool.start(runnable)

    def onPictureDownFinished(self, widget):
        widget.showWaiting(False)

    def onPictureItemAdded(self, widget, index, title, path):
        """Add Category Image Item
        :param widget:            PictureWidget corresponding to this classification
        :param index:             Serial number
        :param title:             title
        :param path:              Picture path
        """
        widget.addItem(index, title, path)

    def showEvent(self, event):
        super(SkinDialog, self).showEvent(event)
        self.previewWidget.setGeometry(self.widgetSkinBg.rect())
