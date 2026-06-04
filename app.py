from reportlab.pdfgen import canvas
from groq import Groq
import streamlit as st
import pdfplumber
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Powered Mock Interview & Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #00FFAA;
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GROQ CLIENT ----------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- SESSION STATE ----------------
if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# ---------------- TITLE ----------------
st.markdown("""
<h1>
🤖 AI Mock Interview Platform
</h1>
""", unsafe_allow_html=True)

st.write(
    "Upload your resume and get "
    "AI-generated interview questions, "
    "ATS score, and answer evaluation."
)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "AI Model",
        "Llama 3.3"
    )

with col2:
    st.metric(
        "Resume Analysis",
        "Enabled ✅"
    )

with col3:
    st.metric(
        "Mock Interview",
        "Ready 🚀"
    )
# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("🚀 About Project")

    st.info("""
    AI Mock Interview Platform

    Features:
    ✅ Resume Analysis  
    ✅ ATS Score  
    ✅ Job Description Matching  
    ✅ AI Interview Questions  
    ✅ AI Answer Evaluation  
    ✅ PDF Report Download
    """)

    st.divider()

    st.subheader("🛠 Tech Stack")

    st.write("""
    - Python
    - Streamlit
    - Groq API
    - PDFPlumber
    - ReportLab
    """)

    st.divider()

    st.success(
        "Built by Anjleena Gupta ✨"
    )

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type="pdf"
)

# ---------------- GLOBAL VARIABLES ----------------
detected_skills = []
resume_text = ""

required_skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Data Structures",
    "DBMS",
    "C++",
    "Java",
    "Git"
]

