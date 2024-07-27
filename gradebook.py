import json
import os
from policy_repo import PolicyRepository
from grade_repo import GradeRepository
from student import Student, GradePolicy


class Gradebook:
    def __init__(self) -> None:
        self.__students : list[Student] = []
        self.__grade_policy: GradePolicy = GradePolicy(weights={}) 

    def convert_students_tolist(self) -> list[str]:
        output = []
        for student in self.__students:
            output.append(student.conv_to_list())
        return output
            
    def setup_semester(self) -> None:
        print("Setup for the new semester.")
        
        # number of programming assignments, tests and final exam prompts
        num_programming_assignments = int(input("Enter the number of programming assignments (0-6): "))
        while not 0 <= num_programming_assignments <= 6:
            print("Invalid number of programming assignments. It must be between 0 and 6.")
            num_programming_assignments = int(input("Enter the number of programming assignments (0-6): "))

        num_tests = int(input("Enter the number of tests (0-4): "))
        while not 0 <= num_tests <= 4:
            print("Invalid number of tests. It must be between 0 and 4.")
            num_tests = int(input("Enter the number of tests (0-4): "))

        num_final_exams = int(input("Enter the number of final exams (0-1): "))
        while not 0 <= num_final_exams <= 1:
            print("Invalid number of final exams. It must be either 0 or 1.")
            num_final_exams = int(input("Enter the number of final exams (0-1): "))

        # Structure for the relative weights of programming assignments, tests, and final exams
        total_weight = 0
        final_weights = {
        "programming_assignment": {
            "count": num_programming_assignments,
            "weights": {}
        },
        "test": {
            "count": num_tests,
            "weights": {}
        },
        "final_exam": {
            "count": num_final_exams,
            "weight": 0  # initalize first as 0 and then change it if there is a final exam
        }
        }
        # Save weights for programming assignments and tests
        for component in ["programming_assignment", "test"]:
            for i in range(1, final_weights[component]["count"] + 1):
                weight = float(input(f"Enter the weight for {component} {i} as a percentage: "))
                final_weights[component]["weights"][f"{i}"] = weight
                total_weight += weight
        if num_final_exams > 0:
            weight = float(input(f"Enter the weight for final as a percentage: "))
            final_weights["final_exam"]["weight"] = weight
            total_weight += weight
        # Check if total weight is 100%
        if total_weight != 100.0:
            print("The total weight does not add up to 100%. Please start over.")
            self.setup_semester() 
        else:
            # Save the weights to the grade policy and to a JSON file
            self.__grade_policy = GradePolicy(final_weights)
            self.save_policy_to_db()
            self.reset_grades_policy()
            self.__students = [] 
            self.save_students_to_db()
            print("Semester setup complete.")

    def reset_grades_policy(self) -> None:
        # reset grades of all students on new semester
        for student in self.__students:
            student.reset_grade()
    
    # functions for reading/ writing data to files
    def save_policy_to_db(self) -> None:
        policy_repo = PolicyRepository('policy.dat')
        policy_repo.write_policy(self.__grade_policy.weights())
        
    def get_policy_from_db(self) -> None:
        policy_repo = PolicyRepository('policy.dat')
        weights = policy_repo.read_policy()
        if weights is None:
            self.__grade_policy = GradePolicy({})
        else:
            self.__grade_policy = GradePolicy(weights)
        
    def save_students_to_db(self) -> None:
        grade_repo = GradeRepository('Grades.dat')
        grade_repo.write_grade(self.convert_students_tolist())
        
    def get_students_from_db(self) -> None:
        grade_repo = GradeRepository('Grades.dat')
        self.__students = grade_repo.read_grade()

    
    def add_student(self) -> None:
        if not self.__grade_policy.weights():
            print("No grade policy set yet.")
            return
        # Prompt for student's ID
        student_id = int(input("Enter the student's ID (1-9999): "))
        while student_id < 1 or student_id > 9999:
            print("Invalid ID. ID must be between 1 and 9999.")
            student_id = int(input("Enter the student's ID (1-9999): "))

        # Prompt for student's last name
        last_name = input("Enter the student's last name (20 chars max): ")
        while len(last_name) > 20:
            print("Last name too long. It must be at most 20 characters.")
            last_name = input("Enter the student's last name (20 chars max): ")

        # Prompt for student's first name
        first_name = input("Enter the student's first name (20 chars max): ")
        while len(first_name) > 20:
            print("First name too long. It must be at most 20 characters.")
            first_name = input("Enter the student's first name (20 chars max): ")
            
        stud = Student(student_id, first_name, last_name)
        if stud not in self.__students:
            self.__students.append(stud)
            print(f"\nStudent {first_name} {last_name} added successfully.")
            self.save_students_to_db()
        else:
            print(f"\nStudent with ID {student_id} already exists.")
            

    # this function checks if the policy is set and wether students are available or not 
    def check_student_policy(self) -> int:
        if not self.__grade_policy.weights():
            print("No grade policy set yet.")
            return 0
        if not self.__students:
            print("No students added yet.")
            return 0
        return 1

    # customized to record score for all types of scores based on the target
    def record_score(self, target_component: str) -> None:
        if not self.check_student_policy():
            return
        # use grade policy to setup the grades for all students
        grade_policy = self.__grade_policy.weights()
        prog_assig = grade_policy[target_component]
        assig_num = int(input(f"Enter the {target_component} number to be recorded: "))
        while assig_num <= 0 or assig_num > prog_assig["count"]:
            print(f"Invalid {target_component} number, Try again.")
            assig_num = int(input(f"Enter the {target_component} number to be recorded: "))

        # Iterate through all assignments in the grade policy to record scores for each
        for component, details in grade_policy.items():
            if component == "final_exam" and details["count"] == 0:
                continue 

            for i in range(1, details["count"] + 1):
                if component == target_component and i == assig_num:
                    assignment_key = f"{component} {i}"  # Like "programming_assignment 1"
                    print(f"\nRecording scores for {assignment_key}")

                    # Prompt for each student's score
                    for student in self.__students:
                        score = float(input(f"Enter score (0-100) for {student.first_name} {student.last_name}, ID {student.student_id} for {assignment_key} (out of 100): "))
                        while not 0 <= score <= 100:
                            print("Invalid Score, try again.")
                            score = float(input(f"Enter score (0-100) for {student.first_name} {student.last_name}, ID {student.student_id} for {assignment_key} (out of 100): "))
                        if component == "final_exam":
                            score = (score / 100) * details["weight"]
                        else:
                            score = (score / 100) * details["weights"][f"{i}"] 
                        student.record_grade(assignment_key, score)
                        print(f"Score for {assignment_key} recorded for {student.first_name} {student.last_name}.")     
        # After recording all scores, save the updated student information
        self.save_students_to_db()

    def record_programming_assignment_score(self) -> None:
        self.record_score("programming_assignment")
        
    def record_test_score(self) -> None:
        self.record_score("test")

    def record_final_exam_score(self) -> None:
        self.record_score("final_exam")
        
    def change_grade(self) -> None:
        if not self.check_student_policy(): # if there is no students or policy exit
            return  
        student_id = int(input("Enter the student's ID to change the grade: "))
         # the new score value
        new_grade = float(input(f"Enter the new score for student (out of 100): "))
        while not 0 <= new_grade <= 100:
            print("Invalid New Grade, try again.")
            new_grade = float(input(f"Enter the new score for student (out of 100): "))
        
        input_to_component = {
        'P': 'programming_assignment',
        'T': 'test',
        'F': 'final_exam'
        }

        component_input = input("Enter the type of score (P for programming_assignment, T for test, F for final_exam): ").upper()
        while component_input not in input_to_component:
            print("Invalid score type. Try again.")
            component_input = input("Enter the score type (P for programming_assignment, T for test, F for final_exam): ").upper()
        component = input_to_component[component_input]
        grade_policy = self.__grade_policy.weights()
        # search for student
        student_found = False
        for student in self.__students:
            if student.student_id == student_id:
                student_found = True
                assignment_num = int(input(f"Enter the {component} number to change the grade: "))
                while assignment_num <= 0 or assignment_num > self.__grade_policy.weights()[component]['count']:
                    print(f"Invalid {component} number. Try again")
                    assignment_num = int(input(f"Enter the {component} number to change the grade: "))
                assignment_key = f"{component} {assignment_num}"
                if component == "final_exam":
                    new_grade = (new_grade / 100) * grade_policy[f"{component}"]["weight"]
                else:
                    new_grade = (new_grade / 100) * grade_policy[f"{component}"]["weights"][f"{assignment_num}"] 
                # Update the student's grade for the specified assignment
                student.record_grade(assignment_key, new_grade)
                print(f"\n\nGrade for {assignment_key} updated for student ID {student_id}.")

        if not student_found:
            print("\nStudent not found with the entered ID.")
            return

        # Save updated student information to the database
        self.save_students_to_db()

    def calculate_final_scores(self) -> None:
        if not self.check_student_policy():
            return
        for student in self.__students:
            student.calculate_final_grade(self.__grade_policy.weights())
            # print(f"{student}\n{student.final_score}")
            student.record_grade("final_score", student.final_score)
        self.save_students_to_db()
        print("\nStudents final Grades calculated and Saved!\nEnter 'O' to display. ")

    def output_grades(self) -> None:
        if not self.check_student_policy():
            return
        print("\n============= Output for Grade data ============= ")
        print("\nChoose the sorting method for output:")
        print("1: Sort by last name")
        print("2: Sort by student ID")
        choice = input("Enter your choice (1 or 2): ")
        
        # check input
        while choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 or 2.")
            choice = input("Enter your choice (1 or 2): ")
        
        if choice == '1':
            sorted_students = sorted(self.__students, key=Student.lastname_sort)
        else:
            sorted_students = sorted(self.__students, key=Student.student_id_sort)
        
        # Output the sorted grade data
        print("\n============= Output for Grade Data =============")
        for stud in sorted_students:
            stud.show_final_grade()
        

    def save_and_quit(self) -> None:
        self.save_students_to_db()
        self.save_policy_to_db()
    
    def __str__(self) -> str:
        output = ""
        output += f"{self.__grade_policy}"
        for student in self.__students:
            output += str(student) + '\n'
        return output
    
    def display(self) -> None:
        print(self)
