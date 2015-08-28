from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QDialogButtonBox, QSizePolicy, QLabel, QVBoxLayout, QWidget


class QuickstartWizardDialog(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, parent, **kwargs)
        self.__setupUi()

    def __setupUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        heading = self.tr('untitled')
        heading = '<h3>{0}</h3>'.format(heading)

        self.__heading = QLabel(heading, self, objectName='heading')
        self.__heading.setContentsMargins(12, 12, 12, 0)

        self.__buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal)
        self.__buttons.button(QDialogButtonBox.Ok).setAutoDefault(True)

        buttons = QWidget(objectName='button-container')
        buttons_l = QVBoxLayout()
        buttons_l.setContentsMargins(12, 0, 12, 12)
        buttons.setLayout(buttons_l)

        buttons_l.addWidget(self.__buttons)

        layout.addWidget(self.__heading)
        layout.addLayout(self.get_custom_layout())
        layout.addWidget(buttons)

        self.__buttons.accepted.connect(self.accept)
        self.__buttons.rejected.connect(self.reject)

        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setHeading(self, heading):
        self.__heading.setText(heading)

    def heading(self):
        return self.__heading.text()

    def get_custom_layout(self):
        return QVBoxLayout()

    def get_patch(self):
        return {}
