from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QFont

from .quickstartwizarddialog import QuickstartWizardDialog


class MotorImageryClassificationQuickstartWizardDialog(QuickstartWizardDialog):
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
                ######## Step 3

        step_3 = self.step("What are the marker labels corresponding to the "
                           "events that you would like to classify? "
                           "You can enter them seperated by comma, "
                           "e.g. left, right.")
        step_3.setWordWrap(True)
        step_3.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        assign_targets = QLineEdit("left, right")

        custom_layout.addWidget(step_3)
        custom_layout.addWidget(assign_targets)

        ######## Step 4

        step_4 = self.step('What is the desired channel range you want to '
                           'include in the pipeline process? For example you '
                           'can exclude channels that are known to be trigger '
                           'channels. ')
        step_4.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        channel_select_start = QLineEdit("0")

        # Time bounds end.
        channel_select_end = QLineEdit("20")

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

        step_5 = self.step('What is the range for the time window to be '
                           'extracted around each event marker that shall be '
                           'classified?')
        step_5.setContentsMargins(0, 15, 0, 0)

        # Time bounds start.
        time_bounds_start = QLineEdit("0.5")

        # Time bounds end.
        time_bounds_end = QLineEdit("3.5")

        # Form layout.
        time_bounds_form = QFormLayout()
        time_bounds_form.addRow(self.tr('Beginning of time range'),
                                time_bounds_start)
        time_bounds_form.addRow(self.tr('End of time range'), time_bounds_end)

        custom_layout.addWidget(step_5)
        custom_layout.addLayout(time_bounds_form)

        # ######## Step 6
        #
        # step_6 = self.step('Enter the desired frequency band to be retained in '
        #                    'the data stream, in Hz.')
        # step_6.setContentsMargins(0, 15, 0, 0)
        #
        # # Low frequency band.
        # low_frequency_band = QLineEdit("4")
        #
        # # High frequency band.
        # high_frequency_band = QLineEdit("42")
        #
        # # Form layout.
        # frequency_bands_form = QFormLayout()
        # frequency_bands_form.addRow(self.tr('Pass-band start frequency'),
        #                             low_frequency_band)
        # frequency_bands_form.addRow(self.tr('Pass-band end frequency'),
        #                             high_frequency_band)
        #
        # custom_layout.addWidget(step_6)
        # custom_layout.addLayout(frequency_bands_form)
        #
        # ######## Step 7
        #
        # step_7 = self.step("Enter the number of spatial filters to be "
        #                    "designed per target class. (typically "
        #                    "between 1 and 4)")
        # step_7.setContentsMargins(0, 15, 0, 0)
        #
        # # Assign targets.
        # num_features = QLineEdit("3")
        #
        # custom_layout.addWidget(step_7)
        # custom_layout.addWidget(num_features)

        ######## Attributes.
        self._query_name = query_name
        self._output_stream = output_stream
        self._assign_targets = assign_targets
        self._channel_select_start = channel_select_start
        self._channel_select_end = channel_select_end
        self._time_bounds_start = time_bounds_start
        self._time_bounds_end = time_bounds_end
        # self._cutoff_frequncy = cutoff_frequncy
        # self._decimation_rate = decimation_rate
        # self._spectral_bounds_start = spectral_bounds_start
        # self._spectral_bounds_end = spectral_bounds_end

        return custom_layout

    def get_patch(self):

        if not self._query_name.text():
            self._query_name.setText("type='EEG'")
        else:
            self._query_name.setText("name=" + "'" + self._query_name.text() +
                                     "'")

        target_list = [x.strip() for x in self._assign_targets.text().split(',')]
        target_dict = str({target_list[x]:x for x in range(len(
            target_list))})

        return {

            'LSL Input': {
                'query': self._query_name.text()
            },
            'LSL Output': {
                'stream_name': self._output_stream.text(),

            },
            'Assign Targets': {
                 'mapping': target_dict,
            },
            'Select Range':{
                'selection':'{0}:{1}'.format(
                    self._channel_select_start.text(),
                                                   self._channel_select_end.text())
            },
            'Segmentation': {
                'time_bounds': '({0}, {1})'.format(self._time_bounds_start.text(),
                                                   self._time_bounds_end.text())
            }
            # 'FIR Filter': {
            #     'frequencies': '[{0}, {1}, {2}, {3}]'.format(band_lo-1,
            #                                                  band_lo, band_hi,
            #                                                  band_hi+1)
            # },
            # 'Filter Bank Common Spatial Patterns': {
            #     'desired_number_of_filters': self._num_features.text()
            # }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
