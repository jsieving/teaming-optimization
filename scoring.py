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
    mutual_preference = ((student1.name in student2.preferences) +
    (student2.name in student1.preferences))
    skill_coverage = math.sqrt(
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

    return (4*scaled_commitment + 3*scaled_preference +
        2*scaled_topics + scaled_skill)