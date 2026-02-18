import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ MUST BE FIRST
st.set_page_config(
    page_title="GradGenie AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>

/* ===============================
   GOOGLE FONTS
================================ */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ===============================
   GLOBAL THEME
================================ */
html, body, [class*="css"]  {
    font-family: 'DM Sans', sans-serif;
    background: #0a0a0f;
    color: #e8e6f0;
}

/* ===============================
   HEADLINES (Premium Serif)
================================ */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: -0.02em;
}

/* Gradient Hero Title */
.hero-title {
    font-size: 48px;
    font-weight: 600;
    background: linear-gradient(135deg, #ffffff 30%, #c77dff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.hero-sub {
    color: #7a7890;
    font-size: 15px;
}

/* ===============================
   BADGE PILLS
================================ */
.badge-row {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 25px;
}

.badge {
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
}

.badge-branch {
    background: rgba(124,92,252,0.15);
    border: 1px solid rgba(124,92,252,0.4);
    color: #c77dff;
}

.badge-mode {
    background: rgba(240,192,96,0.12);
    border: 1px solid rgba(240,192,96,0.3);
    color: #f0c060;
}

/* ===============================
   INPUT BOX
================================ */
textarea, .stTextInput>div>div>input {
    background: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #e0e0e0 !important;
    color: #000000 !important;
    height: 45px !important;
    min-height: 45px !important;
    max-height: 45px !important;
    font-size: 14px !important;
    padding: 12px 20px 12px 40px !important;
    overflow: hidden !important;
    outline: none !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15) !important;
    transform: translateY(-2px) !important;
    transition: all 0.25s ease !important;
}
textarea:hover {
    box-shadow: 0 4px 10px rgba(0,0,0,0.18) !important;
}

textarea:focus {
    box-shadow: 0 4px 10px rgba(0,0,0,0.18) !important;
}

textarea::placeholder {
    color: #999999 !important;
    opacity: 1 !important;
}
            /* Kill Streamlit's default red/pink focus border completely */
div[data-testid="stTextArea"] textarea:focus {
    border-color: #000000 !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15) !important;
    outline: none !important;
}

div[data-testid="stTextArea"] textarea:hover {
    border-color: #000000 !important;
    outline: none !important;
}

div[data-testid="stTextArea"] > div {
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stTextArea"] > div:focus-within {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
            /* Allow shadow to show fully outside the container */
div[data-testid="stTextArea"] {
    margin-top: -25px !important;
    overflow: visible !important;
    padding-bottom: 8px !important;
}

div[data-testid="stTextArea"] > div {
    border: none !important;
    box-shadow: none !important;
    overflow: visible !important;
    padding-bottom: 6px !important;
}


/* ===============================
   GENERATE BUTTON (Premium)
================================ */
div.stButton > button {
    background: linear-gradient(135deg, #c0c0c0 0%, #2d2d2d 100%);
    color: white;
    border-radius: 14px;
    padding: 0.6rem 1.6rem;
    font-weight: 500;
    border: none;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    transition: all 0.25s ease;
}

/* Hover Lift */
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.55);
}

/* ===============================
   AI OUTPUT CARD
================================ */
.ai-card {
    background: #16162a;
    border-radius: 18px;
    padding: 20px 24px;
    border: 1px solid rgba(124,92,252,0.25);
    box-shadow: 0 0 0 1px rgba(124,92,252,0.05), 0 10px 30px rgba(0,0,0,0.4);
    margin-top: 20px;
}

/* AI Heading inside output */
.ai-card h3 {
    color: #c77dff;
    margin-bottom: 10px;
}
            
/* Style headings inside st.success response box */
div[data-testid="stAlert"] h1,
div[data-testid="stAlert"] h2,
div[data-testid="stAlert"] h3 {
    font-family: sans-serif !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
    margin-top: 16px !important;
    margin-bottom: 6px !important;
}

div[data-testid="stAlert"] h1 {
    font-size: 24px !important;
}

div[data-testid="stAlert"] h2 {
    font-size: 20px !important;
}

div[data-testid="stAlert"] h3 {
    font-size: 18px !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] li {
    font-size: 16px !important;
    font-family: sans-serif !important;
    color: #2d2d2d !important;
}


