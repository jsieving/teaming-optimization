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


def assign_teams_rec(four_cliques, five_cliques, i, chosen_cliques, assigned_students, num_students, n):
    num_students_left = num_students - len(assigned_students)
    # If you can divide remaining students by 4, but not 5,
    if (num_students_left % 4 == 0) and (num_students_left % 5 != 0):
        # Start picking from 4-cliques
        cliques = four_cliques
        # And make it impossible to go back to 5-cliques
        five_cliques = four_cliques
    else:
        cliques = five_cliques

    # Base case: no more cliques to choose from
    if i >= len(cliques):
        return 10000, None
    # Base case: no more cliques required -> return cost & choices
    if n == 0:
        print(0, chosen_cliques)
        return assignment_cost(chosen_cliques), chosen_cliques[:]

    # Additional base case: choose the next best clique of unassigned students
    if n == 1:
        if num_students-len(assigned_students) < 4:
            # Can't create any more teams, so just score what you have
            return assignment_cost(chosen_cliques), chosen_cliques[:]

        j = i
        # Find the first team of unassigned students, since they are sorted
        # by score
        while j < 1000 and overlaps(cliques[j].nodes, assigned_students):
            j += 1
        if j >= len(cliques):
            # There are no cliques with the remaining students without silver
            # bullets
            return 10000, None

        new_cliques = chosen_cliques + [cliques[j]]
        # Calculate the overall score
        cost = assignment_cost(new_cliques)
        return cost, new_cliques

    # Recursive case:
    # Get current clique
    curr_clique = cliques[i]
    # Set costs for including or excluding very high by default
    cost_incl, cost_excl = 10000, 10000
    # Set both team options to None
    teams_incl, teams_excl = None, None
    # If ith clique does not overlap:
    if not overlaps(curr_clique.nodes, assigned_students):
        #   Get cost & choices for including ith clique
        new_cliques = chosen_cliques + [curr_clique]
        new_assigned_students = assigned_students | curr_clique.nodes
        cost_incl, teams_incl = assign_teams_rec(
            four_cliques, five_cliques, i+1, new_cliques, new_assigned_students, num_students, n-1)

    if not teams_incl or team_compatibility(teams_incl[-1]) < 8:
        # Get cost & choices for excluding ith clique
        cost_excl, teams_excl = assign_teams_rec(
            four_cliques, five_cliques, i+1, chosen_cliques, assigned_students, num_students, n)

    if cost_excl > cost_incl:
        cost, teams = cost_incl, teams_incl
    else:
        cost, teams = cost_excl, teams_excl
    return cost, teams
