"""
Functions which take in a list of students and produce a team assignment
"""
from random import shuffle
from copy import copy, deepcopy
from helpers import count_students, num_size_teams, sorted_teams

def random_assignments(students, prior_teams=None):
    """
    Randomly assign Students into teams of 4 or 5.

    Optionally provide pre-formed teams or partial teams, and these will be
    copied and filled up with 4 or 5 students each.
    May use as a baseline for scoring another algorithm.
    """
    # Count total students and return unchanged input if not enough for a team
    teams = deepcopy(prior_teams) or []
    total_students = len(students) + count_students(teams)
    if total_students < 4:
        return students, prior_teams

    # Copy and randomly shuffle students to be assigned
    students = copy(students)
    shuffle(students)

    # Figure out how many teams should have 5 students
    teams_of_5, teams_of_4 = num_size_teams(total_students)
    
    # Create any empty teams necessary
    while len(teams) < teams_of_5 + teams_of_4:
        teams.append([])

    # Fill each team up to the number of students that minimizes teams
    for i, team in enumerate(teams):
        team_size = 5 if i < teams_of_5 else 4
        while len(team) < team_size:
            team.append(students.pop())
    
    return students, sorted_teams(teams)
