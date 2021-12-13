import joblib
import time
from networkx.classes import graph
from assignments import (
    assign_teams_greedy, assign_teams_random, assign_teams_rec)
from helpers import num_size_teams
from clique_finding import find_k_clique
from scoring import (
    assignment_cost, team_compatibility, team_evaluation)


# Try to load a graph of students
student_graph_suffix = input(
    "Enter suffix for student graph filename: student_graph_")
student_graph_filename = "data/student_graph_" + student_graph_suffix
try:
    student_graph = joblib.load(student_graph_filename)
except FileNotFoundError:
    print("File '%s' not found. Please run data_loader.py to generate student graphs." %
          student_graph_filename)
    exit()

# Load or create all 4-cliques
four_cliques_filename = "data/four_cliques_" + student_graph_suffix
try:
    four_cliques = joblib.load(four_cliques_filename)
    print("%i 4-cliques loaded" % len(four_cliques))
except FileNotFoundError:
    print(four_cliques_filename, "not found. Generating 4-cliques...")
    # Compute all possible 4-cliques
    four_cliques = find_k_clique(student_graph, 4)
    print("%i 4-cliques found." % len(four_cliques))

    # Do not save any cliques containing silver bullets
    # They shouldn't make it this far, but checking can save a lot of time
    four_cliques = [
        team for team in four_cliques if team.graph['compat'] > 0]
    print("%i nonzero 4-cliques found." % len(four_cliques))

    joblib.dump(four_cliques, four_cliques_filename)
    print("4-cliques saved in", four_cliques_filename)

# Load or create all 5-cliques
five_cliques_filename = "data/five_cliques_" + student_graph_suffix
try:
    five_cliques = joblib.load(five_cliques_filename)
    print("%i 5-cliques loaded" % len(five_cliques))
except FileNotFoundError:
    print(five_cliques_filename, "not found. Generating 5-cliques...")
    # Compute all possible 5-cliques
    five_cliques = find_k_clique(student_graph, 5)
    print("%i 5-cliques found." % len(five_cliques))

    # Do not save any cliques containing silver bullets
    # They shouldn't make it this far, but checking can save a lot of time
    five_cliques = [
        team for team in five_cliques if team.graph['compat'] > 0]
    print("%i nonzero 5-cliques found." % len(five_cliques))

    joblib.dump(five_cliques, five_cliques_filename)
    print("5-cliques saved in", five_cliques_filename)

rescore = input("Would you like to re-score the cliques? [N/y]: ")
if 'y' in rescore.lower():
    # Find team compatability of each 4-clique
    for team in four_cliques:
        # Compute team compatibility and store as a property of the graph
        team.graph['compat'] = team_compatibility(team.nodes)

    # Find team compatability of each 5-clique
    for team in five_cliques:
        # Compute team compatibility and store as a property of the graph
        team.graph['compat'] = team_compatibility(team.nodes)

    # sort the cliques by highest compatibility scores
    four_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)
    five_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)

print("All cliques loaded and scored.")

# Figure out how many groups of 4 and 5 to create
num_students = len(student_graph.nodes)
num_5teams, num_4teams = num_size_teams(num_students)
print("Students: %i; 4-teams: %i; 5-teams: %i" %
      (num_students, num_4teams, num_5teams))

# print("Running random assignments...")
# rand_teams = assign_teams_random(
#     four_cliques, five_cliques, num_4teams, num_5teams)
# print("Cost: (lower is better): %.3f" % assignment_cost(rand_teams))
# for team in rand_teams:
#     print(team.nodes, "\tCompat: %.2f; Eval: %.2f" %
#           (team_compatibility(team), team_evaluation(team)))


# print("Running greedy...")
# # Greedily assign required numbers of teams of 4 and 5
# greedy_teams = assign_teams_greedy(
#     four_cliques, five_cliques, num_4teams, num_5teams)
# print("Cost: (lower is better): %.3f" % assignment_cost(greedy_teams))
# for team in greedy_teams:
#     print(team.nodes, "\tCompat: %.2f Eval: %.2f" %
#           (team.graph['compat'], team_evaluation(team)))


print("Running recursive backtracking...")

# # Demote 4-cliques so 5s will be chosen first
# for team in four_cliques:
#     team.graph['compat'] = team.graph['compat'] - 1

# # Make combination of all cliques
# all_cliques = five_cliques + four_cliques
# all_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)

cost, teams = assign_teams_rec(
    four_cliques[:10000], five_cliques[:10000], 0, [], set(), num_students, num_5teams+num_4teams)

print("Cost: (lower is better): %.3f" % cost)
for team in teams:
    print(team.nodes, "\tCompat: %.2f Eval: %.2f" %
          (team.graph['compat'], team_evaluation(team)))
