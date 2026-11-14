package moai.sentinel.layout
import rego.v1

deny contains msg if {
    node := input.html.nodes[_]
    node.tag == "hr"
    not valid_rule_class(object.get(node.attributes, "class", ""))
    msg := sprintf("STRUCTURAL VIOLATION: Unscoped <hr> detected at line %d. Assign .rule-datum, .rule-measure, or .rule-inline.", [node.line])
}
valid_rule_class(class_attr) if {
    allowed := {"rule-datum", "rule-measure", "rule-inline"}
    classes := split(class_attr, " ")
    some class in classes
    class in allowed
}
