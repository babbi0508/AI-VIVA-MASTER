import streamlit as st
import random
import re

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI VIVA MASTER",
    page_icon="🎓",
    layout="centered"
)

# ---------------------------------------------------------
# QUESTION BANK
# ---------------------------------------------------------
QUESTION_BANK = {

    "Python": [
        {
            "question": "What are the main features of Python?",
            "keywords": [
                "high-level", "interpreted", "easy", "simple",
                "portable", "object-oriented", "dynamic",
                "standard library"
            ]
        },
        {
            "question": "What is a function in Python?",
            "keywords": [
                "reusable", "block", "code", "def",
                "reduce", "repetition"
            ]
        },
        {
            "question": "What is a list in Python?",
            "keywords": [
                "ordered", "mutable", "collection",
                "elements", "square", "brackets"
            ]
        },
        {
            "question": "What is a tuple in Python?",
            "keywords": [
                "ordered", "immutable", "collection",
                "elements", "parentheses"
            ]
        },
        {
            "question": "What is a dictionary in Python?",
            "keywords": [
                "key", "value", "pairs", "mutable",
                "collection"
            ]
        },
        {
            "question": "What is inheritance?",
            "keywords": [
                "class", "properties", "methods",
                "parent", "child", "reuse"
            ]
        },
        {
            "question": "What is Pandas?",
            "keywords": [
                "python", "library", "data",
                "analysis", "manipulation", "tabular"
            ]
        },
        {
            "question": "What is a dataset?",
            "keywords": [
                "collection", "data", "training",
                "testing", "analysis", "machine learning"
            ]
        },
        {
            "question": "What is data visualization?",
            "keywords": [
                "data", "charts", "graphs",
                "visual", "patterns", "trends"
            ]
        },
        {
            "question": "What is correlation?",
            "keywords": [
                "relationship", "variables", "strength",
                "direction", "positive", "negative"
            ]
        }
    ],

    "Machine Learning": [
        {
            "question": "What is Machine Learning?",
            "keywords": [
                "machine", "learning", "data",
                "patterns", "prediction", "algorithm"
            ]
        },
        {
            "question": "What is supervised learning?",
            "keywords": [
                "labeled", "data", "input",
                "output", "training", "prediction"
            ]
        },
        {
            "question": "What is unsupervised learning?",
            "keywords": [
                "unlabeled", "data", "patterns",
                "groups", "clustering"
            ]
        },
        {
            "question": "What is classification?",
            "keywords": [
                "categorical", "class", "labels",
                "prediction", "classification"
            ]
        },
        {
            "question": "What is regression?",
            "keywords": [
                "continuous", "value", "prediction",
                "dependent", "variable"
            ]
        },
        {
            "question": "What is overfitting?",
            "keywords": [
                "training", "data", "new",
                "unseen", "poor", "generalization"
            ]
        },
        {
            "question": "What is underfitting?",
            "keywords": [
                "simple", "model", "training",
                "data", "poor", "performance"
            ]
        }
    ],

    "Artificial Intelligence": [
        {
            "question": "What is Artificial Intelligence?",
            "keywords": [
                "machines", "human", "intelligence",
                "tasks", "learning", "decision"
            ]
        },
        {
            "question": "What is an AI model?",
            "keywords": [
                "data", "patterns", "prediction",
                "algorithm", "trained"
            ]
        },
        {
            "question": "What is NLP?",
            "keywords": [
                "language", "human", "computer",
                "text", "speech", "processing"
            ]
        },
        {
            "question": "What is Computer Vision?",
            "keywords": [
                "images", "videos", "computer",
                "visual", "objects", "recognition"
            ]
        }
    ],

    "Data Science": [
        {
            "question": "What is Data Science?",
            "keywords": [
                "data", "statistics", "programming",
                "machine learning", "analysis", "insights"
            ]
        },
        {
            "question": "What is data analysis?",
            "keywords": [
                "data", "clean", "analyze",
                "patterns", "insights", "decision"
            ]
        },
        {
            "question": "What is data visualization?",
            "keywords": [
                "data", "charts", "graphs",
                "visual", "patterns", "trends"
            ]
        },
        {
            "question": "What is correlation?",
            "keywords": [
                "relationship", "variables", "strength",
                "direction", "positive", "negative"
            ]
        }
    ],

    "Java": [
        {
            "question": "What is Java?",
            "keywords": [
                "programming", "object-oriented",
                "class", "platform", "independent", "JVM"
            ]
        },
        {
            "question": "What is OOP?",
            "keywords": [
                "object", "class", "inheritance",
                "encapsulation", "polymorphism", "abstraction"
            ]
        },
        {
            "question": "What is inheritance in Java?",
            "keywords": [
                "class", "parent", "child",
                "properties", "methods", "reuse"
            ]
        },
        {
            "question": "What is encapsulation?",
            "keywords": [
                "data", "methods", "class",
                "private", "access", "security"
            ]
        }
    ]
}

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current" not in st.session_state:
    st.session_state.current = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "started" not in st.session_state:
    st.session_state.started = False

