# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import time
import logging
import uuid
import shutil



from biokbase.workspace.client import Workspace
from AlignmentSetEditor.core.EditAlignmentSet import EditAlignmentSet
from AlignmentSetEditor.core.htmlreportutils import htmlreportutils

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
    GIT_URL = "git@github.com:pranjan77/Alignmentseteditor"
    GIT_COMMIT_HASH = "b107886d223e8b60a371d0bf7c10c3671406a2e9"

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
        self.hr = htmlreportutils()
        self.workspace_client = Workspace(self.ws_url)
        self.edit_alignmentset = EditAlignmentSet(config, self.__LOGGER)
        #END_CONSTRUCTOR
        pass


    def edit_alignment_set(self, ctx, params):
        """
        Edit models
        :param params: instance of type "EditAlignmentSetParams" (*
           EditMediaParams object: arguments for the edit alignment function
           alignment_set_ref     - Input alignment set object to be edited
           alignments_to_remove  - Optional, List of alignment objects (refs)
           to be removed alignments_to_add     - Optional, List of alignment
           objects (refs) to be added - If object already in the input set,
           it will not be added - *** Either alignments_to_remove or
           alignments_to_add should be given *** workspace_name        -
           workspace name for the output output_object_name    - output
           object name *) -> structure: parameter "alignment_set_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "alignments_to_remove" of list of type "obj_ref" (An X/Y/Z style
           reference), parameter "alignments_to_add" of list of type
           "obj_ref" (An X/Y/Z style reference), parameter "workspace_name"
           of String, parameter "output_object_name" of String
        :returns: instance of type "EditAlignmentSetResult" -> structure:
           parameter "report_name" of String, parameter "report_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "alignment_set_ref" of type "obj_ref" (An X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN edit_alignment_set

        #alignment_set_ref = self.edit_alignmentset.edit_alignment_set(params)
        # Get all the genome ids from our ReadsAlignment references (it's the genome_id key in
        # the object metadata). Make a set out of them.
        # If there's 0 or more than 1 item in the set, then either those items are bad, or they're
        # aligned against different genomes.
        alignment_set_ref = params['alignment_set_ref']
        obj_data = self.workspace_client.get_objects2({"objects": [{'ref':alignment_set_ref}]})["data"][0]
 
        data = obj_data["data"]
            
        refs = list()
        for item in data["items"]:
            refs.append(item["ref"])

        for ref in params['alignments_to_add']:
             refs.append(ref)

        ref_list = list([{"ref": r} for r in refs])

             
        info = self.workspace_client.get_object_info3({"objects": ref_list, "includeMetadata": 1})
        num_genomes = len(set([item[10]["genome_id"] for item in info["infos"]]))
        if num_genomes == 0 or num_genomes > 1:
            raise ValueError("All input alignments must be aligned "
                             "against the same genome reference. "
                             "All alignments must be created in the same narrative. "
                             "Alignments created in different narratives can not "
                             "be combined into a set.")
        new_alignment_set_ref = self.edit_alignmentset.edit_alignment_set(params)
        returnVal = {'alignment_set_ref': new_alignment_set_ref}

        #END edit_alignment_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method edit_alignment_set return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def display_alignment_set(self, ctx, params):
        """
        Display Alignment set details
        :param params: instance of type "DisplayAlignmentSetParams" ->
           structure: parameter "alignment_set_ref" of type "obj_ref" (An
           X/Y/Z style reference), parameter "workspace_name" of String
        :returns: instance of type "DisplayAlignmentSetResult" -> structure:
           parameter "report_name" of String, parameter "report_ref" of type
           "obj_ref" (An X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN display_alignment_set
        alignment_set_ref = params['alignment_set_ref']
        obj_data = self.workspace_client.get_objects2({"objects": [{'ref':alignment_set_ref}]})["data"][0]
 
        data = obj_data["data"]
            
        refs = list()
        for item in data["items"]:
            refs.append(item["ref"])


        ref_list = list([{"ref": r} for r in refs])

             
        info = self.workspace_client.get_object_info3({"objects": ref_list, "includeMetadata": 1})


        report_string = '<table><tr><th>Ref</th><th>Name</th></tr>'

        for count,alignment in enumerate(info['infos']):
           ref = str(alignment[6]) + "/" + str(alignment[0]) + "/" + str(alignment[4])
           name = alignment[1]
           report_string += '<tr><td>' + str(count) + '</td><td>' + str(ref) + '</td><td>' + str(name) + '</td></tr>'

        report_string +='</table>'
      
        directory = str(uuid.uuid4())
        path = os.path.join("/kb/module/work/tmp", directory)
        os.mkdir(path)
        html_path=os.path.join(path,"index.html")

        print (html_path)
        with open (html_path, "w") as f:
            f.write("<html><body>")
            f.write(report_string)
            f.write("</body></html>")
        returnVal = self.hr.create_html_report(path, params['workspace_name'])
 

        #END display_alignment_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method display_alignment_set return value ' +
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
