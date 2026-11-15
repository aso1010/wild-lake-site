package moai.engagements
import rego.v1

default allow := false
allow if {
 count(input.pages) == 2
 input.faq_script_bytes < 1024
 faq := input.pages[0]
 faq.route == "/faq"
 faq.canonical == "https://wildlakestudio.com/faq"
 faq.question_count == 14
 terms := input.pages[1]
 terms.route == "/terms"
 terms.canonical == "https://wildlakestudio.com/terms"
 terms.section_count == 9
 every page in input.pages {
  page.unique_ids == true
  count(page.remote_origins) == 0
 }
}
