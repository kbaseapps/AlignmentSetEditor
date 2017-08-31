# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import time
import logging

from core.EditAlignmentSet import EditAlignmentSet
#END_HEADER


class AlignmentSetEditor:
    '''
    Module Name:
    AlignmentSetEditor

    Module Description:
    A KBase module: AlignmentSetEditor
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "6ad66af999a9585501af0ecf3a8870d7076aa24f"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.__LOGGER = logging.getLogger('EditAlignmentSet')
        self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        self.config = config
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        self.edit_alignmentset = EditAlignmentSet(config, self.__LOGGER)
        #END_CONSTRUCTOR
        pass


    def edit_alignment_set(self, ctx, params):
        """
        Edit models
        :param params: instance of type "EditAlignmentSetParams"
           (EditMediaParams object: arguments for the edit model function) ->
           structure: parameter "alignment_set_ref" of type "obj_ref" (An
           X/Y/Z style reference), parameter "alignments_to_remove" of list
           of type "obj_ref" (An X/Y/Z style reference), parameter
           "alignments_to_add" of list of type "obj_ref" (An X/Y/Z style
           reference), parameter "workspace_name" of String, parameter
           "output_object_name" of String
        :returns: instance of type "EditAlignmentSetResult" -> structure:
           parameter "report_name" of String, parameter "report_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "alignment_set_ref" of type "obj_ref" (An X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN edit_alignment_set

        alignment_set_ref = self.edit_alignmentset.edit_alignment_set(params)

        returnVal = {'alignment_set_ref': alignment_set_ref}

        #END edit_alignment_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method edit_alignment_set return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
