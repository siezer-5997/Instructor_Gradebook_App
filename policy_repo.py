import os
import json
from student import GradePolicy

class PolicyRepository:
    def __init__(self, filename: str) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__filename = os.path.join(script_dir, filename)
        
    def write_policy(self, policies) -> None:
        with open(self.__filename, "w") as file:
            json.dump(policies, file, indent=4)
            print("Policy saved.")
    
    def read_policy(self):
        if not os.path.exists(self.__filename):
            # If the file doesn't exist, create a new empty file and return an empty list
            print("No existing policy file found. Creating a new empty file.")
            with open(self.__filename, "w") as file:
                json.dump([], file)  # Create an empty JSON array in the file
            return None
        with open(self.__filename, 'r') as file:
            try:
                weights = json.load(file)
                print("Policy loaded successfully.")
                return weights
            except json.JSONDecodeError as e:
                print("No Grading Policy in Database. File empty.")
                return None
