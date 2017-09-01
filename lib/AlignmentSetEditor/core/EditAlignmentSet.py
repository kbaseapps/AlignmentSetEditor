import os
import uuid
import re
import shutil
import logging
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
        self.scratch = os.path.join(config['scratch'], 'EAS_' + str(uuid.uuid4()))
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

        alignments_to_add = params.get(self.PARAM_IN_ALIGNS_ADD)
        alignments_to_remove = params.get(self.PARAM_IN_ALIGNS_RM)

        if alignments_to_add is None and alignments_to_remove is None:
            raise ValueError('Either "alignments_to_remove" or "alignments_to_add" should be given')

        return ws_name_id

    def _add_alignments(self, alignment_set_items, alignment_refs_list):

        for alignment_ref in alignment_refs_list:

            found = False
            for set_item in alignment_set_items:
                if set_item.get('ref') == alignment_ref:
                    print('{} already in the input Alignment Set. Not added'.format(alignment_ref))
                    found = True
                    break

            if not found:
                alignment_set_items.append({
                                'ref': alignment_ref
                            })

        return alignment_set_items

    def _remove_alignments(self, input_alignment_set, alignment_set_items, alignments_to_remove):

        for input_item in input_alignment_set:
            if not (input_item.get('ref') in alignments_to_remove):
                alignment_set_items.append(input_item)

        return alignment_set_items

    def _save_alignment_set(self, ws_name, obj_name, set_data):

        res = self.setAPI.save_reads_alignment_set_v1({
                                        "workspace": ws_name,
                                        "output_object_name": obj_name,
                                        "data": set_data
                                        })
        return res.get('set_ref')

    def edit_alignment_set(self, params):

        print('==============  PARAMS  ==============')
        pprint(params)
        print('======================================')

        ws_name_id = self._process_params(params)
        obj_name = params.get(self.PARAM_IN_OBJ_NAME_ID)

        alignment_set_ref = params.get(self.PARAM_IN_ALIGNSET_REF)

        print('INPUT ALIGNMENT SET REF: ' + alignment_set_ref)
        
        alignment_set_obj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': alignment_set_ref
                                    })

        alignment_set_obj_type = alignment_set_obj.get('info')[2]

        print('alignment_set_obj_type::::::: ' + alignment_set_obj_type)

        if not re.match('KBaseSets.ReadsAlignmentSet-\d.\d', alignment_set_obj_type):
            raise ValueError(TypeError(self.PARAM_IN_ALIGNSET_REF + ' should be of type ' +
                            'KBaseSets.ReadsAlignmentSet'))

        input_alignment_set = alignment_set_obj.get('data').get('items')

        alignments_to_remove = params.get(self.PARAM_IN_ALIGNS_RM, None)
        alignments_to_add = params.get(self.PARAM_IN_ALIGNS_ADD, None)

        set_items = list()
        if alignments_to_remove is not None:
            set_items = self._remove_alignments(input_alignment_set, set_items, alignments_to_remove)
        if alignments_to_add is not None:
            set_items = self._add_alignments(set_items, alignments_to_add)

        print('==============  SET_ITEMS ==============')
        pprint(set_items)

        set_data = {'description': 'Edited from {}'.format(alignment_set_ref),
                    'items': set_items}

        output_alignment_set_ref = self._save_alignment_set(ws_name_id,
                                                           obj_name,
                                                           set_data)
        return output_alignment_set_ref
