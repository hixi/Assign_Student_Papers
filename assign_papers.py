''' The The algorithm in 'serialdictatorship.py' has been referenced.
    https://github.com/j2kun/top-trading-cycles/blob/master/serialdictatorship.py
'''
# Final commit by Simran on 6/2/17

from __future__ import print_function
import random
import csv
import sys
import logging
import argparse

''' read_csv() reads the files containing the paper IDs and students preferences

    1. The students preferences are stored in a list of lists (students_pref_list).
       The structure is as follows: [[student1, pref 1, pref2, pref3, pref4],
                                     [student2, pref 1, pref2, pref3, pref4],
                                     [student3, pref 1, pref2, pref3, pref4]...]
    2. The paper IDs are stored in a list (papers_list)
'''        

def read_csv(students_file_path, papers_file_path):

    students_pref_list = []
    papers_list = []			

    with open(students_file_path, "r") as student_preference_file:
        reader = csv.reader(student_preference_file, delimiter=' ', quotechar='|')
        # It is assumed that the first row contains headers
        headers = next(reader)
        for row in reader:
            row_list = row[0].split(",")
            students_pref_list.append(row_list[0:5])
        
    with open(papers_file_path, "r") as papers_file:
        reader = csv.reader(papers_file, delimiter=' ', quotechar='|')
        headers = next(reader)
        for row in reader:
            papers_list.append(row[0])
          
    assign_papers(students_pref_list, papers_list)
 

''' assign_papers() assigns papers to students and stores the assignment in a dictionary (assignment_dict)
    
    Pseudo Code:
    1. Shuffle the students list randomly
    2. Store the paper IDs in a set (availablePapers)
    3. Assign each student his first available preference in order and 
       3.1. store the assignment in a dictionary (See code on line 74)
       3.2. delete the assigned paper from the availablePapers set (line 75)
    4. If none of the student's preferences are available, randomly assign him a paper in the end.
'''

def assign_papers(students_pref_list, papers_list, seed = None):

    if seed is not None:
        random.seed(seed)

    # Create a deep copy of the 'students_pref_list' list of lists and shuffle it randomly   
    studentsPreferences = students_pref_list[:]
    random.shuffle(studentsPreferences)
    logging.debug("\nThe student list after shuffling is:\n" + str(studentsPreferences) + "\n")

    assignment_dict = dict()                # Will contain the final assignment
    availablePapers = set(papers_list[:])   # Contains the papers that are available
      
    for student_pref in studentsPreferences:
        for x in range(1, 5):	
            if(student_pref[x] == ''):      # In case the student has less than 4 preferences
                break
            elif(student_pref[x] in availablePapers):
                assignment_dict[student_pref[0]] = student_pref[x]    
                availablePapers.remove(student_pref[x])                           
                break
                
    for student_pref in studentsPreferences:             
        if (student_pref[0] not in assignment_dict.keys()):      # If student has not been assigned any paper   
            assigned_paper = random.sample(availablePapers, 1)   # Assign a random paper to student
            assignment_dict[student_pref[0]] = assigned_paper[0]
            availablePapers.remove(assigned_paper[0])

    logging.debug("The final assignment is:\n" + str(assignment_dict) + "\n")
    logging.info("Assignment complete. Please see the file assignment_result.csv for the output.\n")

    write_csv(assignment_dict)

   
''' write_csv() writes back the output (Student_ID: Paper_allocated) to assignment_result.csv '''

def write_csv(allocation_dict):

    with open('assignment_result.csv', "w") as allocation_result_file:
        fieldnames = ["Student_ID", "Paper_allocated"]
        writer = csv.DictWriter(allocation_result_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writeheader()
        for key in allocation_dict: 
            writer.writerow({'Student_ID': key, 'Paper_allocated':allocation_dict[key]})


''' main() parses the command line arguments '''

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("studentprefs_file", help="Path to the csv file containing the student IDs and their preferences", default="student_preferences.csv")
    parser.add_argument("papers_file", help="Path to the csv file containing the paper IDs", default="papers.csv")
    parser.add_argument("-v", "--verbose", action="store_true", help="Get a verbose output")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    read_csv(args.studentprefs_file, args.papers_file)
    
if __name__ == "__main__":
    main(sys.argv[1:])
