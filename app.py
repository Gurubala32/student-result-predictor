from pathlib import Path
import os
import pickle
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_model.pkl"
VERSION_PATH = BASE_DIR / "VERSION"

app = Flask(__name__)

def get_model_version():
    return os.getenv("MODEL_VERSION", VERSION_PATH.read_text(encoding="utf-8").strip())

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None
    study_hours = ""
    attendance = ""
    internal_marks = ""

    if request.method == "POST":
        try:
            study_hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            internal_marks = float(request.form["internal_marks"])

            if study_hours < 0:
                raise ValueError("Study hours cannot be negative.")
            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")
            if not 0 <= internal_marks <= 100:
                raise ValueError("Internal marks must be between 0 and 100.")

            result = model.predict([[study_hours, attendance, internal_marks]])[0]
            prediction = "Pass" if int(result) == 1 else "Fail"
        except ValueError as exc:
            error = str(exc) or "Please enter valid numeric values."
        except (KeyError, TypeError):
            error = "Please fill in all three fields."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        model_version=get_model_version(),
        study_hours=study_hours,
        attendance=attendance,
        internal_marks=internal_marks,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
