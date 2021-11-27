#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.FramelessWindow
@description: Borderless window
"""
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

# Enumerate left upper right and four fixed points
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FramelessWindow(QWidget):

    MARGIN = 2  # The outermost control, the left and right sideways 2

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self._pos = None  # Mouse Press position
        self._pressed = False  # Mouse
        self._canmove = False  # Can move
        self.Direction = None  # Cursor direction
        # Mouse track
        self.setMouseTracking(True)
        # Background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Rimless
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def paintEvent(self, event):
        # Since it is a full transparent background window, it is difficult to discover the border of the transparency of 1 in the redraw event, which is used to adjust the window size.
        super(FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.MARGIN))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        # Mouse presses the event record position
        super(FramelessWindow, self).mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            self._pos = event.pos()
            self._pressed = True
            if self.childAt(self._pos) != None:
                # The position of the mouse click on other controls
                self._canmove = True

    def mouseReleaseEvent(self, event):
        # Mouse bomb event
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self._canmove = False
        self.Direction = None

    def mouseDoubleClickEvent(self, event):
        # Mouse double-click event
        super(FramelessWindow, self).mouseDoubleClickEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.childAt(self._pos) != None:
                # The position of the mouse click on other controls
                if self.isMaximized() or self.isFullScreen():
                    self.showNormal()
                else:
                    self.showMaximized()

    def mouseMoveEvent(self, event):
        # Mouse movement event
        super(FramelessWindow, self).mouseMoveEvent(event)

        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGIN, self.height() - self.MARGIN
        if self.isMaximized() or self.isFullScreen():
            # Maximize or full screen is ignored
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if self._canmove:
            self.move(self.mapToGlobal(event.pos() - self._pos))
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.MARGIN and yPos <= self.MARGIN:
            # Upper left corner
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # In the lower right corner
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.MARGIN:
            # Upper right corner
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.MARGIN and hm <= yPos:
            # Left lower corner
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.MARGIN and self.MARGIN <= yPos <= hm:
            # left
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.MARGIN <= yPos <= hm:
            # right
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.MARGIN <= xPos <= wm and 0 <= yPos <= self.MARGIN:
            # above
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.MARGIN <= xPos <= wm and hm <= yPos <= self.height():
            # under
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def leaveEvent(self, event):
        # Mouse leave event
        self.setCursor(Qt.ArrowCursor)  # Restore mouse shape
        super(FramelessWindow, self).leaveEvent(event)

    def changeEvent(self, event):
        # Window change event
        super(FramelessWindow, self).changeEvent(event)
        if event.type() == QEvent.WindowStateChange:  # Window status change
            state = self.windowState()
            if state == (state | Qt.WindowMaximized):
                # Maximize, to remove the left and right boundaries, if you don't remove it, there will be gaps in the border place.
                self.layout().setContentsMargins(0, 0, 0, 0)
            else:
                # To keep the left and right boundary, otherwise there is no border that cannot be adjusted
                self.layout().setContentsMargins(
                    self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # Maximization or full screen is not allowed
            return
        super(FramelessWindow, self).move(pos)

    def _resizeWidget(self, pos):
        # Adjust the window size
        if self.Direction == None:
            return
        mpos = pos - self._pos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # Upper left corner
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # In the lower right corner
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos = pos
        elif self.Direction == RightTop:  # Upper right corner
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos.setX(pos.x())
        elif self.Direction == LeftBottom:  # Left lower corner
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos.setY(pos.y())
        elif self.Direction == Left:  # left
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # right
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos = pos
            else:
                return
        elif self.Direction == Top:  # above
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # under
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos = pos
            else:
                return
        self.setGeometry(x, y, w, h)
