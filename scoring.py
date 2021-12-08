'''
Functions for scoring team assignments on different metrics
'''
import numpy as np
from math import comb, perm
from helpers import (
    count_met_partner_prefs,
    count_mutual_partner_prefs,
    percent_strongly_skilled,
    skill_deficiency,
    sorted_topic_votes,
    violates_silver_bullets
)

def sample_score_func(teams):
    squared_errors_sum = 0
    for team in teams:
        min_commitment = min([student.commitment for student in team])
        max_commitment = max([student.commitment for student in team])
        squared_errors_sum += (max_commitment - min_commitment) ** 2
    return np.sqrt(squared_errors_sum)


def team_compatibility(team):
    '''
    Computes a score for 1 team.
    If any 2 students have silver bullet between them, returns 0.
    '''
    if violates_silver_bullets(team):
        return 0

    # Evaluate team on commitment, topic agreement, partner prefs,
    # skill deficiency & skill distribution
    commitment_variance = np.var([student.commitment for student in team])
    topic_votes = sorted_topic_votes(team)
    num_topics_considered = max(2, len(topic_votes))
    top_2_topic_votes = sum(topic_votes[:2])
    met_partner_prefs = count_met_partner_prefs(team)
    skill_defncy = skill_deficiency(team)
    skill_distribution = percent_strongly_skilled(team)

    # Normalize all values to be 0 (worst possible) -> 1 (best possible)
    scaled_commitment = (4 - commitment_variance) / 4
    scaled_topics = top_2_topic_votes / (len(team) * num_topics_considered)
    scaled_preference = met_partner_prefs / perm(len(team), 2)
    scaled_skill_defncy = 1 - skill_defncy

    # Return weighted score (yep, we're normalizing and then weighting them)
    return (
        4 * scaled_commitment +
        3 * scaled_skill_defncy + 
        3 * skill_distribution +
        2 * scaled_topics +
        scaled_preference
    )


def compatibility(student1, student2):
    '''
    Computes a compatibility score between 2 students.
    If students have silver bullet between them, returns -infinity.
    '''
    if (student1.name in student2.silver_bullets or
        student2.name in student1.silver_bullets):
        return -float("inf")

    commitment_spread = abs(student1.commitment - student2.commitment)
    common_topics = len(student1.interests & student2.interests)
    mutual_preference = (
        (student1.name in student2.preferences) +
        (student2.name in student1.preferences)
    )
    skill_coverage = np.sqrt(
        max(student1.mgmt, student2.mgmt)**2
        + max(student1.elec, student2.elec)**2
        + max(student1.prog, student2.prog)**2
        + max(student1.cad,  student2.cad)**2
        + max(student1.fab,  student2.fab)**2
    )

    scaled_commitment = (4-commitment_spread) / 4
    scaled_topics = min(2, common_topics) / 2
    scaled_preference = mutual_preference / 2
    scaled_skill = skill_coverage / 16

    return (
        4 * scaled_commitment +
        3 * scaled_preference +
        2 * scaled_topics +
        scaled_skill
    )