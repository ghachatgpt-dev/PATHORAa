import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from tkinter import filedialog

# PATHFINDER - Student Career Guidance Application
# Install PDF support with: pip install reportlab

DB_NAME = "pathfinder.db"
PURPLE = "#6941C6"
DARK = "#292044"
BG = "#F4F1FB"
WHITE = "#FFFFFF"
GREEN = "#27834A"

# Each career has keywords used by the matching engine.
CAREERS = [
    ("Software Developer", "Technology", "Creates websites, applications and software.", "Python, JavaScript, databases, problem solving", ["technology", "computers", "mathematics"], ["coding", "problem solving", "logical thinking"], ["gaming", "coding", "building projects"], ["creativity", "analytical thinking", "patience"]),
    ("Data Scientist", "Technology", "Analyses data to find patterns and support decisions.", "Python, statistics, SQL, data visualisation", ["technology", "mathematics", "science"], ["coding", "research", "analytical thinking"], ["coding", "puzzles", "experiments"], ["logical thinking", "curiosity", "patience"]),
    ("Cybersecurity Analyst", "Technology", "Protects computer systems, networks and information.", "Networking, security tools, Python, risk analysis", ["technology", "computers", "security"], ["problem solving", "technical skills", "research"], ["gaming", "coding", "puzzles"], ["curiosity", "patience", "attention to detail"]),
    ("Web Designer", "Technology", "Plans the look and experience of websites.", "HTML, CSS, user experience, visual design", ["technology", "art", "design"], ["design", "coding", "creativity"], ["designing", "drawing", "editing"], ["creativity", "imagination", "attention to detail"]),
    ("AI / Machine Learning Engineer", "Technology", "Builds systems that learn from data.", "Python, mathematics, statistics, machine learning", ["technology", "mathematics", "science"], ["coding", "research", "problem solving"], ["coding", "puzzles", "experiments"], ["curiosity", "analytical thinking", "patience"]),
    ("Game Developer", "Technology", "Creates computer and mobile games.", "Programming, game engines, storytelling, design", ["technology", "computers", "art"], ["coding", "design", "problem solving"], ["gaming", "coding", "drawing"], ["creativity", "imagination", "patience"]),
    ("IT Support Specialist", "Technology", "Helps people solve computer and network problems.", "Computer systems, troubleshooting, communication", ["technology", "computers"], ["communication", "problem solving", "technical skills"], ["gaming", "building projects"], ["patience", "helpfulness", "responsibility"]),
    ("Network Engineer", "Technology", "Builds and maintains computer networks.", "Networking, cybersecurity, troubleshooting", ["technology", "computers", "physics"], ["technical skills", "problem solving", "logical thinking"], ["building projects", "gaming"], ["analytical thinking", "patience", "attention to detail"]),
    ("Doctor", "Health & Medicine", "Diagnoses illnesses and treats patients.", "Biology, chemistry, communication, clinical skills", ["biology", "science", "health"], ["research", "communication", "problem solving"], ["reading", "volunteering", "helping people"], ["compassion", "patience", "responsibility"]),
    ("Nurse", "Health & Medicine", "Provides patient care and supports medical teams.", "Biology, patient care, communication, teamwork", ["biology", "science", "health"], ["communication", "teamwork", "organisation"], ["volunteering", "helping people"], ["compassion", "patience", "responsibility"]),
    ("Pharmacist", "Health & Medicine", "Prepares and advises on the safe use of medicines.", "Chemistry, biology, accuracy, communication", ["chemistry", "biology", "health"], ["research", "communication", "attention to detail"], ["reading", "experiments", "helping people"], ["responsibility", "patience", "analytical thinking"]),
    ("Dentist", "Health & Medicine", "Prevents and treats problems involving teeth and gums.", "Biology, chemistry, precision, communication", ["biology", "science", "health"], ["technical skills", "communication", "problem solving"], ["reading", "helping people"], ["patience", "attention to detail", "responsibility"]),
    ("Physiotherapist", "Health & Medicine", "Helps people improve movement and physical function.", "Biology, anatomy, coaching, communication", ["biology", "health", "sports"], ["communication", "problem solving", "teaching"], ["sports", "helping people", "volunteering"], ["compassion", "patience", "encouragement"]),
    ("Medical Laboratory Scientist", "Health & Medicine", "Tests samples to help diagnose and monitor disease.", "Biology, chemistry, laboratory methods, accuracy", ["biology", "chemistry", "science"], ["research", "technical skills", "attention to detail"], ["experiments", "reading"], ["curiosity", "patience", "analytical thinking"]),
    ("Nutritionist", "Health & Medicine", "Advises people on food, diet and healthy living.", "Biology, nutrition, communication, research", ["biology", "health", "food"], ["communication", "research", "teaching"], ["cooking", "reading", "helping people"], ["compassion", "curiosity", "patience"]),
    ("Civil Engineer", "Engineering", "Designs roads, bridges, buildings and infrastructure.", "Mathematics, physics, CAD, project management", ["technology", "physics", "mathematics"], ["design", "problem solving", "technical skills"], ["building", "designing", "experiments"], ["analytical thinking", "creativity", "responsibility"]),
    ("Mechanical Engineer", "Engineering", "Designs and improves machines and mechanical systems.", "Mathematics, physics, CAD, mechanics", ["technology", "physics", "mathematics"], ["design", "problem solving", "technical skills"], ["building", "robotics", "experiments"], ["curiosity", "analytical thinking", "creativity"]),
    ("Electrical Engineer", "Engineering", "Works with electrical equipment and power systems.", "Physics, mathematics, circuits, programming", ["technology", "physics", "mathematics"], ["technical skills", "problem solving", "logical thinking"], ["robotics", "building", "experiments"], ["analytical thinking", "patience", "curiosity"]),
    ("Robotics Engineer", "Engineering", "Designs and builds robots and automated systems.", "Programming, electronics, mechanics, mathematics", ["technology", "physics", "mathematics"], ["coding", "design", "problem solving"], ["robotics", "building", "gaming"], ["creativity", "curiosity", "analytical thinking"]),
    ("Aerospace Engineer", "Engineering", "Designs aircraft, spacecraft and flight systems.", "Physics, mathematics, engineering design", ["technology", "physics", "mathematics"], ["technical skills", "design", "problem solving"], ["building", "experiments", "reading"], ["curiosity", "analytical thinking", "discipline"]),
    ("Architect", "Design & Creative Arts", "Plans and designs buildings and spaces.", "Drawing, mathematics, CAD, design principles", ["art", "design", "mathematics"], ["drawing", "design", "problem solving"], ["drawing", "building", "designing"], ["creativity", "imagination", "attention to detail"]),
    ("Graphic Designer", "Design & Creative Arts", "Creates visual content for brands and communication.", "Illustration, typography, colour theory, design software", ["art", "design", "creativity"], ["drawing", "design", "communication"], ["photography", "drawing", "editing"], ["creativity", "imagination", "attention to detail"]),
    ("Animator", "Design & Creative Arts", "Creates moving images for films, games and media.", "Animation software, drawing, storytelling", ["art", "design", "technology"], ["drawing", "design", "creativity"], ["gaming", "drawing", "editing"], ["imagination", "creativity", "patience"]),
    ("Fashion Designer", "Design & Creative Arts", "Designs clothing, accessories and fashion collections.", "Fashion illustration, textiles, sewing, trend research", ["art", "design", "fashion"], ["drawing", "design", "creativity"], ["designing", "drawing", "sewing"], ["creativity", "confidence", "attention to detail"]),
    ("Photographer", "Design & Creative Arts", "Takes and edits photographs for different purposes.", "Camera skills, lighting, editing, composition", ["art", "media", "creativity"], ["photography", "editing", "communication"], ["photography", "travelling", "storytelling"], ["creativity", "patience", "attention to detail"]),
    ("Film Director", "Media & Communication", "Leads the creative work involved in making films.", "Storytelling, leadership, communication, production", ["art", "media", "writing"], ["leadership", "communication", "creativity"], ["storytelling", "photography", "acting"], ["creativity", "confidence", "leadership"]),
    ("Journalist", "Media & Communication", "Researches and reports news and current events.", "Writing, interviewing, research, media ethics", ["writing", "media", "history"], ["writing", "research", "communication"], ["reading", "photography", "storytelling"], ["curiosity", "confidence", "creativity"]),
    ("Public Relations Specialist", "Media & Communication", "Builds and manages the public image of organisations.", "Writing, communication, media planning", ["media", "business", "writing"], ["communication", "writing", "organisation"], ["networking", "reading", "storytelling"], ["confidence", "creativity", "leadership"]),
    ("Content Creator", "Media & Communication", "Produces digital content for online audiences.", "Video editing, writing, social media, storytelling", ["media", "art", "technology"], ["communication", "creativity", "editing"], ["photography", "gaming", "storytelling"], ["creativity", "confidence", "initiative"]),
    ("Lawyer", "Law & Public Service", "Advises clients and represents them in legal matters.", "Research, writing, public speaking, legal reasoning", ["law", "politics", "history"], ["communication", "writing", "research"], ["debating", "reading", "public speaking"], ["confidence", "leadership", "critical thinking"]),
    ("Diplomat", "Law & Public Service", "Represents a country and supports international relations.", "Communication, languages, negotiation, research", ["politics", "history", "languages"], ["communication", "research", "negotiation"], ["reading", "travelling", "debating"], ["confidence", "empathy", "patience"]),
    ("Police Officer", "Law & Public Service", "Helps protect the public and enforce the law.", "Communication, observation, decision making", ["law", "security", "sports"], ["communication", "problem solving", "teamwork"], ["sports", "volunteering"], ["discipline", "responsibility", "confidence"]),
    ("Social Worker", "Law & Public Service", "Supports individuals, families and communities.", "Communication, counselling, advocacy, organisation", ["society", "health", "education"], ["listening", "communication", "problem solving"], ["volunteering", "reading", "helping people"], ["empathy", "patience", "responsibility"]),
    ("Entrepreneur", "Business & Finance", "Starts and manages a business or new venture.", "Business planning, marketing, finance, leadership", ["business", "economics", "innovation"], ["leadership", "communication", "marketing"], ["selling", "networking", "creating projects"], ["confidence", "creativity", "initiative"]),
    ("Accountant", "Business & Finance", "Maintains financial records and prepares financial reports.", "Accounting, mathematics, spreadsheets, accuracy", ["business", "economics", "mathematics"], ["mathematics", "organisation", "analytical thinking"], ["puzzles", "reading", "planning"], ["honesty", "patience", "attention to detail"]),
    ("Banker", "Business & Finance", "Helps customers and organisations manage money and finance.", "Finance, mathematics, communication, analysis", ["business", "economics", "mathematics"], ["communication", "mathematics", "problem solving"], ["reading", "networking", "planning"], ["responsibility", "confidence", "attention to detail"]),
    ("Marketing Manager", "Business & Finance", "Plans campaigns to promote products and services.", "Marketing, communication, research, creativity", ["business", "media", "creativity"], ["communication", "marketing", "research"], ["networking", "photography", "creating projects"], ["creativity", "confidence", "leadership"]),
    ("Economist", "Business & Finance", "Studies how people, businesses and countries use resources.", "Economics, mathematics, statistics, research", ["economics", "politics", "mathematics"], ["research", "mathematics", "analytical thinking"], ["reading", "debating", "puzzles"], ["curiosity", "analytical thinking", "patience"]),
    ("Human Resources Officer", "Business & Finance", "Supports recruitment, staff development and workplace needs.", "Communication, organisation, conflict resolution", ["business", "society", "psychology"], ["communication", "organisation", "listening"], ["reading", "networking", "helping people"], ["empathy", "patience", "fairness"]),
    ("Teacher", "Education", "Helps learners develop knowledge and useful skills.", "Subject knowledge, lesson planning, communication", ["education", "science", "literature"], ["communication", "explaining", "organisation"], ["reading", "mentoring", "volunteering"], ["patience", "empathy", "responsibility"]),
    ("Educational Psychologist", "Education", "Studies how students learn and supports learning needs.", "Psychology, research, communication, assessment", ["education", "psychology", "science"], ["research", "listening", "communication"], ["reading", "mentoring", "helping people"], ["empathy", "patience", "curiosity"]),
    ("Librarian", "Education", "Organises information and helps people find resources.", "Research, organisation, information technology", ["education", "literature", "history"], ["organisation", "research", "communication"], ["reading", "learning", "helping people"], ["patience", "curiosity", "attention to detail"]),
    ("Research Scientist", "Science & Environment", "Conducts experiments and develops scientific knowledge.", "Research methods, statistics, laboratory skills", ["science", "biology", "chemistry"], ["research", "problem solving", "analytical thinking"], ["experiments", "reading", "puzzles"], ["curiosity", "patience", "attention to detail"]),
    ("Environmental Scientist", "Science & Environment", "Studies environmental issues and ways to protect nature.", "Biology, chemistry, data analysis, field research", ["science", "biology", "environment"], ["research", "problem solving", "communication"], ["nature", "reading", "volunteering"], ["curiosity", "responsibility", "patience"]),
    ("Veterinarian", "Science & Environment", "Provides medical care for animals.", "Biology, animal care, communication, clinical skills", ["biology", "science", "animals"], ["problem solving", "communication", "research"], ["animals", "volunteering", "reading"], ["compassion", "patience", "responsibility"]),
    ("Biotechnologist", "Science & Environment", "Uses biological systems to develop useful products and processes.", "Biology, chemistry, laboratory methods, research", ["biology", "chemistry", "science"], ["research", "technical skills", "problem solving"], ["experiments", "reading"], ["curiosity", "analytical thinking", "patience"]),
    ("Agricultural Scientist", "Science & Environment", "Improves crops, soil, livestock and food production.", "Biology, chemistry, research, data analysis", ["biology", "science", "agriculture"], ["research", "problem solving", "technical skills"], ["gardening", "nature", "experiments"], ["curiosity", "patience", "responsibility"]),
    ("Psychologist", "People & Behaviour", "Studies thoughts, emotions and human behaviour.", "Psychology, research, listening, communication", ["psychology", "science", "human behaviour"], ["communication", "research", "listening"], ["reading", "helping people", "volunteering"], ["empathy", "patience", "understanding"]),
    ("Counsellor", "People & Behaviour", "Helps people discuss challenges and make informed choices.", "Active listening, communication, counselling skills", ["psychology", "education", "health"], ["listening", "communication", "problem solving"], ["helping people", "reading", "volunteering"], ["empathy", "patience", "understanding"]),
    ("Sports Coach", "Sports & Fitness", "Trains and motivates individuals or teams in sport.", "Coaching, fitness, communication, planning", ["sports", "health", "biology"], ["leadership", "communication", "teaching"], ["sports", "fitness", "mentoring"], ["discipline", "confidence", "encouragement"]),
    ("Sports Scientist", "Sports & Fitness", "Uses science to improve athletic performance and wellbeing.", "Biology, physiology, data analysis, sports science", ["sports", "biology", "science"], ["research", "analytical thinking", "communication"], ["sports", "fitness", "experiments"], ["curiosity", "discipline", "patience"]),
    ("Chef", "Hospitality & Tourism", "Plans and prepares meals in homes or professional kitchens.", "Cooking, food safety, planning, creativity", ["food", "art", "business"], ["cooking", "organisation", "creativity"], ["cooking", "travelling", "creating projects"], ["creativity", "patience", "attention to detail"]),
    ("Hotel Manager", "Hospitality & Tourism", "Oversees hotel services and guest experiences.", "Customer service, leadership, finance, organisation", ["business", "tourism", "languages"], ["communication", "leadership", "organisation"], ["travelling", "networking", "helping people"], ["confidence", "responsibility", "patience"]),
    ("Tourism Officer", "Hospitality & Tourism", "Promotes destinations and supports travel experiences.", "Communication, planning, marketing, customer service", ["tourism", "history", "languages"], ["communication", "marketing", "organisation"], ["travelling", "photography", "learning"], ["curiosity", "confidence", "helpfulness"]),
]

