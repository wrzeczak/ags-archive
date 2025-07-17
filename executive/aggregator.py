#------------------------------------------------------------------------------
# AGGREGATOR - create CSV file for legislation to sort information
#
# CSV FILE FORMAT that this application uses:
# Number,Date,President,Title,Summary,Repealed
# int, str, str, str, str, bool or str
# "Repealed" will be false when the EO has *not* been repealed, and a string 
#  if it has been, containing some info on its repealment
#------------------------------------------------------------------------------

import pandas as pd
from questionary import prompt

#------------------------------------------------------------------------------

CSV_PATH = "./executive-orders/eos.csv" # todo: argparse this

df = pd.read_csv(CSV_PATH)

#------------------------------------------------------------------------------

def validate_nonempty(text):
    if len(text) == 0: return "This field is required!"
    return True

def validate_number(text):
    try:
        int(text)
    except:
        return "Input a number!"
    return True

# date format: Month DD YYYY
def validate_date(text):
    error_message = "Date format incorrect! Month DD YYYY i.e. April 20 2025"

    casts = [str, int, int]
    chunks = text.split()

    # an empty enter will return False
    if type(chunks) is bool: return error_message

    # make sure there are three chunks
    if len(chunks) != 3: return error_message

    # and that each chunk has a piece of data
    for c in chunks:
        if len(c) == 0: return error_message

    # and that that data is of the correct type
    try:
        for t, c in zip(casts, chunks):
            t(c)
    except:
        return error_message
    
    return validate_nonempty(text)

repeal_default = "Not yet verified."
summary_default = "No summary yet written."
doclink_default = "Unavailable."
msglink_default = "Unavailable."

#------------------------------------------------------------------------------

questions = [
    {
        "type": "text",
        "name": "Number",
        "message": "E.O. Number?",
        "validate": validate_number
    },
    {
        "type": "text",
        "name": "Date",
        "message": "Signage Date?",
        "validate": validate_date
    },
    {
        "type": "text",
        "name": "President",
        "message": "President Issued By?",
        "validate": validate_nonempty
    },
    {
        "type": "text",
        "name": "Title",
        "message": "E.O. Title?",
        "validate": validate_nonempty
    },
    {
        "type": "text",
        "name": "Summary",
        "message": "Summary of E.O:",
        "default": summary_default
    },
    {
        "type": "confirm",
        "name": "Repealed",
        "message": "Has this E.O. been repealed?",
        "default": repeal_default
    },
    {   #! this question intentionally overwrites the result of the previous question 
        "type": "text",
        "name": "Repealed",
        "message": "Repeal Information:",
        "when": lambda x: x["Repealed"] == True
    },
    {
        "type": "text",
        "name": "DocumentLink",
        "message": "Google Docs link:",
        # "default": doclink_default
    },
    {
        "type": "text",
        "name": "SignageLink",
        "message": "Signage message link:",
        # "default": msglink_default
    }
]

result = prompt(questions)

#------------------------------------------------------------------------------

# result["Number"] = int(result["Number"]) # prompt() returns it as a string
if result["Repealed"] is False: result["Repealed"] = "Still in force."

for k in result:
    result[k] = [result[k]] # pandas wants all these things to be vectors

new_df = pd.concat([df, pd.DataFrame(result)], ignore_index=True)

# print(result)
# print(new_df)

new_df.to_csv(CSV_PATH, mode="w", header=True, index=False)