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


def skill_deficiency(team):
    '''
    Calculates how much a team is lacking overall in 4 key areas:
    management, electrical, programming, and mechanical (CAD + fabrication).

    Assumes that the team's ability in an area is equal to the ability of
    the strongest student in that area. Currently this is the sum of interest
    and experience, and a score of 8 is considered to be completely sufficient
    for any given area.
    
    For example, if a team has a student with 3 interest in programming and 5
    experience, or 4 and 4, that team will be considered to be sufficiently
    covered for programming.

    The overall deficiency is calculated as the distance that a team is from
    having at least 8 in each area, with each area treated like a dimension.
    **This means that having a small deficiency in several areas is better than
    having a big deficiency in 1 area.**
    '''
    # Find out how good (interested + experienced) the best student on the team
    # is for each area
    max_mgmt = max(student.mgmt for student in team)
    max_elec = max(student.elec for student in team)
    max_prog = max(student.prog for student in team)
    max_mech = max(student.mech for student in team)

    # If the best student handles each area, how deficient will the team be
    deficient_mgmt = max(0, 8-max_mgmt)**2
    deficient_elec = max(0, 8-max_elec)**2
    deficient_prog = max(0, 8-max_prog)**2
    deficient_mech = max(0, 8-max_mech)**2

    # Basically computing the "distance" from complete sufficiency
    overall_deficiency = np.sqrt(sum(
        [deficient_mgmt, deficient_elec, deficient_prog, deficient_mech]
    ))

    # Max possible is 12, so noramlize to 0 -> 1
    return overall_deficiency / 12


def exp_deficiency(team):
    '''
    Like skill_deficiency, but focuses only on experience for technical areas.
    '''
    # Find out how good (interested + experienced) the best student on the team
    # is for each area
    max_elec = max(student.exp_elec for student in team)
    max_prog = max(student.exp_prog for student in team)
    max_fan = max(student.exp_fab for student in team)
    max_cad = max(student.exp_cad for student in team)

    # If the best student handles each area, how deficient will the team be
    deficient_elec = max(0, 4-max_elec)**2
    deficient_prog = max(0, 4-max_prog)**2
    deficient_fab = max(0, 4-max_fab)**2
    deficient_cad = max(0, 4-max_cad)**2

    # Basically computing the "distance" from complete sufficiency
    overall_deficiency = np.sqrt(sum(
        [deficient_elec, deficient_prog, deficient_fab, deficient_cad]
    ))

    # Max possible is 6, so noramlize to 0 -> 1
    return overall_deficiency / 6


def intr_deficiency(team):
    '''
    Like skill_deficiency, but focuses only on interest for technical areas.
    '''
    # Find out how good (interested + experienced) the best student on the team
    # is for each area
    max_elec = max(student.intr_elec for student in team)
    max_prog = max(student.intr_prog for student in team)
    max_fan = max(student.intr_fab for student in team)
    max_cad = max(student.intr_cad for student in team)

    # If the best student handles each area, how deficient will the team be
    deficient_elec = max(0, 4-max_elec)**2
    deficient_prog = max(0, 4-max_prog)**2
    deficient_fab = max(0, 4-max_fab)**2
    deficient_cad = max(0, 4-max_cad)**2

    # Basically computing the "distance" from complete sufficiency
    overall_deficiency = np.sqrt(sum(
        [deficient_elec, deficient_prog, deficient_fab, deficient_cad]
    ))

    # Max possible is 6, so noramlize to 0 -> 1
    return overall_deficiency / 6


def percent_strongly_skilled(team):
    '''
    Returns the percent of students on a team who are "strongly skilled" at 
    something.

    "Strongly skilled" is defined as having a total score of 8 or more in
    combined interest and experience.
    The goal of this function is to find teams where a couple of students are
    strong in a lot of areas, and might end up with the responsibility of
    teaching their teammates a lot. **This is kind of a proxy for making sure
    that there is a separate student who can "lead" the team in each area.**

    If any student does not have a particular strong skill, this will return
    less than 1.
    '''
    good_mgmt_students = filter(lambda student: student.mgmt >= 8, team)
    good_elec_students = filter(lambda student: student.elec >= 8, team)
    good_prog_students = filter(lambda student: student.prog >= 8, team)
    good_mech_students = filter(lambda student: student.mech >= 8, team)
    specialized_students = set().union(
        good_mgmt_students, good_elec_students,
        good_prog_students, good_mech_students
    )

    return len(specialized_students) / len(team)


def sorted_topic_votes(team):
    '''
    Returns a list of the numbers of students who voted for different topics,
    sorted by number of votes.

    For example, if 3 people on the team vote for a music-related project, 2
    vote for a robotics-related project, and 1 votes for an art-related project,
    this will return [3, 2, 1].

    By taking the first n items from the output, another function could figure
    out how much agreement there can be on the project topic if n topics could
    be incorporated into the project.
    '''
    all_topics = {} # topics liked by some # of students

    # Count up votes for each candidate topic
    for student in team:
        for topic in student.interests:
            all_topics[topic] = all_topics.get(topic, 0) + 1

    return sorted(all_topics.values(), reverse=True)
