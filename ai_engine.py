import re

def analyze_match(job_desc, resume):
    if not job_desc or not resume:
        return {"score": 0, "matched_skills": [], "missing_skills": [], "suggestion": "Please provide both Job Description and Resume"}

    job_words = set(re.findall(r'\w+', job_desc.lower()))
    resume_words = set(re.findall(r'\w+', resume.lower()))

    common = job_words.intersection(resume_words)
    missing = job_words - resume_words
    
    # Remove small common words
    stop_words = {'and','the','is','a','an','for','to','in','with','of','on','we','are','you','as','at','be','by','it','this','that'}
    common = [w for w in common if w not in stop_words and len(w) > 2]
    missing = [w for w in missing if w not in stop_words and len(w) > 2]

    score = 0
    if len(job_words) > 0:
        score = int((len(common) / len(job_words)) * 100)
        if score > 95:
            score = 85 # realistic score

    return {
        "score": score,
        "matched_skills": list(common)[:15],
        "missing_skills": list(missing)[:15],
        "suggestion": f"Your resume matches {score}%. Try adding these keywords: {', '.join(list(missing)[:5])}"
    }

def analyze(job_desc, resume):
    return analyze_match(job_desc, resume)