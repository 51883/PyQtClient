#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.MainWindow
@description:
"""
import cgitb
import os
from random import randint
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSlot, QUrl, QProcess,\
    QProcessEnvironment, QLibraryInfo, QCoreApplication
from PyQt5.QtGui import QEnterEvent, QIcon

from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import initLog, AppLog, Setting
from Utils.GitThread import CloneThread, UpgradeThread
from Widgets.Dialogs.DonateDialog import DonateDialog
from Widgets.Dialogs.ErrorDialog import ErrorDialog
from Widgets.Dialogs.LoginDialog import LoginDialog
from Widgets.Dialogs.UpdateDialog import UpdateDialog
from Widgets.FramelessWindow import FramelessWindow
from Widgets.MainWindowBase import MainWindowBase


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Setting.init(self)
        self._initLanguage()
        self._initUi()
        self._initSignals()
        # Load the window size and restore
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        # Display login dialog after 200 milliseconds
        QTimer.singleShot(200, self._initCatalog)
        QTimer.singleShot(500, self.treeViewCatalogs.initCatalog)
        # Initialization web page
        QTimer.singleShot(500, self._initWebView)
        # Check for updates
        QTimer.singleShot(5000, UpgradeThread.start)
        # Display donation window
        QTimer.singleShot(
            randint(1000 * 60 * 5, 2000 * 60 * 5), self._initDonate)

    def initLogin(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        # Refresh avatar style
        if Constants._Account != '' and Constants._Password != '':
            self.buttonHead.image = Constants.ImageAvatar
            self.buttonHead.setToolTip(Constants._Username)

    def _initDonate(self):
        # Display donation window
        alipayImg = os.path.join(
            Constants.DirProjects, 'Donate', 'zhifubao.png')
        wechatImg = os.path.join(Constants.DirProjects, 'Donate', 'weixin.png')
        if os.path.exists(alipayImg) and os.path.exists(wechatImg):
            dialog = DonateDialog(alipayImg, wechatImg, self)
            dialog.exec_()

    def _initUpdate(self):
        # Display Update Dialog
        self.udialog = UpdateDialog()
        self.udialog.show()

    def _initCatalog(self):
        # Update directory
        self._showNotice(QCoreApplication.translate(
            'MainWindow', 'Update Example Started'))
        CloneThread.start()

    @pyqtSlot(str)
    def renderCode(self, code):
        """Display code
        """
        content = repr(code)
        self._runJs("updateCode({});".format(content))

    @pyqtSlot(str)
    def renderReadme(self, path=''):
        """Load README.MD and display
        """
        path = path.replace('\\', '/')
        if not path:
            path = os.path.join(Constants.DirProjects, 'README.md')
            Constants.CurrentReadme = ''
        elif path.count('/') == 0:
            path = os.path.join(Constants.DirCurrent, path, 'README.md')
            Constants.CurrentReadme = path
        elif not path.endswith('README.md'):
            path = path + '/README.md'
            Constants.CurrentReadme = path
        if not os.path.exists(path):
            AppLog.debug('{} not exists'.format(path))
            self._runJs('updateText("");')
            return
        if not os.path.isfile(path):
            AppLog.warn('file {} not exists'.format(path))
            return
        Constants.DirCurrent = os.path.dirname(path).replace('\\', '/')
        AppLog.debug('DirCurrent change to: {}'.format(Constants.DirCurrent))
        AppLog.debug('render: {}'.format(path))
        Constants.CurrentReadme = path      # Record the path to prevent duplicate loading
        AppLog.debug('readme dir: {}'.format(Constants.DirCurrent))
        content = repr(open(path, 'rb').read().decode())
        self._runJs("updateText({});".format(content))

    def _exposeInterface(self):
        """Exposure to JS calls the local method interface
        """
        self.webViewContent.page().mainFrame().addToJavaScriptWindowObject('_mainWindow', self)

    def _runFile(self, file):
        """Sub process running file
        :param file:    document
        """
        file = os.path.abspath(file)
        process = QProcess(self)
        process.setProperty('file', file)
        process.readChannelFinished.connect(self.onReadChannelFinished)

        env = QProcessEnvironment.systemEnvironment()
#         libpath = get_python_lib()
#         env.insert('QT_QPA_PLATFORM_PLUGIN_PATH', os.path.join(
#             libpath, 'PyQt5', 'Qt', 'plugins', 'platforms'))
#         env.insert('QT_QPA_PLATFORM_PLUGIN_PATH',
#                    os.path.abspath('platforms'))
        env.insert('QML_IMPORT_PATH', os.path.abspath('qml'))
        env.insert('QML2_IMPORT_PATH', env.value('QML_IMPORT_PATH'))
        if os.name == 'nt':
            env.insert(
                'PATH', QLibraryInfo.location(
                    QLibraryInfo.BinariesPath) + os.pathsep + env.value('PATH')
            )
        env.insert(
            'PATH', os.path.dirname(
                os.path.abspath(sys.argv[0])) + os.pathsep + env.value('PATH')
        )
        process.setProcessEnvironment(env)

#         if sys.executable.endswith('python.exe'):
        process.setWorkingDirectory(os.path.dirname(file))
        process.start(sys.executable, [file])

    def _runJs(self, code):
        """Execute JS
        :param code:
        """
        self.webViewContent.page().mainFrame().evaluateJavaScript(code)

    def onReadChannelFinished(self):
        process = self.sender()
        message = process.readAllStandardError().data()
        try:
            message = message.decode(errors='ignore')
        except Exception as e:
            AppLog.exception(e)
            return
        if process.exitCode() != 0 and len(message.strip()) > 0:
            file = str(process.property('file'))
            reqfile = os.path.abspath(os.path.join(
                os.path.dirname(file), 'requirements.txt'))
            AppLog.debug('reqfile: {}'.format(reqfile))
            dialog = ErrorDialog(message, self, reqfile=reqfile)
            dialog.exec_()

    def onUrlLoaded(self, name):
        """Loading the parametric URL
        :param name:
        """
        url = QUrl.fromLocalFile(os.path.abspath(Constants.HomeFile))
        url.setQuery('name={}'.format(name))
        self.webViewContent.load(url)

    def onLinkClicked(self, url):
        """Load URL
        :param url:
        """
        self.webViewContent.load(QUrl(url))

    def closeEvent(self, event):
        # Storage window location
        Setting.setValue('geometry', self.saveGeometry())
        super(MainWindow, self).closeEvent(event)

    def eventFilter(self, obj, event):
        # Event filter
        if obj == self.widgetMain and isinstance(event, QEnterEvent):
            # Restored to standard mouse styles after solving the mouse to enter other controls
            self.setCursor(Qt.ArrowCursor)
        return FramelessWindow.eventFilter(self, obj, event)

    def changeEvent(self, event):
        # Window change event
        FramelessWindow.changeEvent(self, event)
        if event.type() == QEvent.WindowStateChange:  # Window status change
            state = self.windowState()
            if state == (state | Qt.WindowMaximized):
                # Maximize the status, display the restore button
                self.buttonMaximum.setVisible(False)
                self.buttonNormal.setVisible(True)
            else:
                # Hide Restore button
                self.buttonMaximum.setVisible(True)
                self.buttonNormal.setVisible(False)


def main():
    if int(QtCore.PYQT_VERSION_STR.split('.')[1]) > 5:
        # for > Qt 5.5
        os.putenv('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    else:
        # for Qt 5.5
        os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    if os.name == 'nt':
        os.environ['PATH'] = QLibraryInfo.location(
            QLibraryInfo.BinariesPath) + os.pathsep + os.environ['PATH']
    os.makedirs(Constants.DirErrors, exist_ok=True)
    os.makedirs(Constants.DirProject, exist_ok=True)
    os.makedirs(os.path.dirname(Constants.UpgradeFile), exist_ok=True)
    # Abnormal capture
    sys.excepthook = cgitb.Hook(1, Constants.DirErrors, 5, sys.stderr, '')
    # Initialization log
    initLog(Constants.LogName, Constants.LogFile)
    # Run app
    app = QSingleApplication('qtsingleapp-pyqtclient', sys.argv)
    if app.isRunning():
        # Activate window
        app.sendMessage('show', 1000)
    else:
        app.setQuitOnLastWindowClosed(True)
        app.setWindowIcon(QIcon('Resources/Images/app.ico'))
        # First run
        w = MainWindow()
        app.setActivationWindow(w)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir('../')
    main()
