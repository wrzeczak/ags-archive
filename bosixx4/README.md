# AGS PDF Parser

This is a collection of scripts that will automatically parse the dates of bills and format them into a webpage.

First, run the `pdf_dater.py` script. This will automatically search for something of the format "Month Day Year" and output a .csv file with filenames and their respective timestamps. Then, run the `pdf_patcher.py` script; this will allow you to manually add dates to any that the dater couldn't parse. Then, run the `pdf_pager.py` script, which will take the .csv file produced by the dater and patcher together and create a webpage.