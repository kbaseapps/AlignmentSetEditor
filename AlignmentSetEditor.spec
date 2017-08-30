/*
A KBase module: AlignmentSetEditor
*/

module AlignmentSetEditor {
    /*
        Insert your typespec information here.
    */

    /*
        An X/Y/Z style reference
    */
    typedef string obj_ref;

    /*
    EditMediaParams object: arguments for the edit model function
    */
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
    funcdef edit_alignment_set(EditAlignmentSetParams params) returns (EditAlignmentSetResult) authentication required;
};


