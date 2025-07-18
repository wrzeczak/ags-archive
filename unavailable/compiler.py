#--------------------------------------------------------------------------
# ROTBILLCOMPILER -- compiles the .entry files in /bills/ that the
#                    spitter outputs into a single webpage
#--------------------------------------------------------------------------

from os import listdir
from os.path import isfile, join
from datetime import datetime
from pytz import timezone
import subprocess

bill_dir = "unavailable-bills/"
output_path = "unavailable-bills.html"

# NOTE: In order for the entries to be sorted chronologically, they must be input chronologically
# i.e. you must add them as you go along
entries = [j for j in listdir(bill_dir) if isfile(join(bill_dir, j)) and j.endswith(".entry")] # get a list of filenames in the bill_dir which are files and end with ".entry"
entries = [int(j[:-6]) for j in entries] # entries are named 123456.entry, so this chops off the last 6 chars ('.entry') and turns the name into a number ('1234' -> 1234)
entries = sorted(entries) # sort ascending so that we can sort by creation date
entries = [f"{j}.entry" for j in entries] # turn 123456 into "123456.entry" for every entry number

with open(output_path, "w", errors="ignore", encoding="utf8") as o: # open the output file "unavailable-bills.html"
    with open(join(bill_dir, "header"), "r", errors="ignore", encoding="utf8") as header: # open the header, which contains the basic structure of the html file
        for h in header.readlines(): print(h, end="", file=o) # print the header to the output file
    
    print("C: Printed header...")
    
    print("<!--------------------------------------------------------------------------------->", file=o) # print this to the output file, helps keep things tidy

    for path in entries: # loop over every entry file
        with open(join(bill_dir, path), "r", errors="ignore", encoding="utf8") as f: # open each entry file
            for l in f.readlines(): print(l, end="", file=o) # read the lines of each entry file (which are already formatted html) and print them into the main output file
            print(f"C: Printed {f.name}...")

    print("<!--------------------------------------------------------------------------------->", file=o)

    t = datetime.now(timezone("US/Central")) # get the current time in the central time zone (i am nothing if not Texan) - this server is located in dallas, last I checked

    # the footer is not a file because i have it update with the time!
    print(f'<footer style="color: #ddd;">\n\tLast updated {t.strftime("%m/%d/%y")} at {t.strftime("%H:%M %Z")}.\n This file is (<a href="https://wrzeczak.net/stolow/spitter.py">semi-</a>) <a href="https://wrzeczak.net/stolow/compiler.py">autogenerated</a>, please see the #sim-history channel for a GitHub link to the source, and notify @wrzeczak of any errors on the page. Thanks!</footer>', file=o) # print the footer, similarly to the header

    print("C: Printed footer...")

print(f"C: Making backup of {bill_dir}...")

subprocess.call(["cp", "-r", bill_dir, f"backup-{bill_dir}"])
subprocess.call(["diff", bill_dir, f"backup-{bill_dir}"])

print("C: Done! :)")