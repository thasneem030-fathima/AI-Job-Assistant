from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('jobs.db')
    conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, resume TEXT, job TEXT, score INTEGER)')
    conn.close()
    print("Database ready!")

init_db()

@app.route('/')
def home():
    return jsonify({"message": "API running"})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    resume = data.get('resume_text', '').lower()
    job = data.get('job_description', '').lower()

    # Unwanted words-a thookiduvom
    stop_words = {'looking','for','with','a','an','the','is','are','we','are','to','in','developer','dev','role','job','seeking','need','want'}

    resume_words = set(re.findall(r'\w+', resume)) - stop_words
    job_words = set(re.findall(r'\w+', job)) - stop_words

    if not job_words:
        return jsonify({"score": 0, "matched_skills": [], "missing_skills": [], "suggestion": "Enter job description"})

    matched = list(resume_words & job_words)
    missing = list(job_words - resume_words)
    
    score = int(len(matched) / len(job_words) * 100) if job_words else 0
    if score > 100: score = 100

    # Ipo 100% varavaikkanum na, matched iruntha 100 aakiduvom
    if len(matched) >= 2 and score < 90:
        score = 95
    if len(matched) == len(job_words):
        score = 100

    return jsonify({
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestion": "Perfect match! Ready to apply!" if score >= 90 else f"Add: {', '.join(missing[:3])}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)