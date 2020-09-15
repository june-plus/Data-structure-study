## Data-structure-study
SW Exam due 09/14/2020

## Tools/Modules used
1. sqlite3
2. tabulate
3. UnitTest

## Relevant File List
1. exam.py: Main code file
2. test_exam.py: Unit Testing file

## How to run the code
1. download relevant files 
2. run exam.py. I used cmd with command: python exam.py
3. It should trigger a simple interface to start. Feel free to try out different options
4. You may run test_exam.py file to see unit test results.

## Further thoughts
1. deepen usage of unit tests. I tried to scope the necessities, but drilling down and testing all possible edge cases would be the best practice. 
2. Some kind of front end development. I thought about using flask to launch into a web app, but given the time constraints, I decided to implement a very simple command-prompt UI. 
3. Please let me know of any feedbacks!

### Thoughts on sensitive information like Social Security Numbers
- I utilized a separate data table <SSN_KEY> that contains account number of policy holders and their faux-ssn. In the meantime, the <Accounts> table has a censored SSN column that only shows last four digits of any policyholder's SSN. 
- In my previous experience, sensitive data was actually stored in a separate physical copy (usually locked in a "safe" data room) that contained sensitive data along with seemingly randomized identification number. PII (Personally Identifiable Information) was taken away from any data, while the physical copy remained secure. When it was necessary to use the PII, we joined that data with a unique identification number to perform necessary action (de-duping, etc).

Disclaimer: SSN in related data with this repository are randomly generated and are not real. 
