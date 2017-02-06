# Assign_Student_Papers
Program to assign papers to students based on their preferences following the Serial Dictatorship algorithm

## Notes

The program takes two CSV files as input and writes back the output to a new CSV file. Following are the details.

**Input files**
- student_preferences.csv: Contains the Student IDs and their preferences (Student_ID, Pref1, Pref2, Pref3, Pref4)
- papers.csv: Contains all the Paper_IDs 

**Output file**
- assignment_result.csv: The allocation results (Student_ID, Paper_ID) are written back to this file

- It is assumed that the first row of the input files contains headers.
- The CSV files in this repository are just an example of the expected format.  
 
## Usage

`assign_papers.py studentprefs_file paperIDs_file [-h][-v]`

**Positional Arguments**
- studentprefs_file: Path to the file containing the Student IDs and their preferences
- paperIDs_file: Path to the file containing all the paper IDs

**Optional Arguments**
- -h, --help: Enabling this flag will display the help message and exit
- -v, --verbose: Enabling this flag will produce a verbose output on the command line

## References

The *Serial Dictatorship and House Allocation* algorithm has been referenced ([Link to code](https://github.com/j2kun/top-trading-cycles/blob/master/serialdictatorship.py)). However, it has been appropriately modified for this problem.
