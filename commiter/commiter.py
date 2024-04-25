import tkinter as tk
from tkinter import ttk
import time
import threading
import subprocess

class GitAutoCommitApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Git Auto Commit")
        
        self.commit_interval = 10  # Default interval in minutes
        self.repository_path = "C:\\Users\\oldma\\AppData\\Roaming\\.betacraft\\Update\\saves"
        self.running = False
        
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.master, text="Auto Commit", variable=self.checkbox_var)
        self.checkbox.grid(row=0, column=0, padx=10, pady=10)

        self.interval_label = ttk.Label(self.master, text="Commit Interval (minutes):")
        self.interval_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.interval_entry = ttk.Entry(self.master)
        self.interval_entry.grid(row=1, column=1, padx=10, pady=5)
        self.interval_entry.insert(0, self.commit_interval)
        
        self.start_button = ttk.Button(self.master, text="Start", command=self.start_auto_commit)
        self.start_button.grid(row=4, column=0, columnspan=1, padx=10, pady=5)

        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_auto_commit)
        self.stop_button.grid(row=4, column=1, columnspan=1, padx=10, pady=5)
        self.stop_button.config(state="disabled")

        self.close_button = ttk.Button(self.master, text="Exit", command=self.exit)
        self.close_button.grid(row=5, column=0, columnspan=1, padx=10, pady=5)

        # create 2 text boxes + lable
        # nr 1 is for the path to the git repo
        # nr 2 is for the commit message

        self. path_label = ttk.Label(self.master, text="Path to Git Repo:")
        self.path_label.grid(row=3, column=0, padx=10, pady=5)

        self.path_entry = ttk.Entry(self.master)
        self.path_entry.grid(row=3, column=1, columnspan=1, padx=10, pady=5)
        self.path_entry.insert(0, self.repository_path)

        self.commit_label = ttk.Label(self.master, text="Commit Message:")
        self.commit_label.grid(row=2, column=0, padx=10, pady=5)

        self.commit_entry = ttk.Entry(self.master)
        self.commit_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=5)

        

    def start_auto_commit(self):
        if not self.running:
            try:
                self.commit_interval = int(self.interval_entry.get())
                self.running = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.auto_commit_thread = threading.Thread(target=self.auto_commit)
                self.auto_commit_thread.start()
            except ValueError:
                print("Please enter a valid integer for commit interval.")
                self.interval_entry.delete(0, tk.END)
                self.interval_entry.insert(0, str(self.commit_interval))

    def stop_auto_commit(self):
        if self.running:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def auto_commit(self):
        while self.running:
            if self.checkbox_var.get():
                try:
                    self.repository_path = self.path_entry.get()
                    msg = self.commit_entry.get()
                    if (len(msg) == 0):
                        msg = "No Commit Message"
                    subprocess.run(["git", "add", "."], cwd=self.repository_path)
                    subprocess.run(["git", "commit", "-m", msg], cwd=self.repository_path)
                    subprocess.run(["git", "push"], cwd=self.repository_path)
                    print("Committed changes.")
                except Exception as e:
                    print("Error:", e)
                time.sleep(self.commit_interval * 60)
            else:
                time.sleep(1)
                print("nope")

    def exit(self):
        self.running = False
        self.master.destroy()

def main():
    root = tk.Tk()
    app = GitAutoCommitApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()