#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月13日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.TreeView
@description: 
"""
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals
from Utils.SortFilterModel import SortFilterModel


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class TreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super(TreeView, self).__init__(*args, **kwargs)
        self._initModel()
        self._initSignals()

    def _initModel(self):
        """Set the directory tree model"""
        self._dmodel = QStandardItemModel(self)
        self._fmodel = SortFilterModel(self)
        self._fmodel.setSourceModel(self._dmodel)
        self.setModel(self._fmodel)

    def _initSignals(self):
        Signals.itemJumped.connect(self.onItemJumped)
        Signals.filterChanged.connect(self._fmodel.setFilterRegExp)
        self.clicked.connect(self.onClicked)
        self.doubleClicked.connect(self.onDoubleClicked)

    def rootItem(self):
        """Get root node item"""
        return self._dmodel.invisibleRootItem()

    def findItems(self, name):
        """Find item according to your name
        :param name:
        """
        return self._dmodel.findItems(name)

    def onItemJumped(self, name):
        items = self.findItems(name)
        if not items:
            return
        index = self._fmodel.mapFromSource(
            self._dmodel.indexFromItem(items[0]))
        self.setCurrentIndex(index)
        self.expand(index)
#         # Show readme
        Signals.urlLoaded.emit(name)

    def listSubDir(self, pitem, path):
        """Travers
        :param item:    Superior Item
        :param path:    contents
        """
        paths = os.listdir(path)
        files = []
        for name in paths:
            spath = os.path.join(path, name)
            if not os.path.isfile(spath):
                continue
            spath = os.path.splitext(spath)
            if len(spath) == 0:
                continue
            if spath[1] == '.py' and spath[0].endswith('__init__') == False:
                files.append(name)

        # Item already exists
        existsItems = [pitem.child(i).text() for i in range(pitem.rowCount())]

        for name in files:
            if name in existsItems:
                continue
            file = os.path.join(path, name).replace('\\', '/')
            item = QStandardItem(name)
            # Add custom data
            item.setData(False, Constants.RoleRoot)       # Not rooted
            item.setData(file, Constants.RolePath)
            try:
                item.setData(open(file, 'rb').read().decode(
                    errors='ignore'), Constants.RoleCode)
            except Exception as e:
                AppLog.warn(
                    'read file({}) code error: {}'.format(file, str(e)))
            pitem.appendRow(item)

    def initCatalog(self):
        """Initialize the local repository tree
        """
        AppLog.debug('')
        if not os.path.exists(Constants.DirProjects):
            return
        pitem = self._dmodel.invisibleRootItem()
        # Only traversing the root directory
        for name in os.listdir(Constants.DirProjects):
            file = os.path.join(Constants.DirProjects,
                                name).replace('\\', '/')
            if os.path.isfile(file):  # Skip file
                continue
            if name.startswith('.') or name == 'Donate' or name == 'Test':  # Not shown. The beginning of the file folder
                continue
            items = self.findItems(name)
            if items:
                item = items[0]
            else:
                item = QStandardItem(name)
                # Add custom data
                # Item identity for drawing progress bars
                item.setData(True, Constants.RoleRoot)
                # The absolute path of the directory or file
                item.setData(os.path.abspath(os.path.join(
                    Constants.DirProjects, name)), Constants.RolePath)
                pitem.appendRow(item)
            # Travers
            self.listSubDir(item, file)
        # Sort
        self._fmodel.sort(0, Qt.AscendingOrder)

    def onClicked(self, modelIndex):
        """Item click
        :param modelIndex:        Here is the qmodelindex in the agent model, not true
        """
        root = modelIndex.data(Constants.RoleRoot)
        path = modelIndex.data(Constants.RolePath)
        code = modelIndex.data(Constants.RoleCode)
        AppLog.debug('is root: {}'.format(root))
        AppLog.debug('path: {}'.format(path))
        if not root and os.path.isfile(path) and code:
            # Top right display code
            Signals.showCoded.emit(code)
        if root and os.path.isdir(path):
            if self.isExpanded(modelIndex):
                self.collapse(modelIndex)
            else:
                self.expand(modelIndex)
            # Show readme
            Signals.showReadmed.emit(os.path.join(path, 'README.md'))

    def onDoubleClicked(self, modelIndex):
        """Item double click
        :param modelIndex:        Here is the qmodelindex in the agent model, not true
        """
        root = modelIndex.data(Constants.RoleRoot)
        path = modelIndex.data(Constants.RolePath)
        AppLog.debug('is root: {}'.format(root))
        AppLog.debug('path: {}'.format(path))
        if not root and os.path.isfile(path):
            # Run code
            Signals.runExampled.emit(path)
#         if root and os.path.isdir(path):
#             # Show readme
#             Signals.showReadmed.emit(os.path.join(path, 'README.md'))

    def enterEvent(self, event):
        super(TreeView, self).enterEvent(event)
        # Mouse enters the display scroll bar
        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event):
        super(TreeView, self).leaveEvent(event)
        # The mouse leaves hidden scroll bar
        self.verticalScrollBar().setVisible(False)
