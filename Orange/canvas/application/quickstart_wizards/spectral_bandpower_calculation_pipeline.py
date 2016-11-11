from PyQt4.QtGui import QCheckBox, QFormLayout, QLabel, QLineEdit, \
    QVBoxLayout, QFont

from neuropype.nodes.network import LSLInput

from .quickstartwizarddialog import QuickstartWizardDialog


class SpectralBandpowerQuickstartWizardDialog(QuickstartWizardDialog):
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

        step_2 = self.step('What is the EEG frequency range of '
                           'interest, in Hz.')
        step_2.setContentsMargins(0, 15, 0, 0)

        # Low transition start.
        low_transition_start = QLineEdit(str(6), self)

        # Low transition end.
        low_transition_end = QLineEdit(str(8), self)

        # High transition start.
        high_transition_start = QLineEdit(str(12), self)

        # High transition end.
        high_transition_end = QLineEdit(str(15), self)

        # Form layout.
        bandpass_form = QFormLayout()
        bandpass_form.addRow(self.tr('Pass-band up-ramp start frequency'), low_transition_start)
        bandpass_form.addRow(self.tr('Pass-band up-ramp end frequency'), low_transition_end)
        bandpass_form.addRow(self.tr('Pass-band down-ramp start frequency'), high_transition_start)
        bandpass_form.addRow(self.tr('Pass-band down-ramp end frequency'), high_transition_end)

        custom_layout.addWidget(step_2)
        custom_layout.addLayout(bandpass_form)

        ######## Step 5

        step_3 = self.step('What would you like to call your output streams?')
        step_3.setContentsMargins(0, 15, 0, 0)

        # Raw-data outlet.
        raw_outlet = QLineEdit('RawData', self)

        # Spectrum outlet.
        spectrum_outlet = QLineEdit('Spectrum', self)

        # Alpha outlet.
        alpha_outlet = QLineEdit('AlphaPower', self)

        # Form layout.
        outlet_form = QFormLayout()
        outlet_form.addRow(self.tr('Raw Data'), raw_outlet)
        outlet_form.addRow(self.tr('Power Spectrum'), spectrum_outlet)
        outlet_form.addRow(self.tr('Retained Band'), alpha_outlet)

        custom_layout.addWidget(step_3)
        custom_layout.addLayout(outlet_form)

        ######## Attributes
        self._query_name = query_name
        self._low_transition_start = low_transition_start
        self._low_transition_end = low_transition_end
        self._high_transition_start = high_transition_start
        self._high_transition_end = high_transition_end
        self._raw_outlet = raw_outlet
        self._spectrum_outlet = spectrum_outlet
        self._alpha_outlet = alpha_outlet

        return custom_layout

    def get_patch(self):
        if not self._query_name.text():
            self._query_name.setText("type='EEG'")
        else:
            self._query_name.setText("name=" + "'" + self._query_name.text() +
                                     "'")
        return {
            'LSL Input': {
                'query': self._query_name.text()
            },
            'IIR Bandpass': {
                'frequencies': '({0}, {1}, {2}, {3})'.format(self._low_transition_start.text(),
                                                             self._low_transition_end.text(),
                                                             self._high_transition_start.text(),
                                                             self._high_transition_end.text()),
            },
            'Raw Outlet': {
                'stream_name': self._raw_outlet.text()
            },
            'Spectrum Outlet': {
                'stream_name': self._spectrum_outlet.text()
            },
            'Alpha Outlet': {
                'stream_name': self._alpha_outlet.text()
            }
        }
