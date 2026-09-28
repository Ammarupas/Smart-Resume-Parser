# Resume Parser Project

This project reads resumes in PDF or DOCX format and extracts key information such as:
- Name
- Email
- Phone number
- Skills

## Requirements
- Python 3.x
- Libraries: PyPDF2, python-docx, spacy

## Setup
Install the required libraries using:

```
pip install PyPDF2 python-docx spacy
python -m spacy download en_core_web_sm
```

## How to Run
Place your resume file in the same directory and rename it as `sample_resume.pdf` or change the filename in the code.

Run the script using:

```
python resume_parser.py
```

## Output
A JSON file named `parsed_resume.json` will be generated with the extracted information.
