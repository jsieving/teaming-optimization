'''
Functions for scoring team assignments on different metrics
'''
import math

def sample_score_func(teams):
    squared_errors_sum = 0
    for team in teams:
        min_commitment = min([student.commitment for student in team])
        max_commitment = max([student.commitment for student in team])
        squared_errors_sum += (max_commitment - min_commitment) ** 2
    return math.sqrt(squared_errors_sum)
