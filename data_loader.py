"""
Deals with importing data from survey results and converting to Student
objects.

When run as a main program, saves graph and clique data created from a sample
of the loaded data.
"""
import itertools as it
import joblib
import networkx as nx
import pandas as pd
import random
from copy import deepcopy
from clique_finding import find_k_clique
from helpers import violates_anti_prefs
from student import Student


def load_student_data(filename):
    data = pd.read_csv(filename)
    students = []

    num_students = len(data)
    commitments = random.choices(
        range(1, 6), weights=[1, 3, 4, 3, 1.5], k=num_students)

    # Each row represents a student
    for idx, row in data.iterrows():
        anti_prefs_data = row["AntiPrefs"]
        if str(anti_prefs_data) != "nan":
            anti_prefs = set([sb.strip()
                              for sb in str(anti_prefs_data).split(";")])
        else:
            anti_prefs = set()

        prefs_data = row["Prefs"]
        if str(prefs_data) != "nan":
            preferences = set([pref.strip()
                              for pref in str(prefs_data).split(";")])
        else:
            preferences = set()

        # Convert topics to set
        topics_data = row["ProjTopics"]
        if str(topics_data) != "nan":
            topics = set([intr.strip()
                         for intr in str(topics_data).split(";")])
        else:
            topics = set()

        # Create student and add to list
        s = Student(
            name=row["Student"],
            pronouns=row["Pronouns"],
            commitment=commitments[idx],
            topics=topics,
            preferences=preferences,
            anti_prefs=anti_prefs,
            intr_mgmt=row["IntLeadership"],
            exp_mgmt=row["ExpLeadership"],
            intr_elec=row["IntElecProto"],
            exp_elec=row["ExpElecProto"],
            intr_prog=row["IntProg"],
            exp_prog=row["ExpProg"],
            intr_cad=row["IntMechCAD"],
            exp_cad=row["ExpMechCAD"],
            intr_fab=row["IntMechFab"],
            exp_fab=row["ExpMechFab"],
        )
        students.append(s)

    students.sort(key=lambda student: student.name)
    return students


def create_student_graph(students):
    """
    Given a list of Student objects, creates a graph connecting all students
    except those that have a silver bullet between them

    Arguments:
        a list containing Student objects

    Returns:
        a networkx Graph object where the nodes are Student objects and the edges
        are possible (non-silver-bulleted) connections
    """
    # add all the students as nodes in the graph
    student_graph = nx.Graph()
    student_graph.add_nodes_from(students)

    # add edges between students that have no silver bullets between them
    for student1, student2 in it.combinations(students, 2):
        if not student1.dislikes(student2) and not student2.dislikes(student1):
            student_graph.add_edge(student1, student2)

    return student_graph


def create_save_k_cliques(k, student_graph, suffix):
    # Load all 4-cliques
    k_cliques_filename = "data/%i_cliques_%s" % (k, suffix)
    # Compute all possible 4-cliques
    print("Generating %i-cliques..." % k)
    k_cliques = find_k_clique(student_graph, k)
    print("%i %i-cliques found." % (len(k_cliques), k))

    # Do not save any cliques that put anti-preferences together
    # They shouldn't make it this far, but checking can save a lot of time
    k_cliques = [team for team in k_cliques if not violates_anti_prefs(team)]
    print("%i valid %i-cliques found." % (len(k_cliques), k))

    joblib.dump(k_cliques, k_cliques_filename)
    print("%i-cliques saved in %s" % (k, k_cliques_filename))


if __name__ == "__main__":
    survey_file_suffix = input(
        "Enter suffix for survey data filename: anonymized_surveys_")
    survey_filename = "data/anonymized_surveys_" + survey_file_suffix + ".csv"

    num_students = int(input("Enter a number of students: "))

    # Parse data from survey to create Student objects
    try:
        students = load_student_data(survey_filename)
    except FileNotFoundError:
        print("File %s not found. Please check your working folder and spelling." %
              survey_filename)
        exit()
    print("Students loaded: ", len(students))

    students_sample = deepcopy(random.sample(
        students, num_students))
    students_sample.sort(key=lambda student: student.name)

    # Create the graph from the previously-loaded students, connecting
    # non-silver-bulleted Student objects as vertices # with edge weights
    # representing compatibility
    sample_student_graph = create_student_graph(students_sample)
    graph_filename = "data/student_graph_" + \
        survey_file_suffix + str(num_students)
    joblib.dump(sample_student_graph, graph_filename)
    print("Saving", graph_filename)

    cliques_suffix = survey_file_suffix + str(num_students)

    create_save_k_cliques(4, sample_student_graph, cliques_suffix)
    create_save_k_cliques(5, sample_student_graph, cliques_suffix)
