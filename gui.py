from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import mysql.connector
import os

# =========================
# MAIN WINDOW
# =========================
root = Tk()

root.title("Face Attendance System")
root.geometry("1000x700")
root.configure(bg="white")

# =========================
# TITLE
# =========================
title = Label(
    root,
    text="Face Attendance System",
    font=("Arial", 28, "bold"),
    bg="white",
    fg="darkblue"
)

title.pack(pady=20)

# =========================
# SUBJECTS
# =========================
subjects = [
    "Compiler Design",
    "Computer Networks",
    "Machine Learning",
    "Internet of Things",
    "Consumer Behavior",
    "Competitive Programming"
]

# =========================
# SUBJECT DROPDOWN
# =========================
subject_label = Label(
    root,
    text="Select Subject",
    font=("Arial", 16, "bold"),
    bg="white"
)

subject_label.pack(pady=10)

subject_var = StringVar()

subject_dropdown = ttk.Combobox(
    root,
    textvariable=subject_var,
    values=subjects,
    font=("Arial", 14),
    width=35,
    state="readonly"
)

subject_dropdown.current(0)
subject_dropdown.pack(pady=10)

# =========================
# REGISTER FACE FUNCTION
# =========================
def register_face():

    messagebox.showinfo(
        "Register Face",
        "Starting Face Registration..."
    )

    os.system("python register.py")

# =========================
# TRAIN MODEL FUNCTION
# =========================
def train_model():

    messagebox.showinfo(
        "Train Model",
        "Training Model..."
    )

    os.system("python train.py")

# =========================
# START ATTENDANCE FUNCTION
# =========================
def start_attendance():

    selected_subject = subject_var.get()

    os.environ["SUBJECT_NAME"] = selected_subject

    messagebox.showinfo(
        "Attendance",
        f"Starting Attendance for {selected_subject}"
    )

    os.system("python recognize.py")

# =========================
# VIEW ATTENDANCE FUNCTION
# =========================
def view_attendance():

    try:

        # MYSQL CONNECTION
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="860560",
            database="face_attendance"
        )

        cursor = db.cursor()

        # NEW WINDOW
        attendance_window = Toplevel(root)

        attendance_window.title("Attendance Records")
        attendance_window.geometry("1100x500")
        attendance_window.configure(bg="white")

        # TITLE
        heading = Label(
            attendance_window,
            text="Attendance Records",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="darkblue"
        )

        heading.pack(pady=10)

        # =========================
        # TABLE
        # =========================
        columns = (
            "attendance_id",
            "student_id",
            "name",
            "subject",
            "date",
            "time"
        )

        tree = ttk.Treeview(
            attendance_window,
            columns=columns,
            show='headings'
        )

        # HEADINGS
        tree.heading("attendance_id", text="Attendance ID")
        tree.heading("student_id", text="Student ID")
        tree.heading("name", text="Name")
        tree.heading("subject", text="Subject")
        tree.heading("date", text="Date")
        tree.heading("time", text="Time")

        # COLUMN WIDTHS
        tree.column("attendance_id", width=100)
        tree.column("student_id", width=100)
        tree.column("name", width=180)
        tree.column("subject", width=220)
        tree.column("date", width=120)
        tree.column("time", width=120)

        tree.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # =========================
        # FETCH ATTENDANCE
        # =========================
        query = "SELECT * FROM attendance"

        cursor.execute(query)

        records = cursor.fetchall()

        # =========================
        # INSERT DATA
        # =========================
        for row in records:
            tree.insert('', END, values=row)

        db.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

# =========================
# BUTTON FRAME
# =========================
button_frame = Frame(
    root,
    bg="white"
)

button_frame.pack(pady=30)

# =========================
# REGISTER FACE BUTTON
# =========================
register_button = Button(
    button_frame,
    text="Register Face",
    command=register_face,
    font=("Arial", 14, "bold"),
    bg="#3498db",
    fg="white",
    width=25,
    height=2
)

register_button.grid(row=0, column=0, padx=20, pady=15)

# =========================
# TRAIN MODEL BUTTON
# =========================
train_button = Button(
    button_frame,
    text="Train Model",
    command=train_model,
    font=("Arial", 14, "bold"),
    bg="#2ecc71",
    fg="white",
    width=25,
    height=2
)

train_button.grid(row=1, column=0, padx=20, pady=15)

# =========================
# START ATTENDANCE BUTTON
# =========================
attendance_button = Button(
    button_frame,
    text="Start Attendance",
    command=start_attendance,
    font=("Arial", 14, "bold"),
    bg="#9b59b6",
    fg="white",
    width=25,
    height=2
)

attendance_button.grid(row=2, column=0, padx=20, pady=15)

# =========================
# VIEW ATTENDANCE BUTTON
# =========================
view_button = Button(
    button_frame,
    text="View Attendance",
    command=view_attendance,
    font=("Arial", 14, "bold"),
    bg="#f39c12",
    fg="white",
    width=25,
    height=2
)

view_button.grid(row=3, column=0, padx=20, pady=15)

# =========================
# EXIT BUTTON
# =========================
exit_button = Button(
    button_frame,
    text="Exit",
    command=root.destroy,
    font=("Arial", 14, "bold"),
    bg="#e74c3c",
    fg="white",
    width=25,
    height=2
)

exit_button.grid(row=4, column=0, padx=20, pady=15)

# =========================
# FOOTER
# =========================
footer = Label(
    root,
    text="AI Face Recognition Attendance System",
    font=("Arial", 12),
    bg="white",
    fg="gray"
)

footer.pack(side=BOTTOM, pady=15)

# =========================
# RUN GUI
# =========================
root.mainloop()