if "results" not in st.session_state:
    st.session_state.results = []

# ---------------------------------------------------------
# SCORING FUNCTION
# ---------------------------------------------------------
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_score(answer, keywords):
    if not answer.strip():
        return 0, 0

    answer_clean = normalize_text(answer)

    matched = 0

    for keyword in keywords:
        keyword_clean = normalize_text(keyword)

        # Multi-word keywords
        if " " in keyword_clean:
            if keyword_clean in answer_clean:
                matched += 1
        else:
            words = answer_clean.split()

            # exact word match
            if keyword_clean in words:
                matched += 1

    percentage = (matched / len(keywords)) * 100

    # More forgiving scoring
    if percentage >= 70:
        score = 5
    elif percentage >= 50:
        score = 4
    elif percentage >= 30:
        score = 3
    elif percentage > 0:
        score = 2
    else:
        score = 1

    return score, round(percentage)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🎓 AI VIVA MASTER")
st.write("Practice your viva questions and improve your confidence 🚀")

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("⚙️ Viva Settings")

topic = st.sidebar.selectbox(
    "Choose Topic",
    list(QUESTION_BANK.keys())
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

question_count = st.sidebar.slider(
    "Number of Questions",
    min_value=3,
    max_value=min(10, len(QUESTION_BANK[topic])),
    value=3
)

# ---------------------------------------------------------
# START VIVA
# ---------------------------------------------------------
if not st.session_state.started:

    st.info("Choose your topic and start your viva!")

    if st.button("🚀 Start Viva", use_container_width=True):

        selected_questions = random.sample(
            QUESTION_BANK[topic],
            question_count
        )

        st.session_state.questions = selected_questions
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.results = []
        st.session_state.started = True

        st.rerun()

# ---------------------------------------------------------
# VIVA SCREEN
# ---------------------------------------------------------
else:

    current = st.session_state.current
    total = len(st.session_state.questions)

    if current < total:

        question_data = st.session_state.questions[current]

        st.progress((current) / total)

        st.subheader(
            f"Question {current + 1} of {total}"
        )

        st.markdown(
            f"### {question_data['question']}"
        )

        answer = st.text_area(
            "Your Answer",
            height=180,
            placeholder="Type your answer here...",
            key=f"answer_box_{current}"
        )

        if st.button(
            "✅ Submit Answer",
            use_container_width=True
        ):

            score, percentage = calculate_score(
                answer,
                question_data["keywords"]
            )

            st.session_state.score += score

            st.session_state.results.append({
                "question": question_data["question"],
                "answer": answer,
                "score": score,
                "percentage": percentage
            })

            if current + 1 < total:
                st.session_state.current += 1
                st.rerun()
            else:
                st.session_state.current = total
                st.rerun()

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------
    else:

        total_score = total * 5
        final_score = st.session_state.score

        percentage = round(
            (final_score / total_score) * 100
        )

        st.success("🎉 Viva Completed!")

        st.metric(
            "Final Score",
            f"{final_score}/{total_score}"
        )

        st.metric(
            "Percentage",
            f"{percentage}%"
        )

        if percentage >= 80:
            st.success(
                "Excellent! Your viva preparation is strong."
            )
        elif percentage >= 60:
            st.info(
                "Good job! Keep practicing to improve."
            )
        else:
            st.warning(
                "Keep practicing. You can improve!"
            )

        st.markdown("## 📋 Question-wise Results")

        for i, result in enumerate(
            st.session_state.results,
            start=1
        ):

            st.markdown(
                f"### Q{i}. {result['question']}"
            )

            st.write(
                f"**Score:** {result['score']}/5"
            )

            st.write(
                f"**Your Answer:** {result['answer']}"
            )

            st.write(
                f"**Keywords matched:** "
                f"{result['percentage']}%"
            )

            st.divider()

        if st.button(
            "🔄 Start New Viva",
            use_container_width=True
        ):

            st.session_state.questions = []
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.results = []
            st.session_state.started = False

            st.rerun()