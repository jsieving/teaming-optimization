import joblib
from assignments import assign_teams_greedy, random_assignments, assign_teams
from data_loader import load_student_data, create_student_graph
from helpers import num_size_teams
from clique_finding import find_k_clique
from scoring import (
    compatibility,
    sample_score_func,
    team_compatibility,
    team_evaluation
)

filename = input(
    "Enter file name with survey data [team_sample_data.csv]: ") or "team_sample_data.csv"

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

four_cliques_filename = "four_cliques"
all_student_graph_filename = "all_student_graph"
try:
    four_cliques = joblib.load(four_cliques_filename)
    all_student_graph = joblib.load(all_student_graph_filename)
except FileNotFoundError:
    # Parse data from survey to create Student objects
    filename = input(
        "Enter file name with survey data [team_sample_data.csv]: ") or "team_sample_data.csv"
    students = load_student_data(filename)
    num_students = len(students)

    # Create a graph connecting non-silver-bulleted Student objects as vertices with edge weights representing compatibility
    all_student_graph = create_student_graph(students)

    # Figure out how many groups of 4 and 5 to create
    num_5teams, num_4teams = num_size_teams(num_students)

    # Compute all possible 4-cliques
    four_cliques = find_k_clique(all_student_graph, 4)

    # Find team compatability of each clique
    for team in four_cliques:
        # compute team compatibility and store as a property of the graph
        team.graph['compat'] = team_compatibility(team.nodes)

    # sort the cliques by highest compatibility scores
    four_cliques = [team for team in four_cliques if team.graph['compat'] > 0]
    four_cliques.sort(key=lambda team: team.graph['compat'], reverse=True)

    joblib.dump(four_cliques, four_cliques_filename)
    joblib.dump(all_student_graph, all_student_graph_filename)

# for team in four_cliques:
#     print(team, team.graph)
print(len(four_cliques))


print("All teams sorted. Running greedy..")
cost, teams = assign_teams_greedy(four_cliques, None, 4, 0)
print("Cost:", cost)
print(type(teams))
for team in teams:
    print(team.nodes, team.graph['compat'])

# print("Running recursive backtracking...")
# cost, teams = assign_teams(
#     four_cliques[:100], 0, [], all_student_graph.nodes, 2)
