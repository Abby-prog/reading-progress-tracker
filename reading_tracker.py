import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Reading Progress Tracker", layout="wide")

# --- Title ---
st.title("?? Reading Progress Tracker")
st.write("Track a child's reading development over time with visual insights, strategies, and recommended activities.")

# --- Stage Labels and Colors ---
stage_labels = [
    ("Non-Reader", 0, 4, "#f8d7da"),
    ("Pre-Emergent", 5, 7, "#ffeeba"),
    ("Emergent", 8, 10, "#d4edda"),
    ("Progressive", 11, 13, "#c3e6cb"),
    ("Proficient", 14, 16, "#bee5eb"),
    ("High Proficient", 17, 18, "#d1ecf1"),
    ("Exceeding Reader", 19, 19, "#d6d8d9")
]

# --- Activities Mapping ---
activities = {
    "Non-Reader": [
        "Read aloud daily using picture books.",
        "Introduce alphabet songs.",
        "Point to words as you read."
    ],
    "Pre-Emergent": [
        "Practice letter-sound matching.",
        "Play rhyming word games.",
        "Use flashcards for sight words."
    ],
    "Emergent": [
        "Encourage reading simple sentences.",
        "Have them retell short stories.",
        "Highlight repeated words in books."
    ],
    "Progressive": [
        "Introduce short chapter books.",
        "Discuss story plots and characters.",
        "Encourage writing short summaries."
    ],
    "Proficient": [
        "Encourage independent reading daily.",
        "Explore different genres together.",
        "Have discussions about themes."
    ],
    "High Proficient": [
        "Analyze author’s writing style.",
        "Write alternative story endings.",
        "Introduce age-appropriate classic literature."
    ],
    "Exceeding Reader": [
        "Encourage book reviews and essays.",
        "Explore literature analysis.",
        "Engage in debates on book themes."
    ]
}

# --- Input Section ---
st.header("?? Input Assessment Data")

num_entries = st.number_input("How many assessments do you want to enter?", min_value=1, max_value=20, value=4)

dates = []
scores = []
strategies = []

for i in range(num_entries):
    st.subheader(f"Assessment #{i + 1}")
    col1, col2, col3 = st.columns(3)
    with col1:
        date_str = st.date_input(f"Date for Assessment #{i + 1}", key=f"date_{i}")
        dates.append(date_str)
    with col2:
        score = st.slider(f"Reading Score (0–19)", min_value=0, max_value=19, key=f"score_{i}")
        scores.append(score)
    with col3:
        strategy = st.text_area(f"Strategy used during this stage", key=f"strat_{i}")
        strategies.append(strategy)

# --- Plot Graph ---
if st.button("?? Generate Progress Tracker") and dates:
    fig, ax = plt.subplots(figsize=(14, 6))

    # Convert dates
    dates_dt = [datetime.combine(d, datetime.min.time()) for d in dates]

    # Plot reading score line
    ax.plot(dates_dt, scores, marker='o', color='darkblue', linewidth=2)

    # Add background stage bands
    for label, low, high, color in stage_labels:
        ax.axhspan(low, high, facecolor=color, alpha=0.4)

    # Annotate scores and strategies
    for i, (d, s, strat) in enumerate(zip(dates_dt, scores, strategies)):
        ax.text(d, s + 0.4, str(s), ha='center', fontsize=9)
        if strat:
            ax.text(d, s - 1.5, strat, ha='center', fontsize=7, rotation=15,
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    # Arrows for score change
    for i in range(1, len(scores)):
        color = "green" if scores[i] > scores[i-1] else "red" if scores[i] < scores[i-1] else "gray"
        ax.annotate("",
                    xy=(dates_dt[i], scores[i]),
                    xytext=(dates_dt[i-1], scores[i-1]),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=color))

    # Formatting
    ax.set_title("Reading Progress Over Time", fontsize=16)
    ax.set_xlabel("Assessment Date", fontsize=12)
    ax.set_ylabel("Reading Score (0–19)", fontsize=12)
    ax.set_ylim(0, 20)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.autofmt_xdate()

    st.pyplot(fig)

    # --- Auto Stage Detection ---
    latest_score = scores[-1]
    detected_stage = None
    for label, low, high, _ in stage_labels:
        if low <= latest_score <= high:
            detected_stage = label
            break

    # --- Activities Section ---
    st.header("?? Suggested Activities Based on Latest Stage")
    if detected_stage:
        st.subheader(f"?? Latest Stage: **{detected_stage}** (Score: {latest_score})")
        st.markdown("Here are activities tailored for this stage:")
        for act in activities[detected_stage]:
            st.markdown(f"- {act}")
    else:
        st.warning("Unable to detect stage for the latest score.")