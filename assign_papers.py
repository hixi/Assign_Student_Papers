''' The The algorithm in 'serialdictatorship.py' has been referenced.
    https://github.com/j2kun/top-trading-cycles/blob/master/serialdictatorship.py
'''
# Final commit by Simran on 6/2/17

from __future__ import print_function
from pathlib import Path
import random
import csv
import sys
import logging
import argparse
import collections

''' read_csv() reads the files containing the paper IDs and students preferences

1. The students preferences are stored in a list of lists (students_pref_list)
   The structure is as follows: [[student1, pref 1, pref2, pref3, pref4],
                                 [student2, pref 1, pref2, pref3, pref4],
                                 [student3, pref 1, pref2, pref3, pref4]...]
2. The paper IDs are stored in a list (papers_list)
'''       

def read_csv(students_file_path, papers_file_path):

    students_pref_list = []
    papers_list = []			
    
    try:
        with open(students_file_path, "r") as student_preference_file:
            reader = csv.reader(student_preference_file, delimiter=' ', quotechar='|')
            # It is assumed that the first row contains headers
            headers = next(reader)
            for row in reader:
                row_list = row[0].split(",")
                students_pref_list.append(row_list[0:5])
    except FileNotFoundError:
        sys.exit("FileNotFoundError: " + students_file_path + " not found.\nPlease enter a valid path")
    except IOError as e:
        sys.exit("An I/O error was encountered: %s" % ( str(e) ) )
    
    try:
        with open(papers_file_path, "r") as papers_file:
            reader = csv.reader(papers_file, delimiter=' ', quotechar='|')
            headers = next(reader)
            for row in reader:
                papers_list.append(row[0])
    except FileNotFoundError:
        sys.exit("FileNotFoundError: " + papers_file_path + " not found.\nPlease enter a valid path")
    except IOError as e:
        sys.exit("An I/O error was encountered: %s" % (str(e)))
        
    return students_pref_list, papers_list


''' assign_papers() assigns papers to students and stores the assignment in a dictionary
    
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

    # Create a deep copy of 'students_pref_list' and shuffle it randomly   
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
                assignment_dict[student_pref[0]] = [student_pref[x], str(x)]    
                availablePapers.remove(student_pref[x])                           
                break
                
    for student_pref in studentsPreferences:             
        if (student_pref[0] not in assignment_dict.keys()):      # If student has not been assigned a paper   
            assigned_paper = random.sample(availablePapers, 1)   # Assign a random paper to student
            assignment_dict[student_pref[0]] = [assigned_paper[0], ""]
            availablePapers.remove(assigned_paper[0])
     
    assignment_dict = {int(k):v for k,v in assignment_dict.items()}
    orderedDict = collections.OrderedDict(sorted(assignment_dict.items()))

    logging.debug("The final assignment is: (Stud_ID, [Paper assigned, Preference no.])")
    logging.debug("\n" + str(orderedDict) + "\n")
    logging.info("Assignment complete")
    
    return orderedDict


''' write_csv() writes back the output (Student_ID: Paper_allocated) to assignment_result.csv '''
 
def write_csv(orderedDict, output_filepath):
    
    try:
        with open(output_filepath, "w") as assignment_result_file:
            fieldnames = ["Stud_ID", "Paper_assigned", "Pref_No"]
            writer = csv.DictWriter(assignment_result_file, delimiter=',', 
                                    lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
            for key in orderedDict: 
                writer.writerow({'Stud_ID': key, 'Paper_assigned':orderedDict[key][0], 
                                 "Pref_No": orderedDict[key][1]})               
        success = True
    except IOError as e:
        print("An I/O error was encountered while writing to output file:\n %s" % ( str(e) ) )
        success = False

    return success

''' main() parses the command line arguments '''

def main(argv):
    
    # By default, do not overwrite the output file
    writeOutputToFile = False

    # Accept user input from command line 
    parser = argparse.ArgumentParser()
    parser.add_argument("studentprefs_file", help="Path to csv file containing student IDs and preferences")
    parser.add_argument("papers_file", help="Path to csv file containing the paper IDs")
    parser.add_argument("-o", help = "Path to the output file. Default is assignment_result.csv", 
                        default="assignment_result.csv")
    parser.add_argument("-v", "--verbose", action="store_true", help="Get a verbose output")
    parser.add_argument("-e", "--enforce", action="store_true", help="Enforce output file overwrite")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)
        
    out_file = Path(args.o)
    
    # If the output file already exists, overwrite only if the user has enabled -enforce
    if out_file.is_file():
        if args.enforce:
            print("\nPlease note that the output file " + args.o + " will be overwritten")
            writeOutputToFile = True
        else:
            print("\n Note:  The output file " + args.o + " already exists.")
            print("\tTo overwrite the file, please enable the enforce (-e) flag.")
            print("\tElse, specify a new path for the output file.\n")
    # If output file does not already exist, create and write to it
    else:
         writeOutputToFile =  True
        
    students_pref_list, papers_list = read_csv(args.studentprefs_file, args.papers_file)
    orderedDict = assign_papers(students_pref_list, papers_list)
    
    if writeOutputToFile:
        success = write_csv(orderedDict, args.o)
        if success:
            logging.info("Please see the file " + args.o + " for the assignment results")
            
            
if __name__ == "__main__":
    main(sys.argv[1:])
