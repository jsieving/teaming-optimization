from assignments import random_assignments
from data_loader import load_student_data
from helpers import compatibility
from scoring import sample_score_func

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