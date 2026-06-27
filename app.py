import streamlit as st
import pandas as pd

st.set_page_config(page_title="Exam Progress Tracker", layout="centered")
st.title("📊 Exam Progress Tracker")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["subject", "mark", "mistakes"])

class Progress:
    def __init__(self, df):
        self.df = df

    def add_entry(self, subject, mark, mistakes):
        new_row = {"subject": subject, "mark": mark, "mistakes": mistakes}
        self.df.loc[len(self.df)] = new_row

    def calculate(self, mistake, mark):
        mistake_values = {'c': 4, 'n': 3, 'l': 2, 'p': 1, 'x': 0}
        mark_gap = ((25 - mark) / 25) * 10
        total = sum(mistake_values[m] for m in mistake)
        mistake_weight = min(total / 10 * 10, 10)
        score = (mark_gap * 0.5) + (mistake_weight * 0.5)
        return score

    def band(self, score):
        if score >= 4:
            return "Needs serious study"
        elif score >= 3:
            return "Need improvement"
        else:
            return "Keep this momentum"

    def analyse(self):
        results = []
        for _, row in self.df.iterrows():
            score = self.calculate(row["mistakes"], row["mark"])
            results.append({
                "Subject": row["subject"],
                "Marks": row["mark"],
                "Points": round(score, 2),
                "Suggestion": self.band(score),
            })
        return pd.DataFrame(results)


p = Progress(st.session_state.df)

MISTAKE_OPTIONS = {
    "c": "Conceptual",
    "p": "Exam pressure",
    "n": "Not studied",
    "l": "Lack of practise",
    "x": "Nothing",
}

st.subheader("Add Subjects, Marks and Mistakes")

with st.form("add_subject_form", clear_on_submit=True):
    subject = st.text_input("Subject")
    mark = st.number_input("Mark (out of 25)", min_value=0.0, max_value=25.0, step=0.1)

    st.write("Mistakes")
    cols = st.columns(len(MISTAKE_OPTIONS))
    selected = []
    for col, (code, label) in zip(cols, MISTAKE_OPTIONS.items()):
        with col:
            if st.checkbox(f"{code} - {label}", key=f"chk_{code}"):
                selected.append(code)

    submitted = st.form_submit_button("Add Subject")

    if submitted:
        if not subject.strip():
            st.error("Please enter a subject name.")
        elif not selected:
            st.error("Please select at least one mistake.")
        else:
            p.add_entry(subject.strip(), float(mark), selected)
            st.success(f"{subject} added successfully.")

st.subheader("Your Progress")

col1, col2 = st.columns(2)
show_result = col1.button("Show Result", use_container_width=True)
show_graph = col2.button("Show Graph", use_container_width=True)

if st.session_state.df.empty:
    st.info("No data yet — add subjects above to get started.")
else:
    if show_result:
        result_df = p.analyse()
        st.dataframe(result_df, use_container_width=True, hide_index=True)

    if show_graph:
        chart_df = st.session_state.df.set_index("subject")["mark"]
        st.bar_chart(chart_df)

    with st.expander("View raw data"):
        st.dataframe(st.session_state.df, use_container_width=True, hide_index=True)

st.divider()
if st.button("🗑️ Clear all data"):
    st.session_state.df = pd.DataFrame(columns=["subject", "mark", "mistakes"])
    st.rerun()
st.divider()


st.divider()
st.markdown("**Follow me on Instagram:** [@__sidharthh._](https://instagram.com/__sidharthh._)")    
