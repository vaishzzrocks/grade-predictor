import streamlit as st
import pandas as pd

st.title("Grade Predictor App")

all_scores = {}

num_levels = st.number_input(
    "How many levels of study do you want to enter?",
    min_value=1,
    step=1
)

previous_subjects = []

for i in range(num_levels):
    st.header(f"Level {i + 1}")

    level = st.text_input(
        "Level of study (eg. Sec 1, Sec 2, JC1)",
        key=f"level_{i}"
    )

    num_exams = st.number_input(
        f"How many exams for {level}?",
        min_value=1,
        step=1,
        key=f"num_exams_{i}"
    )

    exam_names = []

    for j in range(num_exams):
        exam = st.text_input(
            f"Exam name {j + 1} for {level} (eg. SA1,WA1, End of Year Exam)",
            key=f"exam_{i}_{j}"
        )

        if exam:
            exam_names.append(exam)

    if i == 0:
        use_previous_subjects = "No"
    else:
        use_previous_subjects = st.radio(
            f"Do you want {level} to use the same subjects as the previous level?",
            ["Yes", "No"],
            key=f"use_previous_subjects_{i}"
        )

    if use_previous_subjects == "Yes":
        subjects = previous_subjects
        st.write("Using the same subjects as the previous level:")
        st.write(", ".join(subjects))

    else:
        num_subjects = st.number_input(
            f"How many subjects for {level}?",
            min_value=1,
            step=1,
            key=f"num_subjects_{i}"
        )

        subjects = []

        for s in range(num_subjects):
            subject = st.text_input(
                f"Subject {s + 1} for {level}",
                key=f"subject_{i}_{s}"
            )

            if subject:
                subjects.append(subject)

    previous_subjects = subjects

    if level:
        all_scores[level] = {}

    for subject in subjects:
        scores = []

        for exam in exam_names:
            score = st.number_input(
                f"Score for {subject} in {exam}",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                key=f"score_{i}_{subject}_{exam}"
            )

            scores.append(score)

        if level and subject:
            all_scores[level][subject] = scores

    if level and exam_names:
        st.subheader(f"{level} Results")

        table_data = []

        for subject, scores in all_scores[level].items():
            row = {"Subject": subject}

            for exam, score in zip(exam_names, scores):
                row[exam] = score

            table_data.append(row)

        if table_data:
            st.dataframe(pd.DataFrame(table_data))


st.divider()

target_exam = st.text_input("What exam do you want to predict a score for?")

available_levels = list(all_scores.keys())

chosen_levels = st.multiselect(
    "Which levels do you want to use for prediction?",
    available_levels
)

if st.button("Predict Scores"):
    subject_scores = {}

    for level in chosen_levels:
        for subject in all_scores[level]:
            if subject not in subject_scores:
                subject_scores[subject] = []

            for score in all_scores[level][subject]:
                subject_scores[subject].append(score)

    st.subheader(f"Predicted Scores for {target_exam}")

    prediction_data = []

    for subject, scores in subject_scores.items():
        if len(scores) > 0:
            average_score = sum(scores) / len(scores)
            latest_score = scores[-1]

            predicted_score = latest_score * 0.7 + average_score * 0.3

            prediction_data.append({
                "Subject": subject,
                "Predicted Score": f"{predicted_score:.1f}%"
            })

    if prediction_data:
        st.table(pd.DataFrame(prediction_data))
    else:
        st.warning("Please enter your levels, subjects, scores, and choose at least one level.")