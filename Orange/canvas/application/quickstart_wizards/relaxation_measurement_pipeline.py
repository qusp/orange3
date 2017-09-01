from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog

from neuropype.nodes.network import LSLInput

class RelaxationQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        ######## Step 1

        step_1 = self.step("Enter the corresponding query for the input data "
                           "stream (e.g., name='InStreamTest', "
                           "or hostname='myhost' and type='EEG')")
        step_1.setContentsMargins(0, 5, 0, 0)

        # Query.
        default_query = LSLInput.port('query').default
        query = QLineEdit(str(default_query), self)

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(query)

        ######## Step 2
        step_2 = self.step('Enter the name and the unique source ID for the '
                           'output stream.')
        step_2.setContentsMargins(0, 15, 0, 0)

        # Output stream.
        output_stream = QLineEdit("OutStreamTest")

        # Source ID.
        source_id = QLineEdit("uniquesrcid56")

        # Form layout.
        output_form = QFormLayout()
        output_form.addRow(self.tr('Output stream name'), output_stream)
        output_form.addRow(self.tr('Output stream UID'), source_id)

        custom_layout.addWidget(step_2)
        custom_layout.addLayout(output_form)

        ######## Attributes.
        self._query = query
        self._output_stream = output_stream
        self._source_id = source_id

        return custom_layout

    def get_patch(self):

        return {
            'LSL Input': {
                'query': self._query.text(),
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),
                'source_id': self._source_id.text()
            }
        }
