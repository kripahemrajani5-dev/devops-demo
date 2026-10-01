from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)

def get_db():

    conn = sqlite3.connect("hospital.db")

    conn.row_factory = sqlite3.Row

    return conn

def create_table():

    conn = get_db()

    conn.execute("""

        CREATE TABLE IF NOT EXISTS appointments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_name TEXT NOT NULL,

            doctor TEXT NOT NULL,

            department TEXT NOT NULL,

            appointment_date TEXT NOT NULL,

            phone TEXT NOT NULL

        )

    """)

    conn.commit()

    conn.close()

@app.route("/")

def home():

    conn = get_db()

    appointments = conn.execute(

        "SELECT * FROM appointments ORDER BY appointment_date"

    ).fetchall()

    conn.close()

    return render_template(

        "index.html",

        appointments=appointments

    )

@app.route("/add", methods=["POST"])

def add_appointment():

    patient_name = request.form["patient_name"]

    doctor = request.form["doctor"]

    department = request.form["department"]

    appointment_date = request.form["appointment_date"]

    phone = request.form["phone"]

    conn = get_db()

    conn.execute("""

        INSERT INTO appointments

        (patient_name, doctor, department, appointment_date, phone)

        VALUES (?, ?, ?, ?, ?)

    """, (

        patient_name,

        doctor,

        department,

        appointment_date,

        phone

    ))

    conn.commit()

    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")

def delete_appointment(id):

    conn = get_db()

    conn.execute(

        "DELETE FROM appointments WHERE id = ?",

        (id,)

    )

    conn.commit()

    conn.close()

    return redirect("/")

if __name__ == "__main__":

    create_table()

    app.run(host="0.0.0.0", port=5000)