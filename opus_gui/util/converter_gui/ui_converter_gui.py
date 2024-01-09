# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Dropbox/urbansim/xml_converter/src/converter_gui.ui'
#
# Created: Sat May  9 13:38:44 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ConverterGui(object):
    def setupUi(self, ConverterGui):
        ConverterGui.setObjectName("ConverterGui")
        ConverterGui.resize(618, 380)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ConverterGui)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stack_steps = QtWidgets.QStackedWidget(ConverterGui)
        self.stack_steps.setObjectName("stack_steps")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.frame_error = QtWidgets.QFrame(self.page)
        self.frame_error.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_error.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_error.setObjectName("frame_error")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_error)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.p0_info_icon = QtWidgets.QLabel(self.frame_error)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p0_info_icon.sizePolicy().hasHeightForWidth())
        self.p0_info_icon.setSizePolicy(sizePolicy)
        self.p0_info_icon.setPixmap(QtWidgets.QPixmap(":/images/images/messagebox_info.png"))
        self.p0_info_icon.setMargin(5)
        self.p0_info_icon.setObjectName("p0_info_icon")
        self.horizontalLayout_2.addWidget(self.p0_info_icon)
        self.p0_warning_icon = QtWidgets.QLabel(self.frame_error)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p0_warning_icon.sizePolicy().hasHeightForWidth())
        self.p0_warning_icon.setSizePolicy(sizePolicy)
        self.p0_warning_icon.setPixmap(QtWidgets.QPixmap(":/images/images/messagebox_warning.png"))
        self.p0_warning_icon.setMargin(5)
        self.p0_warning_icon.setObjectName("p0_warning_icon")
        self.horizontalLayout_2.addWidget(self.p0_warning_icon)
        self.p0_text = QtWidgets.QLabel(self.frame_error)
        self.p0_text.setWordWrap(True)
        self.p0_text.setObjectName("p0_text")
        self.horizontalLayout_2.addWidget(self.p0_text)
        self.verticalLayout.addWidget(self.frame_error)
        self.frame = QtWidgets.QFrame(self.page)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.le_filename = QtWidgets.QLineEdit(self.frame)
        font = QtWidgets.QFont()
        font.setPointSize(10)
        self.le_filename.setFont(font)
        self.le_filename.setFrame(True)
        self.le_filename.setReadOnly(False)
        self.le_filename.setObjectName("le_filename")
        self.horizontalLayout_5.addWidget(self.le_filename)
        self.pb_get_filename = QtWidgets.QToolButton(self.frame)
        self.pb_get_filename.setObjectName("pb_get_filename")
        self.horizontalLayout_5.addWidget(self.pb_get_filename)
        self.verticalLayout.addWidget(self.frame)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pb_next = QtWidgets.QPushButton(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_next.sizePolicy().hasHeightForWidth())
        self.pb_next.setSizePolicy(sizePolicy)
        icon = QtWidgets.QIcon()
        icon.addPixmap(QtWidgets.QPixmap(":/images/images/forward.png"), QtWidgets.QIcon.Normal, QtWidgets.QIcon.Off)
        self.pb_next.setIcon(icon)
        self.pb_next.setIconSize(QtCore.QSize(32, 32))
        self.pb_next.setObjectName("pb_next")
        self.horizontalLayout.addWidget(self.pb_next)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stack_steps.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_page2 = QtWidgets.QFrame(self.page_2)
        self.frame_page2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_page2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_page2.setObjectName("frame_page2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_page2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.p1_ok_icon = QtWidgets.QLabel(self.frame_page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_ok_icon.sizePolicy().hasHeightForWidth())
        self.p1_ok_icon.setSizePolicy(sizePolicy)
        self.p1_ok_icon.setPixmap(QtWidgets.QPixmap(":/images/images/apply.png"))
        self.p1_ok_icon.setMargin(5)
        self.p1_ok_icon.setObjectName("p1_ok_icon")
        self.horizontalLayout_8.addWidget(self.p1_ok_icon)
        self.p1_info_icon = QtWidgets.QLabel(self.frame_page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_info_icon.sizePolicy().hasHeightForWidth())
        self.p1_info_icon.setSizePolicy(sizePolicy)
        self.p1_info_icon.setPixmap(QtWidgets.QPixmap(":/images/images/messagebox_info.png"))
        self.p1_info_icon.setMargin(5)
        self.p1_info_icon.setObjectName("p1_info_icon")
        self.horizontalLayout_8.addWidget(self.p1_info_icon)
        self.p1_warning_icon = QtWidgets.QLabel(self.frame_page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_warning_icon.sizePolicy().hasHeightForWidth())
        self.p1_warning_icon.setSizePolicy(sizePolicy)
        self.p1_warning_icon.setPixmap(QtWidgets.QPixmap(":/images/images/messagebox_warning.png"))
        self.p1_warning_icon.setMargin(5)
        self.p1_warning_icon.setObjectName("p1_warning_icon")
        self.horizontalLayout_8.addWidget(self.p1_warning_icon)
        self.p1_text = QtWidgets.QLabel(self.frame_page2)
        self.p1_text.setWordWrap(True)
        self.p1_text.setObjectName("p1_text")
        self.horizontalLayout_8.addWidget(self.p1_text)
        self.pb_show_warnings = QtWidgets.QPushButton(self.frame_page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_show_warnings.sizePolicy().hasHeightForWidth())
        self.pb_show_warnings.setSizePolicy(sizePolicy)
        self.pb_show_warnings.setObjectName("pb_show_warnings")
        self.horizontalLayout_8.addWidget(self.pb_show_warnings)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.frame_2 = QtWidgets.QFrame(self.frame_page2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.le_filename_out = QtWidgets.QLineEdit(self.frame_2)
        font = QtWidgets.QFont()
        font.setPointSize(10)
        self.le_filename_out.setFont(font)
        self.le_filename_out.setFrame(True)
        self.le_filename_out.setReadOnly(False)
        self.le_filename_out.setObjectName("le_filename_out")
        self.horizontalLayout_6.addWidget(self.le_filename_out)
        self.pb_get_filename_out = QtWidgets.QToolButton(self.frame_2)
        self.pb_get_filename_out.setObjectName("pb_get_filename_out")
        self.horizontalLayout_6.addWidget(self.pb_get_filename_out)
        self.verticalLayout_3.addWidget(self.frame_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.verticalLayout_4.addWidget(self.frame_page2)
        self.frame_log = QtWidgets.QFrame(self.page_2)
        self.frame_log.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_log.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_log.setObjectName("frame_log")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_log)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.txt_log = QtWidgets.QTextEdit(self.frame_log)
        self.txt_log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.txt_log.setObjectName("txt_log")
        self.verticalLayout_5.addWidget(self.txt_log)
        self.verticalLayout_4.addWidget(self.frame_log)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pb_back = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_back.sizePolicy().hasHeightForWidth())
        self.pb_back.setSizePolicy(sizePolicy)
        icon1 = QtWidgets.QIcon()
        icon1.addPixmap(QtWidgets.QPixmap(":/images/images/back.png"), QtWidgets.QIcon.Normal, QtWidgets.QIcon.Off)
        self.pb_back.setIcon(icon1)
        self.pb_back.setIconSize(QtCore.QSize(32, 32))
        self.pb_back.setObjectName("pb_back")
        self.horizontalLayout_3.addWidget(self.pb_back)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.pb_log = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_log.sizePolicy().hasHeightForWidth())
        self.pb_log.setSizePolicy(sizePolicy)
        icon2 = QtWidgets.QIcon()
        icon2.addPixmap(QtWidgets.QPixmap(":/images/images/messagebox_info.png"), QtWidgets.QIcon.Normal, QtWidgets.QIcon.Off)
        self.pb_log.setIcon(icon2)
        self.pb_log.setIconSize(QtCore.QSize(32, 32))
        self.pb_log.setCheckable(True)
        self.pb_log.setChecked(False)
        self.pb_log.setFlat(False)
        self.pb_log.setObjectName("pb_log")
        self.horizontalLayout_3.addWidget(self.pb_log)
        self.pb_save = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_save.sizePolicy().hasHeightForWidth())
        self.pb_save.setSizePolicy(sizePolicy)
        icon3 = QtWidgets.QIcon()
        icon3.addPixmap(QtWidgets.QPixmap(":/images/images/filesave.png"), QtWidgets.QIcon.Normal, QtWidgets.QIcon.Off)
        self.pb_save.setIcon(icon3)
        self.pb_save.setIconSize(QtCore.QSize(32, 32))
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout_3.addWidget(self.pb_save)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.stack_steps.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.stack_steps)

        self.retranslateUi(ConverterGui)
        self.stack_steps.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ConverterGui)

    def retranslateUi(self, ConverterGui):
        ConverterGui.setWindowTitle(QtWidgets.QApplication.translate("ConverterGui", "Converter for Opus Project Files", None, QtWidgets.QApplication.UnicodeUTF8))
        self.p0_text.setText(QtWidgets.QApplication.translate("ConverterGui", "error message", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_get_filename.setToolTip(QtWidgets.QApplication.translate("ConverterGui", "Select file to convert", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_get_filename.setText(QtWidgets.QApplication.translate("ConverterGui", "...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_next.setText(QtWidgets.QApplication.translate("ConverterGui", "Inspect", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_next.setShortcut(QtWidgets.QApplication.translate("ConverterGui", "Ctrl+K", None, QtWidgets.QApplication.UnicodeUTF8))
        self.p1_text.setText(QtWidgets.QApplication.translate("ConverterGui", "information", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_show_warnings.setText(QtWidgets.QApplication.translate("ConverterGui", "warnings", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_get_filename_out.setText(QtWidgets.QApplication.translate("ConverterGui", "...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_back.setText(QtWidgets.QApplication.translate("ConverterGui", "Inspect another file", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_back.setShortcut(QtWidgets.QApplication.translate("ConverterGui", "Ctrl+K", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_log.setText(QtWidgets.QApplication.translate("ConverterGui", "Log", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_log.setShortcut(QtWidgets.QApplication.translate("ConverterGui", "Ctrl+K", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_save.setText(QtWidgets.QApplication.translate("ConverterGui", "Save", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pb_save.setShortcut(QtWidgets.QApplication.translate("ConverterGui", "Ctrl+K", None, QtWidgets.QApplication.UnicodeUTF8))

from . import resources_rc
