from assignments import random_assignments
from data_loader import load_student_data
from helpers import num_size_teams
from clique_finding import find_k_clique
from scoring import (
    compatibility,
    sample_score_func,
    team_compatibility,
    team_evaluation
)


filename = input("Enter file name with survey data [team_sample_data.csv]: ") or "team_sample_data.csv"

students = load_student_data(filename)
print("First student: ", students[0])

print("Students loaded: ", len(students))

leftovers, teams = random_assignments(students)

print(teams)
print("Score (higher is worse): %.2f" % sample_score_func(teams))
print("%d students could not be assigned to teams." % len(leftovers))
print(compatibility(*teams[0][:2]))
print(compatibility(*students[:2]))
for team in teams:
    print(team_compatibility(team))
    print(team_evaluation(team))


# Parse data from survey to create Student objects
filename = input("Enter file name with survey data [team_sample_data.csv]: ") or "team_sample_data.csv"
students = load_student_data(filename)
num_students = len(students)

# Create a graph connecting non-silver-bulleted Student objects as vertices with edge weights representing compatibility

# Figure out how many groups of 4 and 5 to create 
num_5teams, num_4teams = num_size_teams(num_students)

# Compute all 4-cliques and take the top n (computed in previous step) non-overlapping groups of size 4
find_k_clique(graph, num_4teams)

# Eliminate all people assigned in the 5-clique from possible candidates 

# Compute all 5-cliques and take top m non-overlapping groups of 
