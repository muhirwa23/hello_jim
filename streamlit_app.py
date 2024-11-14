# Import necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import os
from groq import Groq
import time
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import plotly.graph_objects as go
import requests
import random

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Set page configuration
st.set_page_config(
    page_title="Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        background-color: #f9f9f9;
    }
    .main {
        padding: 20px;
    }
    .sidebar {
        background-color: #ffffff;
        padding: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #FF6B6B;
        border-radius: 8px;
        height: 50px;
        font-size: 16px;
    }
    .stProgress > div > div > div > div {
        background-color: #FF6B6B;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 30px;
    }
    .metric-box {
        background-color: #FF6B6B;
        color: white;
        padding: 20px;
        border-radius: 10px;
        width: 200px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #2F4F4F;
    }
    .card {
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    .container-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .container-header h4 {
        font-size: 18px;
    }
    .sidebar-header {
        font-size: 20px;
        color: #2F4F4F;
    }
    .stSlider {
        color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# Multilingual Support
def set_language():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'
    lang = st.sidebar.selectbox("Choose Language / Hitamo Ururimi", ["English", "Kinyarwanda"], index=0)
    st.session_state['language'] = lang

def _(text):
    translations = {
        "Welcome to the Mental Health Dashboard": "Murakaza neza kuri Dashboard y'Ubuzima bwo mu Mutwe",
        "This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot.":
            "Iyi dashboard itanga ishusho y'ubuzima bwo mu mutwe bw'urubyiruko rw'u Rwanda. Reba ibigaragara mu mibare, gutekereza ku byashoboka, no gukoresha chatbot yacu.",
        # Add more translations as needed
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# Load all provided datasets (using simulated data for now)
@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    # Simulate loading datasets with random values
    youth_health_data = pd.DataFrame({
        'Age': np.random.randint(15, 25, 100),
        'Depression_Score': np.random.uniform(1, 10, 100),
        'Anxiety_Score': np.random.uniform(1, 10, 100),
        'Region': np.random.choice(['Kigali', 'Northern', 'Eastern', 'Western'], 100),
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Physical_Activity': np.random.uniform(0, 14, 100)
    })
    mental_health_data = pd.DataFrame({
        'Depression_Score': np.random.uniform(1, 10, 100),
        'Anxiety_Score': np.random.uniform(1, 10, 100),
        'Stress_Level': np.random.uniform(1, 10, 100),
    })
    dhs_data = pd.DataFrame({
        'Region': np.random.choice(['Kigali', 'Northern', 'Eastern', 'Western'], 100),
        'Depression_Score': np.random.uniform(1, 10, 100),
        'Anxiety_Score': np.random.uniform(1, 10, 100),
    })
    general_population_data = pd.DataFrame({
        'Age': np.random.randint(15, 60, 100),
        'Depression_Score': np.random.uniform(1, 10, 100),
    })
    mental_health_youth_data = pd.DataFrame({
        'Date': pd.date_range(start="2022-01-01", periods=100, freq='D'),
        'Depression_Score': np.random.uniform(1, 10, 100)
    })
    return youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data

# Function to display Key Metrics on the Home Page
def display_metrics():
    # Placeholder for metrics - these can be updated dynamically based on data analysis
    metric_data = {
        "Average Depression Score": np.random.uniform(2.0, 6.0),
        "Average Anxiety Score": np.random.uniform(2.0, 6.0),
        "Region with Highest Depression": "Kigali",
        "Percentage Youth Engaged in Physical Activity": 75
    }
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Average Depression Score**")
        st.metric(label="", value=f"{metric_data['Average Depression Score']:.2f}")
    with col2:
        st.markdown(f"**Average Anxiety Score**")
        st.metric(label="", value=f"{metric_data['Average Anxiety Score']:.2f}")
    with col3:
        st.markdown(f"**Region with Highest Depression**")
        st.metric(label="", value=metric_data["Region with Highest Depression"])
    with col4:
        st.markdown(f"**Percentage Youth in Physical Activity**")
        st.metric(label="", value=f"{metric_data['Percentage Youth Engaged in Physical Activity']}%")

# Function for Hierarchical Demographics Analysis
def hierarchical_demographics_analysis(mental_youth_data):
    st.header("Hierarchical Demographics Analysis")
    
    # Simulated hierarchical data for demo
    fig = px.sunburst(
        mental_youth_data,
        path=['Region', 'Gender', 'Age'],
        values='Depression_Score',
        title="Hierarchical Demographics of Depression Scores by Region, Gender, and Age",
        color='Depression_Score',
        template="presentation"
    )
    st.plotly_chart(fig, use_container_width=True)

# Visuals Section with Unique Tableau-Style Charts
def enhanced_visualizations(youth_data, mental_data, dhs_data, gen_pop_data):
    st.header("📊 Visuals")
    
    # Unique Tableau-style visuals
    # Funnel Chart
    st.subheader("Funnel Chart Example")
    funnel_data = pd.DataFrame({
        'Stage': ['Awareness', 'Interest', 'Consideration', 'Conversion'],
        'Count': [1000, 800, 600, 400]
    })
    fig_funnel = px.funnel(funnel_data, x="Count", y="Stage", title="Funnel Chart of User Engagement")
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Sankey Diagram
    st.subheader("Sankey Diagram Example")
    sankey_data = pd.DataFrame({
        'Source': ['Facebook', 'Instagram', 'Twitter', 'Others'],
        'Target': ['Leads', 'Leads', 'Leads', 'Leads'],
        'Value': [100, 300, 150, 50]
    })
    fig_sankey = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=["Facebook", "Instagram", "Twitter", "Others", "Leads"]),
        link=dict(source=[0, 1, 2, 3], target=[4, 4, 4, 4], value=[100, 300, 150, 50])
    ))
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    # Treemap
    st.subheader("Treemap Example")
    fig_treemap = px.treemap(
        youth_data, 
        path=['Region', 'Gender'], 
        values='Depression_Score', 
        title="Treemap of Depression Scores by Region and Gender"
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Bubble Chart
    st.subheader("Bubble Chart Example")
    fig_bubble = px.scatter(
        youth_data, 
        x="Age", 
        y="Depression_Score", 
        size="Depression_Score", 
        color="Region", 
        hover_name="Gender", 
        title="Bubble Chart of Depression Score vs Age"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# Predictive model feature
def predictive_modeling():
    st.header("🤖 Predictive Modeling")
    st.markdown("Use the sliders to predict the depression score.")

    # Prediction form
    with st.form(key="prediction_form"):
        col1, col2, col3, col4 = st.columns(4)
        age = st.slider("Age", min_value=15, max_value=25, value=20)
        social_media = st.slider("Social Media Usage (hours/day)", min_value=0, max_value=12, value=3)
        physical_activity = st.slider("Physical Activity (hours/week)", min_value=0, max_value=14, value=4)
        sleep_duration = st.slider("Sleep Duration (hours/night)", min_value=4, max_value=12, value=7)
        submit_button = st.form_submit_button("Predict")

    if submit_button:
        prediction = age * 0.2 + social_media * 0.1 - physical_activity * 0.3 + sleep_duration * 0.2
        st.success(f"Predicted Depression Score: **{prediction:.2f}**")

# Chatbot Interface with Groq API integration
def generate_text(prompt, max_tokens=100):
    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",  
            max_tokens=max_tokens,
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm having trouble connecting right now. Please try again later."

def chatbot_interface():
    st.header("🗣️ Mental Health Chatbot")

    st.markdown("""
    <div style="text-align: center;">
        <h3>Hello! I'm <strong>Menti</strong>, your mental health assistant 🤖</h3>
        <p>Feel free to share your thoughts, ask about mental health resources, or get tips for stress management.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat history container
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    chat_html = '<div class="chat-container">'
    for chat in st.session_state['history']:
        user_html = f'<div class="user-message">{chat["user"]}</div>'
        assistant_html = f'<div class="assistant-message">{chat["assistant"]}</div>'
        chat_html += user_html + assistant_html
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # User input
    user_input = st.text_input("You:", "", key="input", placeholder="Type your message here...", label_visibility="collapsed")

    if user_input:
        st.session_state['history'].append({"user": user_input, "assistant": "Menti is typing..."})
        st.experimental_rerun()  # Temporarily display typing indicator

        # Generate response from Groq API
        assistant_response = generate_text(user_input)
        st.session_state['history'][-1]["assistant"] = assistant_response
        st.experimental_rerun()  # Refresh with updated response

# Sidebar Innovations and Mental Health Resources
def innovative_features():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 Mental Health Resources")
    with st.sidebar.expander("Hotlines and Contacts", expanded=True):
        st.markdown("""
        - **Hotlines:**
            - Rwanda Mental Health Hotline: **1234**
        - **Online Resources:**
            - [Ministry of Health Rwanda](https://www.moh.gov.rw)
            - [WHO Mental Health](https://www.who.int/mental_health/en/)
        """)
    st.sidebar.header("💡 Daily Mental Health Tip")
    tips = [
        "Take a short walk to clear your mind.",
        "Practice deep breathing exercises.",
        "Reach out to a friend or family member.",
        "Write down your thoughts in a journal.",
        "Try a new hobby or activity.",
        "Maintain a balanced diet and stay hydrated.",
        "Set achievable goals and celebrate small wins.",
        "Get enough sleep to rejuvenate your mind.",
        "Listen to your favorite music to relax.",
        "Practice mindfulness or meditation."
    ]
    tip = random.choice(tips)
    st.sidebar.info(f"**Tip:** {tip}")

# Main function to navigate through the app
def main():
    set_language()

    # Sidebar navigation
    options = [
        _("Home"),
        _("Visuals"),
        _("Predictive Modeling"),
        _("Chatbot")
    ]
    icons = ["house", "bar-chart", "cpu", "chat-dots"]

    selected = option_menu(
        menu_title=_("Main Menu"),
        options=options,
        icons=icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#FF6B6B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#FF6B6B"},
        },
    )

    # Load data if not loaded already
    if 'data' not in st.session_state:
        youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data = load_data()
        st.session_state['data'] = youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data
    youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data = st.session_state['data']

    innovative_features()

    # Handle navigation selection
    if selected == _("Home"):
        display_metrics()
        hierarchical_demographics_analysis(mental_youth_data)
    elif selected == _("Visuals"):
        enhanced_visualizations(youth_data, mental_data, dhs_data, gen_pop_data)
    elif selected == _("Predictive Modeling"):
        predictive_modeling()
    elif selected == _("Chatbot"):
        chatbot_interface()

if __name__ == "__main__":
    main()
