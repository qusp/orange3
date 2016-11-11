from PyQt4.QtGui import QFileDialog, QFormLayout, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QFont

from .quickstartwizarddialog import QuickstartWizardDialog


class ERPClassificationQuickstartWizardDialog(QuickstartWizardDialog):
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
                           "e.g. correct, incorrect.")
        step_3.setWordWrap(True)
        step_3.setContentsMargins(0, 15, 0, 0)

        # Assign targets.
        assign_targets = QLineEdit("correct, incorrect")

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

        # ######## Step 6
        #
        # step_6 = self.step('Enter the desired cut-off frequency for the '
        #                    'anti-aliasing lowpass filter, in Hz. (e.g. if the '
        #                    'reduced sampling rate is going to be 100Hz, '
        #                    'the cut-off frequency should be lower than 50Hz.)')
        #
        # step_6.setContentsMargins(0, 15, 0, 0)
        #
        # # Assign cut-off frequency.
        # cutoff_frequncy = QLineEdit("50")
        #
        # custom_layout.addWidget(step_6)
        # custom_layout.addWidget(cutoff_frequncy)
        #
        # ######## Step 7
        # step_7 = self.step("Enter the decimation ratio to be used to reduce "
        #                    "the sampling rate.")
        # step_7.setContentsMargins(0, 15, 0, 0)
        #
        # # Assign targets.
        # decimation_rate = QLineEdit("1")
        #
        # custom_layout.addWidget(step_7)
        # custom_layout.addWidget(decimation_rate)
        #
        # ######## Step 8
        #
        # step_8 = self.step('Enter the spectral range to '
        #                    'be considered for ERP detection, in Hz.')
        # step_8.setContentsMargins(0, 15, 0, 0)
        #
        # # Time bounds start.
        # spectral_bounds_start = QLineEdit("0.1")
        #
        # # Time bounds end.
        # spectral_bounds_end = QLineEdit("15")
        #
        # # Form layout.
        # spectral_bounds_form = QFormLayout()
        # spectral_bounds_form.addRow(self.tr('Beginning of spectral range'),
        #                         spectral_bounds_start)
        # spectral_bounds_form.addRow(self.tr('End of spectral range'),
        #                         spectral_bounds_end)
        #
        # custom_layout.addWidget(step_8)
        # custom_layout.addLayout(spectral_bounds_form)



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
                'selection':'{0}:{1}'.format(self._channel_select_start.text(),
                                                   self._channel_select_end.text())
            },
            'Segmentation': {
                'time_bounds': '({0}, {1})'.format(self._time_bounds_start.text(),
                                                   self._time_bounds_end.text())
            }
            # 'FIR Filter': {
            #     'frequencies': '[{0}, {1}]'.format(cutoff - 5, cutoff)
            # },
            # 'Decimate':{
            #     'factor':self._decimation_rate.text()
            # },
            # 'Spectral Selection':{
            #     'frequencies':'({0}, {1})'.format(self._spectral_bounds_start.text(),
            #         self._spectral_bounds_end.text())
            # }
        }

    def open_file_dialog(self):
        import os
        path = QFileDialog.getOpenFileName(self, self.tr('Open File'), os.getcwd())
        if path:
            self._training_set.setText(path)
