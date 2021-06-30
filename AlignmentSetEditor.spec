/*
A KBase module: AlignmentSetEditor
*/

module AlignmentSetEditor {
    /*
        Module to edit Alignment sets
    */

    /*
        An X/Y/Z style reference
    */
    typedef string obj_ref;

    /**
    EditMediaParams object: arguments for the edit alignment function

    alignment_set_ref     - Input alignment set object to be edited
	alignments_to_remove  - Optional, List of alignment objects (refs) to be removed
	alignments_to_add     - Optional, List of alignment objects (refs) to be added
	                      - If object already in the input set, it will not be added
	                      - *** Either alignments_to_remove or alignments_to_add should be given ***
	workspace_name        - workspace name for the output
	output_object_name    - output object name
    **/

    typedef structure {
		obj_ref         alignment_set_ref;
		list<obj_ref>   alignments_to_remove;
		list<obj_ref>   alignments_to_add;
		string          workspace_name;
		string          output_object_name;
    } EditAlignmentSetParams;

    typedef structure {
		string          report_name;
		obj_ref         report_ref;
		obj_ref         alignment_set_ref;
    } EditAlignmentSetResult;

    /*
    Edit models
    */
    funcdef edit_alignment_set(EditAlignmentSetParams params)
                      returns (EditAlignmentSetResult)
                      authentication required;


    typedef structure {
        obj_ref         alignment_set_ref;
        string          workspace_name;
    } DisplayAlignmentSetParams;

    typedef structure {
        string          report_name;
        obj_ref         report_ref;
    } DisplayAlignmentSetResult;

    /*
    Display Alignment set details
    */
    funcdef display_alignment_set(DisplayAlignmentSetParams params)
                      returns (DisplayAlignmentSetResult)
                      authentication required;


};


