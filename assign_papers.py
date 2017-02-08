"""
The algorithm in 'serialdictatorship.py' has been referenced.
https://github.com/j2kun/top-trading-cycles/blob/master/serialdictatorship.py

Final commit by Simran on 8/2/17
"""

from __future__ import print_function
from pathlib import Path
import random
import csv
import sys
import logging
import argparse
import collections


def read_csv(students_file_path, papers_file_path):

    """ read_csv() reads the paper IDs and students preferences files
        1. The students preferences are stored in a list of lists
           The structure is as follows:
           students_pref_list: [[student1, pref 1, pref2, pref3, pref4],
                                [student2, pref 1, pref2, pref3, pref4],
                                [student3, pref 1, pref2, pref3, pref4]...]
        2. The paper IDs are stored in a list (papers_list)
    """

    students_pref_list = []
    papers_list = []

    try:
        with open(students_file_path, "r") as student_preference_file:
            reader = csv.reader(student_preference_file,
                                delimiter=' ', quotechar='|')
            # It is assumed that the first row contains headers
            next(reader)
            for row in reader:
                row_list = row[0].split(",")
                students_pref_list.append(row_list[0:5])
    except FileNotFoundError:
        sys.exit("FileNotFoundError: " + students_file_path +
                 " not found.\nPlease enter a valid path.")
    except IOError as e:
        sys.exit("An I/O error was encountered: %s" % (str(e)))

    try:
        with open(papers_file_path, "r") as papers_file:
            reader = csv.reader(papers_file, delimiter=' ', quotechar='|')
            next(reader)
            for row in reader:
                papers_list.append(row[0])
    except FileNotFoundError:
        sys.exit("FileNotFoundError: " + papers_file_path +
                 " not found.\nPlease enter a valid path.")
    except IOError as e:
        sys.exit("An I/O error was encountered: %s" % (str(e)))

    return students_pref_list, papers_list


def assign_papers(students_pref_list, papers_list, seed=None):

    """ assign_papers() assigns papers to students and
        stores the assignment in a dictionary

        Pseudo Code:
        1. Shuffle the students list randomly
        2. Store the paper IDs in a set (available_papers)
        3. Assign each student his first available preference in order and
           3.1. store the assignment in a dictionary (See code on line 74)
           3.2. delete assigned paper from the available_papers set (line 75)
        4. If none of the student's preferences are available,
           randomly assign him a paper in the end.
    """

    if seed is not None:
        random.seed(seed)

    # Create a deep copy of 'students_pref_list' and shuffle it randomly
    students_preferences = students_pref_list[:]
    random.shuffle(students_preferences)
    logging.debug("\nThe student list after shuffling is:\n" +
                  str(students_preferences) + "\n")

    # assignment_dict will contain the final assignment
    assignment_dict = dict()
    # available_papers set contains the papers that are available
    available_papers = set(papers_list[:])

    for student_pref in students_preferences:
        for x in range(1, 5):
            # In case the student has less than 4 preferences
            if student_pref[x] == '':
                break
            elif student_pref[x] in available_papers:
                assignment_dict[student_pref[0]] = [student_pref[x], str(x)]
                available_papers.remove(student_pref[x])
                break

    for student_pref in students_preferences:
        # If student has not been assigned a paper
        if student_pref[0] not in assignment_dict.keys():
            # Assign a random paper to student
            assigned_paper = random.sample(available_papers, 1)
            assignment_dict[student_pref[0]] = [assigned_paper[0], ""]
            available_papers.remove(assigned_paper[0])

    assignment_dict = {int(k): v for k, v in assignment_dict.items()}
    ordered_dict = collections.OrderedDict(sorted(assignment_dict.items()))

    logging.debug("The final assignment is: " +
                  "(Stud_ID, [Paper assigned, Pref no.])")
    logging.debug("\n" + str(ordered_dict) + "\n")
    logging.info("Assignment complete")

    return ordered_dict


def write_csv(ordered_dict, output_filepath):

    """ write_csv() writes back the output (Student_ID: Paper_allocated)
        to assignment_result.csv
    """

    try:
        with open(output_filepath, "w") as assignment_result_file:
            fieldnames = ["Stud_ID", "Paper_assigned", "Pref_No"]
            writer = csv.DictWriter(assignment_result_file, delimiter=',',
                                    lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
            for key in ordered_dict:
                writer.writerow({'Stud_ID': key,
                                 'Paper_assigned': ordered_dict[key][0],
                                 'Pref_No': ordered_dict[key][1]})

        logging.info("Please see the file " + output_filepath +
                     " for the assignment results")

    except IOError as e:
        print("An I/O error occurred while writing to output file:\n %s"
              % (str(e)))


def main(argv):

    """ main() parses the command line arguments """

    # By default, do not overwrite the output file
    write_output_to_file = False

    # Accept user input from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("studentprefs_file",
                        help="Path to csv file containing " +
                             "student IDs and preferences")
    parser.add_argument("papers_file",
                        help="Path to csv file containing the paper IDs")
    parser.add_argument("-o",
                        help="Path to the output file. " +
                             "Default is assignment_result.csv",
                        default="assignment_result.csv")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Get a verbose output")
    parser.add_argument("-e", "--enforce", action="store_true",
                        help="Enforce output file overwrite")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    students_pref_list, papers_list = read_csv(args.studentprefs_file,
                                               args.papers_file)
    ordered_dict = assign_papers(students_pref_list, papers_list)

    out_file = Path(args.o)

    # If the output file already exists, overwrite only if -enforce is enabled
    if out_file.is_file():
        if args.enforce:
            print("\nPlease note that the output file " + args.o +
                  " will be overwritten")
            write_output_to_file = True
        else:
            print("\n Note:  The output file " + args.o + " already exists.")
            print("\tTo overwrite file, please enable the enforce (-e) flag")
            print("\tor specify a new path for the output file.")
            print("\tAlternatively, you can view the result " +
                  "with the -v flag.\n")
    # If output file does not already exist, create and write to it
    else:
        write_output_to_file = True

    if write_output_to_file:
        write_csv(ordered_dict, args.o)

if __name__ == "__main__":
    main(sys.argv[1:])
