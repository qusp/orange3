from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog


class ERPClassificationQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        ######## Step 1

        step_1 = self.step("Enter the corresponding query for the input data "
                           "stream (e.g., name='InStreamTest', "
                           "or hostname='myhost' and type='EEG')")
        step_1.setContentsMargins(0, 15, 0, 0)

        # Query string.
        query_string = QLineEdit("name='InStreamTest'")

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(query_string)

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

        ######## Step 3

        step_3 = self.step("Enter the marker labels in the marker stream "
                           " and the corresponding numerical labels to  be "
                           "assigned to them.")
        step_3.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        assign_targets = QLineEdit("{'incorrect': 0, 'correct': 1}")

        custom_layout.addWidget(step_3)
        custom_layout.addWidget(assign_targets)

        ######## Step 4

        step_4 = self.step('Enter the desired channel selection for the input '
                           'data stream. Exclude the channels that '
                           'are known to contain no valid data.')
        step_4.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        channel_select_start = QLineEdit("0")

        # Time bounds end.
        channel_select_end = QLineEdit("64")

        # Form layout.
        channel_select_form = QFormLayout()
        channel_select_form.addRow(self.tr('Beginning of desired channel '
                                           'range'),
                                channel_select_start)
        channel_select_form.addRow(self.tr('End of desired channel range'),
                               channel_select_end)

        custom_layout.addWidget(step_4)
        custom_layout.addLayout(channel_select_form)

        ######## Step 5

        step_5 = self.step('Enter the time segment of interest'
                           'to be used for windowing the data stream, '
                           'in seconds.')
        step_5.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        time_bounds_start = QLineEdit("-0.2")

        # Time bounds end.
        time_bounds_end = QLineEdit("0.8")

        # Form layout.
        time_bounds_form = QFormLayout()
        time_bounds_form.addRow(self.tr('Beginning of time range'),
                                time_bounds_start)
        time_bounds_form.addRow(self.tr('End of time range'), time_bounds_end)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(time_bounds_form)

        ######## Step 6

        step_6 = self.step('Enter the desired cut-off frequency for the '
                           'anti-aliasing lowpass filter, in Hz. (e.g. if the '
                           'reduced sampling rate is going to be 100Hz, '
                           'the cut-off frequency should be lower than 50Hz.)')

        step_6.setContentsMargins(0, 15, 0, 0)

        # Assign cut-off frequency.
        cutoff_frequncy = QLineEdit("50")

        custom_layout.addWidget(step_6)
        custom_layout.addWidget(cutoff_frequncy)

        ######## Step 7
        step_7 = self.step("Enter the decimation ratio to be used to reduce "
                           "the sampling rate.")
        step_7.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        decimation_rate = QLineEdit("1")

        custom_layout.addWidget(step_7)
        custom_layout.addWidget(decimation_rate)

        ######## Step 8

        step_8 = self.step('Enter the spectral range to '
                           'be considered for ERP detection, in Hz.')
        step_8.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        spectral_bounds_start = QLineEdit("0.1")

        # Time bounds end.
        spectral_bounds_end = QLineEdit("15")

        # Form layout.
        spectral_bounds_form = QFormLayout()
        spectral_bounds_form.addRow(self.tr('Beginning of spectral range'),
                                spectral_bounds_start)
        spectral_bounds_form.addRow(self.tr('End of spectral range'),
                                spectral_bounds_end)

        custom_layout.addWidget(step_8)
        custom_layout.addLayout(spectral_bounds_form)



        ######## Attributes.

        self._query_string = query_string
        self._output_stream = output_stream
        self._source_id = source_id
        self._assign_targets = assign_targets
        self._channel_select_start = channel_select_start
        self._channel_select_end = channel_select_end
        self._time_bounds_start = time_bounds_start
        self._time_bounds_end = time_bounds_end
        self._cutoff_frequncy = cutoff_frequncy
        self._decimation_rate = decimation_rate
        self._spectral_bounds_start = spectral_bounds_start
        self._spectral_bounds_end = spectral_bounds_end

        return custom_layout

    def get_patch(self):
        cutoff = float(self._cutoff_frequncy.text())

        return {

            'LSL Input': {
                'query': self._query_string.text()
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),
                'source_id': self._source_id.text()
            },
            'Assign Targets': {
                'mapping': self._assign_targets.text()
            },
            'Select Range':{
                'selection':'({0}, {1})'.format(self._channel_select_start.text(),
                                                   self._channel_select_end.text())
            },
            'Segmentation': {
                'time_bounds': '({0}, {1})'.format(self._time_bounds_start.text(),
                                                   self._time_bounds_end.text())
            },
            'FIR Filter': {
                'frequencies': '[{0}, {1}]'.format(cutoff - 5, cutoff)
            },
            'Decimate':{
                'factor':self._decimation_rate.text()
            },
            'Spectral Selection':{
                'frequencies':'({0}, {1})'.format(self._spectral_bounds_start.text(),
                    self._spectral_bounds_end.text())
            }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
