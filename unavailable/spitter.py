#--------------------------------------------------------------------------
# ROTBILLSPITTER -- turns rotted bills into entires on the stolow
#                   website, for my own archival ease-of-use
#--------------------------------------------------------------------------

import markdown
from time import time

actions_dict = {}

actions_dict["UK"] = "Locate copy or declaration of unenforceability."
actions_dict["NR"] = "None, law was repealed."
actions_dict["ND"] = "None, law was declared unenforceable."

print("#-- ROT BILL SPITTER -------------------------------\n")

link = input("Link (copy+paste)?: ")
title = input("Title (copy+paste)?: ")
date_signed = input("Date signed (Month Day Year)?: ")
embed_info = input("Embedded info (copy+paste)?: ")
action_status_input = input("[Enter] UK - Text lost & enforc. unknown [1] NR - Bill repealed [2] ND - Bill declared unenf. [3] TBD [4] - Other\nAction status?: ")

action_status = ""
if action_status_input == '':
    action_status = actions_dict["UK"]
elif int(action_status_input) == 1:
    action_status = actions_dict["NR"]
elif int(action_status_input) == 2:
    action_status = actions_dict["ND"]
elif int(action_status_input) == 3:
    action_status = "TBD."
else:
    action_status = input("Enter custom action status message: ")

if not action_status == "TBD.":
    extra_info = markdown.markdown(input("Extra information [Markdown formatted]?: "))
    extra_info = extra_info[3:-4] # chop off the surrounding <p> tags that markdown.markdown generates
else:
    extra_info = "TBD."

with open(f"./bills/{int(time())}.entry", "w", errors="ignore", encoding="utf8") as f:
    print(f'\n<p><a href="{link}" target="_blank">{title}</a>, signed {date_signed} &mdash;&nbsp; "{embed_info}"\n\t<br/><b>ACTION NEEDED &mdash;</b> <u>{action_status}</u> {extra_info}</p>\n', file=f)
    print(f"\nOutput to {f.name}!\n")

print("#---------------------------------------------------\n")
