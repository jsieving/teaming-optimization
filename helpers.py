import numpy as np

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