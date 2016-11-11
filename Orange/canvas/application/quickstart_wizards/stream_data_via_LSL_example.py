from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog


class StreamDataviaLSLQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        ######## Step 1

        step_1 = self.step('Please choose the recording you want to stream.')
        step_1.setContentsMargins(0, 5, 0, 0)

        # File dialog.
        file_dialog_btn = QPushButton(self.tr('Open file'))
        file_dialog_btn.clicked.connect(self.open_file_dialog)

        # Training set.
        training_set = QLabel(self.tr('No file is selected...'))

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(file_dialog_btn)
        custom_layout.addWidget(training_set)


        ######## Attributes.
        self._training_set = training_set


        return custom_layout

    def get_patch(self):
        return {
            'Import SET': {
                'filename': self._training_set.text()
            }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
