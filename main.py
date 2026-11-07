from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int

student = Student("Artyom", "двадцать")
print(student.name)
print(student.age)
print(student)