skills = [
    "Python",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "C++",
    "Java",
    "DSA",
    "NLP",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "DBMS",
    "OOPs"
]

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_resume_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# ---------------- RESUME ANALYSIS ----------------
if uploaded_file is not None:

    resume_text = extract_resume_text(
        uploaded_file
    )

    st.success(
        "Resume Uploaded Successfully!"
    )

    st.subheader(
        "📄 Extracted Resume Text"
    )

    st.text_area(
        "Resume Content",
        resume_text,
        height=250
    )

    # Detect Skills
    for skill in skills:
        if (
            skill.lower()
            in resume_text.lower()
        ):
            detected_skills.append(
                skill
            )

    st.subheader(
        "🛠 Detected Skills"
    )

    if detected_skills:
        for skill in detected_skills:
            st.write(
                f"✅ {skill}"
            )
    else:
        st.write(
            "No skills detected"
        )

    # ATS SCORE
    st.subheader(
        "📊 ATS Resume Score"
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(
                skill
            )
        else:
            missing_skills.append(
                skill
            )

    score = int(
        (
            len(matched_skills)
            / len(required_skills)
        ) * 100
    )

    st.progress(score / 100)

    st.metric(
        label="ATS Resume Score",
        value=f"{score}%"
    )

    st.subheader(
        "Matched Skills"
    )

    for skill in matched_skills:
        st.success(skill)

    st.subheader(
        "Missing Skills"
    )

    for skill in missing_skills:
        st.error(skill)

    # Resume Suggestions
    st.subheader(
        "📌 Resume Suggestions"
    )

    if len(detected_skills) < 5:
        st.write(
            "✅ Add more technical skills"
        )

    if "Projects" not in resume_text:
        st.write(
            "✅ Add a Projects section"
        )

    if "Internship" not in resume_text:
        st.write(
            "✅ Add internship or practical experience"
        )

    if (
        "certification"
        not in resume_text.lower()
    ):
        st.write(
            "✅ Add certifications"
        )

    st.write(
        "✅ Add measurable achievements"
    )
    if score >= 80:
        st.success("🔥 Strong Resume")
    elif score >= 50:
        st.warning("⚡ Good Resume, needs improvement")
    else:
        st.error("❌ Weak Resume")
# ---------------- JOB DESCRIPTION ----------------
st.divider()

st.subheader(
    "📄 Job Description Matching"
)

job_description = st.text_area(
    "Paste Job Description Here"
)

if st.button(
    "Check Resume Match"
):

    if uploaded_file is None:
        st.warning(
            "Please upload resume first"
        )

    else:

        jd_skills = [
            "Python",
            "Machine Learning",
            "SQL",
            "DBMS",
            "Java",
            "C++",
            "Git",
            "Deep Learning",
            "NLP",
            "Data Structures"
        ]

        matched = []
        missing = []

        resume_skills_text = (
            " ".join(
                detected_skills
            )
        )

        for skill in jd_skills:

            combined_text = (
                resume_skills_text.lower()
                + job_description.lower()
            )

            if (
                skill.lower()
                in combined_text
            ):
                matched.append(
                    skill
                )
            else:
                missing.append(
                    skill
                )

        match_score = int(
            (
                len(matched)
                / len(jd_skills)
            ) * 100
        )

        st.metric(
            label="JD Match Score",
            value=f"{match_score}%"
        )

        st.progress(
            match_score / 100
        )

# ---------------- QUESTIONS ----------------
st.divider()

st.subheader(
    "🎯 Generate Interview Questions"
)

role = st.selectbox(
    "Choose Role",
    [
        "AI Engineer",
        "Data Scientist",
        "Software Engineer",
        "Machine Learning Engineer",
        "Data Analyst",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer"
    ]
)

difficulty = st.selectbox(
    "Select Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

if st.button(
    "Generate Questions"
):

    if uploaded_file is None:
        st.warning(
            "Please upload resume first"
        )

    else:

        
        prompt = f"""
You are a technical interviewer.

Generate 5 interview questions.

Role: {role}

Candidate Skills:
{detected_skills}

Difficulty: {difficulty}

Rules:
- Questions should match role and skills
- Include technical + scenario-based questions
- Only numbered questions
- No explanations
"""

        try:

            with st.spinner(
                "Generating interview questions..."
            ):

                response = (
                    client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                )

                st.session_state.generated_questions = (
                    response.choices[0]
                    .message.content
                )

        except Exception as e:
            st.error(
                f"Error: {e}"
            )

# ---------------- DISPLAY QUESTIONS ----------------
if st.session_state.generated_questions:

    st.download_button(
        label="Download Questions",
        data=st.session_state.generated_questions,
        file_name="interview_questions.txt",
        mime="text/plain"
    )

    st.subheader(
        "Interview Questions"
    )

    st.write(
        st.session_state.generated_questions
    )
st.subheader("🧠 Answer Evaluation")

user_answer = st.text_area(
    "Write your answer here"
)

if st.button("Evaluate Answer"):

    evaluation_prompt = f"""
    You are an expert technical interviewer.

    Evaluate this candidate answer.

    Question:
    {st.session_state.generated_questions}

    Candidate Answer:
    {user_answer}

    Give:

    1. Technical Accuracy score out of 10
    2. Communication score out of 10
    3. Confidence score out of 10
    4. Overall Rating out of 10
    5. Strengths
    6. Weaknesses
    7. Improvement Tips
    8. Short Feedback
    """

    try:

        with st.spinner(
            "Evaluating answer..."
        ):

            evaluation = (
                client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": evaluation_prompt
                        }
                    ]
                )
            )

            feedback = (
                evaluation
                .choices[0]
                .message.content
            )

            st.session_state.feedback = (
                feedback
            )

            st.subheader(
                "Evaluation Result"
            )

            st.write(
                feedback
            )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

st.divider()   

st.subheader("Download Interview Report")
if st.button("Generate PDF Report"):
    file_name = "Interview_Report.pdf" 
    c = canvas.Canvas(file_name) 
    c.drawString(
        100,
        800,
        "AI Mock Interview Report"
        )
    c.drawString(
        100,
        770,
        f"Detected Skills: {', '.join(detected_skills)}" )
    c.drawString(
        100,
        740, 
        "Generated Questions:" ) 
    c.drawString( 100, 
                 720,
                 st.session_state.generated_questions ) 
    feedback_text = st.session_state.get( 
                 "feedback",
                 "No feedback available"
                 ) 
    c.drawString(
        100,
        680,
        "Evaluation Feedback:" )
    c.drawString( 
                 100,
                 660,
                 feedback_text ) 
    c.save() 
    with open(file_name, "rb") as pdf_file: 
        st.download_button( 
            label="Download Report",
            data=pdf_file,
            file_name=file_name,
            mime="application/pdf" )
st.divider()

st.markdown(
    """
    <hr>
    <center>
    Made with ❤️ by <b>Anjleena Gupta</b><br>
    AI-Powered Mock Interview Platform
    </center>
    """,
    unsafe_allow_html=True
)

