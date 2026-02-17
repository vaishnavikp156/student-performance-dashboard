from flask import Flask, render_template, request, redirect
import csv
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route("/")
def home():
    students = {}

    with open("marks.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students[row["Name"]] = int(row["Marks"])

    average = sum(students.values()) / len(students)
    topper = max(students, key=students.get)

        # Create graph
    names = list(students.keys())
    marks = list(students.values())

    plt.figure(figsize=(8,5))
    plt.bar(names, marks)
    plt.xlabel("Students")
    plt.ylabel("Marks")
    plt.title("Student Performance Chart")

    plt.savefig("static/chart.png")
    plt.close()


    return render_template("index.html",
                           students=students,
                           average=average,
                           topper=topper)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    marks = request.form["marks"]

    # append to csv
    with open("marks.csv", "a") as file:
        file.write(f"\n{name},{marks}")

    return redirect("/")

if __name__ == "__main__":
    app.run()
