import joblib
import time
from networkx.classes import graph
from assignments import assign_teams_greedy, random_assignments, assign_teams
from data_loader import load_student_data, create_student_graph
from helpers import num_size_teams
from clique_finding import find_k_clique
from scoring import (
    assignment_cost,
    compatibility,
    sample_score_func,
    team_compatibility,
    team_evaluation
)


student_graph_suffix = input(
    "Enter suffix for student graph filename: student_graph_")
for i in range(3, 6):
    student_graph_filename = "data/student_graph_" + \
        student_graph_suffix + str(i)
    try:
        student_graph = joblib.load(student_graph_filename)
    except FileNotFoundError:
        print("File '%s' not found. Please run data_loader.py to generate student graphs.")
        exit()

    # Load or create all 4-cliques
    four_cliques_filename = "data/four_cliques_" + \
        student_graph_suffix + str(i)
    try:
        four_cliques = joblib.load(four_cliques_filename)
        print("%i four cliques loaded" % len(four_cliques))
    except FileNotFoundError:
        print(four_cliques_filename, "not found. Generating 4-cliques...")
        # Compute all possible 4-cliques
        timer = time.time()
        four_cliques = find_k_clique(student_graph, 4)
        elapsed = time.time() - timer
        print("%i 4-cliques found." % len(four_cliques))
        print(elapsed)

        # Find team compatability of each clique
        timer = time.time()
        for team in four_cliques:
            # compute team compatibility and store as a property of the graph
            team.graph['compat'] = team_compatibility(team.nodes)
        elapsed = time.time() - timer
        print("All cliques scored.")
        print(elapsed)

        # sort the cliques by highest compatibility scores
        timer = time.time()
        four_cliques = [
            team for team in four_cliques if team.graph['compat'] > 0]
        elapsed = time.time() - timer
        print("%i nonzero 4-cliques found." % len(four_cliques))
        print(elapsed)
        timer = time.time()
        four_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)
        elapsed = time.time() - timer
        print("All cliques sorted.")
        print(elapsed)

        joblib.dump(four_cliques, four_cliques_filename)
        print("4-cliques saved in", four_cliques_filename)

    # Load or create all 5-cliques
    five_cliques_filename = "data/five_cliques_" + \
        student_graph_suffix + str(i)
    try:
        five_cliques = joblib.load(five_cliques_filename)
        print("%i five cliques loaded" % len(five_cliques))
    except FileNotFoundError:
        print(five_cliques_filename, "not found. Generating 5-cliques...")
        # Compute all possible 5-cliques
        timer = time.time()
        five_cliques = find_k_clique(student_graph, 5)
        elapsed = time.time() - timer
        print("%i 5-cliques found." % len(five_cliques))
        print(elapsed)

        # Find team compatability of each clique
        timer = time.time()
        for team in five_cliques:
            # compute team compatibility and store as a property of the graph
            team.graph['compat'] = team_compatibility(team.nodes)
        elapsed = time.time() - timer
        print("All cliques scored.")
        print(elapsed)

        # sort the cliques by highest compatibility scores
        timer = time.time()
        five_cliques = [
            team for team in five_cliques if team.graph['compat'] > 0]
        elapsed = time.time() - timer
        print("%i nonzero 5-cliques found." % len(five_cliques))
        print(elapsed)
        timer = time.time()
        five_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)
        elapsed = time.time() - timer
        print("All cliques sorted.")
        print(elapsed)

        joblib.dump(five_cliques, five_cliques_filename)
        print("5-cliques saved in", five_cliques_filename)


# print("All teams loaded. Running random assignments..")
# _, rand_teams = random_assignments(students)

# print("Cost: (lower is better): %.3f" % assignment_cost(rand_teams))
# for team in rand_teams:
#     print(team, "\tCompat: %.2f Eval: %.2f" % (team_compatibility(
#         team), team_evaluation(team)))

# print("All teams loaded. Running greedy..")
# # Figure out how many groups of 4 and 5 to create
# num_students = len(students)
# num_5teams, num_4teams = num_size_teams(num_students)
# print("Students: %i 4-teams: %i 5-teams: %i" %
#       (num_students, num_4teams, num_5teams))
# # Greedily assign required numbers of teams of 4 and 5
# cost, teams = assign_teams_greedy(
#     four_cliques, five_cliques, num_4teams, num_5teams)
# print("Cost: (lower is better): %.3f" % cost)
# for team in teams:
#     print(team.nodes, "\tCompat: %.2f Eval: %.2f" %
#           (team, graph["compat"], team_evaluation(team.nodes)))


# print("Running recursive backtracking...")
# cost, teams = assign_teams(
#     four_cliques[:100], 0, [], student_graph.nodes, 2)
