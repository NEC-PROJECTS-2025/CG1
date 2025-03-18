from tkinter import *
from functionC import *
from attendanceWebcamC import *
from attendanceVideoC import *
from attendanceImageC import *
from tkinter import filedialog
import tkinter.messagebox
import re  # Import for regex validation
from PIL import ImageTk, Image

def validate_roll_no(roll_no):
    """Validate roll number format: Accepts '21471A05E5', '5E5', or '5467'."""
    pattern = r"^(21471A\d{2}[A-Z]\d|[0-9][A-Z]+[0-9]|\d+)$"
    return bool(re.match(pattern, roll_no))

def clickCapture():
    """Capture image only if roll number is valid."""
    name = enterName.get().strip()
    
    if not name:
        tkinter.messagebox.showerror("Error", "Roll number cannot be empty!")
        return

    if not validate_roll_no(name):
        tkinter.messagebox.showerror("Error", "Invalid Roll Number! Use formats:\n- '21471A05E5'\n- '5E5'\n- '5467'")
        return

    ans = tkinter.messagebox.askyesno("Confirm", f"Do you want to capture image for {name}?")
    if ans:
        captureImages(name)

def startProgramWebcam():
    tkinter.messagebox.showinfo("Info", "Please wait a while, Processing your Database Images...")
    startWebcam()

def startProgram():
    rootStart = Tk()
    rootStart.title("Choose Option")
    rootStart.geometry("500x80+300+600")
    rootStart.configure(bg="#888888")
    Button(rootStart, text="Video", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=callStartVideo).pack(side='left', padx=(40, 0))
    Button(rootStart, text="Image", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=callStartImage).pack(side='right', padx=(0, 40))

def callStartImage():
    filename = filedialog.askdirectory(initialdir=".", title="Select Folder")
    if len(filename) > 0:
        startImage(filename)
    else:
        tkinter.messagebox.showinfo("Info", "Please select an Image Folder")

def callStartVideo():
    filename = filedialog.askopenfilename(initialdir=".", title="Select Video File")
    if len(filename) > 0:
        startVideo(filename)
    else:
        tkinter.messagebox.showinfo("Info", "Please select a Video")

def openExcelOption():
    rootExcel = Tk()
    rootExcel.title("Choose Option")
    rootExcel.geometry("380x140+300+600")
    rootExcel.configure(bg="#888888")
    Button(rootExcel, text="Attendance Live Webcam", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=openExcelWebcam).pack(pady=(5, 2))
    Button(rootExcel, text="Attendance Image", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=openExcelImage).pack(pady=(0, 2))
    Button(rootExcel, text="Attendance Video", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=openExcelVideo).pack(pady=(0, 5))

# Create Main Window
root = Tk()
root.title('Facial Recognition Attendance Program')
root.attributes('-fullscreen', True)  # Set full screen mode
root.configure(background="#000000")

# Close full screen when ESC is pressed
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)

# Load Background Image
img = ImageTk.PhotoImage(Image.open('logo/nec2.jpg'))
heading = Label(root, image=img, borderwidth=0)
heading.pack(pady=20)

sub_heading = Label(root, text="Smart Attendance System", fg='#CDCDCD', bg="#80182A", font=("Cambria", 35), padx=10, pady=5)
sub_heading.pack()

spacer = Label(root, text="", bg="#000000")
spacer.pack(pady=10)

enterName = Entry(root, fg="#440D16", bg="#CDCDCD", font=15)
enterName.pack()

spacer = Label(root, text="", bg="#000000")
spacer.pack(pady=10)

Button(root, text="Add Image to Database", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=clickCapture).pack(pady=(5, 20))
Button(root, text="Start Program with Live Camera", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=startProgramWebcam).pack(pady=(0, 20))
Button(root, text="Import Image/Video", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=startProgram).pack(pady=(0, 20))
Button(root, text="Open Attendance Sheet", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=openExcelOption).pack(pady=(0, 20))
Button(root, text="Exit Fullscreen", fg="#CDCDCD", bg="#80182A", width=25, height=2, command=lambda: root.attributes('-fullscreen', False)).pack(pady=(0, 20))

root.mainloop()
