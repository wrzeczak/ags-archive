#------------------------------------------------------------------------------
# PDF PATCHER - A program to manually append the data created by the dater to
# fix any errors in its parsing
#
# OUTPUT CSV FORMAT: Filename,Date -> str, str
#
# wrzeczak, 16 July 2025, for AmericanGovSim <3
#------------------------------------------------------------------------------

import pandas as pd
from datetime import datetime

INPUT_LIST = "bad_bills.txt"
OUTPUT_CSV = "dates.csv"

#------------------------------------------------------------------------------

df = pd.read_csv(OUTPUT_CSV)

with open(INPUT_LIST, "r") as l:
	files = l.readlines()

	for f in files:
		date = input(f"File {f: <50}\nDate Format: 01 Month 9999 i.e. 03 May 2021 > ")
		
		dt = datetime.timestamp(datetime.strptime(date, "%d %B %Y"))
		print(dt)

		df.loc[len(df)] = { 'Filename': f, 'Date': dt}

df.to_csv(OUTPUT_CSV)