from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog


class MotorImageryClassificationQuickstartWizardDialog(QuickstartWizardDialog):
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
        assign_targets = QLineEdit("{'left': 0, 'right': 1}")

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
        channel_select_end = QLineEdit("19")

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

        step_5 = self.step('Enter the time segment of interest to be used for '
                           'windowing the data stream, in seconds.')
        step_5.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        time_bounds_start = QLineEdit("0.5")

        # Time bounds end.
        time_bounds_end = QLineEdit("3.0")

        # Form layout.
        time_bounds_form = QFormLayout()
        time_bounds_form.addRow(self.tr('Beginning of time range'),
                                time_bounds_start)
        time_bounds_form.addRow(self.tr('End of time range'), time_bounds_end)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(time_bounds_form)

        ######## Step 6

        step_6 = self.step('Enter the desired frequency band to be retained in '
                           'the data stream, in Hz.')
        step_6.setContentsMargins(0, 15, 0, 0)

        # Low frequency band.
        low_frequency_band = QLineEdit("4")

        # High frequency band.
        high_frequency_band = QLineEdit("42")

        # Form layout.
        frequency_bands_form = QFormLayout()
        frequency_bands_form.addRow(self.tr('Pass-band start frequency'),
                                    low_frequency_band)
        frequency_bands_form.addRow(self.tr('Pass-band end frequency'),
                                    high_frequency_band)

        custom_layout.addWidget(step_6)
        custom_layout.addLayout(frequency_bands_form)

        ######## Step 7

        step_7 = self.step("Enter the number of spatial filters to be "
                           "designed per target class. (typically "
                           "between 1 and 4)")
        step_7.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        num_features = QLineEdit("3")

        custom_layout.addWidget(step_7)
        custom_layout.addWidget(num_features)

        ######## Attributes.

        self._query_string = query_string
        self._output_stream = output_stream
        self._source_id = source_id
        self._assign_targets = assign_targets
        self._channel_select_start = channel_select_start
        self._channel_select_end = channel_select_end
        self._time_bounds_start = time_bounds_start
        self._time_bounds_end = time_bounds_end
        self._low_frequency_band = low_frequency_band
        self._high_frequency_band = high_frequency_band
        self._num_features = num_features

        return custom_layout

    def get_patch(self):
        band_lo = float(self._low_frequency_band.text())
        band_hi = float(self._high_frequency_band.text())
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
                'frequencies': '[{0}, {1}, {2}, {3}]'.format(band_lo-1,
                                                             band_lo, band_hi,
                                                             band_hi+1)
            },
            'Filter Bank Common Spatial Patterns': {
                'desired_number_of_filters': self._num_features.text()
            }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
