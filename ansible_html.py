#!/usr/bin/env python3

import sys

class AnsibleColorize:
    """A class for colorizing the output of an Ansible command"""

    def __init__(self, ansible_output):
        """Initialize the AnsibleColorize class with the output of an Ansible command"""
        self.ansible_output = ansible_output

    def colorize(self):
        """Colorize the output of an Ansible command."""
        self.flag_task = False # first task doesnt get tag closures

        colored_output = ''
        for line in self.ansible_output.split("\n"):
            if line.startswith("TASK "):
                if not self.flag_task:
                    self.flag_task = True # first instance doesnt start with a div closure
                    colored_output += '<button type="button" class="collapsible">' + line + '</button><div class="content">\n'
                else:
                    colored_output += '</div><button type="button" class="collapsible">' + line + '</button><div class="content">\n'
            elif line.startswith("ok: "):
                colored_output += '<p class="ok">' + line + '</p>\n'
            elif line.startswith("skipping: "):
                colored_output += '<p class="skip">' + line + '</p>\n'
            elif line.startswith("changed: "):
                colored_output += '<p class="chng">' + line + '</p>\n'
            elif line.startswith("failed: "):
                colored_output += '<p class="fail">' + line + '</p>\n'
            elif line.startswith("fatal: "):
                colored_output += '<p class="fail">' + line + '</p>\n'
            elif " unreachable=1 " in line:
                colored_output += '<p class="unre">' + line + '</p>\n'
            elif line.startswith("PLAY RECAP"):
                colored_output += '</div><button type="button" class="collapsible">' + line + '</button><div class="content">\n'
            else:
                colored_output += '<p class="other">' + line + '</p>\n'
        colored_output += "</div>"
        return colored_output

    def create_html(self):
        """Colorize the output of an Ansible command and wrap it in html with CSS and javascript"""
        html = "<!DOCTYPE HTML>"
        html += "<html><head><title>Ansible Output</title>"
        html += """<style>
body {
  background-color: black;
  color: lightgray;
}
.ok {
  color: green;
}
.skip {
  color: steelblue;
}
.chng {
  color: gold;
}
.fail {
  color: red;
}
.unre {
  color: orange;
}
.other {
  color: lightgray;
}
p {
  margin: 0;
}
button {
  background-color: #111;
  color: #f7f7f7;
}
/* Style the button that is used to open and close the collapsible content */
.collapsible {
  background-color: #111;
  color: #eee;
  cursor: pointer;
  padding: 3px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 14px;
}

/* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
.active, .collapsible:hover {
  background-color: #111;
  color: #f7f7f7;
}

/* Style the collapsible content. Note: hidden by default */
.content {
  padding: 0 2px;
  display: none;
  overflow: hidden;
  background-color: #111;
}
</style></head><body>
"""
        html += "</style></head><body>"

        html += self.colorize()

        html += "<script>"
        html += """
var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
  var content = coll[i].nextElementSibling;
  var paragraphs = content.getElementsByTagName('p');
  var fatal = false;
  for (var j = 0; j < paragraphs.length; j++) {
    if (paragraphs[j].innerText.startsWith('fatal: ')) {
      fatal = true;
      break;
    }
    if (paragraphs[j].innerText.startsWith('PLAY RECAP')) {
      fatal = true;
      break;
    }
  }
  if (fatal) {
    content.style.display = "block";  // set the default state to expanded
  } else {
    content.style.display = "none";  // set the default state to collapsed
  }

  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
"""
        html += "</script></body></html>"
        return html

def main():
    ansible_output = sys.stdin.read()

    obj = AnsibleColorize(ansible_output)
    print(obj.create_html())

if __name__ == "__main__":
    main()
