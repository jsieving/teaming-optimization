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


def assign_teams_random(four_cliques, five_cliques, n_4, n_5):
    """
    Randomly assign Students into teams of 4 or 5.

    Optionally provide pre-formed teams or partial teams, and these will be
    copied and filled up with 4 or 5 students each.
    May use as a baseline for scoring another algorithm.
    """
    # Copy and randomly shuffle cliques to be chosen from
    four_cliques = copy(four_cliques)
    five_cliques = copy(five_cliques)
    shuffle(four_cliques)
    shuffle(five_cliques)

    teams_of_5 = []
    start_at = 0
    while len(teams_of_5) < n_5:
        assigned_students = set()
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

    prev_assigned_students = set(assigned_students)

    teams_of_4 = []
    start_at = 0
    while len(teams_of_4) < n_4:
        assigned_students = prev_assigned_students
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

    return teams_of_4 + teams_of_5
