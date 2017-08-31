# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from AlignmentSetEditor.AlignmentSetEditorImpl import AlignmentSetEditor
from AlignmentSetEditor.AlignmentSetEditorServer import MethodContext
from AlignmentSetEditor.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from SetAPI.SetAPIClient import SetAPI
#from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils

class AlignmentSetEditorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('AlignmentSetEditor'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'AlignmentSetEditor',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = AlignmentSetEditor(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.setAPI = SetAPI(cls.callback_url)
        #cls.rau = ReadsAlignmentUtils(cls.callback_url, service_ver='dev')
        #cls.setupData()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_AlignmentSetEditor_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def setupData(cls):

        # upload genome object
        genbank_file_name = 'minimal.gbff'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.wsName,
                                                    'genome_name': genome_object_name
                                                    })['genome_ref']
        # upload alignment objects
        alignment_file_name = 'accepted_hits.bam'
        alignment_file_path = os.path.join(cls.scratch, alignment_file_name)
        shutil.copy(os.path.join('data', alignment_file_name), alignment_file_path)

        alignment_object_name_1 = 'test_Alignment_1'
        cls.condition_1 = 'test_condition_1'
        destination_ref = cls.wsName + '/' + alignment_object_name_1
        cls.alignment_ref_1 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_1,
                                                        'condition': cls.condition_1,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']

        alignment_object_name_2 = 'test_Alignment_2'
        cls.condition_2 = 'test_condition_2'
        destination_ref = cls.wsName + '/' + alignment_object_name_2
        cls.alignment_ref_2 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_2,
                                                        'condition': cls.condition_2,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Following test uses object refs from a narrative. Comment the next line to run the test
    # @unittest.skip("skipped test_edit_alignment_set_success")
    def test_edit_alignment_set_success(self):

        appdev_alignment_set_ref = '5264/36/9'
        alignments_to_remove = ['2409/380/9', '2409/383/9']
        alignments_to_add = ['2409/381/9', '2409/382/9']

        params = {'alignment_set_ref': appdev_alignment_set_ref,
                  'alignments_to_remove': alignments_to_remove,
                  'workspace_name': self.getWsName(),
                  'output_object_name': 'test_edit_alignment_set',
                  'alignments_to_remove': alignments_to_remove,
                  'alignments_to_add': alignments_to_add
                  }

        edit_retVal = self.getImpl().edit_alignment_set(self.ctx, params)[0]

        inputObj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': appdev_alignment_set_ref
                                    })

        print("============ INPUT EXPRESSION SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        alignment_set_ref = edit_retVal.get('alignment_set_ref')
        outputObj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': alignment_set_ref
                                    })

        print("============ OUTPUT EXPRESSION SET OBJECT ==============")
        pprint(outputObj)
        print("==========================================================")