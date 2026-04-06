# from flask import Flask, render_template, request, send_file
# import pandas as pd
# import os
# import joblib

# # model = joblib.load("log_model.pkl")

# label_map = {
#     0: "Claim Under Process",
#     1: "Patient Letter / Rebill to Secondary",
#     2: "paid"
# }

# app = Flask(__name__)



# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FILE_PATH = os.path.join(BASE_DIR, "data", "Truth_File.csv")
# MODEL_PATH = os.path.join(BASE_DIR, "log_model.pkl")
# model = joblib.load(MODEL_PATH)

# def load_data():
#     df = pd.read_csv(FILE_PATH)
#     df.columns = df.columns.str.strip()

#     if "Date of Service" in df.columns:
#         df["Date of Service"] = pd.to_datetime(df["Date of Service"], errors="coerce")
#         df["Date of Service"] = df["Date of Service"].dt.strftime("%Y-%m-%d")

#     return df

# @app.route("/")
# def home():
#     return render_template("home.html")
# @app.route("/dashboard")
# def dashboard():
#     df = load_data()

#     total_claims = len(df)
#     status_counts = df["Claim Status"].value_counts().to_dict() if "Claim Status" in df.columns else {}
#     outcome_counts = df["Current Claim Outcome"].value_counts().to_dict() if "Current Claim Outcome" in df.columns else {}

#     return render_template(
#         "dashboard.html",
#         total_claims=total_claims,
#         status_counts=status_counts,
#         outcome_counts=outcome_counts
#     )

# @app.route("/patient-claims", methods=["GET", "POST"])
# def patient_claims():
#     df = load_data()
#     patient_id = ""
#     patient_records = []

#     if request.method == "POST":
#         patient_id = request.form.get("patient_id", "").strip()
#         if "Patient ID" in df.columns:
#             filtered = df[df["Patient ID"].astype(str) == patient_id].copy()

#             if "Date of Service" in filtered.columns:
#                 filtered = filtered.sort_values(by="Date of Service", ascending=True)

#             patient_records = filtered.to_dict(orient="records")

#     return render_template(
#         "patient_claims.html",
#         patient_id=patient_id,
#         patient_records=patient_records
#     )

# @app.route("/truth-file")
# def truth_file():
#     df = load_data()
#     records = df.to_dict(orient="records")
#     columns = df.columns.tolist()

#     return render_template(
#         "truth_file.html",
#         records=records,
#         columns=columns
#     )

# @app.route("/download")
# def download():
#     return send_file(FILE_PATH, as_attachment=True)

# @app.route("/predict", methods=["POST"])
# def predict():
#     allowed_amount = float(request.form["allowed_amount"])
#     # annual_benefit_maximum = float(request.form["annual_benefit_maximum"])
#     prior_used_amount = float(request.form["prior_used_amount"])
#     # remaining_benefit_before_claim = float(request.form["remaining_benefit_before_claim"])
#     # claim_status_enc = int(request.form["claim_status_enc"])


#     input_df = pd.DataFrame([{
#         "Allowed Amount": allowed_amount,
#         # "Annual Benefit Maximum": annual_benefit_maximum,
#         "Prior Used Amount": prior_used_amount,
#         # "Remaining Benefit Before Claim": remaining_benefit_before_claim,
#         # "Claim_Status_Enc": claim_status_enc
#     }])

#     prediction = model.predict(input_df)[0]
#     predicted_label = label_map[prediction]

#     return render_template(
#         "patient_claims.html",
#         prediction=predicted_label,
#         patient_id="",
#         patient_records=[]
#     )

# if __name__ == "__main__":
#     app.run(debug=True,port=5001)
# from flask import Flask, render_template, request, send_file
# import pandas as pd
# import os
# import joblib

# label_map = {
#     0: "Claim Under Process",
#     1: "Patient Letter / Rebill to Secondary",
#     2: "paid"
# }

