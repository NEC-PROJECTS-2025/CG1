from tkinter import *
from tkinter import messagebox
import os
import subprocess
import platform

def submit_form():
    year = year_var.get()
    semester = semester_var.get()
    branch = branch_var.get()
    section = section_var.get()
    
    if year == "Select Year" or semester == "Select Semester" or branch == "Select Branch" or section == "Select Section":
        messagebox.showwarning("Input Error", "All fields are required!")
    else:
        messagebox.showinfo("Form Submitted", "Student information submitted successfully!")

        # Define paths to main.py files for each section
        section_mapping = {
            "A": "section_A/mainA.py",
            "B": "section_B/mainB.py",
            "C": "section_C/mainC.py",
            "D": "section_D/mainD.py"
        }
        
        script_relative_path = section_mapping.get(section)
        if script_relative_path:
            script_path = os.path.join(base_path, script_relative_path)

            if os.path.exists(script_path):
                subprocess.Popen(["python", script_path], shell=True)
            else:
                messagebox.showwarning("Error", f"Script {script_path} not found!")

def cancel_form():
    root.destroy()

# Base directory
base_path = "C:/Users/HP/OneDrive/Desktop/Attendance-Face-Detection-master/Attendance-Face-Detection-master/Attendance-Face-Detection-master/"

# Check if running on Colab or a local machine
if platform.system() == "Linux":
    print("Tkinter GUI is not supported in Colab. Run this script locally.")
    exit()
else:
    root = Tk()

root.title("Student Information Form")
root.geometry("450x400")
root.configure(bg="#f0f0f0")

frame = Frame(root, padx=20, pady=20, bg="#f0f0f0")
frame.pack(expand=True)

Label(frame, text="Student Information Form", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

# Variables
year_var = StringVar(value="Select Year")
semester_var = StringVar(value="Select Semester")
branch_var = StringVar(value="Select Branch")
section_var = StringVar(value="Select Section")

# Dropdowns
Label(frame, text="Year:", bg="#f0f0f0", fg="#003366", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=5)
OptionMenu(frame, year_var, "I", "II", "III", "IV").grid(row=1, column=1, pady=5)

Label(frame, text="Semester:", bg="#f0f0f0", fg="#003366", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=5)
OptionMenu(frame, semester_var, "I", "II").grid(row=2, column=1, pady=5)

Label(frame, text="Branch:", bg="#f0f0f0", fg="#003366", font=("Arial", 12)).grid(row=3, column=0, sticky=W, pady=5)
OptionMenu(frame, branch_var, "Computer Science and Engineering", "Electronics and Communication Engineering",
           "Mechanical Engineering", "Electrical Engineering", "Civil Engineering").grid(row=3, column=1, pady=5)

Label(frame, text="Section:", bg="#f0f0f0", fg="#003366", font=("Arial", 12)).grid(row=4, column=0, sticky=W, pady=5)
OptionMenu(frame, section_var, "A", "B", "C", "D").grid(row=4, column=1, pady=5)

# Buttons
Button(frame, text="Submit", command=submit_form, bg="#28a745", fg="white", font=("Arial", 12), width=12).grid(row=5, column=0, pady=20)
Button(frame, text="Cancel", command=cancel_form, bg="#dc3545", fg="white", font=("Arial", 12), width=12).grid(row=5, column=1, pady=20)

root.mainloop()
