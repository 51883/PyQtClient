#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.ThemeManager
@description: Subject management
"""
import os

from PyQt5.QtGui import QFontDatabase, QCursor, QPixmap, QLinearGradient,\
    QRadialGradient, QConicalGradient
from PyQt5.QtWidgets import QApplication

from Utils.ColorThief import ColorThief
from Utils.CommonUtil import AppLog, Setting
from Utils.GradientUtils import GradientUtils


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

# Modify background picture
StylePictureTemplate = """
/*Main window*/
#widgetMain {{
    border-image: url({0});    /*Background picture*/
}}
"""

# Modify color
StyleColorTemplate = """
/*Main window*/
#widgetMain {{
    background: rgba({0}, {1}, {2}, 255);
}}

/ * Button in the search box * /
#buttonClear {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*toolbar*/
#widgetTools {{
    background-color: rgba({0}, {1}, {2}, 60);
}}

/ * Button in the toolbar * /
#buttonGithub, #buttonQQ, #buttonGroup {{
    background: rgba({0}, {1}, {2}, 255);
}}

/ * Back to top, home button * /
#buttonBackToUp, #buttonHome {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/ * Store webpage control * /
#widgetContents {{
    background: rgba(248, 248, 248, 200);
}}

/ * Login window * /
#widgetLogin {{
    background: rgba({0}, {1}, {2}, 210);
}}

/ * Activation status * /
#widgetLogin[_active="true"] {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/ * Donation, update, error, theme window * /
#widgetDonate, #widgetUpdate, #widgetError, #widgetSkin {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
    background: rgba({0}, {1}, {2}, 255);    /*background color*/
}}

/ * Donate window, update window, error, theme window background * /
#widgetImage, #widgetUpdateBg, #widgetErrorBg, #widgetSkinBg {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/ * Update progress bar * /
#progressBarUpdate::chunk {{
    background-color: rgba({0}, {1}, {2}, 255);
}}

/ * PIP button * /
#buttonInstall {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:hover {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:pressed {{
    background: rgba({0}, {1}, {2}, 255);
}}

#tabWidgetSkinMain > QTabBar::tab:selected {{
    color: rgb({0}, {1}, {2});
    border-bottom: 2px solid rgb({0}, {1}, {2});
}}

#widgetCategories > QPushButton:checked {{
    color: rgb({0}, {1}, {2});
}}

#sliderOpacity::groove:horizontal {{
    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba({0}, {1}, {2}, 255), stop:1 rgba(255, 255, 255, 255));
}}
#sliderOpacity::handle:horizontal {{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.9 rgba(255, 255, 255, 255), stop:1 rgba({0}, {1}, {2}, 255));
}}

/ * Wallpaper Control Progress Bar * /
PictureWidget {{
    / * Circle color * /
    qproperty-circleColor: rgb({0}, {1}, {2});
}}

/ * Thumbnail control text hover color * /
#skinBaseItemWidget {{
    qproperty-textHoverColor: rgb({0}, {1}, {2});
}}

#buttonPreviewApply {{
    background: rgb({0}, {1}, {2});
}}
#buttonPreviewApply:hover {{
    background: rgba({0}, {1}, {2}, 200);
}}
#buttonPreviewApply:pressed {{
    background: rgba({0}, {1}, {2}, 230);
}}

/*menu*/
QMenu::item:selected {{
    color: white;
    background: rgba({0}, {1}, {2}, 200);
}}
"""

# Gradient color
StyleGradientTemplate = """
/*Main window*/
#widgetMain {{
    background: {3};
}}

/ * Button in the search box * /
#buttonClear {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*toolbar*/
#widgetTools {{
    background-color: rgba({0}, {1}, {2}, 60);
}}

/ * Button in the toolbar * /
#buttonGithub, #buttonQQ, #buttonGroup {{
    background: rgba({0}, {1}, {2}, 255);
}}

/ * Back to top, home button * /
#buttonBackToUp, #buttonHome {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/ * Store webpage control * /
#widgetContents {{
    background: rgba(248, 248, 248, 200);
}}

/ * Login window * /
#widgetLogin {{
    background: {3};
}}

/ * Activation status * /
#widgetLogin[_active="true"] {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/ * Donation, update, error, theme window * /
#widgetDonate, #widgetUpdate, #widgetError, #widgetSkin {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
    background: {3};    /*background color*/
}}

/ * Donate window, update window, error, theme window background * /
#widgetImage, #widgetUpdateBg, #widgetErrorBg, #widgetSkinBg {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/ * Update progress bar * /
#progressBarUpdate::chunk {{
    background-color: {3};
}}

/ * PIP button * /
#buttonInstall {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:hover {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:pressed {{
    background: rgba({0}, {1}, {2}, 255);
}}

#tabWidgetSkinMain > QTabBar::tab:selected {{
    color: rgb({0}, {1}, {2});
    border-bottom: 2px solid rgb({0}, {1}, {2});
}}

#widgetCategories > QPushButton:checked {{
    color: rgb({0}, {1}, {2});
}}

#sliderOpacity::groove:horizontal {{
    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba({0}, {1}, {2}, 255), stop:1 rgba(255, 255, 255, 255));
}}
#sliderOpacity::handle:horizontal {{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.9 rgba(255, 255, 255, 255), stop:1 rgba({0}, {1}, {2}, 255));
}}

/ * Wallpaper Control Progress Bar * /
PictureWidget {{
    / * Circle color * /
    qproperty-circleColor: rgb({0}, {1}, {2});
}}

/ * Thumbnail control text hover color * /
#skinBaseItemWidget {{
    qproperty-textHoverColor: rgb({0}, {1}, {2});
}}

