import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

# Database Setup
def setup_database():
    conn = sqlite3.connect('sleep_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        userid TEXT NOT NULL UNIQUE
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sleep_data (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT NOT NULL,
        sleep_duration REAL NOT NULL,
        sleep_quality INTEGER NOT NULL,
        FOREIGN KEY (username) REFERENCES users (username)
    )''')
    conn.commit()
    conn.close()

# Main Application Class
class SleepTrackerApp:
    def __init__(self, root):
        # super().__init__()
        self.root = root
        self.root.title("Healthy Sleeping Tracker")
        self.root.geometry("800x600")

        self.conn = sqlite3.connect('sleep_tracker.db')
        self.cursor = self.conn.cursor()

        self.username = None
        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.configure("TNotebook", tabposition='n')
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12), padding=5)
        self.style.configure("TEntry", font=("Helvetica", 12))

        self.notebook = ttk.Notebook(self.root)
        
        # Tabs
        self.home_tab = ttk.Frame(self.notebook)  # Home tab
        self.user_tab = ttk.Frame(self.notebook)
        self.user_tab.pack(fill='both', expand=True)
        self.track_tab = ttk.Frame(self.notebook)
        self.track_tab.pack(fill='both', expand=True)
        self.report_tab = ttk.Frame(self.notebook)
        self.suggestions_tab = ttk.Frame(self.notebook)
        self.profile_tab = ttk.Frame(self.notebook)
        self.statistics_tab = ttk.Frame(self.notebook)  # New tab for statistics
        
        self.notebook.add(self.home_tab, text='Home')  # Add Home tab to notebook
        self.notebook.add(self.user_tab, text='User Management')
        self.notebook.add(self.track_tab, text='Track Sleep')
        self.notebook.add(self.report_tab, text='Report')
        self.notebook.add(self.suggestions_tab, text='Suggestions')
        self.notebook.add(self.profile_tab, text='User Profile')
        self.notebook.add(self.statistics_tab, text='Statistics')  # Add new tab to notebook
        
        self.create_home_tab()
        self.create_user_tab()
        self.create_track_tab()
        self.create_report_tab()
        self.create_suggestions_tab()
        self.create_profile_tab()
        self.create_statistics_tab()  # Create widgets for new tab
        
        self.notebook.pack(expand=1, fill='both')

    def create_home_tab(self):
        ttk.Label(self.home_tab, text="Welcome to the Healthy Sleeping Tracker!", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(self.home_tab, text="Go to User Management", command=lambda: self.notebook.select(self.user_tab)).pack(pady=10)
        ttk.Button(self.home_tab, text="Go to Track Sleep", command=lambda: self.notebook.select(self.track_tab)).pack(pady=10)
        ttk.Button(self.home_tab, text="Go to Report", command=lambda: self.notebook.select(self.report_tab)).pack(pady=10)
        ttk.Button(self.home_tab, text="Go to Suggestions", command=lambda: self.notebook.select(self.suggestions_tab)).pack(pady=10)
        ttk.Button(self.home_tab, text="Go to User Profile", command=lambda: self.notebook.select(self.profile_tab)).pack(pady=10)
        ttk.Button(self.home_tab, text="Go to Statistics", command=lambda: self.notebook.select(self.statistics_tab)).pack(pady=10)
        self.add_back_button(self.home_tab)  # Add the back button to the Home tab
    

    def add_back_button(self, frame):
        back_button = ttk.Button(frame, text="Main Screen", command=self.go_back)
        back_button.pack(pady=10)

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        start_app = StartScreen(root)
        root.mainloop()

    def create_user_tab(self):
        
        ttk.Label(self.user_tab, text="Name:").grid(row=0, column=15, padx=10, pady=10, sticky='e')
        self.user_name = ttk.Entry(self.user_tab)
        self.user_name.grid(row=0, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.user_tab, text="Age:").grid(row=1, column=15, padx=10, pady=10, sticky='e')
        self.user_age = ttk.Entry(self.user_tab)
        self.user_age.grid(row=1, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.user_tab, text="Username:").grid(row=2, column=15, padx=10, pady=10, sticky='e')
        self.user_username = ttk.Entry(self.user_tab)
        self.user_username.grid(row=2, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.user_tab, text="User ID:").grid(row=3, column=15, padx=10, pady=10, sticky='e')
        self.user_userid = ttk.Entry(self.user_tab)
        self.user_userid.grid(row=3, column=20, padx=10, pady=10, sticky='w')

        ttk.Button(self.user_tab, text="Add User", command=self.add_user).grid(row=4, column=20, columnspan=2, pady=10, sticky='nsew')
        ttk.Button(self.user_tab, text="Load User Profile", command=self.load_user_profile).grid(row=5, column=20, columnspan=2, pady=10, sticky='nsew')

    def create_track_tab(self):
        ttk.Label(self.track_tab, text="User ID:").grid(row=0, column=15, padx=10, pady=10, sticky='e')
        self.track_userid = ttk.Entry(self.track_tab)
        self.track_userid.grid(row=0, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.track_tab, text="Date (YYYY-MM-DD):").grid(row=1, column=15, padx=10, pady=10, sticky='e')
        self.track_date = DateEntry(self.track_tab, date_pattern='yyyy-mm-dd')
        self.track_date.grid(row=1, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.track_tab, text="Sleep Duration (hours):").grid(row=2, column=15, padx=10, pady=10, sticky='e')
        self.track_duration = ttk.Entry(self.track_tab)
        self.track_duration.grid(row=2, column=20, padx=10, pady=10, sticky='w')

        ttk.Label(self.track_tab, text="Sleep Quality (1-5):").grid(row=3, column=15, padx=10, pady=10, sticky='e')
        self.track_quality = ttk.Entry(self.track_tab)
        self.track_quality.grid(row=3, column=20, padx=10, pady=10, sticky='w')

        ttk.Button(self.track_tab, text="Track Sleep", command=self.track_sleep).grid(row=4, column=20, columnspan=2, pady=10, sticky='nsew')

    def create_report_tab(self):
        ttk.Label(self.report_tab, text="User ID:").pack(pady=10)
        self.report_userid = ttk.Entry(self.report_tab)
        self.report_userid.pack(pady=10)

        ttk.Button(self.report_tab, text="Generate Report", command=self.generate_report).pack(pady=10)
        self.report_text = tk.Text(self.report_tab)
        self.report_text.pack(expand=1, fill='both')

    def create_suggestions_tab(self):
        ttk.Label(self.suggestions_tab, text="User ID:").pack(pady=10)
        self.suggestions_userid = ttk.Entry(self.suggestions_tab)
        self.suggestions_userid.pack(pady=10)

        self.suggestions_text = tk.Text(self.suggestions_tab)
        self.suggestions_text.pack(expand=1, fill='both')
        ttk.Button(self.suggestions_tab, text="Get Suggestions", command=self.generate_suggestions).pack(pady=10)

    def create_profile_tab(self):
        ttk.Label(self.profile_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.profile_name = ttk.Entry(self.profile_tab)
        self.profile_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.profile_tab, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        self.profile_age = ttk.Entry(self.profile_tab)
        self.profile_age.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.profile_tab, text="Username:").grid(row=2, column=0, padx=10, pady=10)
        self.profile_username = ttk.Entry(self.profile_tab)
        self.profile_username.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.profile_tab, text="User ID:").grid(row=3, column=0, padx=10, pady=10)
        self.profile_userid = ttk.Entry(self.profile_tab)
        self.profile_userid.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(self.profile_tab, text="Update Profile", command=self.update_profile).grid(row=4, column=0, columnspan=2, pady=10)

    def create_statistics_tab(self):
        ttk.Label(self.statistics_tab, text="User ID:").pack(pady=10)
        self.statistics_userid = ttk.Entry(self.statistics_tab)
        self.statistics_userid.pack(pady=10)

        ttk.Button(self.statistics_tab, text="Show Statistics", command=self.show_statistics).pack(pady=10)
        self.statistics_canvas = None

    def add_user(self):
        name = self.user_name.get()
        age = self.user_age.get()
        username = self.user_username.get()
        userid = self.user_userid.get()

        if not name or not age or not username or not userid:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be an integer.")
            return

        try:
            self.cursor.execute("INSERT INTO users (name, age, username, userid) VALUES (?, ?, ?, ?)", 
                                (name, age, username, userid))
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully.")
            self.user_name.delete(0, tk.END)
            self.user_age.delete(0, tk.END)
            self.user_username.delete(0, tk.END)
            self.user_userid.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or User ID already exists.")

    def load_user_profile(self):
        username = self.user_username.get()
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user:
            self.profile_name.delete(0, tk.END)
            self.profile_name.insert(0, user[1])
            self.profile_age.delete(0, tk.END)
            self.profile_age.insert(0, user[2])
            self.profile_username.delete(0, tk.END)
            self.profile_username.insert(0, user[0])
            self.profile_userid.delete(0, tk.END)
            self.profile_userid.insert(0, user[3])
            self.username = username            
        else:
            messagebox.showerror("Error", "User not found.")

    def update_profile(self):
        if not self.username:
            messagebox.showwarning("Input Error", "No user loaded to update profile.")
            return

        name = self.profile_name.get()
        age = self.profile_age.get()
        username = self.profile_username.get()
        userid = self.profile_userid.get()

        if not name or not age or not username or not userid:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be an integer.")
            return

        try:
            self.cursor.execute("UPDATE users SET name=?, age=?, username=?, userid=? WHERE username=?", 
                                (name, age, username, userid, self.username))
            self.conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully.")
            self.username = username
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or User ID already exists.")

    def validate_userid(self, userid):
        self.cursor.execute("SELECT username FROM users WHERE userid=?", (userid,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def track_sleep(self):
        userid = self.track_userid.get()
        date = self.track_date.get()
        sleep_duration = self.track_duration.get()
        sleep_quality = self.track_quality.get()

        if not userid or not date or not sleep_duration or not sleep_quality:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        username = self.validate_userid(userid)
        if not username:
            messagebox.showwarning("Input Error", "Invalid User ID.")
            return

        try:
            sleep_duration = float(sleep_duration)
            sleep_quality = int(sleep_quality)
        except ValueError:
            messagebox.showwarning("Input Error", "Sleep duration must be a number and sleep quality must be an integer.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        self.cursor.execute("INSERT INTO sleep_data (username, date, sleep_duration, sleep_quality) VALUES (?, ?, ?, ?)",
                            (username, date, sleep_duration, sleep_quality))
        self.conn.commit()
        messagebox.showinfo("Success", "Sleep data tracked successfully.")

    def generate_report(self):
        userid = self.report_userid.get()
        username = self.validate_userid(userid)
        if not username:
            messagebox.showwarning("Input Error", "Invalid User ID.")
            return

        self.cursor.execute("SELECT name, age FROM users WHERE username=?", (username,))
        user_info = self.cursor.fetchone()
        if not user_info:
            messagebox.showwarning("Database Error", "User information not found.")
            return

        name, age = user_info

        self.cursor.execute("SELECT date, sleep_duration, sleep_quality FROM sleep_data WHERE username=?", (username,))
        records = self.cursor.fetchall()

        if not records:
            self.report_text.insert(tk.END, "No sleep data found.\n")
            return

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, f"Sleep Report for {name} (Age: {age}), User ID: {userid}\n")
        self.report_text.insert(tk.END, "Date\tDuration\tQuality\n")
        self.report_text.insert(tk.END, "-"*30 + "\n")
        for record in records:
            self.report_text.insert(tk.END, f"{record[0]}\t{record[1]}\t{record[2]}\n")

    def generate_suggestions(self):
        userid = self.suggestions_userid.get()
        username = self.validate_userid(userid)
        if not username:
            messagebox.showwarning("Input Error", "Invalid User ID.")
            return

        self.cursor.execute("SELECT AVG(sleep_duration), AVG(sleep_quality) FROM sleep_data WHERE username=?", (username,))
        avg_duration, avg_quality = self.cursor.fetchone()

        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(tk.END, "Sleep Hygiene Suggestions\n")
        self.suggestions_text.insert(tk.END, "-"*30 + "\n")
        
        if avg_duration is not None:
            self.suggestions_text.insert(tk.END, f"Average Sleep Duration: {avg_duration:.2f} hours\n")
            if avg_duration < 7:
                self.suggestions_text.insert(tk.END, "Try to get at least 7-8 hours of sleep per night.\n")
            elif avg_duration > 9:
                self.suggestions_text.insert(tk.END, "More than 9 hours of sleep might indicate oversleeping. Aim for 7-8 hours.\n")
            else:
                self.suggestions_text.insert(tk.END, "Your sleep duration is within the recommended range.\n")

        if avg_quality is not None:
            self.suggestions_text.insert(tk.END, f"Average Sleep Quality: {avg_quality:.2f}\n")
            if avg_quality < 3:
                self.suggestions_text.insert(tk.END, "Consider improving your sleep environment (e.g., reduce noise, lower room temperature).\n")
            else:
                self.suggestions_text.insert(tk.END, "Your sleep quality seems to be good.\n")

    def show_statistics(self):
        userid = self.statistics_userid.get()
        username = self.validate_userid(userid)
        if not username:
            messagebox.showwarning("Input Error", "Invalid User ID.")
            return

        self.cursor.execute("SELECT date, sleep_duration, sleep_quality FROM sleep_data WHERE username=?", (username,))
        records = self.cursor.fetchall()

        if not records:
            messagebox.showwarning("No Data", "No sleep data found for statistics.")
            return

        dates = [record[0] for record in records]
        durations = [record[1] for record in records]
        qualities = [record[2] for record in records]

        if self.statistics_canvas:
            self.statistics_canvas.get_tk_widget().destroy()

        # Data visualization
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        ax[0].plot(dates, durations, label="Duration (hours)", color="blue")
        ax[0].set_title("Sleep Duration Over Time")
        ax[0].set_ylabel("Hours")
        ax[0].legend()

        ax[1].plot(dates, qualities, label="Quality (1-5)", color="green")
        ax[1].set_title("Sleep Quality Over Time")
        ax[1].set_ylabel("Quality")
        ax[1].legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        self.statistics_canvas = FigureCanvasTkAgg(fig, master=self.statistics_tab)
        self.statistics_canvas.draw()
        self.statistics_canvas.get_tk_widget().pack(expand=1, fill='both')


class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker Application - Start")
        self.root.geometry("500x400")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 16))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.root, text="Welcome to Fitness Tracker Application")
        label.pack(pady=50)

        start_button = ttk.Button(self.root, text="Body Measurement Tracker", command=self.start_body_tracking)
        start_button.pack(pady=10)

        start_button1 = ttk.Button(self.root, text="Healthy Sleep Tracker", command=self.start_sleep_tracking)
        start_button1.pack(pady=10)


    def start_body_tracking(self):
        self.root.destroy()
        root = tk.Tk()
        app = BodyMeasurementTrackerApp(root)
        root.mainloop()

    def start_sleep_tracking(self):
        self.root.destroy()
        root = tk.Tk()
        app = SleepTrackerApp(root)
        root.mainloop()


# Database initialization functions

# Database initialization functions
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS body_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userkeyid INTEGER,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        weight REAL ,
                        height REAL NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS measurements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        weight REAL NOT NULL,
                        bmi REAL,
                        body_fat REAL,
                        muscle_mass REAL,
                        waist_circumference REAL,
                        FOREIGN KEY(user_id) REFERENCES body_users(userkeyid)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        preference TEXT NOT NULL,
                        value TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('body_measurement_tracker.db')

initialize_db()
setup_database()

class BodyMeasurementTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Measurement Tracker")
        self.root.geometry("900x700")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TFrame', padding=10)
        self.style.configure('TNotebook', padding=10)
        self.style.configure('TNotebook.Tab', font=('Helvetica', 12))

        self.units = self.load_units()
        self.create_widgets()

    def load_units(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE preference='units'")
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return 'metric'

    def save_units(self, units):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO settings (preference, value) VALUES ('units', ?)", (units,))
        conn.commit()
        conn.close()
        self.units = units
        messagebox.showinfo("Success", "Preferences saved successfully")
        self.switch_tab(0)  # Switch to Home tab

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.pack(fill='both', expand=True)

        self.add_user_frame = ttk.Frame(self.notebook)
        self.add_user_frame.pack(fill='both', expand=True)

        self.log_measurement_frame = ttk.Frame(self.notebook)
        self.log_measurement_frame.pack(fill='both', expand=True)

        self.view_measurements_frame = ttk.Frame(self.notebook)
        self.view_measurements_frame.pack(fill='both', expand=True)

        self.generate_report_frame = ttk.Frame(self.notebook)
        self.generate_report_frame.pack(fill='both', expand=True)

        self.settings_frame = ttk.Frame(self.notebook)
        self.settings_frame.pack(fill='both', expand=True)

        self.notebook.add(self.main_frame, text='Home')
        self.notebook.add(self.add_user_frame, text='Add User')
        self.notebook.add(self.log_measurement_frame, text='Log Measurement')
        self.notebook.add(self.view_measurements_frame, text='View Measurements')
        self.notebook.add(self.generate_report_frame, text='Generate Report')
        self.notebook.add(self.settings_frame, text='Settings')

        self.create_home_tab()
        self.create_add_user_tab()
        self.create_log_measurement_tab()
        self.create_view_measurements_tab()
        self.create_generate_report_tab()
        self.create_settings_tab()

    def create_home_tab(self):
        label = ttk.Label(self.main_frame, text="Welcome to Body Measurement Tracker", font=("Helvetica", 16))
        label.pack(pady=20)

        self.add_user_button = ttk.Button(self.main_frame, text="Add User", command=lambda: self.switch_tab(1))
        self.add_user_button.pack(pady=10)

        self.log_measurement_button = ttk.Button(self.main_frame, text="Log Measurement", command=lambda: self.switch_tab(2))
        self.log_measurement_button.pack(pady=10)

        self.view_measurements_button = ttk.Button(self.main_frame, text="View Measurements", command=lambda: self.switch_tab(3))
        self.view_measurements_button.pack(pady=10)

        self.generate_report_button = ttk.Button(self.main_frame, text="Generate Report", command=lambda: self.switch_tab(4))
        self.generate_report_button.pack(pady=10)

        self.add_back_button(self.main_frame)  # Add the back button to the Home tab
        

    def switch_tab(self, tab_index):
        self.notebook.select(tab_index)

    def add_back_button(self, frame):
        back_button = ttk.Button(frame, text="Main Screen", command=self.go_back)
        back_button.pack(pady=10)

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        start_app = StartScreen(root)
        root.mainloop()

    def create_add_user_tab(self):
        frame = self.add_user_frame

        ttk.Label(frame, text="Name").pack(pady=5)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.pack(pady=5)

        ttk.Label(frame, text="Age").pack(pady=5)
        self.age_entry = ttk.Entry(frame)
        self.age_entry.pack(pady=5)

        if self.units == 'metric':
            weight_label = "Weight (kg)"
        else: 
            weight_label = "Weight (lbs)"
        ttk.Label(frame, text=weight_label).pack(pady=5)
        self.weight_entry = ttk.Entry(frame)
        self.weight_entry.pack(pady=5)

        height_label = "Height (cm)" if self.units == 'metric' else "Height (in)"
        ttk.Label(frame, text=height_label).pack(pady=5)
        self.height_entry = ttk.Entry(frame)
        self.height_entry.pack(pady=5)

        ttk.Label(frame, text="User ID").pack(pady=5)
        self.user_id_entry = ttk.Entry(frame)
        self.user_id_entry.pack(pady=5)

        ttk.Button(frame, text="Add User", command=self.save_user).pack(pady=20)
        # self.add_back_button(frame)  # Add the back button

    def save_user(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        weight = int(self.age_entry.get())
        height = int(self.age_entry.get())

        # # Check if weight and height strings are empty
        # if weight == '' or height == '':
        #     messagebox.showerror("Error", "Please enter weight and height.")
        #     return
        user_id = self.user_id_entry.get()
        user_id = 12

        if self.units == 'imperial':
            weight = float(weight) / 2.205  # Convert lbs to kg
            height = float(height) * 2.54   # Convert inches to cm

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO body_users (userkeyid, name, age, weight, height) VALUES (?, ?, ?, ?, ?)', 
                    (user_id, name, age, weight, height))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User added successfully")


    def create_log_measurement_tab(self):
        frame = self.log_measurement_frame

        ttk.Label(frame, text="User ID").pack(pady=5)
        self.user_id_entry = ttk.Entry(frame)
        self.user_id_entry.pack(pady=5)

        ttk.Label(frame, text="Date").pack(pady=5)
        self.date_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)

        weight_label = "Weight (kg)" if self.units == 'metric' else "Weight (lbs)"
        ttk.Label(frame, text=weight_label).pack(pady=5)
        self.weight_entry = ttk.Entry(frame)
        self.weight_entry.pack(pady=5)

        height_label = "Height (cm)" if self.units == 'metric' else "Height (in)"
        ttk.Label(frame, text=height_label).pack(pady=5)
        self.height_entry = ttk.Entry(frame)
        self.height_entry.pack(pady=5)

        ttk.Label(frame, text="Body Fat (%)").pack(pady=5)
        self.body_fat_entry = ttk.Entry(frame)
        self.body_fat_entry.pack(pady=5)

        ttk.Label(frame, text="Muscle Mass (%)").pack(pady=5)
        self.muscle_mass_entry = ttk.Entry(frame)
        self.muscle_mass_entry.pack(pady=5)

        waist_label = "Waist Circumference (cm)" if self.units == 'metric' else "Waist Circumference (in)"
        ttk.Label(frame, text=waist_label).pack(pady=5)
        self.waist_circumference_entry = ttk.Entry(frame)
        self.waist_circumference_entry.pack(pady=5)

        ttk.Button(frame, text="Log Measurement", command=self.save_measurement).pack(pady=20)
        # self.add_back_button(frame)  # Add the back button

    def save_measurement(self):
        user_id = self.user_id_entry.get()
        date = self.date_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        body_fat = self.body_fat_entry.get()
        muscle_mass = self.muscle_mass_entry.get()
        waist_circumference = self.waist_circumference_entry.get()

        if not weight or not height: #zuric1234.
            messagebox.showerror("Error", "Please enter both weight and height.")
            return

        if self.units == 'imperial':
            weight = float(weight) / 2.205  # Convert lbs to kg
            height = float(height) * 2.54   # Convert inches to cm

        weight = float(weight)
        height = float(height) / 100  # Convert cm to meters for BMI calculation
        bmi = weight / (height ** 2)  # Calculate BMI

        if body_fat:
            body_fat = float(body_fat)
        else:
            body_fat = None

        if muscle_mass:
            muscle_mass = float(muscle_mass)
        else:
            muscle_mass = None

        if waist_circumference:
            waist_circumference = float(waist_circumference)
        else:
            waist_circumference = None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO measurements (user_id, date, weight, bmi, body_fat, muscle_mass, waist_circumference) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (user_id, date, weight, bmi, body_fat, muscle_mass, waist_circumference))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Measurement logged successfully")

    def create_view_measurements_tab(self):
        frame = self.view_measurements_frame

        ttk.Label(frame, text="User ID").pack(pady=5)
        self.view_user_id_entry = ttk.Entry(frame)
        self.view_user_id_entry.pack(pady=5)

        ttk.Button(frame, text="View Measurements", command=self.view_measurements).pack(pady=20)

        self.measurements_tree = ttk.Treeview(frame, columns=("Date", "Weight", "BMI", "Body Fat", "Muscle Mass", "Waist Circumference"), show='headings')
        self.measurements_tree.heading("Date", text="Date")
        self.measurements_tree.heading("Weight", text="Weight (kg)")
        self.measurements_tree.heading("BMI", text="BMI")
        self.measurements_tree.heading("Body Fat", text="Body Fat (%)")
        self.measurements_tree.heading("Muscle Mass", text="Muscle Mass (%)")
        self.measurements_tree.heading("Waist Circumference", text="Waist Circumference (cm)")

        self.measurements_tree.pack(fill='both', expand=True)
        # self.add_back_button(frame)  # Add the back button

    def view_measurements(self):
        user_id = self.view_user_id_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT date, weight, bmi, body_fat, muscle_mass, waist_circumference FROM measurements WHERE user_id=?', (user_id,))
        measurements = cursor.fetchall()
        conn.close()

        for row in self.measurements_tree.get_children():
            self.measurements_tree.delete(row)

        for measurement in measurements:
            self.measurements_tree.insert("", "end", values=measurement)

    def create_generate_report_tab(self):
        frame = self.generate_report_frame

        ttk.Label(frame, text="User ID").pack(pady=5)
        self.report_user_id_entry = ttk.Entry(frame)
        self.report_user_id_entry.pack(pady=5)

        ttk.Label(frame, text="Start Date").pack(pady=5)
        self.start_date_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack(pady=5)

        ttk.Label(frame, text="End Date").pack(pady=5)
        self.end_date_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        self.end_date_entry.pack(pady=5)

        ttk.Button(frame, text="Generate Report", command=self.generate_report).pack(pady=20)
        # self.add_back_button(frame)  # Add the back button

    def generate_report(self):
        user_id = self.report_user_id_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT date, weight, bmi, body_fat, muscle_mass, waist_circumference FROM measurements WHERE user_id=? AND date BETWEEN ? AND ?', 
                       (user_id, start_date, end_date))
        measurements = cursor.fetchall()
        conn.close()

        dates = [measurement[0] for measurement in measurements]
        weights = [measurement[1] for measurement in measurements]
        bmis = [measurement[2] for measurement in measurements]
        body_fats = [measurement[3] for measurement in measurements]
        muscle_masses = [measurement[4] for measurement in measurements]
        waist_circumferences = [measurement[5] for measurement in measurements]

        plt.figure(figsize=(10, 6))

        plt.subplot(2, 3, 1)
        plt.plot(dates, weights, marker='o')
        plt.title('Weight')
        plt.xlabel('Date')
        plt.ylabel('Weight (kg)')

        plt.subplot(2, 3, 2)
        plt.plot(dates, bmis, marker='o')
        plt.title('BMI')
        plt.xlabel('Date')
        plt.ylabel('BMI')

        plt.subplot(2, 3, 3)
        plt.plot(dates, body_fats, marker='o')
        plt.title('Body Fat (%)')
        plt.xlabel('Date')
        plt.ylabel('Body Fat (%)')

        plt.subplot(2, 3, 4)
        plt.plot(dates, muscle_masses, marker='o')
        plt.title('Muscle Mass (%)')
        plt.xlabel('Date')
        plt.ylabel('Muscle Mass (%)')

        plt.subplot(2, 3, 5)
        plt.plot(dates, waist_circumferences, marker='o')
        plt.title('Waist Circumference (cm)')
        plt.xlabel('Date')
        plt.ylabel('Waist Circumference (cm)')

        plt.tight_layout()
        plt.show()

    def create_settings_tab(self):
        frame = self.settings_frame

        ttk.Label(frame, text="Units").pack(pady=5)
        self.units_var = tk.StringVar(value=self.units)
        ttk.Radiobutton(frame, text="Metric (kg, cm)", variable=self.units_var, value="metric").pack(pady=5)
        ttk.Radiobutton(frame, text="Imperial (lbs, in)", variable=self.units_var, value="imperial").pack(pady=5)

        ttk.Button(frame, text="Save Preferences", command=lambda: self.save_units(self.units_var.get())).pack(pady=20)
        # self.add_back_button(frame)  # Add the back button


if __name__ == "__main__":
    start_root = tk.Tk()
    start_app = StartScreen(start_root)
    start_root.mainloop()
