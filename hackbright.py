"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    first, last, github = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (first, last, github)
    return (first, last, github)


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM Projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    # row = [title, desctiption, max_grade]
    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
        SELECT grade
        FROM Grades
        WHERE student_github = ?
          AND project_title = ?
        """
    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    print "Student %s in project %s received grade of %s" % (
        github, title, row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """INSERT INTO Grades (student_github, project_title, grade)
               VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (github, title, grade))
    db_connection.commit()
    print "Successfully assigned grade of %s for %s in %s" % (
        grade, github, title)

def get_grade_by_student(first_name):
    """Get all of a student's grades, line by line."""

    QUERY = """
        SELECT g.project_title, g.grade 
        FROM Students AS s JOIN Grades AS g 
        ON s.github = g.student_github
        WHERE s.first_name = ?
    """

    db_cursor.execute(QUERY, (first_name,))
    row = db_cursor.fetchall()
    return_list = []
    
    if row != []:
        for project in row:
            return_list.append(project) #may need to .append
        return return_list
    else:
        print 'Please try again and enter a FIRST NAME'

def get_grades_by_project(title):
    """Get all of the grades for a project by student."""

    QUERY = """
        SELECT first_name, grade 
        FROM Students JOIN Grades
        ON github = student_github
        WHERE project_title = ?
    """

    db_cursor.execute(QUERY, (title,))
    return db_cursor.fetchall() #returns list of tuples with first name, grade info


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
