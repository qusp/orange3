
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BugReport.ui'
#
# Created: Mon Oct  3 11:36:32 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

import os
import json
import platform
import tempfile
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class BugReport(QtGui.QDialog):
    def __init__(self, container):
        super(BugReport, self).__init__()
        self.container = container
        self.setup_ui()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(os.path.join('..', 'widgets', 'icons', 'bug.svg'))),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.show()

    def setup_ui(self):
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(422, 439)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_email = QtGui.QLabel(self)
        self.label_email.setObjectName(_fromUtf8("label_email"))
        self.gridLayout.addWidget(self.label_email, 0, 1, 1, 1)
        self.label_type = QtGui.QLabel(self)
        self.label_type.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_type, 6, 1, 1, 1)

        self.lineEdit_name = QtGui.QLineEdit(self)
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.gridLayout.addWidget(self.lineEdit_name, 1, 0, 1, 1)

        self.lineEdit_email = QtGui.QLineEdit(self)
        self.lineEdit_email.setObjectName(_fromUtf8("lineEdit_email"))
        self.gridLayout.addWidget(self.lineEdit_email, 1, 1, 1, 1)

        self.textEdit_description = QtGui.QTextEdit(self)
        self.textEdit_description.setObjectName(_fromUtf8("textEdit_description"))
        self.gridLayout.addWidget(self.textEdit_description, 3, 0, 1, 2)

        self.checkBox_error_trace = QtGui.QCheckBox(self)
        self.checkBox_error_trace.setObjectName(_fromUtf8("checkBox_error_trace"))
        self.gridLayout.addWidget(self.checkBox_error_trace, 5, 0, 1, 1)
        self.checkBox_error_trace.setChecked(True)

        self.checkBox_os_info = QtGui.QCheckBox(self)
        self.checkBox_os_info.setObjectName(_fromUtf8("checkBox_os_info"))
        self.gridLayout.addWidget(self.checkBox_os_info, 6, 0, 1, 1)
        self.checkBox_os_info.setChecked(True)

        self.checkBox_include_patch = QtGui.QCheckBox(self)
        self.checkBox_include_patch.setObjectName(_fromUtf8("checkBox_include_patch"))
        self.gridLayout.addWidget(self.checkBox_include_patch, 7, 0, 1, 1)
        self.checkBox_include_patch.setChecked(True)

        self.checkBox_include_data = QtGui.QCheckBox(self)
        self.checkBox_include_data.setObjectName(_fromUtf8("checkBox_include_data_in_patch"))
        self.gridLayout.addWidget(self.checkBox_include_data, 8, 0, 1, 1)

        self.checkBox_include_data_files = QtGui.QCheckBox(self)
        self.checkBox_include_data_files.setObjectName(_fromUtf8("checkBox_include_data_files"))
        self.gridLayout.addWidget(self.checkBox_include_data_files, 9, 0, 1, 1)

        self.label_name = QtGui.QLabel(self)
        self.label_name.setObjectName(_fromUtf8("label_name"))
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.label_description = QtGui.QLabel(self)
        self.label_description.setObjectName(_fromUtf8("label_description"))
        self.gridLayout.addWidget(self.label_description, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)

        self.comboBox_priority = QtGui.QComboBox(self)
        self.comboBox_priority.setObjectName(_fromUtf8("comboBox_priority"))
        self.gridLayout.addWidget(self.comboBox_priority, 5, 1, 1, 1)
        [self.comboBox_priority.addItem(item) for item in ['Low', 'Medium', 'High']]
        self.comboBox_priority.setCurrentIndex(1)

        self.comboBox_type = QtGui.QComboBox(self)
        self.comboBox_type.setObjectName(_fromUtf8("comboBox_type"))
        self.gridLayout.addWidget(self.comboBox_type, 7, 1, 1, 1)
        [self.comboBox_type.addItem(item) for item in ['Unspecified', 'Feature request', 'Annoyance', 'Showstopper']]
        self.comboBox_type.setCurrentIndex(0)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 1, 1, 1)

        self.retranslate_ui()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        self.setWindowTitle(_translate("Dialog", "Bug Report", None))
        self.label_name.setText(_translate("Dialog", "Name", None))
        self.label_email.setText(_translate("Dialog", "e-mail", None))
        self.label_description.setText(_translate("Dialog", "Bug description", None))
        self.checkBox_error_trace.setText(_translate("Dialog", "Include console output", None))
        self.checkBox_os_info.setText(_translate("Dialog", "Include OS info", None))
        self.checkBox_include_patch.setText(_translate("Dialog", "Include patch", None))
        self.checkBox_include_data.setText(_translate("Dialog", "Include data in the patch", None))
        self.checkBox_include_data_files.setText(_translate("Dialog", "Include imported data files", None))
        self.label_3.setText(_translate("Dialog", "Priority", None))
        self.label_type.setText(_translate("Dialog", "Type", None))
        try:
            self.lineEdit_name.setText(self.container.bug_report.last_name)
            self.lineEdit_email.setText(self.container.bug_report.last_email)
        except:
            pass

    def accept(self):
        try:
            bug_id = '{}'.format(abs(hash(os.times())))

            bug_info = {'console_output': None, 'platform': None, 'python': None, 'patch': None, 'data_in_patch': None,
                        'priority': str(self.comboBox_priority.currentText()),
                        'type': str(self.comboBox_type.currentText()),
                        'sender': str(self.lineEdit_name.text()),
                        'e-mail': str(self.lineEdit_email.text()),
                        'description': str(self.textEdit_description.toPlainText())
                        }

            document = self.container.current_document()
            curr_scheme = document.scheme()
            filename = curr_scheme.title + '_' + bug_id if len(curr_scheme.title) else bug_id
            filename = os.path.join(tempfile.gettempdir(), filename)
            curr_scheme.signal_manager.graph.save_json(filename)
            with open(filename, 'r') as f:
                patch = f.read()
            os.remove(filename)
            ows_filename = filename + '.ows'
            self.container.save_scheme_to(curr_scheme, ows_filename)
            with open(ows_filename, 'r') as f:
                ows_content = f.read()

            if self.checkBox_include_data.checkState():
                bug_info['data'] = [node.data for node in curr_scheme.signal_manager.graph.nodes()]
                # TODO: Fix neuropype.engine.graph.Graph.save_state
                """
                with open(filename, 'w') as f:
                    curr_scheme.signal_manager.graph.save_state(f)
                with open(filename, 'r') as f:
                    state = f.read()
                """

            if self.checkBox_include_data_files.checkState():
                files_to_collect = []
                for node in curr_scheme.signal_manager.graph.nodes():
                    if str(type(node)).find('ImportXDF') > -1 or str(type(node)).find('ImportSET') > -1:
                        if os.path.exists(node.filename):
                            files_to_collect.append(node.filename)
            else:
                files_to_collect = []

            if self.checkBox_error_trace.checkState():
                bug_info['console_output'] = str(self.container.output_dock.widget().toPlainText())

            if self.checkBox_os_info.checkState():
                bug_info['platform'] = os.uname()
                bug_info['python'] = {'version': platform.python_version(),
                                      'compiler': platform.python_compiler(),
                                      'build': platform.python_build()},
            if self.checkBox_include_patch.checkState():
                bug_info['patch'] = json.loads(patch)

            msg_info = 'Sender: ' + bug_info['sender'] + '\n' + \
                       'e-mail: ' + bug_info['e-mail'] + '\n\n' + \
                       'Bug description:\n' + bug_info['description'] + '\n\n' + \
                       'PS: Metadata saved with the pickle module.'

            subject = 'Bug Report       ' + \
                      'Type: ' + str(self.comboBox_type.currentText()) + '       ' +\
                      'Priority: ' + str(self.comboBox_priority.currentText())

            msg = MIMEMultipart()
            msg.preamble = ''
            msg.epilogue = ''

            body = MIMEMultipart('alternative')
            body.attach(MIMEText(msg_info, 'plain'))
            msg.attach(body)
            msg['Subject'] = subject

            filename = 'debug_info_' + bug_id + '.pk'
            attachment = MIMEApplication(pickle.dumps(bug_info))
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)
            attachment = MIMEText(ows_content)
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ows_filename))
            msg.attach(attachment)

            for f in files_to_collect:
                attachment = MIMEApplication(open(f, 'rb').read())
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
                msg.attach(attachment)

            receiver = bug_info['e-mail']
            file_bug(msg, receiver)
            self.close()
        except Exception as e:
            dlg = QtGui.QMessageBox()
            if str(e).find('message size limit') > -1:
                dlg.critical(dlg, "NeuroPype", 'Attached files exceeded file size limits!')
            else:
                dlg.critical(dlg, "NeuroPype", str(e))
        self.save_state()

    def save_state(self):
        self.container.bug_report.last_email = self.lineEdit_email.text()
        self.container.bug_report.last_name = self.lineEdit_name.text()


def file_bug(msg, receiver):
    host = "smtp.gmail.com"
    port = "587"
    sender = "bugreporter2a5bbb76179f4696b4@gmail.com"
    msg['From'] = sender
    msg['To'] = "support@neuropype.io"
    msg["Cc"] = receiver
    server = smtplib.SMTP(host + ':' + port)
    server.starttls()
    server.login(sender, "b7e70df443a642a09abc3de5ea14144a")
    server.sendmail(sender, receiver, msg.as_string())
    server.close()