# Database helpers
def connect_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with connect_db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            interests TEXT, skills TEXT, hobbies TEXT, strengths TEXT,
            top_career TEXT, top_score INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")

def password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def normalise(text):
    return [part.strip().lower() for part in text.split(",") if part.strip()]

def get_matches(interests, skills, hobbies, strengths):
    matches = []
    for career in CAREERS:
        name, category, description, future_skills, ci, cs, ch, cp = career
        im = set(interests) & set(ci)
        sm = set(skills) & set(cs)
        hm = set(hobbies) & set(ch)
        pm = set(strengths) & set(cp)

        # Weights: interests 30%, skills 30%, hobbies 15%, strengths 25%.
        raw = len(im) * 3 + len(sm) * 3 + len(hm) * 1.5 + len(pm) * 2.5
        maximum = len(ci) * 3 + len(cs) * 3 + len(ch) * 1.5 + len(cp) * 2.5
        score = round(raw / maximum * 100) if maximum else 0

        if score > 0:
            matches.append({
                "name": name, "category": category, "description": description,
                "future_skills": future_skills, "score": score,
                "reasons": {
                    "Interests": sorted(im), "Skills": sorted(sm),
                    "Hobbies": sorted(hm), "Strengths": sorted(pm)
                }
            })
    return sorted(matches, key=lambda x: x["score"], reverse=True)

class PathFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PathFinder | Student Career Guide")
        self.root.geometry("1120x790")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)
        self.user_id = None
        self.username = None
        self.last_matches = []
        self.last_inputs = {}
        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, subtitle="Discover your strengths. Explore your future."):
        top = tk.Frame(self.root, bg=PURPLE, height=100)
        top.pack(fill="x")
        tk.Label(top, text="PATHFINDER", font=("Arial", 25, "bold"),
                 fg=WHITE, bg=PURPLE).pack(pady=(14, 2))
        tk.Label(top, text=subtitle, font=("Arial", 11),
                 fg=WHITE, bg=PURPLE).pack()

    def show_login(self):
        self.clear()
        self.header("Your interests can point towards exciting possibilities.")
        card = tk.Frame(self.root, bg=WHITE, padx=35, pady=28)
        card.place(relx=0.5, rely=0.55, anchor="center", width=430)
        tk.Label(card, text="Welcome to PathFinder", font=("Arial", 19, "bold"),
                 bg=WHITE, fg=DARK).pack(pady=(0, 18))
        tk.Label(card, text="Username", bg=WHITE, fg=DARK).pack(anchor="w")
        username = ttk.Entry(card, font=("Arial", 12))
        username.pack(fill="x", pady=(4, 12), ipady=5)
        tk.Label(card, text="Password", bg=WHITE, fg=DARK).pack(anchor="w")
        password = ttk.Entry(card, show="*", font=("Arial", 12))
        password.pack(fill="x", pady=(4, 18), ipady=5)

        def login():
            u, p = username.get().strip(), password.get()
            if not u or not p:
                messagebox.showwarning("Missing details", "Enter your username and password.")
                return
            with connect_db() as con:
                row = con.execute("SELECT id, username, password_hash FROM users WHERE username=?",
                                  (u,)).fetchone()
            if row and row[2] == password_hash(p):
                self.user_id, self.username = row[0], row[1]
                self.show_dashboard()
            else:
                messagebox.showerror("Login failed", "Incorrect username or password.")

        def register():
            u, p = username.get().strip(), password.get()
            if len(u) < 3 or len(p) < 6:
                messagebox.showwarning("Registration", "Use a username of at least 3 characters and password of at least 6 characters.")
                return
            try:
                with connect_db() as con:
                    con.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)",
                                (u, password_hash(p)))
                messagebox.showinfo("Account created", "Your account is ready. You can now log in.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Username unavailable", "That username is already registered.")

        tk.Button(card, text="LOG IN", command=login, bg=PURPLE, fg=WHITE,
                  font=("Arial", 11, "bold"), relief="flat", pady=10,
                  cursor="hand2").pack(fill="x", pady=(0, 9))
        tk.Button(card, text="CREATE ACCOUNT", command=register, bg="#EAE4FA",
                  fg=DARK, font=("Arial", 10, "bold"), relief="flat",
                  pady=9, cursor="hand2").pack(fill="x")
        tk.Label(card, text="Your assessments are saved to this computer.",
                 bg=WHITE, fg="#777777", font=("Arial", 9)).pack(pady=(15, 0))

    def show_dashboard(self):
        self.clear()
        self.header(f"Welcome, {self.username}! Explore what you could become.")
        nav = tk.Frame(self.root, bg=WHITE, padx=12, pady=10)
        nav.pack(fill="x")
        for label, command in [
            ("Dashboard", self.show_dashboard),
            ("Career Assessment", self.show_assessment),
            ("Explore Careers", self.show_explore),
            ("My History", self.show_history),
            ("Log Out", self.logout)
        ]:
            tk.Button(nav, text=label, command=command, bg=WHITE, fg=PURPLE,
                      relief="flat", font=("Arial", 10, "bold"),
                      cursor="hand2").pack(side="left", padx=8)

        body = tk.Frame(self.root, bg=BG, padx=35, pady=30)
        body.pack(fill="both", expand=True)
        tk.Label(body, text="Your future is not one-size-fits-all.",
                 font=("Arial", 23, "bold"), bg=BG, fg=DARK).pack(anchor="w")
        tk.Label(body, text="PathFinder connects your interests, skills, hobbies and strengths "
                            "to career ideas worth exploring.",
                 font=("Arial", 12), bg=BG, fg="#555555",
                 wraplength=850, justify="left").pack(anchor="w", pady=12)

        stats = tk.Frame(body, bg=BG)
        stats.pack(fill="x", pady=15)
        with connect_db() as con:
            total = con.execute("SELECT COUNT(*) FROM assessments WHERE user_id=?",
                                (self.user_id,)).fetchone()[0]
        self.stat_card(stats, str(len(CAREERS)), "Careers to explore")
        self.stat_card(stats, str(total), "Saved assessments")
        self.stat_card(stats, "4", "Profile areas assessed")

        tk.Label(body, text="How it works", font=("Arial", 17, "bold"),
                 bg=BG, fg=DARK).pack(anchor="w", pady=(22, 8))
        for line in [
            "1. Tell us what subjects and activities interest you.",
            "2. Add the skills you have and the strengths that describe you.",
            "3. Get ranked career suggestions with explanations and next steps.",
            "4. Save your results and create a PDF report."
        ]:
            tk.Label(body, text=line, font=("Arial", 11), bg=BG, fg=DARK).pack(anchor="w", pady=4)

        tk.Button(body, text="START MY CAREER ASSESSMENT", command=self.show_assessment,
                  bg=PURPLE, fg=WHITE, font=("Arial", 12, "bold"),
                  relief="flat", padx=22, pady=13, cursor="hand2").pack(anchor="w", pady=25)

    def stat_card(self, parent, value, label):
        card = tk.Frame(parent, bg=WHITE, padx=25, pady=18)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        tk.Label(card, text=value, font=("Arial", 22, "bold"),
                 bg=WHITE, fg=PURPLE).pack()
        tk.Label(card, text=label, font=("Arial", 10),
                 bg=WHITE, fg=DARK).pack()

    def navigation(self, parent):
        nav = tk.Frame(parent, bg=WHITE, padx=8, pady=8)
        nav.pack(fill="x")
        for label, command in [
            ("Dashboard", self.show_dashboard),
            ("Career Assessment", self.show_assessment),
            ("Explore Careers", self.show_explore),
            ("My History", self.show_history),
            ("Log Out", self.logout)
        ]:
            tk.Button(nav, text=label, command=command, bg=WHITE, fg=PURPLE,
                      relief="flat", font=("Arial", 9, "bold"),
                      cursor="hand2").pack(side="left", padx=7)

    def show_assessment(self):
        self.clear()
        self.header("Complete your profile to discover career matches.")
        self.navigation(self.root)
        outer = tk.Frame(self.root, bg=BG, padx=30, pady=15)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="Career Discovery Assessment",
                 font=("Arial", 20, "bold"), bg=BG, fg=DARK).pack(anchor="w", pady=(0, 5))
        tk.Label(outer, text="Enter comma-separated keywords. Use the examples as a guide.",
                 font=("Arial", 10), bg=BG, fg="#666666").pack(anchor="w", pady=(0, 12))

        fields = [
            ("Interests", "Subjects or topics you enjoy", "technology, biology, mathematics"),
            ("Skills", "Things you can do or are learning", "coding, communication, drawing"),
            ("Hobbies", "Activities you enjoy in your free time", "gaming, reading, photography"),
            ("Strengths", "Personal qualities that describe you", "creativity, leadership, patience")
        ]
        self.assessment_entries = {}
        for key, title, example in fields:
            frame = tk.Frame(outer, bg=WHITE, padx=14, pady=9)
            frame.pack(fill="x", pady=6)
            tk.Label(frame, text=title, font=("Arial", 11, "bold"),
                     bg=WHITE, fg=DARK).pack(anchor="w")
            entry = ttk.Entry(frame, font=("Arial", 11))
            entry.pack(fill="x", pady=(5, 2), ipady=5)
            entry.insert(0, example)
            self.assessment_entries[key] = entry

        tk.Button(outer, text="FIND MY CAREER MATCHES", command=self.run_assessment,
                  bg=PURPLE, fg=WHITE, font=("Arial", 12, "bold"),
                  relief="flat", padx=20, pady=12, cursor="hand2").pack(anchor="w", pady=15)

    def run_assessment(self):
        values = {key: normalise(entry.get())
                  for key, entry in self.assessment_entries.items()}
        if not any(values.values()):
            messagebox.showwarning("No answers", "Please enter at least one answer.")
            return
        self.last_inputs = values
        self.last_matches = get_matches(values["Interests"], values["Skills"],
                                        values["Hobbies"], values["Strengths"])
        if not self.last_matches:
            messagebox.showinfo("No direct matches",
                                "No direct keyword matches were found. Try using broader terms such as technology, science, design, communication or creativity.")
            return
        top = self.last_matches[0]
        with connect_db() as con:
            con.execute("""INSERT INTO assessments
                (user_id, created_at, interests, skills, hobbies, strengths, top_career, top_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.user_id, datetime.now().strftime("%Y-%m-%d %H:%M"),
                 ", ".join(values["Interests"]), ", ".join(values["Skills"]),
                 ", ".join(values["Hobbies"]), ", ".join(values["Strengths"]),
                 top["name"], top["score"]))
        self.show_results()

    def show_results(self):
        self.clear()
        self.header("Your career matches are ready.")
        self.navigation(self.root)
        outer = tk.Frame(self.root, bg=BG, padx=22, pady=12)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="Your Top Career Matches",
                 font=("Arial", 20, "bold"), bg=BG, fg=DARK).pack(anchor="w")
        tk.Label(outer, text="These suggestions are based on the keywords you entered. "
                             "A match score is a guide, not a measure of your ability.",
                 font=("Arial", 10), bg=BG, fg="#555555",
                 wraplength=950).pack(anchor="w", pady=5)

        container = tk.Frame(outer, bg=BG)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for i, item in enumerate(self.last_matches[:10], 1):
            card = tk.Frame(inner, bg=WHITE, padx=15, pady=12,
                            highlightbackground="#DDD5F5", highlightthickness=1)
            card.pack(fill="x", pady=6, padx=5)
            tk.Label(card, text=f"{i}. {item['name']}  |  {item['score']}% match",
                     font=("Arial", 13, "bold"), bg=WHITE, fg=PURPLE).pack(anchor="w")
            tk.Label(card, text=f"Category: {item['category']}   •   {item['description']}",
                     font=("Arial", 10), bg=WHITE, fg=DARK,
                     wraplength=900, justify="left").pack(anchor="w", pady=4)
            reasons = [f"{k}: {', '.join(v)}" for k, v in item["reasons"].items() if v]
            tk.Label(card, text="Why it matched: " + ("; ".join(reasons) if reasons else "Some related profile keywords."),
                     font=("Arial", 9), bg=WHITE, fg="#555555",
                     wraplength=900, justify="left").pack(anchor="w", pady=3)
            tk.Label(card, text="Skills to explore: " + item["future_skills"],
                     font=("Arial", 9, "bold"), bg=WHITE, fg=DARK,
                     wraplength=900, justify="left").pack(anchor="w", pady=3)

        buttons = tk.Frame(outer, bg=BG)
        buttons.pack(fill="x", pady=10)
        tk.Button(buttons, text="DOWNLOAD PDF REPORT", command=self.export_pdf,
                  bg=PURPLE, fg=WHITE, font=("Arial", 10, "bold"),
                  relief="flat", padx=15, pady=10).pack(side="left", padx=(0, 10))
        tk.Button(buttons, text="EXPLORE ALL CAREERS", command=self.show_explore,
                  bg="#EAE4FA", fg=DARK, font=("Arial", 10, "bold"),
                  relief="flat", padx=15, pady=10).pack(side="left")

    def export_pdf(self):
        if not self.last_matches:
            messagebox.showinfo("No results", "Complete an assessment first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{self.username}_career_report.pdf")
        if not path:
            return
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("TitleCustom", parent=styles["Title"],
                                     textColor=colors.HexColor(PURPLE),
                                     alignment=TA_CENTER, fontSize=20, spaceAfter=12)
        story = [
            Paragraph("PATHFINDER CAREER REPORT", title_style),
            Paragraph(f"Student: {self.username}", styles["Normal"]),
            Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", styles["Normal"]),
            Spacer(1, 8),
            Paragraph("<b>Your assessment profile</b>", styles["Heading2"])
        ]
        for key, vals in self.last_inputs.items():
            story.append(Paragraph(f"<b>{key}:</b> {', '.join(vals) if vals else 'Not provided'}", styles["BodyText"]))
        story += [Spacer(1, 10), Paragraph("<b>Top career recommendations</b>", styles["Heading2"])]
        for idx, item in enumerate(self.last_matches[:10], 1):
            story.append(Paragraph(f"<b>{idx}. {item['name']} — {item['score']}% match</b> ({item['category']})", styles["BodyText"]))
            story.append(Paragraph(item["description"], styles["BodyText"]))
            reason_text = "; ".join(f"{k}: {', '.join(v)}" for k, v in item["reasons"].items() if v)
            story.append(Paragraph(f"<b>Matching profile:</b> {reason_text or 'Some related profile keywords.'}", styles["BodyText"]))
            story.append(Paragraph(f"<b>Skills to explore:</b> {item['future_skills']}", styles["BodyText"]))
            story.append(Spacer(1, 8))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Important: This report is for career exploration only. "
                               "It is not a professional aptitude test or a guarantee of success. "
                               "Research course requirements and speak with a qualified career adviser.",
                               styles["Italic"]))
        try:
            doc = SimpleDocTemplate(path, pagesize=A4, rightMargin=18*mm,
                                    leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
            doc.build(story)
            messagebox.showinfo("PDF saved", f"Your career report was saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("PDF error", f"Could not create the report:\n{exc}")

    def show_explore(self):
        self.clear()
        self.header("Explore career paths and the skills they use.")
        self.navigation(self.root)
        outer = tk.Frame(self.root, bg=BG, padx=22, pady=15)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="Career Explorer", font=("Arial", 20, "bold"),
                 bg=BG, fg=DARK).pack(anchor="w")
        search_var = tk.StringVar()
        search = ttk.Entry(outer, textvariable=search_var, font=("Arial", 11))
        search.pack(fill="x", pady=10, ipady=5)

        content = tk.Frame(outer, bg=BG)
        content.pack(fill="both", expand=True)
        left = tk.Frame(content, bg=WHITE, padx=8, pady=8, width=330)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)
        right = tk.Frame(content, bg=WHITE, padx=18, pady=15)
        right.pack(side="left", fill="both", expand=True)
        listbox = tk.Listbox(left, font=("Arial", 10), activestyle="dotbox",
                             selectbackground=PURPLE, height=25)
        listbox.pack(fill="both", expand=True)

        detail = tk.Text(right, wrap="word", font=("Arial", 11), bg=WHITE,
                         fg=DARK, relief="flat", height=20)
        detail.pack(fill="both", expand=True)

        filtered = []

        def show_detail(event=None):
            selection = listbox.curselection()
            if not selection:
                return
            career = filtered[selection[0]]
            detail.config(state="normal")
            detail.delete("1.0", "end")
            detail.insert("end", career[0] + "\n", "heading")
            detail.insert("end", f"Category: {career[1]}\n\n")
            detail.insert("end", career[2] + "\n\n")
            detail.insert("end", "Useful skills to develop\n", "subheading")
            detail.insert("end", career[3] + "\n\n")
            detail.insert("end", "Related interests\n", "subheading")
            detail.insert("end", ", ".join(career[4]) + "\n\n")
            detail.insert("end", "Related skills\n", "subheading")
            detail.insert("end", ", ".join(career[5]) + "\n\n")
            detail.insert("end", "Related hobbies\n", "subheading")
            detail.insert("end", ", ".join(career[6]) + "\n\n")
            detail.insert("end", "Related strengths\n", "subheading")
            detail.insert("end", ", ".join(career[7]))
            detail.tag_config("heading", font=("Arial", 17, "bold"), foreground=PURPLE)
            detail.tag_config("subheading", font=("Arial", 11, "bold"), foreground=PURPLE)
            detail.config(state="disabled")

        def refresh(*args):
            nonlocal filtered
            term = search_var.get().strip().lower()
            filtered = [c for c in CAREERS if term in " ".join(
                [c[0], c[1], c[2], c[3]] + c[4] + c[5] + c[6] + c[7]).lower()]
            listbox.delete(0, "end")
            for career in filtered:
                listbox.insert("end", career[0])
            detail.config(state="normal")
            detail.delete("1.0", "end")
            detail.config(state="disabled")

        search_var.trace_add("write", refresh)
        listbox.bind("<<ListboxSelect>>", show_detail)
        refresh()

    def show_history(self):
        self.clear()
        self.header("Review your previous career assessments.")
        self.navigation(self.root)
        outer = tk.Frame(self.root, bg=BG, padx=28, pady=20)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="My Assessment History", font=("Arial", 20, "bold"),
                 bg=BG, fg=DARK).pack(anchor="w", pady=(0, 12))
        columns = ("date", "career", "score")
        tree = ttk.Treeview(outer, columns=columns, show="headings", height=18)
        tree.heading("date", text="Date")
        tree.heading("career", text="Top career match")
        tree.heading("score", text="Match score")
        tree.column("date", width=190)
        tree.column("career", width=450)
        tree.column("score", width=130, anchor="center")
        tree.pack(fill="both", expand=True)
        with connect_db() as con:
            rows = con.execute("""SELECT created_at, top_career, top_score
                                  FROM assessments WHERE user_id=?
                                  ORDER BY id DESC""", (self.user_id,)).fetchall()
        for row in rows:
            tree.insert("", "end", values=(row[0], row[1], f"{row[2]}%"))
        if not rows:
            tk.Label(outer, text="No assessments yet. Complete your first assessment to see it here.",
                     bg=BG, fg="#666666", font=("Arial", 11)).pack(pady=12)

    def logout(self):
        self.user_id = None
        self.username = None
        self.last_matches = []
        self.last_inputs = {}
        self.show_login()


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PathFinderApp(root)
    root.mainloop()
