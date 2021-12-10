"""
Deals with importing data from survey results and converting to Student objects
"""
import pandas as pd
import networkx as nx
import itertools as it
from student import Student


def load_student_data(filename):
    data = pd.read_csv(filename)
    students = []

    # Each row represents a student
    for index, row in data.iterrows():
        # Need to combine data from multiple columns for these fields
        silver_bullet_cols = ["Silver Bullet #1", "Silver Bullet #2"]
        preference_cols = ["Preference #2",
                            "Preference #3",
                            "Preference #4",
                            "Preference #5",
                            "Preference #6"]
        silver_bullets = set()
        preferences = set()

        for col_name in silver_bullet_cols:
            sb = row[col_name]
            if str(sb) != "nan":
                silver_bullets.add(sb)
        
        for col_name in preference_cols:
            pref = row[col_name]
            if str(pref) != "nan":
                preferences.add(pref)

        # Convert interests to set
        interests = row["Category interests (comma separated categories)"]
        if str(interests) != "nan":
            interests = {intr.strip() for intr in interests.split(",")}
        else:
            interests = set()

        # Create student and add to list
        s = Student(
            name=row["Name"],
            commitment=row["Commitment (meet req -> beyond)"],
            interests=interests,
            preferences=preferences,
            silver_bullets=silver_bullets,
            intr_mgmt=row["Mgmt intr."],
            exp_mgmt=row["Mgmt exp."],
            intr_elec=row["Elex intr."],
            exp_elec=row["Elex exp."],
            intr_prog=row["Prog intr."],
            exp_prog=row["Prog exp."],
            intr_cad=row["CAD intr."],
            exp_cad=row["CAD exp."],
            intr_fab=row["Fab intr."],
            exp_fab=row["Fab exp."],
        )
        students.append(s)

    students.sort(key=lambda student:student.name)
    return students


def create_student_graph(students):
    """
    Given an iterable of Student objects, creates a graph connecting all students
    except those that have a silver bullet between them

    Arguments:
        an iterable containing Student objects

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

