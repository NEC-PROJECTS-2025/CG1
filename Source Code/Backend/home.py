from tkinter import *
from PIL import Image, ImageTk
import subprocess
import os

def open_form():
    """Opens the Student Information Form."""
    script_path = "C:/Users/HP/OneDrive/Desktop/Attendance-Face-Detection-master/Attendance-Face-Detection-master/Attendance-Face-Detection-master/form.py"
    if os.path.exists(script_path):
        subprocess.Popen(["python", script_path])
    else:
        print("Error: form.py not found!")

def about_us():
    """Opens the About Us window."""
    about_window = Toplevel(root)
    about_window.title("About Us")
    about_window.geometry("800x600")
    
    bg_image = Image.open("about.jpg").resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = Label(about_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  

    Label(about_window, text="About Us", font=("Arial", 18, "bold"), fg="white", bg="#001F3F").pack(pady=10)
    Label(about_window, text="""The Next-Gen Attendance System is an AI-driven solution designed to enhance efficiency and accuracy in attendance management. Utilizing advanced face detection technology powered by deep learning models like YOLOv8, our system ensures real-time recognition, reducing manual errors and eliminating the possibility of proxy attendance. Traditional attendance methods often involve inefficiencies, but our solution automates the entire process, making it seamless, reliable, and highly secure.  

Our system supports multiple attendance modes, allowing users to mark their presence through live webcam detection, pre-recorded videos, or static images. This flexibility makes it suitable for diverse environments, including educational institutions, corporate offices, and large organizations. By automating attendance tracking and data storage, our solution minimizes administrative workload, enhances record-keeping, and ensures seamless integration with existing systems.  

Security and reliability are at the core of our system. The Next-Gen Attendance System incorporates anti-spoofing measures to prevent fraudulent activities such as photo-based attendance or unauthorized access. Attendance data is automatically stored in organized Excel sheets**, categorized by date and section, ensuring easy retrieval and management. With options for cloud integration, administrators can access records anytime, improving efficiency and transparency.  

Designed for scalability, the Next-Gen Attendance System adapts to different organizational needs, offering a user-friendly dashboard with real-time monitoring and analytics. Administrators can track daily and monthly attendance statistics, generate reports, and analyze trends for better decision-making. By leveraging AI, deep learning, and automation, our system revolutionizes attendance tracking, making it smarter, more secure, and highly efficient.
    """, wraplength=600, justify=LEFT, font=("Arial", 12), fg="white", bg="#001F3F").pack(pady=10)

def contact_us():
    """Opens the Contact Us window."""
    contact_window = Toplevel(root)
    contact_window.title("Contact Us")
    contact_window.geometry("800x600")
    
    bg_image = Image.open("contact.jpg").resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = Label(contact_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  
    
    Label(contact_window, text="Contact Us", font=("Arial", 18, "bold"), fg="white", bg="#001F3F").pack(pady=10)
    Label(contact_window, text="""
Name: Bogyam Indu
Email: bogyamindu9100@gmail.com
Phone: 9100584945

Name: Kongara Abhinaya
Email: abhinayakongara616@gmail.com
Phone: 9550346891

Name: Thumu Tejaswini
Email: thumutejaswini.com
Phone: 830921367
""", font=("Arial", 12), fg="white", bg="#001F3F").pack(pady=10)

# Create Main Window
root = Tk()
root.title("Home - Face Detection Attendance")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Load Background Image
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = Image.open("home.jpeg").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Display Background
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label
Label(root, text="Next-Gen Attendance System", font=("Arial", 24, "bold"), fg="white", bg="black").pack(pady=30)

# Button Styling
button_bg = "#87CEEB"
button_fg = "white"
button_font = ("Arial", 16)
button_width = 25

Button(root, text="Open Form", command=open_form, font=button_font, 
       bg=button_bg, fg=button_fg, width=button_width, relief=FLAT).pack(pady=10)

Button(root, text="About Us", command=about_us, font=button_font, 
       bg=button_bg, fg=button_fg, width=button_width, relief=FLAT).pack(pady=10)

Button(root, text="Contact Us", command=contact_us, font=button_font, 
       bg=button_bg, fg=button_fg, width=button_width, relief=FLAT).pack(pady=10)

# Exit Button to Close Fullscreen
Button(root, text="Exit", command=root.quit, font=button_font, 
       bg="red", fg="white", width=button_width, relief=FLAT).pack(pady=20)

root.mainloop()
