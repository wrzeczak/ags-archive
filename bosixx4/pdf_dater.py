#------------------------------------------------------------------------------
# PDF DATER - A program to search through AGS' PDF bills and figure out their
# date information. By convention, bills have a date of submission printed on
# them, and this program outputs a CSV file with each bill's filename and the
# date found printed on it.
#
# OUTPUT CSV FORMAT: Filename,Date -> str, str
# ERROR OUTPUT: a list of filenames with bills whose dates could not be read
#
# wrzeczak, 16 July 2025, for AmericanGovSim <3
#------------------------------------------------------------------------------

import fitz
from os import listdir
from os.path import join
import pandas as pd
from time import mktime
import datetime
# from datetime.datetime import strptime

BILL_FOLDER = "billarchive-april2indy"
OUTPUT_CSV = "dates.csv"
ERROR_OUTPUT = "bad_bills.txt"

# correct me if i'm wrong...
MONTH_NAMES = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

output_dictionary = {}
bad_files = []

#------------------------------------------------------------------------------
# read dates from pdfs

for doc in listdir(BILL_FOLDER):
	if(doc.endswith(".pdf")):
		print(f"Opening {doc + '...': <100} ", end="")

		date_text = ""
		pages = fitz.open(join(BILL_FOLDER, doc))

		# the date is by convention printed on the first page
		text = pages[0].get_text().split()

		date_bits = []

		month_index = -1
		for i, bit in enumerate(text):
			if bit.lower() in MONTH_NAMES:
				month_index = i
				break

		# copy the text over
		date_bits.extend(text[month_index:month_index + 3])

		# exclude clauses like "may be named"
		try:
			if not(list(date_bits[1])[0] in "123456789"):
				date_bits = []
		except IndexError: 
			# in case month_index == -1, then date_bits stays empty
			date_bits = []

		print(date_bits, end="   ")

		# put the data away for outputting
		if not (date_bits == []):
			if date_bits[1][-3:].strip() in ["th,", "st,", "nd,"]:
				date_bits[1] = date_bits[1][:-3]

			print(date_bits)
			date = " ".join(date_bits).strip().replace(chr(int("0x200b", 16)), "")
			# store dates as timecodes rather than strings
			try:
				t = datetime.datetime.strptime(date, "%B %d %Y")
			except ValueError:
				t = datetime.datetime.strptime(date, "%B %d, %Y")

			output_dictionary[join(BILL_FOLDER, doc)] = datetime.datetime.timestamp(t)
		else:
			bad_files.append(join(BILL_FOLDER, doc))
			print()

#------------------------------------------------------------------------------
# output data and errors

df = pd.DataFrame({"Filename": output_dictionary.keys(), "Date": output_dictionary.values()})
df.to_csv(OUTPUT_CSV, encoding="utf-8", index=False)

with open(ERROR_OUTPUT, "w") as e:
	e.write("\n".join(bad_files))

print(f"\n\tOutput {len(output_dictionary.keys())} file-date pair(s) to {OUTPUT_CSV}, and failed to parse {len(bad_files)} file-date pair(s) (see {ERROR_OUTPUT}).\n")