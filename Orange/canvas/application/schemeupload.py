import json
import warnings
import requests
import random
import ast
import copy

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QDialog, QFormLayout, QSizePolicy, QLineEdit, \
    QComboBox, QTextEdit, QVBoxLayout, QLabel, QDialogButtonBox, QHBoxLayout

from neuropype.engine import Graph
from neuropype.utilities.cloud.graph_ops import rewrite_lsl2zmq, \
    deduce_inlet_name, deduce_outlet_name
from neuropype.nodes import LSLInput, LSLOutput, InputPort
from neuropype.nodes import ZMQInput, ZMQOutput, MultiplexPackets, \
    DemultiplexPackets

from ..gui.utils import StyledWidget_paintEvent, StyledWidget


class SchemeUploadSettingsEdit(QWidget):
    """Editor widget for upload settings."""
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.graph = None
        self.inlet_map = {}   # map from input name to inlet (e.g., 'default')
        self.outlet_map = {}  # map from output name to outlet (e.g., 'default')
        self.had_warnings = False  # whether there were warnings during patch processing
        self.__setupUi()

    def __setupUi(self):
        layout = QFormLayout()
        layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # name of the pipeline
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText(self.tr("untitled"))
        self.name_edit.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Fixed)
        # class of the pipeline (either streaming or batch)
        self.class_edit = QComboBox(self)
        self.class_edit.addItem(self.tr("Streaming"))
        self.class_edit.addItem(self.tr("Batch"))

        # description
        self.desc_edit = QTextEdit(self)
        self.desc_edit.setTabChangesFocus(True)

        # parameters (TODO: replace by some sort of property grid/table)
        #self.parameters_edit = QTextEdit(self)
        #self.parameters_edit.setText(self.tr("{}"))
        #self.parameters_edit.setTabChangesFocus(True)

        sub_layout = QHBoxLayout()
        # meta-data
        self.metadata_edit = QTextEdit(self)
        self.metadata_edit.setText(self.tr("{}"))
        self.metadata_edit.setTabChangesFocus(True)
        sub_layout.addWidget(self.metadata_edit)

        # user properties
        self.userproperties_edit = QTextEdit(self)
        self.userproperties_edit.setText(self.tr("{}"))
        self.userproperties_edit.setTabChangesFocus(True)
        sub_layout.addWidget(self.userproperties_edit)

        # access token
        self.accesstoken_edit = QLineEdit(self)
        self.accesstoken_edit.setPlaceholderText(self.tr("01234567-89ab-cdef-"
                                                         "0123-456789abcdef"))
        self.accesstoken_edit.setText(self.tr("0db986d2-8de8-47bd-9a86-276fbccf447d"))

        self.accesstoken_edit.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Fixed)

        # API URL
        self.apiurl_edit = QComboBox(self)
        self.apiurl_edit.addItem(self.tr("https://api.neuroscale.io"))
        self.apiurl_edit.addItem(self.tr("http://testingpl-platform-nheffw2rqyof-675729029.us-west-1.elb.amazonaws.com"))
        self.apiurl_edit.setCurrentIndex(0)

        layout.addRow(self.tr("Pipeline Name"), self.name_edit)
        layout.addRow(self.tr("Pipeline Class"), self.class_edit)
        layout.addRow(self.tr("Description"), self.desc_edit)
        #layout.addRow(self.tr("Parameters"), self.parameters_edit)
        layout.addRow(self.tr("Metadata / User Properties"), sub_layout)
        layout.addRow(self.tr("NeuroScale Access Token"), self.accesstoken_edit)
        layout.addRow(self.tr("NeuroScale API URL"), self.apiurl_edit)

        self.__schemeIsUntitled = True

        self.setLayout(layout)

    def setScheme(self, scheme):
        """Set the scheme to upload."""
        self.inlet_map = {}
        self.outlet_map = {}
        self.graph = scheme.signal_manager.graph
        # set documentation
        self.name_edit.setText(scheme.title or "untitled")
        self.desc_edit.setPlainText(scheme.description or "")
        # determine whether this is a streaming or batch pipeline
        inlets = [s for s in self.graph.sources() if isinstance(s, LSLInput)]
        outlets = [s for s in self.graph.sinks() if isinstance(s, LSLOutput)]
        params = [s for s in self.graph.sources() if isinstance(s, InputPort)]
        forbidden = [s for s in self.graph.nodes()
                     if isinstance(s, (ZMQInput, ZMQOutput, DemultiplexPackets,
                                       MultiplexPackets))]
        if forbidden:
            raise RuntimeError("The given patch appears to contain nodes that "
                               "would normally be auto-generated (%s); please "
                               "remove them and use LSL nodes instead." %
                               forbidden)
        is_streaming = len(inlets) + len(outlets) > 0
        self.class_edit.setCurrentIndex(0 if is_streaming else 1)
        # pre-generate JSON meta-data
        if is_streaming:
            input_nodes = {}
            output_nodes = {}
            # parse the LSLInput nodes
            for n in inlets:
                name = deduce_inlet_name(n)
                if n.query.startswith("type='"):
                    modality = n.query[6:-1]
                elif n.query.startswith("name='"):
                    modality = 'EEG'
                else:
                    modality = 'EEG'
                srate = n.nominal_rate or 0.0
                labels = n.channel_names or ['dummy']

                signal_stream = {"name": "signal",
                                 "type": modality,
                                 "sampling_rate": srate,
                                 "channels": [{"label": l} for l in labels]}
                marker_stream = {"name": "markers",
                                 "type": "Markers",
                                 "sampling_rate": 0,
                                 "channels": [{"label": "dummy"}]}
                upstreams = ([signal_stream, marker_stream]
                             if n.marker_query else [signal_stream])
                node_decl = {"name": name, "streams": upstreams}
                if name in input_nodes:
                    raise RuntimeError("There is more than one inlet with "
                                       "query name '%s' in the graph; if there "
                                       "is more than one, at least one of them "
                                       "must have the query name set to a "
                                       "unique string." % name)
                input_nodes[name] = node_decl
                self.inlet_map[name] = n
            # parse the LSLOutput nodes
            for n in outlets:
                name = deduce_outlet_name(n)
                srate = n.srate or 10.0
                output_stream = {"name": "signal",
                                 "type": "Control",
                                 "sampling_rate": srate,
                                 "channels": [{"label": "dummy"}]}
                marker_stream = {"name": "markers",
                                 "type": "Markers",
                                 "sampling_rate": 0,
                                 "channels": [{"label": "dummy"}]}
                downstreams = ([output_stream, marker_stream]
                               if n.send_markers else [output_stream])
                node_decl = {"name": name, "streams": downstreams}
                if name in output_nodes:
                    raise RuntimeError("There is more than one outlet with "
                                       "name '%s' in the graph; if there is "
                                       "more than one, at least one of them "
                                       "must have the stream name set to a "
                                       "unique string." % name)
                output_nodes[name] = node_decl
                self.outlet_map[name] = n
            # sanity-check node names
            if len(input_nodes) > 1 and 'default' not in input_nodes:
                print("WARNING: A pipeline should have exactly one input "
                      "node with name 'default', unless none of the nodes "
                      "can be considered the default.")
                self.had_warnings = True
            if len(output_nodes) > 1 and 'default' not in output_nodes:
                print("WARNING: A pipeline should have exactly one output "
                      "node with name 'default', unless none of the nodes "
                      "can be considered the default.")
                self.had_warnings = True
            if len(input_nodes) == 1 and 'default' not in input_nodes:
                warnings.warn("WARNING: A pipeline should have exactly one "
                              "input node with name 'default' (query set to "
                              "name='default' for LSLInput node).")
                self.had_warnings = True
            if len(output_nodes) == 1 and 'default' not in output_nodes:
                warnings.warn("WARNING: A pipeline should have exactly one "
                              "output node with name 'default' (stream name "
                              "for LSLOutput node).")
                self.had_warnings = True
            # construct node meta-data
            metadata = {"nodes": {"in": list(input_nodes.values()),
                                  "out": list(output_nodes.values())}}
            metadata_encoded = json.dumps(metadata, indent=2)
            self.metadata_edit.setText(metadata_encoded)
        else:
            self.metadata_edit.setText("{}")
        # pre-generate parameters
        param_entries = {}
        for n in params:
            name = n.portname
            desc = n.description
            default = ast.literal_eval(n.default)
            if name in param_entries:
                raise RuntimeError("There is more than one input node with "
                                   "port name '%s' in the graph; if there is "
                                   "more than one, at least one of them must "
                                   "have the port name set to a unique string."
                                   % name)
            param_entries[name] = {"descrption": desc,
                                   "value": default,
                                   "node": "TODO"}  # TODO!!!
        params_encoded = json.dumps(param_entries, indent=2)
        # self.parameters_edit.setText(params_encoded)

    def paintEvent(self, event):
        return StyledWidget_paintEvent(self, event)

    def title(self):
        return str(self.name_edit.text()).strip()

    def description(self):
        return str(self.desc_edit.toPlainText()).strip()


class SchemeUploadDialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.scheme = None
        self.__setupUi()

    def __setupUi(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = SchemeUploadSettingsEdit(self)
        self.editor.layout().setContentsMargins(20, 20, 20, 20)
        self.editor.layout().setSpacing(15)
        self.editor.setSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.MinimumExpanding)

        heading = self.tr("Upload Pipeline to NeuroScale")
        heading = "<h3>{0}</h3>".format(heading)
        self.heading = QLabel(heading, self, objectName="heading")

        # Insert heading
        self.editor.layout().insertRow(0, self.heading)
        self.buttonbox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        # Insert button box
        self.editor.layout().addRow(self.buttonbox)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        layout.addWidget(self.editor, stretch=10)
        self.setLayout(layout)

    def setScheme(self, scheme):
        """Set the scheme to upload."""
        self.scheme = scheme
        self.editor.setScheme(scheme)

    def upload(self):
        """Upload the current contents of the editor widgets."""
        api_url = self.editor.apiurl_edit.currentText()
        access_token = self.editor.accesstoken_edit.text()
        auth_header = {'Authorization': 'Bearer ' + access_token}

        new_graph = Graph()
        new_graph.load_graph(data=self.editor.graph.save_graph())
        new_graph = rewrite_lsl2zmq(new_graph)
        patch_encoded = new_graph.save_graph()

        params = {
            "name": self.editor.name_edit.text(),
            "type": ("stream"
                     if self.editor.class_edit.currentText() == "Streaming"
                     else "batch"),
            "description": self.editor.desc_edit.toPlainText(),
            "metadata": json.loads(self.editor.metadata_edit.toPlainText()),
            "patch": json.loads(patch_encoded),
            "properties": json.loads(self.editor.userproperties_edit.toPlainText()),
        }
        # get the id of any previous pipeline with that same name, if any
        prev_id = self.pipeline_id(self.editor.name_edit.text(), api_url,
                                   auth_header)
        # post or patch the pipeline
        if not prev_id:
            r = requests.post(api_url + '/v1/pipelines',
                              headers=auth_header, json=params)
        else:
            headers = {'Authorization': auth_header['Authorization'],
                       'Content-Type': 'application/json'}
            r = requests.patch(api_url + '/v1/pipelines/' + prev_id,
                               headers=headers, data=json.dumps(params))
        # handle outcome
        if r.status_code == 201 or r.status_code == 200:
            if not self.editor.had_warnings:
                print("patch successfully uploaded.")
            else:
                print("patch uploaded WITH SOME WARNINGS. Your patch may not "
                      "run as expected.")
        else:
            raise RuntimeError('Could not upload patch (HTTP %i)' %
                               r.status_code)

    # noinspection PyMethodMayBeStatic
    def pipeline_id(self, name, api_url, auth_header):
        """Retrieve the id of a pipeline with a given name."""
        r = requests.get(api_url + '/v1/pipelines', headers=auth_header)
        if r.status_code == 200:  # 200: ok
            body = r.json()
            pipelines = body['data']
            for p in pipelines:
                if p['name'] == name:
                    return p['id']
            else:
                return None
        else:
            raise RuntimeError("Could not query available pipelines "
                               "(HTTP %s); check your API URL and "
                               "credentials." % r.status_code)
