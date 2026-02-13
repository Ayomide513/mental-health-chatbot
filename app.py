import streamlit as st
import joblib
from chatbot import MentalHealthChatbot
from utils import prepare_input, get_risk_level, generate_recommendations
from config import CRISIS_RESOURCES
from data_logger import DataLogger

st.set_page_config(
    page_title="Mental Health Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Fix text color in chat messages */
    .stChatMessage p {
        color: #2c3e50 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 5px;
    }
    
    h1 {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin: 20px 0;
    }
    
    /* Fix heading colors in result cards */
    .result-card h2, .result-card h3 {
        color: #2c3e50 !important;
    }
    
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        font-weight: 600;
        color: #2c3e50 !important;
    }
    
    .stAlert {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        border-left: 5px solid #667eea;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .risk-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_model():
    model = joblib.load('model_xgb.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()
logger = DataLogger()

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MentalHealthChatbot()

st.title("Mental Health Assistant")
st.markdown('<p class="subtitle">Your AI-powered companion for mental wellness</p>', unsafe_allow_html=True)

st.info("Privacy Notice: Your responses are saved anonymously to improve our service.")

with st.sidebar:
    st.markdown("### Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("F1 Score", "0.65")
    with col2:
        st.metric("Accuracy", "73%")
    
    stats = logger.get_stats()
    if stats:
        st.markdown("---")
        st.markdown("### Usage Analytics")
        st.metric("Total Assessments", stats['total_assessments'])
        st.metric("High Risk Cases", stats['high_risk_count'])
        st.metric("Average Risk", f"{stats['average_risk']:.1f}%")
    
    st.markdown("---")
    st.markdown("### Crisis Resources")
    st.markdown("""
    **24/7 Support:**
    - Suicide Prevention: 988
    - Crisis Text: HOME to 741741
    - International: iasp.info
    """)
    
    st.markdown("---")
    if st.button("Start New Assessment", use_container_width=True):
        st.session_state.chatbot.reset()
        st.rerun()

chatbot = st.session_state.chatbot

st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.markdown("### Conversation")

for msg in chatbot.conversation_history:
    st.chat_message("assistant").write(msg['question'])
    st.chat_message("user").write(msg['response'])

if not chatbot.is_complete():
    current_question = chatbot.get_current_question()
    st.chat_message("assistant").write(current_question)
    
    user_input = st.chat_input("Type your answer here...")
    
    if user_input:
        success, feedback = chatbot.process_response(user_input)
        st.rerun()

else:
    st.success("Assessment complete! Analyzing your responses...")
    
    data = chatbot.get_collected_data()
    input_array = prepare_input(data)
    input_scaled = scaler.transform(input_array)
    
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1] * 100
    
    risk_level, risk_color = get_risk_level(probability)
    
    logger.log_assessment(data, prediction, probability, risk_level)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("## Your Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Depression Risk")
        st.markdown(f"<h1 style='text-align: center; color: {risk_color};'>{probability:.1f}%</h1>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Risk Level")
        risk_class = f"risk-{risk_level.lower()}"
        st.markdown(f"<div style='text-align: center; margin-top: 20px;'><span class='{risk_class}'>{risk_level}</span></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("### Status")
        status = "At Risk" if prediction == 1 else "Healthy"
        status_color = "#f5576c" if prediction == 1 else "#4ade80"
        st.markdown(f"<h2 style='text-align: center; color: {status_color}; margin-top: 15px;'>{status}</h2>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("## Personalized Recommendations")
    
    recommendations = generate_recommendations(data)
    
    if recommendations:
        for idx, rec in enumerate(recommendations):
            with st.expander(f"{rec['area']}: {rec['issue']}", expanded=idx==0):
                st.markdown(f"**Action Plan:** {rec['action']}")
    else:
        st.success("Excellent! You're maintaining great mental health habits. Keep up the amazing work!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.warning("Important: This is a screening tool, not a medical diagnosis. Please consult a healthcare professional for proper evaluation.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <p style='font-size: 0.9rem;'>Built with ML and AI | F1 Score: 0.65 | Trained on 100,000 students</p>
    <p style='font-size: 0.8rem; opacity: 0.8;'>For educational and screening purposes only</p>
</div>
""", unsafe_allow_html=True)