#buttonPreviewApply {{
    background: rgb({0}, {1}, {2});
}}
#buttonPreviewApply:hover {{
    background: rgba({0}, {1}, {2}, 200);
}}
#buttonPreviewApply:pressed {{
    background: rgba({0}, {1}, {2}, 230);
}}

/*menu*/
QMenu::item:selected {{
    color: white;
    background: rgba({0}, {1}, {2}, 200);
}}
"""


class ThemeManager:

    ThemeDir = 'Resources/Themes'
    ThemeName = 'Default'

    # mouse
    CursorDefault = 'default.png'
    CursorPointer = 'pointer.png'

    # Mouse picture cache
    Cursors = {}

    @classmethod
    def styleSheet(cls):
        """Get the style of Application
        """
        return QApplication.instance().styleSheet()

    @classmethod
    def loadTheme(cls):
        """Depending on the configuration loading theme
        :param cls:
        :param parent:
        """
        ThemeManager.ThemeName = Setting.value('theme', 'Default', str)
        # Load the font in the topic
        path = cls.fontPath()
        AppLog.info('fontPath: {}'.format(path))
        if os.path.isfile(path):
            QFontDatabase.addApplicationFont(path)
        # Loading the subject
        path = cls.stylePath()
        AppLog.info('stylePath: {}'.format(path))
        try:
            QApplication.instance().setStyleSheet(
                open(path, 'rb').read().decode('utf-8', errors='ignore'))
            return 1
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadFont(cls):
        """Load font
        """
        ThemeManager.ThemeName = Setting.value('theme', 'Default', str)
        # Load the font in the topic
        path = cls.fontPath()
        AppLog.info('fontPath: {}'.format(path))
        if os.path.isfile(path):
            QFontDatabase.addApplicationFont(path)

    @classmethod
    def loadUserTheme(cls, theme='Default'):
        """Load the theme in the topic directory
        :param cls:
        :param theme:        Folder name
        """
        Setting.setValue('theme', theme)
        cls.loadTheme()

    @classmethod
    def loadColourfulTheme(cls, color, widget=None, replaces={}):
        """Based on the current setting topic color
        :param cls:
        :param color:        background color
        :param widget:        Specified control
        """
        # Loading the subject
        path = cls.stylePath('Default')
        AppLog.info('stylePath: {}'.format(path))
        try:
            styleSheet = open(path, 'rb').read().decode(
                'utf-8', errors='ignore')
            # Need to replace partial style
            colorstr = GradientUtils.styleSheetCode(color)
            if isinstance(color, QLinearGradient) or isinstance(color, QRadialGradient) or isinstance(color, QConicalGradient):
                color = color.stops()[0][1]
            # Replace Name
            templates = StyleGradientTemplate
            for name, value in replaces.items():
                templates = templates.replace(name, value)

            styleSheet += templates.format(
                color.red(), color.green(), color.blue(), colorstr)
            widget = widget or QApplication.instance()
            widget.setStyleSheet(styleSheet)
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadPictureTheme(cls, image=None, widget=None, replaces={}):
        """Set the topic of the picture background
        :param cls:
        :param image:         Background picture
        :param widget:        Specified control
        """
        # Loading the subject
        path = cls.stylePath('Default')
        AppLog.info('stylePath: {}'.format(path))
        try:
            styleSheet = open(path, 'rb').read().decode(
                'utf-8', errors='ignore')
            # Need to replace partial style
            if image and os.path.isfile(image):
                # Get image main tones
                color_thief = ColorThief(image)
                color = color_thief.get_color()
                AppLog.info('dominant color: {}'.format(str(color)))

                # Replace Name
                templates = StylePictureTemplate
                for name, value in replaces.items():
                    templates = templates.replace(name, value)

                styleSheet += templates.format(os.path.abspath(
                    image).replace('\\', '/')) + StyleColorTemplate.format(*color)
            widget = widget or QApplication.instance()
            widget.setStyleSheet(styleSheet)
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadCursor(cls, widget, name='default.png'):
        # Load cursor
        path = cls.cursorPath(name)
        if path in ThemeManager.Cursors:
            widget.setCursor(ThemeManager.Cursors[path])
            return
        AppLog.info('cursorPath: {}'.format(path))
        if os.path.exists(path):
            # Set custom mouse styles and 0 ,0 as the origin
            cur = QCursor(QPixmap(path), 0, 0)
            ThemeManager.Cursors[path] = cur
            widget.setCursor(cur)

    @classmethod
    def cursorPath(cls, name='default.png'):
        """
        :param cls:
        :return: The subject of the mouse picture absolute path
        """
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, ThemeManager.ThemeName, 'cursor', name)).replace('\\', '/')

    @classmethod
    def setPointerCursors(cls, widgets):
        """Set the mouse style of some specified controls
        :param cls:
        """
        path = os.path.abspath(os.path.join(
            ThemeManager.ThemeDir, ThemeManager.ThemeName, 'cursor', cls.CursorPointer)).replace('\\', '/')
        if os.path.exists(path):
            cursor = QCursor(QPixmap(path), 0, 0)
            for w in widgets:
                w.setCursor(cursor)

    @classmethod
    def fontPath(cls):
        """
        :param cls:
        :return: The absolute path of font.ttf in the subject
        """
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, ThemeManager.ThemeName, 'font.ttf')).replace('\\', '/')

    @classmethod
    def stylePath(cls, path=''):
        """
        :param cls:
        :return: The absolute path of style.qss in theme
        """
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, path or ThemeManager.ThemeName, 'style.qss')).replace('\\', '/')
