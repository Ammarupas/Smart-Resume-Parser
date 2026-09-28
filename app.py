from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from resume_parser import parse_resume
import os
import json

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = "resume-parser-secret"

# Folder to store uploaded resumes
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Upload resume
@app.route("/upload", methods=["GET", "POST"])
def upload():

    # If /upload is opened directly in the browser
    if request.method == "GET":
        return redirect(url_for("index"))

    # Check whether file exists
    if "resume" not in request.files:
        flash("⚠️ No file selected.")
        return redirect(url_for("index"))

    file = request.files["resume"]

    # Check filename
    if file.filename == "":
        flash("⚠️ Please select a resume.")
        return redirect(url_for("index"))

    # Check file type
    if not allowed_file(file.filename):
        flash("❌ Only PDF and DOCX files are allowed.")
        return redirect(url_for("index"))

    # Secure the filename
    filename = secure_filename(file.filename)

    # Create file path
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save uploaded resume
    file.save(file_path)

    try:

        # Parse resume
        parsed_data = parse_resume(file_path)

        # Save extracted data as JSON
        with open(
            "parsed_resume.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                parsed_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        # Display result
        return render_template(
            "result.html",
            data=parsed_data,
            filename=filename
        )

    except Exception as e:

        flash(f"❌ Error while parsing resume: {e}")

        return redirect(url_for("index"))


# Start Flask server
if __name__ == "__main__":

    print("------------------------------------")
    print("      AI RESUME PARSER")
    print("------------------------------------")
    print("Open: http://127.0.0.1:5000/")
    print("Press CTRL+C to stop")
    print("------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )