#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.SortFilterModel
@description: Filter Sort MODEL
"""
from PyQt5.QtCore import QSortFilterProxyModel, Qt


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class SortFilterModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterModel, self).__init__(*args, **kwargs)
        # Ignore the case
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # First column filtering
        self.setFilterKeyColumn(0)
        # automatic
        self.setDynamicSortFilter(True)

#     def lessThan(self, source_left, source_right):
#         # Sort by text length and letters
#         if not source_left.isValid() or not source_right.isValid():
#             return False
#         leftData = self.sourceModel().data(source_left)
#         rightData = self.sourceModel().data(source_right)
#         # return super(SortFilterModel, self).lessThan(source_left,
#         # source_right)
#         return len(leftData) < len(rightData)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # filter
        result = super(SortFilterModel, self).filterAcceptsRow(
            sourceRow, sourceParent)
        if result:
            return result
        else:
            sourceIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
            for k in range(self.sourceModel().rowCount(sourceIndex)):
                if self.filterAcceptsRow(k, sourceIndex):
                    return True
        return False
