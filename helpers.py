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