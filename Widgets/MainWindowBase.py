#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.MainWindowBase
@description: 
"""
import os
import webbrowser

from PyQt5.QtCore import pyqtSlot, QUrl, QLocale, QTranslator, QCoreApplication
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QApplication, QMenu, QAction

from Utils import Constants
from Utils.CommonUtil import Signals, Setting, AppLog, openFolder
from Utils.GradientUtils import GradientUtils
from Utils.NetworkAccessManager import NetworkAccessManager
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.SkinDialog import SkinDialog
from Widgets.ToolTip import ToolTip


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class MainWindowBase:

    def _initUi(self):
        """Start UI."""
        self.setupUi(self)
        # Hide Restore button
        self.buttonNormal.setVisible(False)
        # Hide the sliding strip of the catalog tree
        self.treeViewCatalogs.verticalScrollBar().setVisible(False)
        # Load mouse style
        ThemeManager.loadCursor(self.widgetMain)
        ThemeManager.setPointerCursors([
            self.buttonHead,            # Main interface
            self.buttonClear,           # Main interface empty button
            self.buttonGithub,          # Github button
            self.buttonQQ,              # QQ button
            self.buttonGroup,           # Group button
            self.buttonBackToUp,        # Back to top button
            self.buttonHome             # Show homepage readme
        ])
        # Installing event filters to restore mouse styles
        self.widgetMain.installEventFilter(self)
        # Binding Back to Top Tips Box
        ToolTip.bind(self.buttonBackToUp)
        ToolTip.bind(self.buttonHome)
        # Avatar prompt control
        ToolTip.bind(self.buttonHead)
        # Load the subject
        colourful = Setting.value('colourful')
        picture = Setting.value('picture', '', str)
        AppLog.debug('colourful: %s', str(colourful))
        AppLog.debug('picture: %s', picture)
        if picture:
            ThemeManager.loadFont()
            ThemeManager.loadPictureTheme(picture)
        elif colourful:
            ThemeManager.loadFont()
            if isinstance(picture, QColor):
                ThemeManager.loadColourfulTheme(colourful)
            else:
                # JSON data conversion
                ThemeManager.loadColourfulTheme(
                    GradientUtils.toGradient(colourful))
        else:
            ThemeManager.loadTheme()

    def _initSignals(self):
        """Initialization signal groove"""
        self.webViewContent.loadFinished.connect(self._exposeInterface)
        self.webViewContent.linkClicked.connect(self.onLinkClicked)
        # Binding signal groove
        Signals.showCoded.connect(self.renderCode)
        Signals.showReadmed.connect(self.renderReadme)
        Signals.urlLoaded.connect(self.onUrlLoaded)
        Signals.runExampled.connect(self._runFile)
        Signals.cloneFinished.connect(lambda: self._showNotice(
            QCoreApplication.translate(
                'MainWindowBase', 'Update Example Finished')))
        Signals.cloneFinished.connect(self.treeViewCatalogs.initCatalog)
        Signals.cloneFinished.connect(self.renderReadme)
        Signals.progressStoped.connect(self.widgetCatalogs.stop)
        Signals.progressUpdated.connect(self.widgetCatalogs.setValue)
        Signals.updateDialogShowed.connect(self._initUpdate)

    def _initLanguage(self):
        """Loading international translation
        """
        if QLocale.system().language() in (QLocale.China, QLocale.Chinese, QLocale.Taiwan, QLocale.HongKong):
            # Loading Chinese
            translator = QTranslator(self)
            translator.load('Resources/pyqtclient_zh_CN.qm')
            QApplication.instance().installTranslator(translator)
            AppLog.info('install local language')

    def _initWebView(self):
        """Initialization web page"""
        # Right-click menu
        self._webviewMenu = QMenu(QCoreApplication.translate(
            'MainWindowBase', 'Menu'), self.webViewContent)
        self._webviewactRun = QAction(
            QCoreApplication.translate(
                'MainWindowBase', 'Run'), self._webviewMenu, triggered=self._doActRun)
        self._webviewactView = QAction(
            QCoreApplication.translate(
                'MainWindowBase', 'View'), self._webviewMenu, triggered=self._doActView)
        self._webviewactFolder = QAction(
            QCoreApplication.translate(
                'MainWindowBase', 'Open'), self._webviewMenu, triggered=self._doActOpen)
        self._webviewMenu.addAction(self._webviewactRun)
        self._webviewMenu.addAction(self._webviewactView)
        self._webviewMenu.addAction(self._webviewactFolder)

        self.webViewContent.customContextMenuRequested.connect(
            self._showWebMenu)
        settings = self.webViewContent.settings()
        # Set the default encoding
        settings.setDefaultTextEncoding('UTF-8')
        # Open developer tools
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        page = self.webViewContent.page()
        # Set the link to click
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        # Use custom network request classes (easy to handle some links)
        page.setNetworkAccessManager(NetworkAccessManager(self.webViewContent))

        # Load Readme
        self.webViewContent.load(QUrl.fromLocalFile(
            os.path.abspath(Constants.HomeFile)))

    def _doActRun(self):
        """Right-click menu running code
        """
        path = self.sender().data()
        Signals.runExampled.emit(path)

    def _doActView(self):
        """Right-click menu viewing code
        """
        path = self.sender().data()
        try:
            code = open(path, 'rb').read().decode(errors='ignore')
            Signals.showCoded.emit(code)
        except Exception as e:
            AppLog.warn(str(e))

    def _doActOpen(self):
        """Right-click menu open folder
        """
        path = self.sender().data()
        openFolder(path)

    def _showWebMenu(self, pos):
        """Display web page Right-click menu
        :param pos:            Click position
        """
        hit = self.webViewContent.page().currentFrame().hitTestContent(pos)
        url = hit.linkUrl()
        if url.isValid():
            path = url.toLocalFile().strip().replace('\\', '/')
            names = path.split('Markdown/')
            if len(names) == 1:
                return
            path = os.path.abspath(os.path.join(
                Constants.DirCurrent, names[1]))
            AppLog.debug('path: {}'.format(path))
            AppLog.debug('isdir: {}'.format(os.path.isdir(path)))
            self._webviewactRun.setData(path)
            self._webviewactView.setData(path)
            self._webviewactFolder.setData(path)
            if os.path.exists(path) and os.path.isdir(path):
                self._webviewactRun.setVisible(False)
                self._webviewactView.setVisible(False)
                self._webviewactFolder.setVisible(True)
            elif os.path.exists(path) and os.path.isfile(path):
                self._webviewactRun.setVisible(True)
                self._webviewactView.setVisible(True)
                self._webviewactFolder.setVisible(True)
            self._webviewMenu.exec_(QCursor.pos())

    def _showNotice(self, message, timeout=2000):
        """Bottom display prompt
        :param message:        Prompt message
        """
        if hasattr(self, '_tip'):
            self._tip._hideTimer.stop()
            self._tip.close()
            self._tip.deleteLater()
            del self._tip
        self._tip = ToolTip()
        self._tip.setText(message)
        self._tip.show()
        self._tip.move(
            self.pos().x() + int((self.width() - self._tip.width()) / 2),
            self.pos().y() + self.height() - 60,
        )
        self._tip._hideTimer.timeout.connect(self._tip.close)
        self._tip._hideTimer.start(timeout)

    @pyqtSlot()
    def on_buttonSkin_clicked(self):
        """Select theme style
        """
        if not hasattr(self, 'skinDialog'):
            self.skinDialog = SkinDialog(self)
        self.skinDialog.exec_()

    @pyqtSlot()
    def on_buttonIssues_clicked(self):
        """Advice
        """
        webbrowser.open_new_tab(Constants.UrlIssues)

    @pyqtSlot()
    def on_buttonMinimum_clicked(self):
        """Minimization
        """
        self.showMinimized()

    @pyqtSlot()
    def on_buttonMaximum_clicked(self):
        """maximize
        """
        self.showMaximized()

    @pyqtSlot()
    def on_buttonNormal_clicked(self):
        """reduction
        """
        self.showNormal()

    @pyqtSlot()
    def on_buttonClose_clicked(self):
        """closure
        """
        self.close()

    @pyqtSlot()
    def on_buttonHead_clicked(self):
        """Click on the avatar
        """
        if Constants._Account != '' and Constants._Password != '':
            self.renderReadme()
        else:
            self.initLogin()

    def on_lineEditSearch_textChanged(self, text):
        """Filter screening
        """
        Signals.filterChanged.emit(text)

    @pyqtSlot()
    def on_buttonClear_clicked(self):
        """Click the empty button
        """
        self.lineEditSearch.setText('')

    @pyqtSlot()
    def on_buttonGithub_clicked(self):
        """Click the project button
        """
        webbrowser.open_new_tab(Constants.UrlProject)

    @pyqtSlot()
    def on_buttonQQ_clicked(self):
        """Click the QQ button
        """
        webbrowser.open(Constants.UrlQQ)

    @pyqtSlot()
    def on_buttonGroup_clicked(self):
        """Click the group button
        """
        webbrowser.open(Constants.UrlGroup)

    @pyqtSlot()
    def on_buttonBackToUp_clicked(self):
        """Click the back button
        """
        self._runJs('backToUp();')

    @pyqtSlot()
    def on_buttonHome_clicked(self):
        """Home Readme
        """
        self.renderReadme()
