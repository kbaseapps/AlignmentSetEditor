
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
 * <p>Original spec-file type: EditAlignmentSetResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "report_name",
    "report_ref",
    "alignment_set_ref"
})
public class EditAlignmentSetResult {

    @JsonProperty("report_name")
    private String reportName;
    @JsonProperty("report_ref")
    private String reportRef;
    @JsonProperty("alignment_set_ref")
    private String alignmentSetRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("report_name")
    public String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(String reportName) {
        this.reportName = reportName;
    }

    public EditAlignmentSetResult withReportName(String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(String reportRef) {
        this.reportRef = reportRef;
    }

    public EditAlignmentSetResult withReportRef(String reportRef) {
        this.reportRef = reportRef;
        return this;
    }

    @JsonProperty("alignment_set_ref")
    public String getAlignmentSetRef() {
        return alignmentSetRef;
    }

    @JsonProperty("alignment_set_ref")
    public void setAlignmentSetRef(String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
    }

    public EditAlignmentSetResult withAlignmentSetRef(String alignmentSetRef) {
        this.alignmentSetRef = alignmentSetRef;
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
        return ((((((((("EditAlignmentSetResult"+" [reportName=")+ reportName)+", reportRef=")+ reportRef)+", alignmentSetRef=")+ alignmentSetRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
