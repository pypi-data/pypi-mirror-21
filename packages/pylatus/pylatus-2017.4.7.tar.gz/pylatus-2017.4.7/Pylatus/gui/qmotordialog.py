#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


class QMotorDialog(QtWidgets.QDialog):
    sigClosed = QtCore.pyqtSignal()
    sigUpdateMotorViews = QtCore.pyqtSignal()
    sigMoveMotor = QtCore.pyqtSignal(str, float, bool)
    sigStopAllMotors = QtCore.pyqtSignal()

    def __init__(self, parent, keyword):
        super().__init__(parent=parent)
        self.keyword = keyword
        self.motors = {}

    def setupMotors(self):
        self.defineMotors()

    def defineMotors(self):
        for item, obj in self.__dict__.items():
            if not isinstance(obj, QtWidgets.QAbstractSpinBox):
                continue
            # Take the motor name from 'sl01bSpinBox' cutting 'SpinBox': item[:-7]
            guiName = item[:-len(self.keyword)]
            specName = getattr(self.config, guiName, guiName)
            self.motors[specName] = guiName

    def updateMotors(self):
        self.sigUpdateMotorViews.emit()

    def updateMotorPosition(self, name, position):
        if name in self.motors:
            sb = getattr(self, f'{self.motors[name]}{self.keyword}')
            if sb:
                sb.setValue(position)

    @QtCore.pyqtSlot()
    def on_sendButton_clicked(self):
        for name in self.motors:
            spinBox = getattr(self, f'{self.motors[name]}{self.keyword}')
            self.sigMoveMotor.emit(name, spinBox.value())

    @QtCore.pyqtSlot()
    def on_updateButton_clicked(self):
        self.updateMotors()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_F5:
            self.updateMotors()
        elif key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            widget = QtWidgets.QApplication.focusWidget()
            if not isinstance(widget, QtWidgets.QAbstractSpinBox):
                return
            motorName = widget.objectName()[:-len(self.keyword)]
            value = widget.value()
            self.sigMoveMotor.emit(motorName, value, True)

    def setConfig(self, config):
        self.config = config
