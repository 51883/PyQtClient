#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月10日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.NetworkAccessManager
@description: Web network request class
"""
import mimetypes
import os
import webbrowser

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class NetworkAccessManager(QNetworkAccessManager):

    def __init__(self, *args, **kwargs):
        super(NetworkAccessManager, self).__init__(*args, **kwargs)

    def createRequest(self, op, originalReq, outgoingData):
        """Create request
        :param op:           See the type of operationhttp://doc.qt.io/qt-5/qnetworkaccessmanager.html#Operation-enum
        :param originalReq:  Original request
        :param outgoingData: Output Data
        """
        url = originalReq.url()
        surl = url.toString()
        AppLog.debug('access url: {}'.format(surl))

        if surl.endswith('Donate'):
            # Click to reward
            originalReq.setUrl(QUrl())
            return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)
        elif surl.endswith('k=5QVVEdF'):
            # Click on the QQ group link
            webbrowser.open(Constants.UrlGroup)
            originalReq.setUrl(QUrl())
            return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)

        if url.scheme() == 'tencent':
            # Call TX APP
            webbrowser.open(surl)
            originalReq.setUrl(QUrl())
        elif url.scheme() == 'file':
            # Local files, such as some picture files, etc.
            names = surl.split('Markdown/')
            if len(names) > 1:
                rname = names[1]
                path = os.path.join(
                    Constants.DirCurrent, rname).replace('\\', '/')
                if os.path.exists(path) and os.path.isfile(path):
                    if rname[-3:] == '.py':
                        originalReq.setUrl(QUrl())
                        # Run the PY file
                        Signals.runExampled.emit(path)
                    else:
                        originalReq.setUrl(QUrl.fromLocalFile(path))
                elif os.path.exists(path) and os.path.isdir(path):
                    if rname.count('/') == 0:
                        # Jump to the left directory tree
                        originalReq.setUrl(QUrl())
                        Signals.itemJumped.emit(rname)
        else:
            # Only load files, do not load other pages
            if not mimetypes.guess_type(url.fileName())[0]:
                originalReq.setUrl(QUrl())
                # Call system open web page
                webbrowser.open_new_tab(surl)

        return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)
