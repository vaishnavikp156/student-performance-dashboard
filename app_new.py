from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import sqlite3
from flask import Flask, render_template, request, redirect, send_file, session
import matplotlib
matplotlib.use("Agg")

app = Flask(__name__)
app.secret_key = "studentanalyticssecret"

# ---------------- LOGIN ----------------


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            session["role"] = "admin"
            return redirect("/")

        elif username == "student" and password == "1234":
            session["user"] = username
            session["role"] = "viewer"
            return redirect("/")

        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    students = {}
    search = request.args.get("search")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT name, marks FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT name, marks FROM students")

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        students[row[0]] = row[1]

    # calculations
    average = sum(students.values()) / len(students) if students else 0
    topper = max(students, key=students.get) if students else "None"

    # grade calculation
    grades = {}
    for name, mark in students.items():
        if mark >= 90:
            grades[name] = "A"
        elif mark >= 75:
            grades[name] = "B"
        elif mark >= 60:
            grades[name] = "C"
        elif mark >= 50:
            grades[name] = "D"
        else:
            grades[name] = "F"

    # chart
    if students:
        names = list(students.keys())
        marks = list(students.values())

        plt.figure(figsize=(8, 5))
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
                           search=search,
                           grades=grades)


# ---------------- ADD ----------------
@app.route("/add", methods=["POST"])
def add_student():
    if session.get("role") != "admin":
        return redirect("/")

    name = request.form["name"]
    marks = request.form["marks"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO students(name, marks) VALUES(?, ?)", (name, marks))
    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- DELETE ----------------
@app.route("/delete", methods=["POST"])
def delete_student():
    if session.get("role") != "admin":
        return redirect("/")

    name = request.form["name"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name=?", (name,))
    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- EDIT PAGE ----------------
@app.route("/edit/<name>")
def edit_student(name):
    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT marks FROM students WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()

    marks = row[0] if row else ""

    return render_template("edit.html", name=name, marks=marks)


# ---------------- UPDATE ----------------
@app.route("/update", methods=["POST"])
def update_student():
    if session.get("role") != "admin":
        return redirect("/")

    name = request.form["name"]
    new_marks = request.form["marks"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET marks=? WHERE name=?",
                   (new_marks, name))
    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- PDF DOWNLOAD ----------------
@app.route("/download")
def download_report():
    file_path = "report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750
    c.setFont("Helvetica", 14)
    c.drawString(200, 800, "Student Performance Report")

    c.setFont("Helvetica", 11)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, marks FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        text = f"{row[0]}  -  {row[1]} marks"
        c.drawString(100, y, text)
        y -= 25

    c.save()
    return send_file(file_path, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
