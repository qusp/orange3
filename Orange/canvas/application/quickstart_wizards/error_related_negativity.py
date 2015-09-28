from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from .quickstartwizarddialog import QuickstartWizardDialog


class ErrorRelatedNegativityQuickstartWizardDialog(QuickstartWizardDialog):
    def get_custom_layout(self):
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(12, 12, 12, 12)

        template = '<h4>{0}</h4>'

        ######## Step 1

        step_1 = QLabel(template.format(self.tr('Please pick the calibration/training recordings:')))
        step_1.setContentsMargins(0, 5, 0, 0)

        # File dialog.
        file_dialog_btn = QPushButton(self.tr('Open file'))
        file_dialog_btn.clicked.connect(self.open_file_dialog)

        # Training set.
        training_set = QLabel(self.tr('No training set selected...'))

        custom_layout.addWidget(step_1)
        custom_layout.addWidget(file_dialog_btn)
        custom_layout.addWidget(training_set)

        ######## Step 2

        step_2 = QLabel(template.format(self.tr("What data and marker stream do you want to read from? (e.g., "
                                                "name='Cognionics', or hostname='myhost' and name='SNAP-Markers')")))
        step_2.setContentsMargins(0, 15, 0, 0)

        # Query string.
        query_string = QLineEdit("type='EEG'")

        # Marker string.
        marker_string = QLineEdit("type='Markers'")

        # Form layout.
        input_form = QFormLayout()
        input_form.addRow(self.tr('Data stream'), query_string)
        input_form.addRow(self.tr('Marker stream'), marker_string)

        custom_layout.addWidget(step_2)
        custom_layout.addLayout(input_form)

        ######## Step 3

        step_3 = QLabel(template.format(self.tr('Next you can name the output stream (predictions); '
                                                'you can also give it a network-unique id so you can restart the engine'
                                                'seamlessly.')))
        step_3.setContentsMargins(0, 15, 0, 0)

        # Output stream.
        output_stream = QLineEdit('neuropype:ErrorPredictions')

        # Source ID.
        source_id = QLineEdit('(make sure to never use same string more than once on network)')

        # Form layout.
        output_form = QFormLayout()
        output_form.addRow(self.tr('Output stream name'), output_stream)
        output_form.addRow(self.tr('Output stream UID'), source_id)

        custom_layout.addWidget(step_3)
        custom_layout.addLayout(output_form)

        ######## Step 4

        step_4 = QLabel(template.format(self.tr("What markers in your marker stream encode BCI prediction targets, "
                                                "and what is the class that the BCI shall predict?")))
        step_4.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        assign_targets = QLineEdit("{'correct': 0, 'incorrect': 1, 'button': 2}")

        custom_layout.addWidget(step_4)
        custom_layout.addWidget(assign_targets)

        ######## Step 5

        step_5 = QLabel(template.format(self.tr('What is the time range of interest in seconds relative to the markers?')))
        step_5.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        time_bounds_start = QLineEdit(str(-0.2))

        # Time bounds end.
        time_bounds_end = QLineEdit(str(0.8))

        # Form layout.
        time_bounds_form = QFormLayout()
        time_bounds_form.addRow(self.tr('Begining of range'), time_bounds_start)
        time_bounds_form.addRow(self.tr('End of range'), time_bounds_end)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(time_bounds_form)

        ######## Step 6

        step_6 = QLabel(template.format(self.tr('What frequencies do you want to retain?')))
        step_6.setContentsMargins(0, 15, 0, 0)

        # Low frequency band.
        low_frequency_band = QLineEdit(str(0.1))

        # High frequency band.
        high_frequency_band = QLineEdit(str(15))

        # Form layout.
        frequency_bands_form = QFormLayout()
        frequency_bands_form.addRow(self.tr('Pass-band start'), low_frequency_band)
        frequency_bands_form.addRow(self.tr('Pass-band end'), high_frequency_band)

        custom_layout.addWidget(step_6)
        custom_layout.addLayout(frequency_bands_form)

        ######## Attributes.
        self._training_set = training_set
        self._query_string = query_string
        self._marker_string = marker_string
        self._output_stream = output_stream
        self._source_id = source_id
        self._assign_targets = assign_targets
        self._time_bounds_start = time_bounds_start
        self._time_bounds_end = time_bounds_end
        self._low_frequency_band = low_frequency_band
        self._high_frequency_band = high_frequency_band

        return custom_layout

    def get_patch(self):
        return {
            'Import XDF': {
                'filename': self._training_set.text()
            },
            'LSL Input': {
                'query': self._query_string.text(),
                'marker_query': self._marker_string.text()
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),
                'source_id': self._source_id.text()
            },
            'Assign Targets': {
                'mapping': self._assign_targets.text()
            },
            'Segmentation': {
                'time_bounds': '({0}, {1})'.format(self._time_bounds_start.text(),
                                                   self._time_bounds_end.text())
            },
            'Spectral Selection': {
                'frequencies': '[{0}, {1}]'.format(self._low_frequency_band.text(),
                                                   self._high_frequency_band.text())
            }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
