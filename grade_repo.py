import os
import json
from student import Student

class GradeRepository:
    def __init__(self, filename: str) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__filename = os.path.join(script_dir, filename)
        
    def write_grade(self, grades: list[str]) -> None:
        with open(self.__filename, "w") as file:
            json.dump(grades, file, indent=4)
            print("Student Grades saved.")
            
    def read_grade(self) -> list[Student]:
        if not os.path.exists(self.__filename):
            # If the file doesn't exist, create a new empty file and return an empty list
            print("No existing grades file found. Creating a new empty file.")
            with open(self.__filename, "w") as file:
                json.dump([], file)  # Create an empty JSON array in the file
            return []
        with open(self.__filename, "r") as file:
            try:
                grades = json.load(file)
                print("Students grades loaded successfully.")
                return self.make_students(grades)
            except json.JSONDecodeError as e:
                print("No Students in Database. File empty.")
                return []
    
    def make_students(self, grades) -> list[Student]:
        students : list[Student] = []
        for student in grades:
            stu_info = Student(student[0], student[1], student[2])
            grade = student[3]
            for assign_key, score in grade.items():
                stu_info.record_grade(assign_key, score)
            students.append(stu_info)
        return students
    
   