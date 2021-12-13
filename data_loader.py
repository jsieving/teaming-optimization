"""
Deals with importing data from survey results and converting to Student objects
"""
import itertools as it
import joblib
import networkx as nx
import pandas as pd
import random
from copy import deepcopy
from student import Student


def load_student_data(filename):
    data = pd.read_csv(filename)
    students = []

    num_students = len(data)
    commitments = random.choices(
        range(1, 6), weights=[1, 3, 4, 3, 1.5], k=num_students)

    # Each row represents a student
    for idx, row in data.iterrows():
        anti_prefs = row["AntiPrefs"]
        if str(anti_prefs) != "nan":
            silver_bullets = set([sb.strip()
                                 for sb in str(anti_prefs).split(";")])
        else:
            silver_bullets = set()

        prefs = row["Prefs"]
        if str(prefs) != "nan":
            preferences = set([pref.strip() for pref in str(prefs).split(";")])
        else:
            preferences = set()

        # Convert interests to set
        topics = row["ProjTopics"]
        if str(topics) != "nan":
            interests = set([intr.strip() for intr in topics.split(",")])
        else:
            interests = set()

        # Create student and add to list
        s = Student(
            name=row["Student"],
            pronouns=row["Pronouns"],
            commitment=commitments[idx],
            interests=interests,
            preferences=preferences,
            silver_bullets=silver_bullets,
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


if __name__ == "__main__":
    survey_file_suffix = input(
        "Enter suffix for survey data filename: anonymized_surveys_")
    survey_filename = "data/anonymized_surveys_" + survey_file_suffix + ".csv"

    # Parse data from survey to create Student objects
    try:
        students = load_student_data(survey_filename)
    except FileNotFoundError:
        print("File %s not found. Please check your working folder and spelling." %
              survey_filename)
        exit()
    print("Students loaded: ", len(students))

    for i in range(3):
        students_sample = deepcopy(random.sample(
            students, random.randint(20, 24)))
        students_sample.sort(key=lambda student: student.name)

        # Create the graph from the previously-loaded students, connecting
        # non-silver-bulleted Student objects as vertices # with edge weights
        # representing compatibility
        sample_student_graph = create_student_graph(students_sample)
        graph_filename = "data/student_graph_" + survey_file_suffix + str(i)
        joblib.dump(sample_student_graph, graph_filename)
        print("Saving", graph_filename)

    print("Created 3 sample student graphs.")
