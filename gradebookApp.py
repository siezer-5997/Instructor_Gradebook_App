from gradebook import Gradebook

class GradebookApp:
    def __init__(self) -> None:
        self.__gradebook = Gradebook()
        self.__gradebook.get_students_from_db()
        self.__gradebook.get_policy_from_db()
    
    def show_title(self) -> None:
        print("\nInstructor Gradebook Program")
    
    def show_menu(self) -> None:
        print("\n========= MENU ========")
        print("(S) Set up new semester: ")
        print("(A) Add student: ")
        print("(P) Record programming assignment grades: ")
        print("(T) Record test grades: ")
        print("(F) Record final exam grades: ")
        print("(C) Change a grade: ")
        print("(G) Calculate final grades: ")
        print("(O) Output grade data: ")
        print("(Q) Quit: \n")
    
    def process_command(self, command: str) -> bool:
        user_continue = True
        if command == "S":
            self.__gradebook.setup_semester()
        elif command == "A":
            self.__gradebook.add_student()
        elif command == "P":
            self.__gradebook.record_programming_assignment_score()
        elif command == "T":
            self.__gradebook.record_test_score()
        elif command == "F":
            self.__gradebook.record_final_exam_score()
        elif command == "C":
            self.__gradebook.change_grade()
        elif command == "G":
            self.__gradebook.calculate_final_scores()
        elif command == "O":
            self.__gradebook.output_grades()
        elif command == "Q":
            self.__gradebook.save_and_quit()
            user_continue = False
            print("Quiting the program. Have a nice day!")
        else:
            print("Unknown command, please try again.")
        return user_continue
        


def main():
   app = GradebookApp()
   app.show_title()
   
   user_continue = True
   while user_continue is True:
       app.show_menu()
       command = input("Enter your choice: ").upper()
       user_continue = app.process_command(command)


if __name__ == "__main__":
    main()