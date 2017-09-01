# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil
import inspect
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
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil

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
        cls.setAPI = SetAPI(cls.callback_url)
        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.ru = ReadsUtils(cls.callback_url)
        cls.rau = ReadsAlignmentUtils(cls.callback_url)
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
                                                    'workspace_name': cls.getWsName(),
                                                    'genome_name': genome_object_name
                                                    })['genome_ref']
        # upload reads object
        reads_file_name = 'Sample1.fastq'
        reads_file_path = os.path.join(cls.scratch, reads_file_name)
        shutil.copy(os.path.join('data', reads_file_name), reads_file_path)

        reads_object_name_1 = 'test_Reads_1'
        cls.reads_ref_1 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.getWsName(),
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_1
                                               })['obj_ref']
        # upload alignment objects
        alignment_file_name = 'alignment.bam'
        alignment_file_path = os.path.join(cls.scratch, alignment_file_name)
        shutil.copy(os.path.join('data', alignment_file_name), alignment_file_path)

        alignment_object_name_1 = 'test_Alignment_1'
        cls.condition_1 = 'test_condition_1'
        destination_ref = cls.getWsName() + '/' + alignment_object_name_1
        cls.alignment_ref_1 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_1,
                                                        'condition': cls.condition_1,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']

        alignment_object_name_2 = 'test_Alignment_2'
        cls.condition_2 = 'test_condition_2'
        destination_ref = cls.getWsName() + '/' + alignment_object_name_2
        cls.alignment_ref_2 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_1,
                                                        'condition': cls.condition_2,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']
        alignment_object_name_3 = 'test_Alignment_3'
        cls.condition_3 = 'test_condition_3'
        destination_ref = cls.getWsName() + '/' + alignment_object_name_3
        cls.alignment_ref_3 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_1,
                                                        'condition': cls.condition_3,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']
        alignment_object_name_4 = 'test_Alignment_4'
        cls.condition_4 = 'test_condition_4'
        destination_ref = cls.getWsName() + '/' + alignment_object_name_4
        cls.alignment_ref_4 = cls.rau.upload_alignment({'file_path': alignment_file_path,
                                                        'destination_ref': destination_ref,
                                                        'read_library_ref': cls.reads_ref_1,
                                                        'condition': cls.condition_4,
                                                        'library_type': 'single_end',
                                                        'assembly_or_genome_ref': cls.genome_ref
                                                        })['obj_ref']

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Following test uses object refs from a narrative. Comment the next line to run the test
    @unittest.skip("skipped test_edit_alignment_set_success")
    def test_edit_appdev_alignment_set_success(self):

        appdev_alignment_set_ref = '5264/36/9'
        alignments_to_remove = ['2409/380/9', '2409/383/9']
        alignments_to_add = ['2409/381/9', '2409/382/9']

        params = {'alignment_set_ref': appdev_alignment_set_ref,
                  'workspace_name': self.getWsName(),
                  'output_object_name': 'test_edit_alignment_set_1',
                  'alignments_to_remove': alignments_to_remove,
                  'alignments_to_add': alignments_to_add
                  }

        edit_retVal = self.getImpl().edit_alignment_set(self.ctx, params)[0]

        inputObj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': appdev_alignment_set_ref
                                    })

        print("============ INPUT ALIGNMENT SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        alignment_set_ref = edit_retVal.get('alignment_set_ref')
        outputObj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': alignment_set_ref
                                    })

        print("============ OUTPUT ALIGNMENT SET OBJECT ==============")
        pprint(outputObj)
        print("==========================================================")

    #@unittest.skip("skipped test_edit_alignment_set_success")
    def test_edit_ci_alignment_set_success(self):

        ci_alignment_set_ref = '25418/3/2'
        alignments_to_remove = ['23192/126/3', '23192/129/3']
        alignments_to_add = ['25418/5/3', '25418/4/3']

        params = {'alignment_set_ref': ci_alignment_set_ref,
                  'workspace_name': self.getWsName(),
                  'output_object_name': 'test_edit_alignment_set_1',
                  'alignments_to_remove': alignments_to_remove,
                  'alignments_to_add': alignments_to_add
                  }

        edit_retVal = self.getImpl().edit_alignment_set(self.ctx, params)[0]

        inputObj = self.setAPI.get_reads_alignment_set_v1({
            'ref': ci_alignment_set_ref
        })

        print("============ INPUT ALIGNMENT SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        alignment_set_ref = edit_retVal.get('alignment_set_ref')
        outputObj = self.setAPI.get_reads_alignment_set_v1({
            'ref': alignment_set_ref
        })

        print("============ OUTPUT ALIGNMENT SET OBJECT ==============")
        pprint(outputObj)
        print("==========================================================")

    '''
    def test_edit_alignment_set_success(self):

        alignment_set_ref = self.alignment_set
        alignments_to_remove = [self.alignment_ref_1]
        alignments_to_add = [self.alignment_ref_3, self.alignment_ref_4]

        params = {'alignment_set_ref': alignment_set_ref,
                  'workspace_name': self.getWsName(),
                  'output_object_name': 'test_edit_alignment_set_2',
                  'alignments_to_remove': alignments_to_remove,
                  'alignments_to_add': alignments_to_add
                  }

        edit_retVal = self.getImpl().edit_alignment_set(self.ctx, params)[0]

        alignment_set_ref = edit_retVal.get('alignment_set_ref')
        outputObj = self.setAPI.get_reads_alignment_set_v1({
                                    'ref': alignment_set_ref
                                    })

        print("============ OUTPUT ALIGNMENT SET OBJECT ==============")
        pprint(outputObj)
        print("==========================================================")

        output_alignment_set = outputObj.get('data').get('items')

        output_alignment_list = list()
        for alignment in output_alignment_set:
            output_alignment_list.append(alignment.get('ref'))

        self.assertEqual(self.alignment_ref_2 in output_alignment_list, True)
        self.assertEqual(self.alignment_ref_3 in output_alignment_list, True)
        self.assertEqual(self.alignment_ref_4 in output_alignment_list, True)
        self.assertEqual(self.alignment_ref_1 in output_alignment_list, False)

    def edit_alignment_set_failure(self, params, error, exception=ValueError, do_startswith=False):

        test_name = inspect.stack()[1][3]
        print('\n******** starting expected edit fail test: ' + test_name + ' *********')
        print('-------------------------------------------------------------------------------------')

        with self.assertRaises(exception) as context:
            self.getImpl().edit_alignment_set(self.ctx, params)
        if do_startswith:
            self.assertTrue(str(context.exception.message).startswith(error),
                            "Error message {} does not start with {}".format(
                                str(context.exception.message),
                                error))
        else:
            self.assertEqual(error, str(context.exception.message))

    def test_edit_fail_no_alignment_set_ref(self):
        self.edit_alignment_set_failure({
                                        'workspace_name': self.getWsName(),
                                        'output_object_name': 'test_edit_alignment_set_2',
                                        'alignments_to_remove': [self.alignment_ref_1],
                                        'alignments_to_add': [self.alignment_ref_3, self.alignment_ref_4]
                                        },
                                        '"alignment_set_ref" parameter is required, but missing')

    def test_edit_fail_no_ws_name(self):
        self.edit_alignment_set_failure({
                                        'alignment_set_ref': self.alignment_set_ref,
                                        'output_object_name': 'test_edit_alignment_set_2',
                                        'alignments_to_remove': [self.alignment_ref_1],
                                        'alignments_to_add': [self.alignment_ref_3, self.alignment_ref_4]
                                        },
                                        '"workspace_name" parameter is required, but missing')

    def test_edit_fail_no_obj_name(self):
        self.edit_alignment_set_failure({
                                        'workspace_name': self.getWsName(),
                                        'alignment_set_ref': alignment_set_ref,
                                        'alignments_to_remove': [self.alignment_ref_1],
                                        'alignments_to_add': [self.alignment_ref_3, self.alignment_ref_4]
                                        },
                                        '"output_object_name" parameter is required, but missing')

    def test_edit_fail_bad_wsname(self):
        self.edit_alignment_set_failure({
                                        'alignment_set_ref': self.alignment_set_ref,
                                        'workspace_name': '&bad',
                                        'output_object_name': 'test_edit_alignment_set_2',
                                        'alignments_to_remove': [self.alignment_ref_1],
                                        'alignments_to_add': [self.alignment_ref_3, self.alignment_ref_4]
                                        },
                                        'Illegal character in workspace name &bad: &')

    def test_edit_fail_non_existant_wsname(self):
        self.edit_alignment_set_failure({
                                        'alignment_set_ref': self.alignment_set_ref,
                                        'workspace_name': '1s',
                                        'output_object_name': 'test_edit_alignment_set_2',
                                        'alignments_to_remove': [self.alignment_ref_1],
                                        'alignments_to_add': [self.alignment_ref_3, self.alignment_ref_4]
                                        },
                                        'No workspace with name 1s exists')

    def test_edit_fail_no_add_or_rm(self):
        self.edit_alignment_set_failure({
                                        'alignment_set_ref': self.alignment_set_ref,
                                        'workspace_name': self.getWsName(),
                                        'output_object_name': 'test_edit_alignment_set_2'
                                        },
                                        'Either "alignments_to_remove" or "alignments_to_add" should be given')
    '''
