import csv
import matplotlib.pyplot as plt
students = {}

# Read data from CSV file
with open("marks.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["Name"]
        marks = int(row["Marks"])
        students[name] = marks

# Show all students
print("Student Marks List:\n")

for name in students:
    print(name, "scored", students[name])

# Calculate average
total = sum(students.values())
average = total / len(students)

print("\nClass Average:", average)

# Find topper
topper = max(students, key=students.get)
print("Topper is:", topper, "with", students[topper], "marks")

# Find failed students
print("\nFailed Students:")
for name, mark in students.items():
    if mark < 60:
        print(name)

print("\nDetailed Report:\n")

highest = max(students.values())
lowest = min(students.values())

print("Highest Marks:", highest)
print("Lowest Marks:", lowest)

print("\nStudent Grades:")

for name, mark in students.items():
    if mark >= 90:
        grade = "A"
    elif mark >= 75:
        grade = "B"
    elif mark >= 60:
        grade = "C"
    elif mark >= 50:
        grade = "D"
    else:
        grade = "F"

    print(name, "->", mark, "marks | Grade:", grade)


# Graph
names = list(students.keys())
marks = list(students.values())

plt.bar(names, marks)
plt.xlabel("Students")
plt.ylabel("Marks")
plt.title("Student Performance Chart")

plt.show()
