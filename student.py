import json
import os


class Student:
    def __init__(self, student_id, first_name, last_name) -> None:
        self.__student_id = student_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__final_score = 0
        self.__grades : dict[str, float] = {}

    #getters for student
    @property
    def student_id(self):
        return self.__student_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name
    
    @property
    def final_score(self):
        return self.__final_score

    # function to reset student grade
    def reset_grade(self) -> None:
        self.__grades = {}
    
    def lastname_sort(self) -> str:
        return self.last_name
    
    def student_id_sort(self) -> str:
        return self.student_id
    
    def record_grade(self, assignment_key: str, score: float) -> None:
        self.__grades[assignment_key] = score
    
    def convert_score_to_letter(self) -> str:
        if self.__final_score >= 90:
            return 'A'
        elif self.__final_score >= 80:
            return 'B'
        elif self.__final_score >= 70:
            return 'C'
        elif self.__final_score >= 60:
            return 'D'
        else:
            return 'F'
    
    def show_final_grade(self) -> None:
        print(self)
        print(f"Final Score: {self.__final_score}")
        print(f"Grade: {self.convert_score_to_letter()}\n")
        
    def calculate_final_grade(self, grade_policy) -> None:
        # Calculate based on grade_policy weights
        final_grade = 0
        total_weights = 0
        
        for key, component in grade_policy.items():
            if key == 'final_exam' and component['count'] > 0:
                if f"{key} 1" in self.__grades:  # Checking if final exam score is recorded
                    final_grade += self.__grades[f"{key} 1"]
                    total_weights += component['weight']
            else:
                # Handle programming assignments and tests, which have multiple parts
                for part_key, part_weight in component['weights'].items():
                    specific_key = f"{key} {part_key}" 
                    if specific_key in self.__grades:  # Checking if this particular score is recorded
                        final_grade += self.__grades[specific_key]
                        total_weights += part_weight
        
        # Normalize the final grade if the total weight collected is less than 100%
        if total_weights > 0:
            final_grade = (final_grade / total_weights) * 100
            final_grade = round(final_grade, 2)
        self.__final_score = final_grade
        
    def conv_to_list(self) -> list[str]:
        st = []
        st.append(self.__student_id)
        st.append(self.__first_name)
        st.append(self.__last_name)
        st.append(self.__grades)
        return st
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Student):
            return __value.__student_id == self.__student_id
        else:
            return False
    
    def __str__(self) -> str:
        return f"Student ID = {self.__student_id}, name = {self.__first_name} {self.__last_name}"
    
    def display(self) -> None:
        print(self)

class GradePolicy:
    def __init__(self, weights) -> None:
        self.__weights = weights


    def weights(self):
        return self.__weights
    
    def __str__(self) -> str:
        output = ""
        for key, value in self.__weights.items():
            output +=  f"{key}: "
            output += f"{value}\n"
        return output
    
    def display(self) -> None:
        print(self)
