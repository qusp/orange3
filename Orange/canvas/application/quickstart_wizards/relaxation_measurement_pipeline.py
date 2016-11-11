from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton,\
    QVBoxLayout, QFont

from .quickstartwizarddialog import QuickstartWizardDialog

from neuropype.nodes.network import LSLInput

class RelaxationQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

       ######## Step 1

        step_1 = self.step("What is the name of the Lab Streaming Layer (LSL) "
                           "stream you want to use as input? ")
        step_1.setWordWrap(True)

        step_1_explain = self.step(" If you leave this box empty, "
                                   "the pipeline will use any available LSL "
                                   "stream on the network corresponding to an "
                                   "EEG signal. For more information on LSL "
                           "streams you can refer to <a "
                                   "href=https://github.com/sccn/labstreaminglayer/wiki>here.</a>"
                                   " In case you "
                           "have access to LSL Lab recorder, it can provide "
                                   "the names of the LSL streams available on "
                                   "your network.")
        step_1_explain.setWordWrap(True)
        myFont = QFont()
        myFont.setBold(False)
        step_1_explain.setFont(myFont)
        step_1_explain.setOpenExternalLinks(True)

        step_1.setContentsMargins(0, 15, 0, 0)

        # Query string.
        query_name= QLineEdit()

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(query_name)
        custom_layout.addWidget(step_1_explain)

        ######## Step 2

        step_2 = self.step('What would you like to call your output stream?')
        step_2.setContentsMargins(0, 15, 0, 0)

        # Output stream.
        output_stream = QLineEdit("MyOutStream")


        # Form layout.
        output_form = QFormLayout()
        output_form.addRow(self.tr('Output stream name'), output_stream)


        custom_layout.addWidget(step_2)
        custom_layout.addLayout(output_form)


        ######## Attributes.
        self._query_name = query_name
        self._output_stream = output_stream

        return custom_layout

    def get_patch(self):
        if not self._query_name.text():
            self._query_name.setText("type='EEG'")
        else:
            self._query_name.setText("name=" + "'" + self._query_name.text() +
                                     "'")

        return {
            'LSL Input': {
                'query': self._query_name.text(),
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),
            }
        }
