# Teaming Optimization
Final project for Discrete Math, Fall 2021 @ Olin College.

By Jules Brettle [julesbrettle](https://github.com/julesbrettle), Annabelle Platt [@19platta](https://github.com/19platta), and Jane Sieving [@jsieving](https://github.com/jsieving).

## The Project
Our goal was to create an algorithm for making teams of students in a class. We wanted to make it easier to form teams that had favorable qualities for ensuring the team would work well together.

Check out our slides [here](https://docs.google.com/presentation/d/1Ll_B_DNxJBGYxleBAgIEOThlltGwhTpUEhWghReVWVc/) and our annotated bibliography [here](https://docs.google.com/document/d/1NoRDMd6QkGvROQCVAnyaOM9fmAdQCUUvdulM5awfBFY/).

## Usage
Requires `joblib` for opening and saving graph data files, `networkx` for representing students using a graph, and `pandas` for reading student survey data from CSV files.

Using this program requires the creation of graph and clique data based on student survey results. You may use the sample data in `/data`, or generate your own sample from the survey results. If you are doing the former, skip this paragraph. To generate a graph from a custom subset of the results, run `python data_loader.py` to generate a graph and list of all cliques from a subset of the anonymized student data. You will be prompted for a suffix: these are the suffixes of sections of student data from the anonymized survey results; your options are A, B and C. You will also be prompted for a number of students. The number of students in each section varies from 27 to 31, so if you want to simulate more than that, you should merge the rows of multiple sectioned files and save it following the same name pattern with a new suffix.

Run `python main.py` to run the assignment program on your subset of student survey data. You will be prompted for a suffix, consisting of the suffix used for creating a graph and cliques, and the number of students used in that graph. Case and spacing matter for this; it should exactly match the suffix of an existing graph file (and corresponding cliques) in `/data`. To use the sample object uploaded here, enter "A20", "A24", or "A28".

Currently, the program will run both a random assignment algorithm and an greedy one, and print the teams resulting from both, along with some metrics about the teams.

### On your own survey data

TBD: Make it more user friendly to use this algorithm on your own survey results.

## What's where

`assignments.py` - Algorithms that take in a list of students and produce a team assignment go here. \
`clique_finding.py` - The algorithm used to find k-cliques in a graph. \
`data_loader.py` - Imports data from survey results and converts it to Students. Also creates and saves graphs and cliques of students from that data. \
`helpers.py` - Miscellaneous methods that might be useful in multiple contexts, including some functions to evaluate certain metrics that are used for scoring. \
`main.py` - Loads graph and clique data that was previously generated from a sample of students and runs assignment algorithms using that data. \
`scoring.py` - Functions for scoring team assignments on different metrics go here. \
`student.py` - The Student class. \
`test.py` - Code to test helper functions. Currently just tests `overlaps`, but additional tests should go here.
