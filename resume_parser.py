import re
import json
import PyPDF2
import docx
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Expanded skills list
SKILLS = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust",
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP",
    "SQL", "NoSQL", "MongoDB", "MySQL", "PostgreSQL",
    "Data Analysis", "Data Science", "Pandas", "NumPy", "Matplotlib",
    "Communication", "Leadership", "Teamwork", "Problem Solving",
    "UI/UX Design", "Figma", "HTML", "CSS", "HTML/CSS", "Adobe XD",
    "React", "Node.js", "Django", "Flask", "Spring Boot",
    "Git", "GitHub", "Docker", "Kubernetes", "CI/CD", "AWS", "Azure", "GCP",
    "Excel", "Power BI", "Tableau"
]

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file"""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file"""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    """Extract the first email address found in the text"""
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group() if match else None

def extract_phone(text):
    """Extract the first phone number found in the text"""
    match = re.search(r'(\+?\d[\d\s\-()]{9,})', text)
    return match.group().strip() if match else None

def extract_name(text):
    """Try to extract the person's name using spaCy or fallback to top lines"""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    # Fallback: top non-empty line with 1–4 words
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and 1 <= len(line.split()) <= 4:
            return line
    return None

def extract_skills(text):
    """Find and return matching skills from the list"""
    found = []
    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return found

def parse_resume(file_path):
    """Main logic: extract all info from resume"""
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }

# === Main Execution ===
if __name__ == "__main__":
    path = "sample_resume.pdf"  # Replace with your actual file name if different
    parsed_data = parse_resume(path)

    # Save to JSON
    with open("parsed_resume.json", "w") as f:
        json.dump(parsed_data, f, indent=4)

    # Print output
    print("✅ Resume Parsed:")
    print(json.dumps(parsed_data, indent=4))
