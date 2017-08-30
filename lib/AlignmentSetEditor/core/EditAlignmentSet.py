import os
import uuid
import re
import shutil
from pprint import pprint, pformat

from Workspace.WorkspaceClient import Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DataFileUtil.baseclient import ServerError as DFUError
from SetAPI.SetAPIClient import SetAPI

class EditAlignmentSet:
    """
     Constains a set of functions for expression levels calculations.
    """

    PARAM_IN_WS_NAME_ID = 'workspace_name'
    PARAM_IN_OBJ_NAME_ID = 'output_object_name'
    PARAM_IN_ALIGNSET_REF = 'alignment_set_ref'
    PARAM_IN_ALIGNS_ADD = 'alignments_to_add'
    PARAM_IN_ALIGNS_RM = 'alignments_to_remove'

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'EM_' + str(uuid.uuid4()))
        self.ws_url = config['workspace-url']
        self.ws_client = Workspace(self.ws_url)
        self.dfu = DataFileUtil(self.callback_url)
        self.setAPI = SetAPI(self.callback_url)
        pass

    def _process_params(self, params):
        """
        validates params passed to gen expression matrix method
        """
        for p in [self.PARAM_IN_ALIGNSET_REF,
                  self.PARAM_IN_OBJ_NAME_ID,
                  self.PARAM_IN_WS_NAME_ID
                 ]:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        ws_name_id = params.get(self.PARAM_IN_WS_NAME_ID)
        if not isinstance(ws_name_id, int):
            try:
                ws_name_id = self.dfu.ws_name_to_id(ws_name_id)
            except DFUError as se:
                prefix = se.message.split('.')[0]
                raise ValueError(prefix)

        alignments_to_add = params.get(self.PARAM_IN_ALIGN_ADD)
        alignments_to_remove = params.get(self.PARAM_IN_ALIGN_RM)

        if alignments_to_add is None and alignments_to_remove is None:
            raise ValueError('"{}" or "{}" should be given'.format(
                params.get(self.PARAM_IN_ALIGN_ADD),
                params.get(self.PARAM_IN_ALIGN_RM))

    def _add_alignments(self, alignment_set_items, alignment_refs_list):

        for alignment_ref in alignment_refs_list:
            alignment_set_items.append({
                            'ref': alignment_ref
                        })

        return alignment_set_items

    def _remove_alignments(self, input_alignment_set, alignment_set_items, alignments_to_remove):

        for input_item in input_alignment_set:
            if input_item.get('ref') is not in alignments_to_remove:
                alignment_set_items.append(input_item)

        return alignment_set_items

    def save_alignment_set(self, ws_name, obj_name, set_items):

        res = self.setAPI.save_differential_expression_matrix_set_v1({
                                        "workspace": ws_name),
                                        "output_object_name": obj_name,
                                        "data": set_items
                                        })
        return res.get('set_ref')

    def edit_alignment_set(self, params):

        self._process_params(params)

        alignment_set_ref = params.get(self.PARAM_IN_ALIGNSET_REF)

        alignment_set_obj = self.dfu.get_objects(
                                    {'object_refs': [alignment_set_ref]})['data'][0]

        alignment_set_obj_type = alignment_set_obj.get('info')[2]

        if re.match('KBaseSets.AlignmentSet-\d.\d', alignment_set_obj_type):
            raise ValueError(TypeError(self.PARAM_IN_ALIGNSET_REF + ' should be of type ' +
                            'KBaseSets.AlignmentSet'))

        input_alignment_set = alignment_set_obj.get('data').get('items')

        alignments_to_remove = params.get(self.PARAM_IN_ALIGNS_RM)
        alignments_to_add = params.get(self.PARAM_IN_ALIGNS_ADD)

        set_items = list()
        set_items = self._remove_alignments(input_alignment_set, set_items, alignments_to_remove)
        set_items = self._add_alignments(set_items, alignments_to_add)

        output_alignment_set_ref = self._save_alignmentSet(ws_name,
                                                           obj_name,
                                                           set_items)