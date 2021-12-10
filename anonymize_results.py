import csv
import os
from posixpath import basename
from typing import final


def show_columns(data):
    print("Here are the colums in your data:\n" + '-'*20)
    for i, cell in enumerate(data[0]):
        print(str(i)+':', cell)


def clean_name(name):
    name = name.lower().strip()
    for char in '.-–—\'‘’` ':
        name = name.replace(char, '')
    return name


filename = input("Enter file name:\n> ")
while not os.path.exists(filename):
    filename = input("File not found. Please try again:\n> ")

dirname, basename = os.path.split(filename)

with open(filename, 'r', newline='') as csvfile:
    data = []
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)
    print(f"{len(data)} rows loaded.")

header_rows = None
names_col = None
prefs_cols = None
anti_cols = None

header_input = input(
    "\nHow many rows of header data are there?\n(Default 1)> ")
while header_rows is None:
    if len(header_input) == 0:
        header_rows = 1
    else:
        try:
            header_rows = int(header_input)
        except:
            header_input = input("Please enter a single number.\n> ")

data_rows = data[header_rows:]

show_columns(data)

names_input = input(
    "\nWhich column number are student names stored in? We will take care of preferences and anti-preferences in a moment. You can type '?' any time to see the column names again.\n> ")
while names_col is None:
    if '?' in names_input:
        show_columns(data)
        names_input = ''
    else:
        try:
            names_col = int(names_input)
        except:
            names_input = input("Please enter a single number.\n> ")

prefs_input = input(
    "\n\nWhich column numbers are partner preferences stored in? We will take care of anti-preferences in a moment. Please enter numbers separated by commas. You can type '?' any time to see the column names again.\n> ")
while prefs_cols is None:
    if '?' in prefs_input:
        show_columns(data)
        prefs_input = ''
    else:
        try:
            if len(prefs_input) == 0:
                resp = input(
                    "You didn't specify any preference columns. Is this what you meant to do? (y/N)\n> ")
                if 'y' in resp.lower():
                    prefs_cols = []
                    break
            prefs_cols = [int(x.strip()) for x in prefs_input.split(',')]
        except:
            prefs_input = input(
                "Please enter numbers separated by commas.\n> ")

anti_input = input(
    "\n\nWhich column numbers are anti-preferences stored in? Please enter numbers separated by commas. You can type '?' any time to see the column names again.\n> ")
while anti_cols is None:
    if '?' in anti_input:
        show_columns(data)
        anti_input = ''
    else:
        try:
            anti_cols = [int(x.strip()) for x in anti_input.split(',')]
        except:
            anti_input = input(
                "Please enter numbers separated by commas.\n> ")

student_ids = {}
anti_pref_ids = {}

# Loop over names column and replace names with ids
# Add these ids to a dctionary
for i, row in enumerate(data_rows):
    student_name = clean_name(row[names_col])
    student_ids[student_name] = i
    row[names_col] = i

max_id = len(data_rows) - 1
# Loop over preferences and replace names with ids from student id dictionary
if len(prefs_cols) > 0:
    for row in data_rows:
        for col in prefs_cols:
            preference = clean_name(row[col])
            sid = student_ids.get(preference, None)
            # If preference was misspelled, just pretend it's a new student
            # We can randomly map these to listed students later
            if sid is None:
                max_id += 1
                sid = max_id
                student_ids[preference] = sid
            row[col] = sid

# New range of ids for anti-preferences
# IDs will increase in order that they first occur in the spreadsheet *as an
# anti-preference*, which is not correlated to the original id of the student
# that they identify
max_id = 500
# Loop over anti-preferences and replace names with ids from anti-preference id
# dictionary
for row in data_rows:
    for col in anti_cols:
        anti_pref = clean_name(row[col])
        sid = anti_pref_ids.get(anti_pref, None)
        if sid is None:
            # If this student wasn't in the dictionary before, add them
            # As with preferences, misspellings will be treated as unique
            max_id += 1
            sid = max_id
            anti_pref_ids[anti_pref] = sid
        row[col] = sid

# Save output
savename = os.path.join(dirname, "cleaned_" + basename)
with open(savename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

print("\n\nFile saved in", savename)
print("\nThank you for helping us get clean data! Make sure you have deleted any comment / open response columns, email address columns, and optionally the timestamps (we don't need those.) Enjoy this ASCII art to show our appreciation!")

input("> I don't want to look at some stupid art you copied from the internet")

print("""
__●__ ●
 _ █___█
 __ █__ █_
 __ █__ █
 __ ███____________█████
 _█▒░░█_________██▓▒▒▓██ ☆
 █▒░●░░█___ ██▓▒██▓▒▒▓█   ★
 █░█▒░░██_ ██▓▒██▓▒░▒▓█
 _██▒░░██ ██▓▒░██▓▒░▒▓█    ★
 ____█▒░██ ██▓▒░░ ████▓█
 ___█▒░██__██▓▓▒▒░░░██   ★★
 ____█▒░██___████████████
 _____█▒░█▒▒▒▒▒▒▒▒▒▒▒▒█
 ______██████████████████.•°*”~.•°*”~.

Too bad.""")
