
package us.kbase.alignmentseteditor;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: EditAlignmentSetParams</p>
 * <pre>
 * EditMediaParams object: arguments for the edit model function
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "alignment_set_ref",
    "alignments_to_remove",
    "alignments_to_add",
    "workspace_name",
    "output_object_name"
})
public class EditAlignmentSetParams {

    @JsonProperty("alignment_set_ref")
    private java.lang.String alignmentSetRef;
    @JsonProperty("alignments_to_remove")
    private List<String> alignmentsToRemove;
    @JsonProperty("alignments_to_add")
    private List<String> alignmentsToAdd;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("output_object_name")
    private java.lang.String outputObjectName;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("alignment_set_ref")
    public java.lang.String getAlignmentSetRef() {
        return alignmentSetRef;
    }

    @JsonProperty("alignment_set_ref")
    public void setAlignmentSetRef(java.lang.String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
    }

    public EditAlignmentSetParams withAlignmentSetRef(java.lang.String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
        return this;
    }

    @JsonProperty("alignments_to_remove")
    public List<String> getAlignmentsToRemove() {
        return alignmentsToRemove;
    }

    @JsonProperty("alignments_to_remove")
    public void setAlignmentsToRemove(List<String> alignmentsToRemove) {
        this.alignmentsToRemove = alignmentsToRemove;
    }

    public EditAlignmentSetParams withAlignmentsToRemove(List<String> alignmentsToRemove) {
        this.alignmentsToRemove = alignmentsToRemove;
        return this;
    }

    @JsonProperty("alignments_to_add")
    public List<String> getAlignmentsToAdd() {
        return alignmentsToAdd;
    }

    @JsonProperty("alignments_to_add")
    public void setAlignmentsToAdd(List<String> alignmentsToAdd) {
        this.alignmentsToAdd = alignmentsToAdd;
    }

    public EditAlignmentSetParams withAlignmentsToAdd(List<String> alignmentsToAdd) {
        this.alignmentsToAdd = alignmentsToAdd;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public EditAlignmentSetParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("output_object_name")
    public java.lang.String getOutputObjectName() {
        return outputObjectName;
    }

    @JsonProperty("output_object_name")
    public void setOutputObjectName(java.lang.String outputObjectName) {
        this.outputObjectName = outputObjectName;
    }

    public EditAlignmentSetParams withOutputObjectName(java.lang.String outputObjectName) {
        this.outputObjectName = outputObjectName;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((("EditAlignmentSetParams"+" [alignmentSetRef=")+ alignmentSetRef)+", alignmentsToRemove=")+ alignmentsToRemove)+", alignmentsToAdd=")+ alignmentsToAdd)+", workspaceName=")+ workspaceName)+", outputObjectName=")+ outputObjectName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
