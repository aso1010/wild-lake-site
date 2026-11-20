package wildlake.clients

import rego.v1

default allow := false

allow if count(deny) == 0

base := "https://wildlakestudio.com/clients/#"
article_ids := {sprintf("%s%s", [base, id]) | some id in input.article_ids}
person_ids := {person["@id"] | some person in input.persons}
item_ids := {id | some id in input.item_ids}

deny contains sprintf("missing manifest field: %s", [field]) if {
 some field in ["article_ids", "persons", "item_ids", "script_origins", "inline_script_bytes", "stylesheet_urls", "organization"]
 not field in object.keys(input)
}
deny contains "roster must contain twelve unique article IDs" if {
 count(input.article_ids) != 12
}
deny contains "duplicate article ID" if {
 count(article_ids) != count(input.article_ids)
}
deny contains "roster and Person IDs differ" if article_ids != person_ids

deny contains "roster and ItemList IDs differ" if article_ids != item_ids

deny contains "duplicate Person node" if count(person_ids) != count(input.persons)

deny contains "duplicate ListItem reference" if count(item_ids) != count(input.item_ids)

deny contains sprintf("missing image: %s", [person["@id"]]) if {
 some person in input.persons
 not is_string(object.get(person, "image", null))
}
deny contains sprintf("missing identity link: %s", [person["@id"]]) if {
 some person in input.persons
 count(object.get(person, "sameAs", [])) == 0
}
deny contains "third-party script origin" if count(input.script_origins) != 0

deny contains "runtime script exceeds two KiB" if input.inline_script_bytes >= 2048

deny contains "clients page must load one compiled stylesheet" if input.stylesheet_urls != ["/assets/clients-monolith.css"]

deny contains "organization parent differs" if input.organization.parentOrganization["@id"] != "https://seveneightythree.com/#organization"

deny contains "founder does not resolve to canonical person" if input.organization.founder["@id"] != "https://argelysoriach.com/#person"

deny contains "founder canonical identity missing" if {
 some person in input.persons
 person["@id"] == "https://wildlakestudio.com/clients/#argelys-oriach"
 not "https://argelysoriach.com/#person" in person.sameAs
}