/* ===============================
   STATUS DOT
================================ */
.status {
    font-size: 12px;
    color: #7a7890;
    margin-top: 15px;
}

.status-dot {
    height: 8px;
    width: 8px;
    background-color: #4ade80;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 8px #4ade80;
}
            

            /* Remove gap between label and text area */
div[data-testid="stTextArea"] {
    margin-top: -25px !important;
}
            

/* Response Container */
.response-container {
    background: #f9f9fb;
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    padding: 24px 28px;
    margin-top: 24px;
}

/* Response Header */
.response-header {
    font-family: sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 10px;
}

/* Placeholder text */
.response-placeholder {
    font-family: sans-serif;
    font-size: 14px;
    color: #888888;
    font-style: italic;
    margin-bottom: 0px;
}

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 20px 0;
}

/* Try Asking Header */
.try-header {
    font-family: sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 12px;
}

/* Prompt Pill */
.prompt-pill {
    display: inline-block;
    background: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 13px;
    font-family: sans-serif;
    color: #222222;
    margin: 4px 4px 4px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

            /* Remove top empty space only - sidebar safe */
.block-container {
    padding-top: 1rem !important;
    margin-top: 0rem !important;
}

div[data-testid="stAppViewContainer"] > section:first-child {
    padding-top: 0rem !important;
}
            
           /* Nuclear option - remove all sidebar top space */
[data-testid="stSidebar"] > div:nth-child(1) {
    padding-top: 0 !important;
}

[data-testid="stSidebar"] > div:nth-child(2) {
    padding-top: 0 !important;
}

[data-testid="stSidebar"] > div > div {
    padding-top: 0 !important;
    gap: 0 !important;
}

[data-testid="stSidebarContent"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
            


</style>
""", unsafe_allow_html=True)


# Load env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Title
st.title("🎓GradGenie AI")
st.markdown(
    "<p style='font-weight:700; font-size:20px; color:#000000; font-family:sans-serif;'>Your Smart Academic Companion</p>",
    unsafe_allow_html=True
)

# ✅ CHANGED: Bold "Navigation" using markdown with default system font
st.sidebar.markdown(
    "<h1 style='text-align:left; font-family:sans-serif; font-size:24px; font-weight:700; color:#000000;'>GradGenie AI🎓</h1>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='font-size:12px; color:#888888; font-family:sans-serif; margin-top:-15px;'>AI-Powered Guidance For Smarter Studying</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='font-weight:700; font-size:20px; color:#000000; font-family:sans-serif;'>Navigation</p>",
    unsafe_allow_html=True
    
)
st.sidebar.markdown(
    "<p style='font-weight:700; font-size:17px; color:#000000; font-family:sans-serif; margin-bottom:-20px;'>Select Branch</p>",
    unsafe_allow_html=True
)
branch = st.sidebar.selectbox("", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])

st.sidebar.markdown(

    """
    <div style='position:fixed; bottom:20px; left:0; width:250px; font-size:11px; color:#888888; font-family:sans-serif; text-align:center;'>
        © 2026 Shashivardan Jarpati<br>All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)


# Branch intelligence layer
branch_context = {
    "CSE": """
Focus on computer science topics:
- Operating Systems
- Databases
- Computer Networks
- AI/ML
- Programming
Use software, algorithms, and coding examples.
""",
    "ECE": """
Use electronics and communication context:
- Circuits and Signals
- Embedded Systems
- Microprocessors
- Communication Systems
Use waveform, hardware, and signal-based examples.
""",
    "EEE": """
Focus on electrical engineering:
- Electrical Machines
- Power Systems
- Control Systems
- Power Electronics
Use electricity, voltage, motor, and grid-based examples.
""",
    "MECH": """
Use mechanical engineering context:
- Thermodynamics
- Fluid Mechanics
- Heat Transfer
- Manufacturing
Use machines, engines, and physical system examples.
""",
    "CIVIL": """
Use civil engineering context:
- Structures
- Construction
- Concrete Technology
- Soil Mechanics
- Transportation
Use buildings, loads, and infrastructure examples.
"""
}

selected_branch_context = branch_context.get(branch, "")

st.sidebar.markdown(
    "<p style='font-weight:700; font-size:17px; color:#000000; font-family:sans-serif; margin-bottom:-20px;'>Select Mode</p>",
    unsafe_allow_html=True
)
mode = st.sidebar.radio("", ["AI Tutor", "Backlog Rescue", "Doubt Solver", "Smart Exam Mode"])

# Backlog slider
days_left = None
if mode == "Backlog Rescue":
    days_left = st.sidebar.slider(
        "Days left for exam",
        min_value=1,
        max_value=30,
        value=7
    )

exam_type = None
if mode == "Smart Exam Mode":
    exam_type = st.sidebar.selectbox(
        "Select Exam Output Type",
        [
            "5-Mark Answer",
            "10-Mark Answer",
            "Quick Revision",
            "Important Topics",
            "Last-Minute Strategy"
        ]
    )

# ✅ CHANGED: Bold "Branch" and "Mode" with default system font
st.markdown(
    f"<p style='font-weight:700; font-size:18px; color:#000000; font-family:sans-serif;'>Branch: {branch}</p>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='font-weight:700; font-size:18px; color:#000000; font-family:sans-serif;'>Mode: {mode}</p>",
    unsafe_allow_html=True
)

# User input
st.markdown(
    "<p style='font-weight:700; font-size:17px; color:#000000; font-family:sans-serif; margin-bottom:4px;'>Enter your topic or question:</p>",
    unsafe_allow_html=True
)
user_input = st.text_area("", placeholder="🔍  Ask anything about your subject...")

# Button click
if st.button("Generate AI Response"):
    if user_input:
        with st.spinner("GradGenie thinking... 🤖"):

            if mode == "AI Tutor":
                prompt = f"""
You are an academic tutor helping engineering students prepare for exams.
Branch: {branch}
Branch Context: {selected_branch_context}
Explain the topic in:
- Clear exam-ready language
- Structured format
- Concise definitions
- Key points for scoring marks
Topic: {user_input}
"""

            elif mode == "Backlog Rescue":
                prompt = f"""
You are an exam recovery strategist helping an engineering student PASS a subject in limited time.
Branch: {branch}
Branch Context: {selected_branch_context}
Subject: {user_input}
Days left: {days_left}
Give a strict, practical study plan.
"""

            elif mode == "Doubt Solver":
                prompt = f"""
Explain the following concept in simple terms for an engineering student.
Branch: {branch}
Branch Context: {selected_branch_context}
Make it:
- Short
- Easy to understand
- Exam-oriented
Question: {user_input}
"""

            elif mode == "Smart Exam Mode":
                prompt = f"""
You are an exam-focused AI helping engineering students score maximum marks.
Branch: {branch}
Branch Context: {selected_branch_context}
Topic: {user_input}
Output Type: {exam_type}
Rules:
- Be concise and exam-oriented
- Avoid storytelling
- Use structured formatting
- Focus on scoring marks
If 5-Mark Answer: Provide a short structured answer with definition and key points.
If 10-Mark Answer: Provide a detailed answer with headings and examples.
If Quick Revision: Give ultra-short bullet notes for last-minute revision.
If Important Topics: List most expected exam topics and scoring areas.
If Last-Minute Strategy: Give quick preparation plan, what to study, and what to skip.
"""

            try:
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    else:
        st.warning("Please enter a topic.")

if not user_input:
    st.markdown("""
    <div class="response-container">
        <div class="response-header">🤖 AI Response</div>
        <p class="response-placeholder">Your AI-generated answer will appear here once you enter a topic and click Generate.</p>
        <hr class="custom-divider">
        <div class="try-header">💡 Try asking:</div>
        <span class="prompt-pill">Explain OS scheduling algorithms</span>
        <span class="prompt-pill">What is Fourier Transform in signals?</span>
        <span class="prompt-pill">Explain Carnot cycle with diagram</span>
        <span class="prompt-pill">What are ACID properties in DBMS?</span>
        <span class="prompt-pill">Explain RCC beam design steps</span>
    </div>
    """, unsafe_allow_html=True)