# app = Flask(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FILE_PATH = os.path.join(BASE_DIR, "data", "Truth_File.csv")
# MODEL_PATH = os.path.join(BASE_DIR, "log_model.pkl")
# model = joblib.load(MODEL_PATH)


# def load_data():
#     df = pd.read_csv(FILE_PATH)
#     df.columns = df.columns.str.strip()

#     if "Date of Service" in df.columns:
#         df["Date of Service"] = pd.to_datetime(df["Date of Service"], errors="coerce")
#         df["Date of Service"] = df["Date of Service"].dt.strftime("%Y-%m-%d")

#     return df


# @app.route("/")
# def home():
#     return render_template("home.html")


# @app.route("/dashboard")
# def dashboard():
#     df = load_data()

#     total_claims = len(df)
#     status_counts = df["Claim Status"].value_counts().to_dict() if "Claim Status" in df.columns else {}
#     outcome_counts = df["Current Claim Outcome"].value_counts().to_dict() if "Current Claim Outcome" in df.columns else {}

#     return render_template(
#         "dashboard.html",
#         total_claims=total_claims,
#         status_counts=status_counts,
#         outcome_counts=outcome_counts
#     )


# @app.route("/patient-claims", methods=["GET", "POST"])
# def patient_claims():
#     df = load_data()
#     patient_id = ""
#     patient_records = []
#     prediction = None
#     risk_level = None
#     alert_message = None
#     recommendation = None
#     assessment_data = {}

#     if request.method == "POST":
#         form_type = request.form.get("form_type", "")

#         # -----------------------------
#         # Patient search form
#         # -----------------------------
#         if form_type == "search_patient":
#             patient_id = request.form.get("patient_id", "").strip()

#             if "Patient ID" in df.columns:
#                 filtered = df[df["Patient ID"].astype(str) == patient_id].copy()

#                 if "Date of Service" in filtered.columns:
#                     filtered = filtered.sort_values(by="Date of Service", ascending=True)

#                 patient_records = filtered.to_dict(orient="records")

#         # -----------------------------
#         # Claim assessment form
#         # -----------------------------
#         elif form_type == "predict_claim":
#             patient_id = request.form.get("patient_id", "").strip()

#             allowed_amount = float(request.form.get("allowed_amount", 0))
#             prior_used_amount = float(request.form.get("prior_used_amount", 0))

#             input_df = pd.DataFrame([{
#                 "Allowed Amount": allowed_amount,
#                 "Prior Used Amount": prior_used_amount
#             }])

#             prediction_value = model.predict(input_df)[0]
#             prediction = label_map.get(prediction_value, "Unknown")

#             # simple risk assessment logic
#             if prediction == "Patient Letter / Rebill to Secondary":
#                 risk_level = "High"
#                 alert_message = "This claim shows a high risk and may require rebill or secondary review."
#                 recommendation = "Review payer details, benefit usage, and rebill workflow before submission."
#             elif prediction == "Claim Under Process":
#                 risk_level = "Medium"
#                 alert_message = "This claim may need manual verification before final processing."
#                 recommendation = "Review the claim with billing team and verify supporting details."
#             else:
#                 risk_level = "Low"
#                 alert_message = "This claim appears likely to be paid based on current inputs."
#                 recommendation = "Proceed with submission and continue routine monitoring."

#             # also show patient history if patient id is given
#             if patient_id and "Patient ID" in df.columns:
#                 filtered = df[df["Patient ID"].astype(str) == patient_id].copy()

#                 if "Date of Service" in filtered.columns:
#                     filtered = filtered.sort_values(by="Date of Service", ascending=True)

#                 patient_records = filtered.to_dict(orient="records")

#             assessment_data = {
#                 "allowed_amount": allowed_amount,
#                 "prior_used_amount": prior_used_amount
#             }

#     return render_template(
#         "patient_claims.html",
#         patient_id=patient_id,
#         patient_records=patient_records,
#         prediction=prediction,
#         risk_level=risk_level,
#         alert_message=alert_message,
#         recommendation=recommendation,
#         assessment_data=assessment_data
#     )


