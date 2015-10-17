from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog


class RelaxationQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        ######## Step 1

        step_1 = self.step("What data stream do you want to read from? "
                           "(e.g., name='Cognionics' or type='EEG')")
        step_1.setContentsMargins(0, 5, 0, 0)

        # Query string.
        query_string = QLineEdit("type='EEG'")

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(query_string)

        ######## Step 2

        step_2 = self.step("What is the EEG frequency range of interest? "
                           "(e.g., 9-14)")
        step_2.setContentsMargins(0, 15, 0, 0)

        # Frequency range.
        freq_range = QLineEdit("9-14")
        freq_range.setToolTip("In Hz.")

        custom_layout.addWidget(step_2)
        custom_layout.addWidget(freq_range)

        ######## Step 3

        step_3 = self.step("What is the EEG frequency range considered noise? "
                           "(e.g., 4-25) (must encompass freq range of "
                           "interest and its surrounding transition band)")
        step_3.setContentsMargins(0, 15, 0, 0)

        # Noise range.
        noise_range = QLineEdit("4-25")
        noise_range.setToolTip("In Hz.")

        custom_layout.addWidget(step_3)
        custom_layout.addWidget(noise_range)

        ######## Step 4

        step_4 = self.step("Optionally you can give the width of transition bands:")
        step_4.setContentsMargins(0, 15, 0, 0)

        # Transition band.
        trans_band = QLineEdit("1")
        trans_band.setToolTip("In Hz.")

        custom_layout.addWidget(step_4)
        custom_layout.addWidget(trans_band)

        step_5 = self.step('Next you can name the output stream (predictions); '
                           'you can also give it a network-unique id so you '
                           'can restart the engine seamlessly.')
        step_5.setContentsMargins(0, 15, 0, 0)

        # Output stream.
        output_stream = QLineEdit('neuropype:Relaxation')

        # Source ID.
        source_id = QLineEdit('(make sure to never use same string more than once on network)')

        # Form layout.
        output_form = QFormLayout()
        output_form.addRow(self.tr('Output stream name'), output_stream)
        output_form.addRow(self.tr('Output stream UID'), source_id)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(output_form)

        ######## Attributes.
        self._query_string = query_string
        self._freq_range = freq_range
        self._noise_range = noise_range
        self._trans_band = trans_band
        self._output_stream = output_stream
        self._source_id = source_id

        return custom_layout

    def get_patch(self):
        peak_lo, peak_hi = self._freq_range.text().split('-')
        peak_lo = float(peak_lo.strip())
        peak_hi = float(peak_hi.strip())
        noise_lo, noise_hi = self._noise_range.text().split('-')
        noise_lo = float(noise_lo.strip())
        noise_hi = float(noise_hi.strip())
        trans = float(self._trans_band.text())

        return {
            'LSL Input': {
                'query': self._query_string.text(),
            },
            'Peak FIR': {
                'frequencies': '[%s, %s, %s, %s]' % (peak_lo-trans, peak_lo,
                                                     peak_hi, peak_hi+trans)
            },
            'Noise FIR': {
                'frequencies': '[(0, 0), (%s, 0), (%s, 1), (%s, 1), (%s, 0), '
                               '(%s, 0), (%s, 1), (%s, 1), (%s, 0), (-1, 0)]' %
                               (noise_lo-trans, noise_lo, peak_lo-trans, peak_lo,
                                peak_hi, peak_hi+trans, noise_hi, noise_hi+trans)
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),
                'source_id': self._source_id.text()
            }
        }
