from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "Truth_File.csv")

def load_data():
    df = pd.read_csv(FILE_PATH)
    df.columns = df.columns.str.strip()

    if "Date of Service" in df.columns:
        df["Date of Service"] = pd.to_datetime(df["Date of Service"], errors="coerce")
        df["Date of Service"] = df["Date of Service"].dt.strftime("%Y-%m-%d")

    return df

@app.route("/")
@app.route("/dashboard")
def dashboard():
    df = load_data()

    total_claims = len(df)
    status_counts = df["Claim Status"].value_counts().to_dict() if "Claim Status" in df.columns else {}
    outcome_counts = df["Current Claim Outcome"].value_counts().to_dict() if "Current Claim Outcome" in df.columns else {}

    return render_template(
        "dashboard.html",
        total_claims=total_claims,
        status_counts=status_counts,
        outcome_counts=outcome_counts
    )

@app.route("/patient-claims", methods=["GET", "POST"])
def patient_claims():
    df = load_data()
    patient_id = ""
    patient_records = []

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        if "Patient ID" in df.columns:
            filtered = df[df["Patient ID"].astype(str) == patient_id].copy()

            if "Date of Service" in filtered.columns:
                filtered = filtered.sort_values(by="Date of Service", ascending=True)

            patient_records = filtered.to_dict(orient="records")

    return render_template(
        "patient_claims.html",
        patient_id=patient_id,
        patient_records=patient_records
    )

@app.route("/truth-file")
def truth_file():
    df = load_data()
    records = df.to_dict(orient="records")
    columns = df.columns.tolist()

    return render_template(
        "truth_file.html",
        records=records,
        columns=columns
    )

@app.route("/download")
def download():
    return send_file(FILE_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)