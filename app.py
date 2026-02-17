from flask import Flask, render_template, request, redirect
import csv

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def home():
    students = {}

    search = request.args.get("search")

    # read csv
    with open("marks.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            marks = int(row["Marks"])

            if search:
                if search.lower() in name.lower():
                    students[name] = marks
            else:
                students[name] = marks

    # calculations
    average = sum(students.values()) / len(students) if students else 0
    topper = max(students, key=students.get) if students else "None"

    # create chart
    if students:
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
                           topper=topper,
                           search=search)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    marks = request.form["marks"]

    with open("marks.csv", "a") as file:
        file.write(f"\n{name},{marks}")

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_student():
    name = request.form["name"]
    rows = []

    with open("marks.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Name"] != name:
                rows.append(row)

    with open("marks.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Marks"])
        writer.writeheader()
        writer.writerows(rows)

    return redirect("/")


if __name__ == "__main__":
    app.run()
