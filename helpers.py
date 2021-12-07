import numpy as np
import itertools


def count_students(teams):
    '''
    Counts the total number of students assigned in a list of teams.
    '''
    total = 0
    for team in teams:
        total += len(team)
    return total


def sorted_teams(teams):
    '''
    Sorts a list of team assignments in place and returns it.

    Each team is sorted alphabetically by student name. Then, all teams are
    sorted alphabetically by first-listed student name.
    '''
    for team in teams:
        team.sort(key=lambda student:student.name)
    teams.sort(key=lambda team:team[0].name)
    return teams


def num_size_teams(num_students):
    '''
    Takes in a number of students and calculate how many 4 and 5 person teams
    they should be on.

    Returns a tuple of (5-person teams, 4-person teams).
    '''
    # Nonsensical math to figure out how many students on each team
    reqd_teams = min(np.ceil(num_students / 5),
                    np.floor(num_students / 4))
    full_teams_proxy = reqd_teams - (-num_students % 5)
    teams_of_5 = full_teams_proxy if full_teams_proxy >= 0 else reqd_teams
    teams_of_4 = reqd_teams - teams_of_5

    return teams_of_5, teams_of_4


def violates_silver_bullets(team):
    '''
    Checks if there is a silver bullet for any student in a list from any other
    student in the list.
    '''
    all_silver_bullets = set()
    # Merge silver bullets of all team members
    for student in team:
        all_silver_bullets |= student.silver_bullets
    for student in team:
        if student.name in all_silver_bullets:
            return True
    return False


def count_met_partner_prefs(team):
    '''
    Counts the number of instances where a student on a team had requested to
    work with another student on that team.

    For example, if Alice and Bob are on a team and Alice requested to work with Bob, that gets a 1.

    If Alice and Bob both requested each other, that gets a 2.

    If Alice, Bob and Carol are on a team and Alice requested to work with Bob
    and Carol, that gets a 2.

    If Alice, Bob and Carol all mutually rquested each other, that gets a 6.
    '''
    all_preferences = {}  # students who are some # of teammates' preference
    met_partner_prefs = 0  # 1 point for each preference if they're on the team

    # Count up times each student (even non-teammates) was requested by someone
    # on this team
    for student in team:
        for pref in student.preferences:
            all_preferences[pref] = all_preferences.get(pref, 0) + 1

    # Add up # times each student on the team was requested by their teammates
    for student in team:
        met_partner_prefs += all_preferences.get(student.name, 0)

    return met_partner_prefs


def count_mutual_partner_prefs(team):
    '''
    Counts the number of instances where two students on a team both requested
    to work with each other.

    For example, if Alice and Bob are on a team and Alice requested to work with Bob, that gets a 0.

    If Alice and Bob both requested each other, that gets a 1.

    If Alice, Bob and Carol all mutually rquested each other, that gets a 3.
    '''
    mutual_partner_prefs = 0
    for studentA, studentB in itertools.combinations(team, 2):
        if studentA.prefers(studentB) and studentB.prefers(studentA):
            mutual_partner_prefs += 1
        
    return mutual_partner_prefs
