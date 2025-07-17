#------------------------------------------------------------------------------
# PDF PAGER - A program to sort through the data output by the pdf_dater sc-
# -ript and format it into an HTML file for display.  
#
# OUTPUT CSV FORMAT: Filename,Date -> str, str
# ERROR OUTPUT: a list of filenames with bills whose dates could not be read
#
# wrzeczak, 16 July 2025, for AmericanGovSim <3
#------------------------------------------------------------------------------

import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

INPUT_CSV = "dates.csv"
INPUT_ERRORS = "bad_bills.txt"
CSS_PATH = "styles.css"
OUTPUT_PATH = "catalog.html"

df = pd.read_csv(INPUT_CSV)

filenames = df["Filename"].to_list()
dates = [datetime.fromtimestamp(float(d)) for d in df["Date"].to_list()]

input_dict = {}

for f, d in zip(filenames, dates):
	input_dict[f] = d

_filenames = []
_dates = list(set([d for d in dates]))
_dates.sort()


# sort filenames so they appear in chronological and then alphabetical order
for d in _dates:
	bills_dated = [k for k, v in input_dict.items() if v == d]
	bills_dated.sort()
	print(f'{d.strftime("%d %B %Y"): <30}: {bills_dated}')
	_filenames.extend(bills_dated)

#------------------------------------------------------------------------------

HTML_HEADER = f"""<!DOCTYPE html>

<head>
    <link rel="stylesheet" href="{CSS_PATH}">
    <title>AGS Bill Catalog - stolow.net</title>
    <meta content="AGS Bill Catalog - stolow.net" property="og:title"/>
    <meta content="A registry of legislation signed by AGS Presidents, compiled by O. Stolow (wrzeczak). See 'Bill Archives' at https://wrzeczak.net/stolow/index.html, under 'File Archive' for more information. Check the #sim-history channel for updates on progress of this website and this project." property="og:description"/>
    <meta content="#002a6e" data-react-helmet="true" name="theme-color" />
</head>

<body>
<a href="https://wrzeczak.net/stolow/index.html" style="color: #ddd;"><h2>Bill Catalog</h2></a>
<p>A registry of <i>legislation signed by AGS Presidents</i> (i.e. bills, EOs, etc.), compiled by O. Stolow (wrzeczak). See "Bill Archives" at <a href="https://wrzeczak.net/stolow/index.html">wrzeczak.net/stolow/index.html</a>, under "File Archive" for more information. Check the #sim-history channel for updates on progress of this website and this project.</p>
<p>
    <b>FORMAT:</b> <b>Filename</b>, <b>Date</b> listed on the bill (not necessarily signage date). Bills are sorted chronologically, then alphabetically.<br/>
    </p>
<p><b>DATA:</b> <a href="https://wrzeczak.net/stolow/bill-catalog/{INPUT_CSV}">Click here</a> for the data I compiled and used to generate this page (bill archives can be found at the above mentioned link). A similar list is maintained on the <a href="https://docs.google.com/spreadsheets/d/1VzpV6fFQdxr1nBN1rcmo3_7IMqGWMesNOAEbzPs6GW0/edit?gid=919050650#gid=919050650" target="_blank">Federal Master Spreadsheet</a>.</p>
<hr><br/>
<table>
"""

HTML_FOOTER = f"""</table>
</body>
<br/><br/>

<footer>
Last updated {datetime.now(tz=ZoneInfo('America/Chicago')).strftime("%m/%d/%Y at %I:%m %p CDT")}. This file is auto-generated, please see the #sim-history channel for information on source code (GitHub repository), and please ping @wrzeczak there if you find any errors.  
</footer>
"""

with open(OUTPUT_PATH, "w") as f:
	f.write(HTML_HEADER)

	for n, t in zip(_filenames, _dates):
		# get the filename
		n = n.split("\\")[-1] # remove any folder names
		d = t.strftime("%d %B %Y")
		print(f'\t<tr>\n\t\t<td id="filename">{n}</td>\n\t\t<td id="date">{d}</td>\n\t</tr>', file=f)

	f.write(HTML_FOOTER)
