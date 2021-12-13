"""
Functions for scoring team assignments on different metrics
"""
import numpy as np
from math import comb, perm
from helpers import (
    count_met_partner_prefs,
    count_mutual_partner_prefs,
    percent_strongly_skilled,
    exp_deficiency,
    intr_deficiency,
    skill_deficiency,
    sorted_topic_votes,
    violates_silver_bullets
)


def assignment_cost(teams):
    """
    Calculate the overall cost (badness) of a selection of teams.

    Returns a cost value where lower is better and higher is worse.
    """
    try:
        # Assume it's a list of subgraphs
        costs = [team_evaluation(list(clique.nodes))
                 for clique in teams]
    except:
        # Catch if it's a list of lists
        costs = [team_evaluation(team) for team in teams]
    return np.sqrt(sum(costs))


def team_evaluation(team):
    """
    Evaluate how good the algorithm has done on forming a specific team.

    Returns a cost value where lower is better and higher is worse.
    """
    try:
        # Assume it's a subgraph
        team = list(team.nodes)
    except:
        # Continue if it's a list
        pass
    # Determine if one student was a "filler student"
    filler_students = 0
    full_team_cohesion = count_met_partner_prefs(team)
    for i in range(len(team)):
        test_team = team[:i-1] + team[i+1:]
        test_team_cohesion = count_met_partner_prefs(test_team)
        # If the rest of the team is clique-ish
        if test_team_cohesion >= perm(len(test_team), 2) * .75:
            # But no additional preferences include test_student
            if full_team_cohesion == test_team_cohesion:
                # That student was probably a filler
                filler_students += 1

    # 0 (good) -> 1 (bad)
    odd_person_out = 1 if filler_students == 1 else 0

    # Find deficiencies in technical areas
    intr_defncy = intr_deficiency(team)
    exp_defncy = exp_deficiency(team)
    # Check if they are lacking a "good" (intr+exp > 8) PM
    max_pm = max([student.mgmt for student in team])
    # 0 (good) -> 1 (bad)
    pm_defncy = max(0, 8-max_pm) / 8

    # Return weighted cost
    # Lower (good) -> higher (bad)
    return np.sqrt(
        (4 * odd_person_out) ** 2 +
        (3 * pm_defncy) ** 2 +
        (2 * exp_defncy) ** 2 +
        (2 * intr_defncy) ** 2
    )


def team_compatibility(team):
    """
    Computes a score for 1 team.

    Returns a value where lower is worse and higher is better.
    If any 2 students have silver bullet between them, returns 0.
    """
    try:
        # Assume it's a subgraph
        team = list(team.nodes)
    except:
        # Continue if it's a list
        pass

    if violates_silver_bullets(team):
        return 0

    # Evaluate team on commitment, topic agreement, partner prefs,
    # skill deficiency & skill distribution
    # Variance is lower -> better
    commitment_variance = np.var([student.commitment for student in team])
    topic_votes = sorted_topic_votes(team)
    num_topics_considered = max(2, len(topic_votes))
    top_2_topic_votes = sum(topic_votes[:2])  # Higher -> better
    met_partner_prefs = count_met_partner_prefs(team)  # Higher -> better
    skill_defncy = skill_deficiency(team)  # 0 (good) -> 1 (bad)
    skill_distribution = percent_strongly_skilled(team)  # 0 (bad) -> 1 (good)

    # Normalize all values to be 0 (worst possible) -> 1 (best possible)
    scaled_commitment = (4 - commitment_variance) / 4
    scaled_topics = top_2_topic_votes / (len(team) * num_topics_considered)
    scaled_preference = met_partner_prefs / perm(len(team), 2)
    skill_sufficiency = 1 - skill_defncy

    # Return weighted score (yep, we're normalizing and then weighting them)
    return (
        3 * scaled_commitment +
        3 * skill_sufficiency +
        3 * skill_distribution +
        2 * scaled_topics +
        5 * scaled_preference
    )