# @app.route("/truth-file")
# def truth_file():
#     df = load_data()
#     records = df.to_dict(orient="records")
#     columns = df.columns.tolist()

#     return render_template(
#         "truth_file.html",
#         records=records,
#         columns=columns
#     )


# @app.route("/download")
# def download():
#     return send_file(FILE_PATH, as_attachment=True)


# if __name__ == "__main__":
#     app.run(debug=True, port=5001)
from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


log_model = joblib.load("log_model.pkl")
X_test = joblib.load("X_test.pkl")
y_test = joblib.load("y_test.pkl")

label_map = {
    0: "Claim Under Process",
    1: "Patient Letter / Rebill to Secondary",
    2: "paid"
}

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "Truth_File.csv")
MODEL_PATH = os.path.join(BASE_DIR, "log_model.pkl")
model = joblib.load(MODEL_PATH)


def load_data():
    df = pd.read_csv(FILE_PATH)
    df.columns = df.columns.str.strip()

    if "Date of Service" in df.columns:
        df["Date of Service"] = pd.to_datetime(df["Date of Service"], errors="coerce")
        df["Date of Service"] = df["Date of Service"].dt.strftime("%Y-%m-%d")

    return df


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/model-performance")
def model_performance():
    y_pred = log_model.predict(X_test)

    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    precision = round(precision_score(y_test, y_pred, zero_division=0) * 100, 2)
    recall = round(recall_score(y_test, y_pred, zero_division=0) * 100, 2)
    f1 = round(f1_score(y_test, y_pred, zero_division=0) * 100, 2)

    cm = confusion_matrix(y_test, y_pred)

    class_names = [
        "Claim Under Process",
        "Patient Letter / Rebill to Secondary",
        "paid"
    ]

    labels_present = log_model.classes_
    display_labels = [class_names[i] for i in labels_present]

    total = np.sum(cm)
    total_predictions = len(y_pred)
    confusion_details = []

    for i, label in enumerate(display_labels):
        TP = int(cm[i, i])
        FN = int(np.sum(cm[i, :]) - TP)
        FP = int(np.sum(cm[:, i]) - TP)
        TN = int(total - (TP + FP + FN))

        TPR = round(TP / (TP + FN), 2) if (TP + FN) != 0 else 0
        FPR = round(FP / (FP + TN), 2) if (FP + TN) != 0 else 0
        TNR = round(TN / (TN + FP), 2) if (TN + FP) != 0 else 0
        FNR = round(FN / (FN + TP), 2) if (FN + TP) != 0 else 0

        confusion_details.append({
            "label": label,
            "TPR": TPR,
            "FPR": FPR,
            "TNR": TNR,
            "FNR": FNR
        })

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="coolwarm",
        xticklabels=display_labels,
        yticklabels=display_labels,
        linewidths=1,
        linecolor="black"
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template(
        "model_performance.html",
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        confusion_matrix=plot_url,
        confusion_details=confusion_details,
        total_predictions=total_predictions
    )
