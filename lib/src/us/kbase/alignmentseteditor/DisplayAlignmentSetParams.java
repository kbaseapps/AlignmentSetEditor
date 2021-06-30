
package us.kbase.alignmentseteditor;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: DisplayAlignmentSetParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "alignment_set_ref",
    "workspace_name"
})
public class DisplayAlignmentSetParams {

    @JsonProperty("alignment_set_ref")
    private String alignmentSetRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("alignment_set_ref")
    public String getAlignmentSetRef() {
        return alignmentSetRef;
    }

    @JsonProperty("alignment_set_ref")
    public void setAlignmentSetRef(String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
    }

    public DisplayAlignmentSetParams withAlignmentSetRef(String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public DisplayAlignmentSetParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("DisplayAlignmentSetParams"+" [alignmentSetRef=")+ alignmentSetRef)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
