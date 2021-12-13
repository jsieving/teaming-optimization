"""
Functions which produce complete team assignments
"""
import numpy as np
from random import shuffle
from copy import copy, deepcopy
from helpers import count_students, num_size_teams, overlaps, sorted_teams
from scoring import assignment_cost, team_compatibility, team_evaluation


def assign_teams_greedy(four_cliques, five_cliques, n_4, n_5):
    teams_of_4 = []
    start_at = 0
    while len(teams_of_4) < n_4:
        assigned_students = set()
        teams_of_4 = []
        team_idx = start_at
        while team_idx < len(four_cliques):
            curr_team = four_cliques[team_idx]
            # Check overlap of students on top teams
            if not overlaps(curr_team.nodes, assigned_students):
                teams_of_4.append(curr_team)
                assigned_students |= curr_team.nodes
                if len(teams_of_4) == n_4:
                    break
            team_idx += 1
        start_at += 1

    if not five_cliques:
        return assignment_cost(teams_of_4), teams_of_4

    prev_assigned_students = set(assigned_students)

    teams_of_5 = []
    start_at = 0
    while len(teams_of_5) < n_5:
        assigned_students = prev_assigned_students
        teams_of_5 = []
        team_idx = start_at
        while team_idx < len(five_cliques):
            curr_team = five_cliques[team_idx]
            # Check overlap of students on top teams
            if not overlaps(curr_team.nodes, assigned_students):
                teams_of_5.append(curr_team)
                assigned_students |= curr_team.nodes
                if len(teams_of_5) == n_5:
                    break
            team_idx += 1
        start_at += 1

    return teams_of_4 + teams_of_5


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