@app.route("/dashboard")
def dashboard():
    df = load_data()

    total_claims = len(df)
    status_counts = df["Claim Status"].value_counts().to_dict() if "Claim Status" in df.columns else {}
    outcome_counts = df["Current Claim Outcome"].value_counts().to_dict() if "Current Claim Outcome" in df.columns else {}

    class_labels = ["Claim Under Process", "Patient Letter / Rebill to Secondary", "paid"]

    denied_pending_count = 0
    paid_adjusted_count = 0
    under_process_count = 0
    paid_count = 0
    patient_letter_count = 0

    status_bar_chart = None
    status_pie_chart = None
    outcome_bar_chart = None
    outcome_pie_chart = None

    cm = []

    if "Claim Status" in df.columns:
        df["Claim Status"] = df["Claim Status"].astype(str).str.strip().str.title()

        denied_pending_count = len(df[df["Claim Status"].isin(["Denied", "Pending"])])
        paid_adjusted_count = len(df[df["Claim Status"].isin(["Paid", "Adjusted"])])

        status_labels = ["Denied + Pending", "Paid + Adjusted"]
        status_values = [denied_pending_count, paid_adjusted_count]

        plt.figure(figsize=(6, 4))
        plt.bar(status_labels, status_values)
        plt.title("Claim Count Comparison")
        plt.xlabel("Category")
        plt.ylabel("Number of Claims")
        plt.tight_layout()

        img1 = io.BytesIO()
        plt.savefig(img1, format="png", bbox_inches="tight")
        img1.seek(0)
        status_bar_chart = base64.b64encode(img1.getvalue()).decode()
        plt.close()

        plt.figure(figsize=(6, 4))
        plt.pie(status_values, labels=status_labels, autopct="%1.1f%%")
        plt.title("Original Status of the claim")
        plt.tight_layout()

        img2 = io.BytesIO()
        plt.savefig(img2, format="png", bbox_inches="tight")
        img2.seek(0)
        status_pie_chart = base64.b64encode(img2.getvalue()).decode()
        plt.close()

    if "Current Claim Outcome" in df.columns:
        df["Current Claim Outcome"] = df["Current Claim Outcome"].astype(str).str.strip()

        under_process_count = len(df[df["Current Claim Outcome"] == "Claim Under Process"])
        paid_count = len(df[df["Current Claim Outcome"].str.lower() == "paid"])
        patient_letter_count = len(df[df["Current Claim Outcome"] == "Patient Letter / Rebill to Secondary"])

        outcome_labels = [
            "Claim Under Process",
            "Paid",
            "Patient Letter / Rebill to Secondary"
        ]
        outcome_values = [
            under_process_count,
            paid_count,
            patient_letter_count
        ]

        plt.figure(figsize=(7, 4))
        plt.bar(outcome_labels, outcome_values)
        plt.title("New Claim Outcome Comparison")
        plt.xlabel("Outcome Category")
        plt.ylabel("Number of Claims")
        plt.xticks(rotation=15)
        plt.tight_layout()

        img3 = io.BytesIO()
        plt.savefig(img3, format="png", bbox_inches="tight")
        img3.seek(0)
        outcome_bar_chart = base64.b64encode(img3.getvalue()).decode()
        plt.close()

        plt.figure(figsize=(6, 4))
        plt.pie(outcome_values, labels=outcome_labels, autopct="%1.1f%%")
        plt.title("Current Claim Outcome")
        plt.tight_layout()

        img4 = io.BytesIO()
        plt.savefig(img4, format="png", bbox_inches="tight")
        img4.seek(0)
        outcome_pie_chart = base64.b64encode(img4.getvalue()).decode()
        plt.close()

        target_map = {
            "Claim Under Process": 0,
            "Patient Letter / Rebill to Secondary": 1,
            "paid": 2
        }

        eval_df = df.copy()
        eval_df["Target"] = eval_df["Current Claim Outcome"].replace("Paid", "paid").map(target_map)

        features = ["Allowed Amount", "Prior Used Amount"]
        existing_features = [col for col in features if col in eval_df.columns]

        if len(existing_features) == 2:
            eval_df = eval_df.dropna(subset=["Target"] + existing_features)

            if not eval_df.empty:
                X = eval_df[existing_features]
                y = eval_df["Target"].astype(int)

                y_pred = model.predict(X)
                cm_raw = confusion_matrix(y, y_pred, labels=[0, 1, 2])
                cm = cm_raw.tolist()

    return render_template(
        "dashboard.html",
        total_claims=total_claims,
        status_counts=status_counts,
        outcome_counts=outcome_counts,
        cm=cm,
        class_labels=class_labels,
        denied_pending_count=denied_pending_count,
        paid_adjusted_count=paid_adjusted_count,
        under_process_count=under_process_count,
        paid_count=paid_count,
        patient_letter_count=patient_letter_count,
        status_bar_chart=status_bar_chart,
        status_pie_chart=status_pie_chart,
        outcome_bar_chart=outcome_bar_chart,
        outcome_pie_chart=outcome_pie_chart
    )

