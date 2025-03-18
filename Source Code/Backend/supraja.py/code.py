import tkinter as tk
from tkinter import ttk, messagebox
from queue import Queue
import socket
import threading
from IPy import IP
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Advanced Port Scanner with Email")
        self.root.geometry("600x600")
        self.queue = Queue()
        self.open_ports = []
        self.is_scanning = False

        self.setup_ui()

    def setup_ui(self):
        # Target Input
        ttk.Label(self.root, text="Target IP/Hostname:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.target_entry = ttk.Entry(self.root, width=40)
        self.target_entry.grid(row=0, column=1, padx=10, pady=10)

        # Port Range Input
        ttk.Label(self.root, text="Port Range (e.g., 1-1024):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.port_range_entry = ttk.Entry(self.root, width=40)
        self.port_range_entry.grid(row=1, column=1, padx=10, pady=10)

        # Threads Input
        ttk.Label(self.root, text="Number of Threads:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.threads_entry = ttk.Entry(self.root, width=40)
        self.threads_entry.insert(0, "10")
        self.threads_entry.grid(row=2, column=1, padx=10, pady=10)

        # Email Input
        ttk.Label(self.root, text="Recipient Email:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = ttk.Entry(self.root, width=40)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        self.start_button = ttk.Button(self.root, text="Start Scan", command=self.start_scan)
        self.start_button.grid(row=4, column=0, padx=10, pady=10)
        self.stop_button = ttk.Button(self.root, text="Stop Scan", command=self.stop_scan, state="disabled")
        self.stop_button.grid(row=4, column=1, padx=10, pady=10)
        self.save_button = ttk.Button(self.root, text="Save Report", command=self.save_report, state="disabled")
        self.save_button.grid(row=5, column=0, padx=10, pady=10)
        self.email_button = ttk.Button(self.root, text="Send Report via Email", command=self.send_report_email, state="disabled")
        self.email_button.grid(row=5, column=1, padx=10, pady=10)

        # Results Box
        self.results_box = tk.Text(self.root, height=20, width=70)
        self.results_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.results_box.insert("1.0", "Results will appear here...\n")

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def validate_target(self, target):
        try:
            IP(target)
            return target
        except ValueError:
            return socket.gethostbyname(target)

    def scan_worker(self, target):
        while not self.queue.empty() and self.is_scanning:
            port = self.queue.get()
            if self.scan_port(target, port):
                self.open_ports.append(port)
                self.results_box.insert("end", f"Port {port} is open.\n")
                self.results_box.see("end")
            self.progress.step(1)

        # Enable buttons after scan
        self.is_scanning = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.email_button.config(state="normal")

        self.results_box.insert("end", "Scan complete.\n")
        self.results_box.insert("end", f"Open ports: {', '.join(map(str, self.open_ports)) if self.open_ports else 'None'}\n")
        self.results_box.see("end")

    def start_scan(self):
        self.results_box.delete("1.0", "end")
        self.open_ports = []
        self.is_scanning = True
        self.progress['value'] = 0

        target = self.target_entry.get().strip()
        port_range = self.port_range_entry.get().strip()
        threads = int(self.threads_entry.get().strip())

        if not target or not port_range:
            messagebox.showerror("Error", "Please provide target and port range.")
            return

        try:
            target = self.validate_target(target)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid target: {e}")
            return

        try:
            start_port, end_port = map(int, port_range.split("-"))
        except:
            messagebox.showerror("Error", "Port range must be in the format 'start-end'.")
            return

        total_ports = end_port - start_port + 1
        self.progress['maximum'] = total_ports

        for port in range(start_port, end_port + 1):
            self.queue.put(port)

        self.results_box.insert("end", f"Scanning {target} on ports {start_port}-{end_port}...\n")
        self.results_box.insert("end", f"Using {threads} threads...\n")
        self.results_box.see("end")

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        thread_list = []
        for _ in range(threads):
            thread = threading.Thread(target=self.scan_worker, args=(target,))
            thread_list.append(thread)
            thread.start()

    def stop_scan(self):
        self.is_scanning = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.results_box.insert("end", "Scan stopped by user.\n")

    def generate_report(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
        Port Scan Report
        ----------------
        Target: {self.target_entry.get().strip()}
        Open Ports: {', '.join(map(str, self.open_ports)) if self.open_ports else 'None'}
        Scan Date: {now}
        ----------------
        """

    def save_report(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"port_scan_report_{now}.txt"
        with open(filename, "w") as file:
            file.write(self.generate_report())
        messagebox.showinfo("Report Saved", f"Report saved as {filename}")

    def send_report_email(self):
        recipient_email = self.email_entry.get().strip()
        if not recipient_email:
            messagebox.showerror("Error", "Please enter a recipient email address.")
            return

        sender_email = "your_email@example.com"
        sender_password = "your_password"

        report = self.generate_report()
        try:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = f"Port Scan Report for {self.target_entry.get().strip()}"
            message.attach(MIMEText(report, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())

            messagebox.showinfo("Email Sent", f"Report successfully sent to {recipient_email}.")
        except Exception as e:
            messagebox.showerror("Email Failed", f"Failed to send email: {e}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()