@app.route("/patient-claims", methods=["GET", "POST"])
def patient_claims():
    df = load_data()
    risk_score = 0
    form_type = ""
    patient_id = ""
    patient_records = []
    prediction = None
    risk_level = None
    risk_score = 0
    alert_message = None
    recommendation = None
    next_action = None
    confidence_score = 0
    payment_probability = 0
    denial_probability = 0
    process_probability = 0
    assessment_data = {}

    if request.method == "POST":
        form_type = request.form.get("form_type", "")
    
        risk_score = max(0, min(100, int(float(risk_score))))

        if form_type == "search_patient":
            patient_id = request.form.get("patient_id", "").strip()

            if "Patient ID" in df.columns:
                filtered = df[df["Patient ID"].astype(str).str.strip() == patient_id].copy()

                if "Date of Service" in filtered.columns:
                    filtered["Date of Service"] = pd.to_datetime(filtered["Date of Service"], errors="coerce")
                    filtered = filtered.sort_values(by="Date of Service", ascending=True)

                patient_records = filtered.to_dict(orient="records")

        elif form_type == "predict_claim":
            patient_id = request.form.get("patient_id", "").strip()
            allowed_amount = float(request.form.get("allowed_amount", 0))
            prior_used_amount = float(request.form.get("prior_used_amount", 0))

            matched_row = None

            if patient_id and "Patient ID" in df.columns:
                patient_filtered = df[df["Patient ID"].astype(str).str.strip() == patient_id].copy()

                if not patient_filtered.empty:
                    if "Date of Service" in patient_filtered.columns:
                        patient_filtered["Date of Service"] = pd.to_datetime(
                            patient_filtered["Date of Service"], errors="coerce"
                        )
                        patient_filtered = patient_filtered.sort_values(by="Date of Service", ascending=False)

                    matched_row = patient_filtered.iloc[0]

            if matched_row is not None and "Current Claim Outcome" in matched_row:
                prediction = str(matched_row["Current Claim Outcome"]).strip()

                if prediction.lower() == "paid":
                    prediction = "paid"
                    payment_probability = 100.0
                    denial_probability = 0.0
                    process_probability = 0.0
                    confidence_score = 100.0
                    risk_score = 10.0
                    risk_level = "Low"
                    alert_message = "This claim shows a strong payment likelihood (100.0%)."
                    recommendation = "Proceed with submission and track payment posting; no immediate intervention required."
                    next_action = "Continue with standard claim workflow and monitor payment confirmation."

                elif prediction == "Patient Letter / Rebill to Secondary":
                    denial_probability = 100.0
                    process_probability = 0.0
                    payment_probability = 0.0
                    confidence_score = 100.0
                    risk_score = 95.0
                    risk_level = "High"
                    alert_message = "This claim has a high denial or rebill probability (100.0%)."
                    recommendation = "Send a patient letter with full payment details, outstanding balance, and claim explanation. Also verify if the patient has secondary insurance and rebill the claim accordingly."
                    next_action = "Initiate patient communication and rebill process to secondary insurance if applicable."

                elif prediction == "Claim Under Process":
                    process_probability = 100.0
                    denial_probability = 0.0
                    payment_probability = 0.0
                    confidence_score = 100.0
                    risk_score = 60.0
                    risk_level = "Medium"
                    alert_message = "This claim may require manual verification before final processing (100.0%)."
                    recommendation = "Recheck the claim for manual errors, validate all claim details, and correct any issues before resubmission."
                    next_action = "Send claim for manual review and correction by the insurance or billing team."

                else:
                    input_df = pd.DataFrame([{
                        "Allowed Amount": allowed_amount,
                        "Prior Used Amount": prior_used_amount
                    }])

                    prediction_value = model.predict(input_df)[0]
                    prediction = label_map.get(prediction_value, "Unknown")

                    probabilities = model.predict_proba(input_df)[0]
                    class_prob_map = dict(zip(model.classes_, probabilities))

                    process_probability = round(class_prob_map.get(0, 0) * 100, 2)
                    denial_probability = round(class_prob_map.get(1, 0) * 100, 2)
                    payment_probability = round(class_prob_map.get(2, 0) * 100, 2)

                    confidence_score = round(max(probabilities) * 100, 2)
                    risk_score = round(denial_probability + (process_probability * 0.5), 2)

                    if risk_score >= 70:
                        risk_level = "High"
                    elif risk_score >= 40:
                        risk_level = "Medium"
                    else:
                        risk_level = "Low"

                    if denial_probability >= process_probability and denial_probability >= payment_probability:
                        alert_message = f"This claim has a high denial or rebill probability ({denial_probability}%)."
                        recommendation = "Review benefit limits, validate supporting documents, and verify payer billing rules before submission."
                        next_action = "Route this claim to the billing review team for immediate validation and correction."
                    elif process_probability >= denial_probability and process_probability >= payment_probability:
                        alert_message = f"This claim may require manual verification before final processing ({process_probability}%)."
                        recommendation = "Review claim details, verify documents, and confirm eligibility before proceeding."
                        next_action = "Keep this claim in the follow-up queue and perform manual review before final submission."
                    else:
                        alert_message = f"This claim shows a strong payment likelihood ({payment_probability}%)."
                        recommendation = "Proceed with submission and track payment posting; no immediate intervention required."
                        next_action = "Continue with standard claim workflow and monitor payment confirmation."

            else:
                input_df = pd.DataFrame([{
                    "Allowed Amount": allowed_amount,
                    "Prior Used Amount": prior_used_amount
                }])

                prediction_value = model.predict(input_df)[0]
                prediction = label_map.get(prediction_value, "Unknown")

                probabilities = model.predict_proba(input_df)[0]
                class_prob_map = dict(zip(model.classes_, probabilities))

                process_probability = round(class_prob_map.get(0, 0) * 100, 2)
                denial_probability = round(class_prob_map.get(1, 0) * 100, 2)
                payment_probability = round(class_prob_map.get(2, 0) * 100, 2)

                confidence_score = round(max(probabilities) * 100, 2)
                risk_score = round(denial_probability + (process_probability * 0.5), 2)

                if risk_score >= 70:
                    risk_level = "High"
                elif risk_score >= 40:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"

                if denial_probability >= process_probability and denial_probability >= payment_probability:
                    alert_message = f"This claim has a high denial or rebill probability ({denial_probability}%)."
                    recommendation = "Review benefit limits, validate supporting documents, and verify payer billing rules before submission."
                    next_action = "Route this claim to the billing review team for immediate validation and correction."
                elif process_probability >= denial_probability and process_probability >= payment_probability:
                    alert_message = f"This claim may require manual verification before final processing ({process_probability}%)."
                    recommendation = "Review claim details, verify documents, and confirm eligibility before proceeding."
                    next_action = "Keep this claim in the follow-up queue and perform manual review before final submission."
                else:
                    alert_message = f"This claim shows a strong payment likelihood ({payment_probability}%)."
                    recommendation = "Proceed with submission and track payment posting; no immediate intervention required."
                    next_action = "Continue with standard claim workflow and monitor payment confirmation."

            patient_records = []

            assessment_data = {
                "allowed_amount": allowed_amount,
                "prior_used_amount": prior_used_amount,
                "confidence_score": confidence_score,
                "payment_probability": payment_probability,
                "denial_probability": denial_probability,
                "process_probability": process_probability,
                "next_action": next_action
            }

    return render_template(
        "patient_claims.html",
        form_type=form_type,
        patient_id=patient_id,
        patient_records=patient_records,
        prediction=prediction,
        risk_level=risk_level,
        risk_score=risk_score,
        alert_message=alert_message,
        recommendation=recommendation,
        next_action=next_action,
        confidence_score=confidence_score,
        payment_probability=payment_probability,
        denial_probability=denial_probability,
        process_probability=process_probability,
        assessment_data=assessment_data
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))